// popup.js - Popup script

document.addEventListener('DOMContentLoaded', async () => {
  const scoreEl = document.getElementById('score');
  const gaugeFill = document.getElementById('gaugeFill');
  const verdictEl = document.getElementById('verdict');
  const claimsList = document.getElementById('claimsList');
  const scanBtn = document.getElementById('scanBtn');
  const statusEl = document.getElementById('status');
  const settingsLink = document.getElementById('settingsLink');

  // Load current tab's analysis result
  await loadCurrentResult();

  // Handle scan button
  scanBtn.addEventListener('click', async () => {
    scanBtn.disabled = true;
    scanBtn.textContent = 'Scanning...';
    statusEl.style.display = 'block';
    statusEl.textContent = 'Analyzing page content...';
    statusEl.className = 'status-message';

    try {
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      if (!tab || !tab.id || !tab.url) {
        throw new Error('Unable to determine active tab for analysis.');
      }
      const response = await chrome.runtime.sendMessage({
        action: 'analyzePage',
        url: tab.url,
        text: await extractTextFromTab(tab.id)
      });

      if (response.success) {
        displayResult(response.result);
        // Notify content script to highlight if available
        chrome.tabs.sendMessage(tab.id, {
          action: 'highlightResults',
          result: response.result
        }, () => {
          if (chrome.runtime.lastError) {
            console.warn('Highlight message not delivered:', chrome.runtime.lastError.message);
          }
        });
        statusEl.textContent = 'Analysis complete!';
        statusEl.className = 'status-message success';
        setTimeout(() => { statusEl.style.display = 'none'; }, 3000);
      } else {
        showError(response.error);
      }
    } catch (error) {
      showError(error.message);
    } finally {
      scanBtn.disabled = false;
      scanBtn.textContent = 'Scan This Page';
    }
  });

  // Handle settings link
  settingsLink.addEventListener('click', (e) => {
    e.preventDefault();
    chrome.runtime.openOptionsPage();
  });
});

async function loadCurrentResult() {
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (!tab || !tab.url) return;
    const result = await chrome.storage.local.get(`analysis_${tab.url}`);

    if (result[`analysis_${tab.url}`]) {
      displayResult(result[`analysis_${tab.url}`]);
    } else {
      document.getElementById('verdict').textContent = 'Not scanned yet';
      document.getElementById('verdict').className = 'verdict';
      document.getElementById('score').textContent = '--';
      document.getElementById('gaugeFill').style.width = '0%';
      document.getElementById('claimsList').innerHTML = `
        <div class="empty-state">
          <div class="empty-state-icon">📊</div>
          <div class="empty-state-text">Click "Scan This Page" to analyze content</div>
        </div>
      `;
    }
  } catch (error) {
    console.error('Load result error:', error);
  }
}

function displayResult(result) {
  const scoreEl = document.getElementById('score');
  const gaugeFill = document.getElementById('gaugeFill');
  const verdictEl = document.getElementById('verdict');
  const claimsList = document.getElementById('claimsList');

  // Update score
  scoreEl.textContent = Math.round(result.overallRisk);
  scoreEl.classList.remove('loading');

  // Update gauge
  const percentage = Math.min(100, Math.max(0, result.overallRisk));
  gaugeFill.style.width = `${percentage}%`;

  // Update verdict
  verdictEl.textContent = getVerdictText(result.verdict);
  verdictEl.className = `verdict ${result.verdict}`;

  // Filter claims based on threshold
  const threshold = 40; // Default, could be loaded from settings
  const filteredClaims = result.claims ? result.claims.filter(claim => claim.risk >= threshold) : [];

  // Update claims list
  claimsList.innerHTML = '';
  if (filteredClaims.length > 0) {
    filteredClaims.forEach(claim => {
      const claimEl = document.createElement('div');
      claimEl.className = `claim-item ${getRiskLevel(claim.risk)}`;

      claimEl.innerHTML = `
        <div class="claim-category">${claim.category}</div>
        <div class="claim-text">"${claim.text}"</div>
        <div class="claim-risk">Risk: ${claim.risk}%</div>
      `;

      claimsList.appendChild(claimEl);
    });
  } else {
    claimsList.innerHTML = `
      <div class="empty-state">
        <div class="empty-state-icon">🔍</div>
        <div class="empty-state-text">No suspicious claims detected</div>
      </div>
    `;
  }
}

function showError(error) {
  const verdictEl = document.getElementById('verdict');
  const claimsList = document.getElementById('claimsList');

  document.getElementById('score').textContent = 'Error';
  verdictEl.textContent = error;
  verdictEl.className = 'verdict high';
  claimsList.innerHTML = '';
}

async function extractTextFromTab(tabId) {
  try {
    const results = await chrome.scripting.executeScript({
      target: { tabId },
      function: () => {
        const selectors = [
          'article',
          'main',
          '[role="main"]',
          '.article-content',
          '.post-content',
          '.entry-content'
        ];

        const root = selectors
          .map(selector => document.querySelector(selector))
          .find(Boolean) || document.body;

        const walker = document.createTreeWalker(
          root,
          NodeFilter.SHOW_TEXT,
          {
            acceptNode(node) {
              const text = node.nodeValue?.trim();
              if (!text || text.length < 20) return NodeFilter.FILTER_REJECT;

              const parent = node.parentElement;
              if (!parent) return NodeFilter.FILTER_REJECT;
              if (parent.closest('nav, footer, aside, header, form, iframe, script, style, noscript')) {
                return NodeFilter.FILTER_REJECT;
              }

              const style = window.getComputedStyle(parent);
              if (style.display === 'none' || style.visibility === 'hidden' || parseFloat(style.opacity) === 0) {
                return NodeFilter.FILTER_REJECT;
              }

              return NodeFilter.FILTER_ACCEPT;
            }
          }
        );

        const chunks = [];
        let node;
        while ((node = walker.nextNode())) {
          chunks.push(node.nodeValue.trim());
        }

        return chunks.join(' ').replace(/\s+/g, ' ').trim();
      }
    });

    return (results[0]?.result || '').trim();
  } catch (error) {
    console.error('Text extraction error:', error);
    return '';
  }
}

// Helper functions
function getRiskLevel(risk) {
  if (risk <= 30) return 'low';
  if (risk <= 70) return 'medium';
  return 'high';
}

function getVerdictText(verdict) {
  switch (verdict) {
    case 'high': return 'High Risk - Exercise Caution';
    case 'medium': return 'Medium Risk - Verify Information';
    case 'low': return 'Low Risk - Appears Safe';
    default: return 'Unknown';
  }
}
