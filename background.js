// background.js - Service worker for misinformation detector

// Import the classifier (service worker compatible)
importScripts('scorer.js');

// Inline HeuristicsDetector class (fallback)
class HeuristicsDetector {
  constructor() {
    this.patterns = {
      phishing: {
        keywords: ['verify your account', 'suspicious activity', 'login required', 'security alert', 'account suspension', 'confirm identity'],
        urgency: ['immediately', 'urgent', 'act now', 'limited time', 'expires soon'],
        risk: 80
      },
      manipulation: {
        keywords: ['conspiracy', 'secret knowledge', 'they don\'t want you to know', 'wake up', 'red pill', 'deep state'],
        fear: ['dangerous', 'threat', 'crisis', 'emergency', 'catastrophe'],
        risk: 70
      },
      misinformation: {
        keywords: ['microchip', '5g causes', 'vaccines contain', 'globalist', 'new world order', 'illuminati'],
        risk: 60
      },
      spam: {
        keywords: ['make money fast', 'guaranteed income', 'work from home', 'easy money', 'get rich quick'],
        risk: 50
      }
    };
  }

  analyze(text) {
    const claims = [];
    const lowerText = text.toLowerCase();

    for (const [category, pattern] of Object.entries(this.patterns)) {
      const matches = [];
      pattern.keywords.forEach(keyword => {
        const regex = new RegExp(keyword.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi');
        let match;
        while ((match = regex.exec(text)) !== null) {
          matches.push({
            text: match[0],
            start: match.index,
            end: match.index + match[0].length,
            category,
            risk: pattern.risk
          });
        }
      });

      if (category === 'phishing' || category === 'manipulation') {
        pattern.urgency?.forEach(urgent => {
          const regex = new RegExp(urgent.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi');
          let match;
          while ((match = regex.exec(text)) !== null) {
            matches.push({
              text: match[0],
              start: match.index,
              end: match.index + match[0].length,
              category: category + '_urgency',
              risk: Math.min(100, pattern.risk + 10)
            });
          }
        });
      }

      claims.push(...matches);
    }

    // Calculate overall risk
    let overallRisk = 0;
    if (claims.length > 0) {
      const avgRisk = claims.reduce((sum, claim) => sum + claim.risk, 0) / claims.length;
      overallRisk = Math.min(100, avgRisk + (claims.length * 5)); // Bonus for multiple flags
    }

    return {
      overallRisk,
      claims: claims.slice(0, 10), // Limit to top 10 claims
      verdict: this.getVerdict(overallRisk)
    };
  }

  getVerdict(risk) {
    if (risk >= 70) return 'high';
    if (risk >= 40) return 'medium';
    return 'low';
  }
}

// Inline StorageManager class
class StorageManager {
  constructor() {
    this.storage = chrome.storage.local;
  }

  async get(key, defaultValue = null) {
    try {
      const result = await this.storage.get(key);
      return result[key] !== undefined ? result[key] : defaultValue;
    } catch (error) {
      console.error('Storage get error:', error);
      return defaultValue;
    }
  }

  async set(key, value) {
    try {
      await this.storage.set({ [key]: value });
    } catch (error) {
      console.error('Storage set error:', error);
    }
  }

  async remove(key) {
    try {
      await this.storage.remove(key);
    } catch (error) {
      console.error('Storage remove error:', error);
    }
  }

  async clear() {
    try {
      await this.storage.clear();
    } catch (error) {
      console.error('Storage clear error:', error);
    }
  }

  // Specific methods for the extension
  async getAnalysisResult(url) {
    return await this.get(`analysis_${url}`);
  }

  async setAnalysisResult(url, result) {
    await this.set(`analysis_${url}`, {
      ...result,
      timestamp: Date.now()
    });
  }

  async getSettings() {
    return await this.get('settings', {
      provider: 'heuristics', // none, groq, gemini, ollama
      apiKey: '',
      threshold: 40,
      autoScan: true
    });
  }

  async setSettings(settings) {
    await this.set('settings', settings);
  }
}

// Initialize detectors
const heuristicsDetector = new HeuristicsDetector();
const storageManager = new StorageManager();

// Initialize classifier
let classifier = null;
(async () => {
  try {
    // Wait for importScripts to complete
    await new Promise(resolve => setTimeout(resolve, 100));
    if (typeof self !== 'undefined' && self.MisinfoScorer) {
      classifier = await self.MisinfoScorer.loadScorer(chrome.runtime.getURL('weights.json'));
    } else if (typeof loadScorer !== 'undefined') {
      classifier = await loadScorer(chrome.runtime.getURL('weights.json'));
    } else {
      throw new Error('Scorer not available');
    }
    console.log('Classifier loaded successfully');
  } catch (error) {
    console.error('Failed to load classifier:', error);
    console.log('Falling back to heuristics');
  }
})();

// Risk scoring constants
const RISK_THRESHOLDS = {
  LOW: 30,
  MEDIUM: 70,
  HIGH: 100
};

const COLORS = {
  low: '#28a745',    // green
  medium: '#ffc107', // yellow
  high: '#dc3545'    // red
};

const LABELS = {
  low: 'Low Risk',
  medium: 'Medium Risk',
  high: 'High Risk'
};

function getRiskLevel(risk) {
  if (risk <= RISK_THRESHOLDS.LOW) return 'low';
  if (risk <= RISK_THRESHOLDS.MEDIUM) return 'medium';
  return 'high';
}

function getRiskColor(risk) {
  return COLORS[getRiskLevel(risk)];
}

function getRiskLabel(risk) {
  return LABELS[getRiskLevel(risk)];
}

function getVerdictText(verdict) {
  switch (verdict) {
    case 'high':
    case 'high_risk':
      return 'High Risk - Exercise Caution';
    case 'medium':
    case 'medium_risk':
      return 'Medium Risk - Verify Information';
    case 'low':
    case 'low_risk':
      return 'Low Risk - Appears Safe';
    default:
      return 'Unknown';
  }
}

async function analyzeWithClassifier(text) {
  if (!classifier) {
    throw new Error('Classifier not loaded');
  }

  const cleanText = (text || '').replace(/\s+/g, ' ').trim();
  if (!cleanText || cleanText.length < 200) {
    return { overallRisk: 0, claims: [], verdict: 'low' };
  }

  let scoreResult;
  try {
    scoreResult = classifier.score(cleanText);
  } catch (error) {
    console.warn('Classifier scoring failed, falling back to heuristics:', error);
    return heuristicsDetector.analyze(cleanText);
  }

  const riskScore = Math.round(scoreResult.risk_score || 0);

  if (scoreResult.label === 'safe' || riskScore < 45) {
    return { overallRisk: riskScore, claims: [], verdict: 'low' };
  }

  const claims = [];
  const verdict = riskScore >= 70 ? 'high' : 'medium';

  if (scoreResult.label === 'phishing' || scoreResult.label === 'ai_spam') {
    if (riskScore >= 55 || (scoreResult.fraud_score || 0) > 50) {
      claims.push({
        text: cleanText.substring(0, Math.min(200, cleanText.length)),
        start: 0,
        end: Math.min(200, cleanText.length),
        category: scoreResult.label,
        risk: riskScore
      });
    }
  } else if (scoreResult.label === 'misinformation' && riskScore >= 50) {
    claims.push({
      text: cleanText.substring(0, Math.min(200, cleanText.length)),
      start: 0,
      end: Math.min(200, cleanText.length),
      category: scoreResult.label,
      risk: riskScore
    });
  }

  if ((scoreResult.fraud_score || 0) > 60) {
    claims.push({
      text: 'Potential fraudulent content detected',
      start: 0,
      end: Math.min(50, cleanText.length),
      category: 'fraud',
      risk: Math.round(scoreResult.fraud_score)
    });
  }

  return {
    overallRisk: riskScore,
    claims,
    verdict
  };
}

// Message handler
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'analyzePage') {
    handleAnalyzePage(request, sender, sendResponse);
    return true; // Keep message channel open for async response
  } else if (request.action === 'updateBadge') {
    updateBadge(request.level, request.color);
    sendResponse({ success: true });
  }
});

async function handleAnalyzePage(request, sender, sendResponse) {
  const { url, text } = request;

  try {
    // Check cache first
    let result = await storageManager.getAnalysisResult(url);
    if (result && (Date.now() - result.timestamp) < 3600000) { // 1 hour cache
      console.log('Using cached result for', url);
      sendResponse({ success: true, result });
      return;
    }

    // Get settings
    const settings = await storageManager.getSettings();

    // Analyze based on provider
    try {
      if (settings.provider === 'groq' && settings.apiKey) {
        result = await analyzeWithGroq(text, settings.apiKey);
      } else if (settings.provider === 'gemini' && settings.apiKey) {
        result = await analyzeWithGemini(text, settings.apiKey);
      } else if (settings.provider === 'ollama') {
        result = await analyzeWithOllama(text);
      } else if (classifier) {
        result = await analyzeWithClassifier(text);
      } else {
        result = heuristicsDetector.analyze(text);
      }
    } catch (error) {
      console.warn('Provider analysis failed, falling back to heuristics:', error);
      if (classifier) {
        try {
          result = await analyzeWithClassifier(text);
        } catch (classifierError) {
          console.warn('Classifier fallback failed, using heuristics:', classifierError);
          result = heuristicsDetector.analyze(text);
        }
      } else {
        result = heuristicsDetector.analyze(text);
      }
    }

    // Cache result
    await storageManager.setAnalysisResult(url, result);

    sendResponse({ success: true, result });
  } catch (error) {
    console.error('Analysis error:', error);
    sendResponse({ success: false, error: error.message });
  }
}

async function analyzeWithGroq(text, apiKey) {
  const systemPrompt = `You are an expert misinformation detector. Analyze the provided text for potential misinformation, bias, manipulation, or deceptive content.

Your task is to identify specific claims or statements that may be misleading, false, or manipulative. For each suspicious claim, provide:
- The exact text of the claim
- A risk score (0-100) indicating how likely it is to be misinformation
- A category (phishing, conspiracy, manipulation, spam, bias, factual_error, etc.)

Return your analysis as a JSON object with this exact structure:
{
  "overallRisk": <number 0-100 indicating overall risk level>,
  "claims": [
    {
      "text": "<exact text from the input>",
      "start": <character position where claim starts>,
      "end": <character position where claim ends>,
      "category": "<category name>",
      "risk": <number 0-100>
    }
  ],
  "verdict": "<low_risk|medium_risk|high_risk>"
}

Guidelines:
- Focus on factual claims that can be verified
- Look for emotional manipulation, conspiracy theories, phishing attempts
- Consider context and intent
- Be conservative - only flag content that shows clear signs of misinformation
- Return empty claims array for safe content
- Limit to top 10 most suspicious claims

Analyze this text:`;

  const response = await fetch('https://api.groq.com/openai/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      model: 'llama-3.3-70b-versatile',
      messages: [{
        role: 'system',
        content: systemPrompt
      }, {
        role: 'user',
        content: text.substring(0, 15000) // Allow more text
      }],
      temperature: 0.1,
      max_tokens: 2000
    })
  });

  if (!response.ok) {
    throw new Error(`Groq API error: ${response.status} ${response.statusText}`);
  }

  const data = await response.json();
  const content = data.choices[0].message.content;

  try {
    return JSON.parse(content);
  } catch (parseError) {
    console.error('Failed to parse Groq response:', content);
    // Fallback to heuristics if JSON parsing fails
    return heuristicsDetector.analyze(text);
  }
}

async function analyzeWithGemini(text, apiKey) {
  const systemPrompt = `You are an expert misinformation detector. Analyze the provided text for potential misinformation, bias, manipulation, or deceptive content.

Your task is to identify specific claims or statements that may be misleading, false, or manipulative. For each suspicious claim, provide:
- The exact text of the claim
- A risk score (0-100) indicating how likely it is to be misinformation
- A category (phishing, conspiracy, manipulation, spam, bias, factual_error, etc.)

Return your analysis as a JSON object with this exact structure:
{
  "overallRisk": <number 0-100 indicating overall risk level>,
  "claims": [
    {
      "text": "<exact text from the input>",
      "start": <character position where claim starts>,
      "end": <character position where claim ends>,
      "category": "<category name>",
      "risk": <number 0-100>
    }
  ],
  "verdict": "<low_risk|medium_risk|high_risk>"
}

Guidelines:
- Focus on factual claims that can be verified
- Look for emotional manipulation, conspiracy theories, phishing attempts
- Consider context and intent
- Be conservative - only flag content that shows clear signs of misinformation
- Return empty claims array for safe content
- Limit to top 10 most suspicious claims

Analyze this text:`;

  const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${apiKey}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      contents: [{
        parts: [{
          text: systemPrompt + '\n\n' + text.substring(0, 15000)
        }]
      }],
      generationConfig: {
        temperature: 0.1,
        maxOutputTokens: 2000,
        responseMimeType: 'application/json'
      }
    })
  });

  if (!response.ok) {
    throw new Error(`Gemini API error: ${response.status} ${response.statusText}`);
  }

  const data = await response.json();
  const content = data.candidates[0].content.parts[0].text;

  try {
    return JSON.parse(content);
  } catch (parseError) {
    console.error('Failed to parse Gemini response:', content);
    // Fallback to heuristics if JSON parsing fails
    return heuristicsDetector.analyze(text);
  }
}

async function analyzeWithOllama(text) {
  const systemPrompt = `You are an expert misinformation detector. Analyze the provided text for potential misinformation, bias, manipulation, or deceptive content.

Your task is to identify specific claims or statements that may be misleading, false, or manipulative. For each suspicious claim, provide:
- The exact text of the claim
- A risk score (0-100) indicating how likely it is to be misinformation
- A category (phishing, conspiracy, manipulation, spam, bias, factual_error, etc.)

Return your analysis as a JSON object with this exact structure:
{
  "overallRisk": <number 0-100 indicating overall risk level>,
  "claims": [
    {
      "text": "<exact text from the input>",
      "start": <character position where claim starts>,
      "end": <character position where claim ends>,
      "category": "<category name>",
      "risk": <number 0-100>
    }
  ],
  "verdict": "<low_risk|medium_risk|high_risk>"
}

Guidelines:
- Focus on factual claims that can be verified
- Look for emotional manipulation, conspiracy theories, phishing attempts
- Consider context and intent
- Be conservative - only flag content that shows clear signs of misinformation
- Return empty claims array for safe content
- Limit to top 10 most suspicious claims

Analyze this text:`;

  try {
    const response = await fetch('http://localhost:11434/api/generate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        model: 'llama3.2', // or whatever model is available
        prompt: systemPrompt + '\n\n' + text.substring(0, 15000),
        stream: false,
        format: 'json',
        options: {
          temperature: 0.1,
          num_predict: 2000
        }
      })
    });

    if (!response.ok) {
      throw new Error(`Ollama API error: ${response.status} ${response.statusText}`);
    }

    const data = await response.json();
    const content = data.response;

    try {
      return JSON.parse(content);
    } catch (parseError) {
      console.error('Failed to parse Ollama response:', content);
      // Fallback to heuristics if JSON parsing fails
      return heuristicsDetector.analyze(text);
    }
  } catch (networkError) {
    console.error('Ollama connection failed:', networkError);
    throw new Error('Ollama not running. Please start Ollama and ensure llama3.2 model is available.');
  }
}

function updateBadge(level, color) {
  const badgeConfig = {
    low: { text: '✓', color: '#28a745' },
    medium: { text: '⚠', color: '#ffc107' },
    high: { text: '!', color: '#dc3545' }
  };

  const config = badgeConfig[level] || badgeConfig.low;

  chrome.action.setBadgeText({ text: config.text });
  chrome.action.setBadgeBackgroundColor({ color: config.color });
}

// Handle extension installation
chrome.runtime.onInstalled.addListener(() => {
  console.log('Misinformation Detector installed');
});
