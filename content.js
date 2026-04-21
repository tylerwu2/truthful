// content.js - Content script for misinformation detection

class ContentAnalyzer {
  constructor() {
    this.highlights = [];
  }

  init() {
    // Listen for messages from popup or background
    chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
      if (request.action === 'highlightResults') {
        this.highlightResults(request.result);
        sendResponse({ success: true });
      }
    });

    // Auto-scan if enabled
    this.checkAutoScan();
  }

  async checkAutoScan() {
    try {
      const settings = await chrome.storage.local.get('settings');
      if (settings.settings?.autoScan !== false) {
        this.scanPage();
      }
    } catch (error) {
      console.error('Auto-scan check failed:', error);
    }
  }

  async scanPage() {
    const text = this.extractReadableText();
    if (!text || text.length < 100) return; // Skip short pages

    try {
      const response = await chrome.runtime.sendMessage({
        action: 'analyzePage',
        url: window.location.href,
        text: text
      });

      if (response.success) {
        this.highlightResults(response.result);
        this.updateBadge(response.result);
      }
    } catch (error) {
      console.error('Scan failed:', error);
    }
  }

  extractReadableText() {
    // Simple text extraction - remove scripts, styles, etc.
    const elements = document.querySelectorAll('p, h1, h2, h3, h4, h5, h6, li, td, th');
    const texts = [];

    elements.forEach(el => {
      const text = el.textContent?.trim();
      if (text && text.length > 20) {
        texts.push(text);
      }
    });

    return texts.join('\n\n').substring(0, 20000); // Limit length
  }

  highlightResults(result) {
    this.clearHighlights();

    if (!result.claims || result.claims.length === 0) return;

    // Create a map of text to claims for efficient lookup
    const textToClaims = new Map();
    result.claims.forEach(claim => {
      const key = claim.text.toLowerCase().trim();
      if (!textToClaims.has(key)) {
        textToClaims.set(key, []);
      }
      textToClaims.get(key).push(claim);
    });

    // Use TreeWalker to find text nodes
    const walker = document.createTreeWalker(
      document.body,
      NodeFilter.SHOW_TEXT,
      {
        acceptNode: (node) => {
          // Skip script, style, and other non-visible elements
          const parent = node.parentElement;
          if (!parent) return NodeFilter.FILTER_SKIP;

          const tagName = parent.tagName.toLowerCase();
          if (['script', 'style', 'noscript', 'code', 'pre', 'textarea'].includes(tagName)) {
            return NodeFilter.FILTER_SKIP;
          }

          // Skip if text is too short
          if (node.textContent.trim().length < 10) {
            return NodeFilter.FILTER_SKIP;
          }

          return NodeFilter.FILTER_ACCEPT;
        }
      },
      false
    );

    const nodesToProcess = [];
    let node;
    while (node = walker.nextNode()) {
      nodesToProcess.push(node);
    }

    // Process nodes in reverse order to maintain positions
    nodesToProcess.reverse().forEach(textNode => {
      try {
        this.processTextNode(textNode, textToClaims);
      } catch (error) {
        console.warn('Error processing text node for highlight:', error);
      }
    });
  }

  processTextNode(textNode, textToClaims) {
    const text = textNode.textContent;
    const lowerText = text.toLowerCase();

    // Find all matching claims in this text node
    const matches = [];
    for (const [claimText, claims] of textToClaims) {
      let startIndex = 0;
      let index;
      while ((index = lowerText.indexOf(claimText, startIndex)) !== -1) {
        matches.push({
          index,
          length: claimText.length,
          claims: claims
        });
        startIndex = index + 1; // Allow overlapping matches
      }
    }

    if (matches.length === 0) return;

    // Sort matches by position
    matches.sort((a, b) => a.index - b.index);

    // Merge overlapping matches
    const mergedMatches = [];
    let current = null;
    for (const match of matches) {
      if (!current || match.index >= current.index + current.length) {
        current = { ...match };
        mergedMatches.push(current);
      } else {
        // Merge claims
        current.claims.push(...match.claims);
        // Extend length if needed
        current.length = Math.max(current.length, match.index + match.length - current.index);
      }
    }

    // Apply highlights from end to start to maintain positions
    for (let i = mergedMatches.length - 1; i >= 0; i--) {
      const match = mergedMatches[i];
      this.highlightTextRange(textNode, match.index, match.length, match.claims);
    }
  }

  highlightTextRange(textNode, startIndex, length, claims) {
    const text = textNode.textContent;
    const beforeText = text.substring(0, startIndex);
    const highlightText = text.substring(startIndex, startIndex + length);
    const afterText = text.substring(startIndex + length);

    const fragment = document.createDocumentFragment();

    if (beforeText) {
      fragment.appendChild(document.createTextNode(beforeText));
    }

    // Choose the claim with highest risk for styling
    const highestRiskClaim = claims.reduce((max, claim) =>
      claim.risk > max.risk ? claim : max
    );

    const mark = document.createElement('mark');
    mark.textContent = highlightText;
    mark.className = `misinfo-highlight misinfo-${getRiskLevel(highestRiskClaim.risk)}`;
    mark.style.cssText = `
      background-color: ${getRiskColor(highestRiskClaim.risk)}30;
      border-bottom: 2px solid ${getRiskColor(highestRiskClaim.risk)};
      padding: 2px 0;
      cursor: help;
      border-radius: 2px;
      transition: all 0.2s ease;
    `;

    // Create detailed tooltip
    const tooltipText = claims.map(claim =>
      `${claim.category}: ${claim.risk}% risk`
    ).join('\n');

    mark.title = tooltipText;

    // Add hover effects
    mark.addEventListener('mouseenter', () => {
      mark.style.backgroundColor = `${getRiskColor(highestRiskClaim.risk)}50`;
      mark.style.transform = 'scale(1.05)';
    });

    mark.addEventListener('mouseleave', () => {
      mark.style.backgroundColor = `${getRiskColor(highestRiskClaim.risk)}30`;
      mark.style.transform = 'scale(1)';
    });

    fragment.appendChild(mark);

    if (afterText) {
      fragment.appendChild(document.createTextNode(afterText));
    }

    if (textNode.parentNode) {
      textNode.parentNode.replaceChild(fragment, textNode);
      this.highlights.push(mark);
    }
  }

  clearHighlights() {
    const highlights = document.querySelectorAll('.misinfo-highlight');
    highlights.forEach(el => {
      const text = el.textContent;
      if (el.parentNode) {
        el.parentNode.replaceChild(document.createTextNode(text), el);
      }
    });
    this.highlights = [];
  }

  updateBadge(result) {
    // Update browser action badge
    const level = getRiskLevel(result.overallRisk);
    const color = getRiskColor(result.overallRisk);

    chrome.runtime.sendMessage({
      action: 'updateBadge',
      level,
      color
    });
  }
}

// Helper functions (duplicated from scorer.js for content script)
function getRiskLevel(risk) {
  if (risk <= 30) return 'low';
  if (risk <= 70) return 'medium';
  return 'high';
}

function getRiskColor(risk) {
  const colors = {
    low: '#28a745',
    medium: '#ffc107',
    high: '#dc3545'
  };
  return colors[getRiskLevel(risk)];
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    const analyzer = new ContentAnalyzer();
    analyzer.init();
  });
} else {
  const analyzer = new ContentAnalyzer();
  analyzer.init();
}