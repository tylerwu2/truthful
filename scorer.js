/**
 * scorer.js
 * 
 * Self-contained misinformation/phishing scorer for the Chrome extension.
 * No external dependencies. Mirrors the Python training pipeline exactly.
 *
 * Usage (extension background.js or content.js):
 *   import { loadScorer, scoreText } from './scorer.js';
 *   const scorer = await loadScorer();          // loads weights.json once
 *   const result = scorer.score(pageText);
 *
 * Or inline (if bundling weights directly):
 *   const scorer = new Scorer(WEIGHTS);
 *   const result = scorer.score(pageText);
 */


// ---------------------------------------------------------------------------
// Feature extraction — mirrors feature_extractor.py exactly
// ---------------------------------------------------------------------------

function sentences(text) {
  return text.split(/(?<=[.!?])\s+/).map(s => s.trim()).filter(s => s.length > 2);
}

function words(text) {
  return (text.toLowerCase().match(/[a-z']+/g) || []);
}

function safeDiv(a, b, def_ = 0) {
  return b ? a / b : def_;
}

function syntacticFeatures(text) {
  const sents = sentences(text);
  const ws = words(text);
  const nSents = Math.max(sents.length, 1);
  const nWords = Math.max(ws.length, 1);

  const sentLengths = sents.map(s => words(s).length);
  const avgSentLen = safeDiv(sentLengths.reduce((a, b) => a + b, 0), nSents);
  const sentLenVariance = safeDiv(
    sentLengths.reduce((s, l) => s + (l - avgSentLen) ** 2, 0), nSents
  );

  const imperativeVerbs = new Set([
    "click","verify","confirm","send","call","login","log","update","provide",
    "submit","enter","download","install","act","respond","contact","follow",
    "share","buy","order"
  ]);
  const imperativeCount = sents.filter(s => {
    const w = words(s);
    return w.length && imperativeVerbs.has(w[0]);
  }).length;

  const questionCount = sents.filter(s => s.trim().endsWith("?")).length;
  const passiveMatches = (text.match(/\b(is|are|was|were|been|being)\s+\w+ed\b/gi) || []).length;

  return {
    avg_sent_len: avgSentLen,
    sent_len_variance: sentLenVariance,
    imperative_ratio: safeDiv(imperativeCount, nSents),
    question_ratio: safeDiv(questionCount, nSents),
    passive_ratio: safeDiv(passiveMatches, nSents),
  };
}

function statisticalFeatures(text) {
  const ws = words(text);
  const nWords = Math.max(ws.length, 1);
  const nSents = Math.max(sentences(text).length, 1);

  const uniqueWords = new Set(ws);
  const ttr = safeDiv(uniqueWords.size, nWords);

  const freq = {};
  ws.forEach(w => freq[w] = (freq[w] || 0) + 1);
  const hapax = Object.values(freq).filter(c => c === 1).length;
  const hapaxRatio = safeDiv(hapax, nWords);

  const allCaps = (text.match(/\b[A-Z]{3,}\b/g) || []).length;
  const capsRatio = safeDiv(allCaps, nWords);

  const exclCount = (text.match(/!/g) || []).length;
  const exclRatio = safeDiv(exclCount, nSents);

  function countSyllables(word) {
    const w = word.toLowerCase();
    let count = (w.match(/[aeiou]+/g) || []).length;
    if (w.endsWith('e') && count > 1) count--;
    return Math.max(count, 1);
  }
  const syllables = ws.reduce((s, w) => s + countSyllables(w), 0);
  const fkGrade = Math.max(
    0.39 * safeDiv(nWords, nSents) + 11.8 * safeDiv(syllables, nWords) - 15.59,
    0
  );

  return {
    ttr,
    hapax_ratio: hapaxRatio,
    caps_ratio: capsRatio,
    exclamation_ratio: exclRatio,
    fk_grade: fkGrade,
  };
}

function discourseFeatures(text) {
  const t = text.toLowerCase();
  const sents = sentences(text);
  const ws = words(text);
  const nSents = Math.max(sents.length, 1);
  const nWords = Math.max(ws.length, 1);

  const attribution = [
    "according to","researchers","study found","published in","data shows",
    "scientists","university","reported by","sources say","officials said",
    "spokesperson","confirmed by","evidence suggests","peer-reviewed","journal"
  ];
  const attrCount = attribution.filter(p => t.includes(p)).length;

  const claimMarkers = [
    "the truth is","everyone knows","it is a fact","proven that","100%",
    "always","never","all doctors","all scientists","the government",
    "they don't want","big pharma","mainstream media"
  ];
  const claimCount = claimMarkers.filter(p => t.includes(p)).length;

  const hedges = [
    "may","might","could","alleged","reportedly","appears to","suggests",
    "according","possible","likely","unclear","unconfirmed","sources indicate"
  ];
  const hedgeCount = hedges.filter(p => t.includes(p)).length;

  // Named entity proxy: capitalized mid-sentence words
  const namedEntities = (text.match(/(?<= )[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*/g) || []);
  const neDensity = safeDiv(namedEntities.length, nWords);

  const testimonialPattern = (
    text.match(/(i made \$|i earned|paid off|changed my life|— [A-Z]|" ?- ?[A-Z])/gi) || []
  ).length;

  const outgroup = ["they","elites","the establishment","globalists","deep state","mainstream"];
  const ingroup = ["we the people","real americans","true patriots","wake up","sheeple"];
  const outgroupCount = outgroup.reduce((s, w) => s + (t.split(w).length - 1), 0);
  const ingroupCount = ingroup.reduce((s, w) => s + (t.split(w).length - 1), 0);

  return {
    attribution_density: safeDiv(attrCount, nSents),
    unattributed_claim_ratio: safeDiv(claimCount, nSents),
    hedge_density: safeDiv(hedgeCount, nSents),
    named_entity_density: neDensity,
    testimonial_count: Math.min(testimonialPattern, 10),
    outgroup_framing: safeDiv(outgroupCount, nWords),
    ingroup_framing: safeDiv(ingroupCount, nWords),
  };
}

function structuralPhishingFeatures(text) {
  const t = text.toLowerCase();

  const credentialAsks = [
    "credit card number","card number","cvv","social security","ssn",
    "bank account","routing number","password","pin number","mother's maiden",
    "date of birth","full name and address"
  ];
  const credScore = Math.min(credentialAsks.filter(p => t.includes(p)).length, 5);

  const accountThreats = [
    /account.*suspend/,/account.*terminat/,/account.*clos/,/access.*revok/,
    /permanently closed/,/legal action/,/your account will/,/account has been/
  ];
  const threatScore = Math.min(accountThreats.filter(r => r.test(t)).length, 5);

  let suspiciousUrlScore = 0;
  const urls = text.match(/https?:\/\/[^\s<>"]+/gi) || [];
  for (const url of urls) {
    const domainMatch = url.match(/https?:\/\/([^/\s]+)/i);
    if (domainMatch) {
      const d = domainMatch[1].toLowerCase();
      if ((d.match(/\./g) || []).length >= 3) suspiciousUrlScore++;
      if (/\.(ru|xyz|top|click|tk|ml|ga|cf|gq|pw|cc|ws)$/.test(d)) suspiciousUrlScore += 2;
      const brands = ["amazon","paypal","microsoft","apple","google","facebook","netflix","chase","wells","bank"];
      for (const brand of brands) {
        if (d.includes(brand) && !d.endsWith(`${brand}.com`)) suspiciousUrlScore += 2;
      }
    }
  }

  const urgencyWords = [
    "immediately","urgent","within 24 hours","within 48 hours",
    "act now","final notice","last chance","expire"
  ];
  const hasUrgency = urgencyWords.some(w => t.includes(w));
  const urgencyStructural = (hasUrgency && (credScore > 0 || threatScore > 0)) ? 1.0 : 0.0;

  const benign = [
    "best regards","kind regards","sincerely","thank you for","please find attached",
    "as discussed","following up","per our conversation","hope this helps","feel free to"
  ];
  const benignScore = Math.min(benign.filter(p => t.includes(p)).length, 4);

  return {
    credential_ask_count: credScore,
    account_threat_count: threatScore,
    suspicious_url_score: Math.min(suspiciousUrlScore, 6),
    urgency_structural: urgencyStructural,
    benign_context_score: benignScore,
  };
}

function aiGeneratedFeatures(text) {
  const sents = sentences(text);
  const nSents = Math.max(sents.length, 1);
  const ws = words(text);
  const nWords = Math.max(ws.length, 1);
  const t = text.toLowerCase();

  // Sentence length uniformity
  const sentLengths = sents.map(s => words(s).length);
  let uniformity = 0;
  if (sentLengths.length > 2) {
    const mean = sentLengths.reduce((a, b) => a + b, 0) / sentLengths.length;
    const variance = sentLengths.reduce((s, l) => s + (l - mean) ** 2, 0) / sentLengths.length;
    uniformity = 1.0 - Math.min(safeDiv(Math.sqrt(variance), mean + 1), 1.0);
  }

  const transitions = [
    "furthermore","moreover","additionally","in conclusion","it is important to note",
    "it should be noted","as mentioned","in summary","to summarize","notably",
    "significantly","it is worth","one must consider","it is essential"
  ];
  const transitionCount = transitions.filter(p => t.includes(p)).length;

  const absolutes = [
    "best","greatest","most powerful","revolutionary","breakthrough","guaranteed",
    "100%","proven","scientifically proven","you will","you'll never","secret","hidden truth"
  ];
  const absoluteCount = absolutes.filter(p => t.includes(p)).length;

  const freq = {};
  ws.forEach(w => freq[w] = (freq[w] || 0) + 1);
  const sorted = Object.values(freq).sort((a, b) => b - a);
  const top10Coverage = safeDiv(sorted.slice(0, 10).reduce((a, b) => a + b, 0), nWords);

  return {
    sentence_uniformity: uniformity,
    transition_density: safeDiv(transitionCount, nSents),
    absolute_claim_density: safeDiv(absoluteCount, nSents),
    top10_word_coverage: top10Coverage,
  };
}

/**
 * Extract all features in the same order as the Python pipeline.
 * Returns Float64Array for fast matrix math.
 */
function extractFeatures(text) {
  const feats = {
    ...syntacticFeatures(text),
    ...statisticalFeatures(text),
    ...discourseFeatures(text),
    ...structuralPhishingFeatures(text),
    ...aiGeneratedFeatures(text),
  };
  return feats;
}


// ---------------------------------------------------------------------------
// Inference — softmax logistic regression
// ---------------------------------------------------------------------------

function softmax(logits) {
  const max = Math.max(...logits);
  const exps = logits.map(l => Math.exp(l - max));
  const sum = exps.reduce((a, b) => a + b, 0);
  return exps.map(e => e / sum);
}

class Scorer {
  /**
   * @param {Object} weights - parsed weights.json
   */
  constructor(weights) {
    this.featureNames = weights.feature_names;
    this.classes = weights.classes;
    this.mean = weights.scaler_mean;
    this.std = weights.scaler_std;
    this.coef = weights.coef;         // [n_classes][n_features]
    this.intercept = weights.intercept; // [n_classes]
  }

  /**
   * Score a block of text.
   *
   * @param {string} text
   * @returns {{
   *   label: string,           // predicted class name
   *   probabilities: Object,   // {safe, misinformation, phishing, ai_spam}
   *   risk_score: number,      // 0-100 overall risk (0 = safe, 100 = high risk)
   *   fraud_score: number,     // 0-100 phishing/spam signal
   *   features: Object,        // raw feature values (for debugging)
   *   top_signals: Array       // [{name, value, weight, contribution}] top drivers
   * }}
   */
  score(text) {
    if (!text || text.trim().length < 20) {
      return this._emptyResult();
    }

    // 1. Extract features
    const featObj = extractFeatures(text);
    const x = this.featureNames.map(name => featObj[name] ?? 0);

    // 2. Standardize: z = (x - mean) / std
    const z = x.map((v, i) => (v - this.mean[i]) / (this.std[i] + 1e-8));

    // 3. Logits: W @ z + b
    const logits = this.coef.map((row, c) =>
      row.reduce((s, w, j) => s + w * z[j], 0) + this.intercept[c]
    );

    // 4. Softmax probabilities
    const probs = softmax(logits);
    const probMap = Object.fromEntries(this.classes.map((cls, i) => [cls, probs[i]]));

    // 5. Predicted class
    const predIdx = probs.indexOf(Math.max(...probs));
    const label = this.classes[predIdx];

    // 6. Risk scores (0–100)
    //    risk_score: probability of any harmful class
    //    fraud_score: probability of phishing specifically
    const safeProb = probMap["safe"] ?? 0;
    const riskScore = Math.round((1 - safeProb) * 100);
    const fraudScore = Math.round(((probMap["phishing"] ?? 0) + (probMap["ai_spam"] ?? 0) * 0.5) * 100);

    // 7. Top contributing features for this prediction
    const classIdx = predIdx;
    const contributions = this.featureNames.map((name, j) => ({
      name,
      value: featObj[name] ?? 0,
      weight: this.coef[classIdx][j],
      contribution: this.coef[classIdx][j] * z[j],
    }));
    const topSignals = contributions
      .filter(c => Math.abs(c.contribution) > 0.01)
      .sort((a, b) => Math.abs(b.contribution) - Math.abs(a.contribution))
      .slice(0, 5);

    return {
      label,
      probabilities: Object.fromEntries(
        Object.entries(probMap).map(([k, v]) => [k, Math.round(v * 100) / 100])
      ),
      risk_score: riskScore,
      fraud_score: fraudScore,
      features: featObj,
      top_signals: topSignals,
    };
  }

  _emptyResult() {
    return {
      label: "safe",
      probabilities: { safe: 1, misinformation: 0, phishing: 0, ai_spam: 0 },
      risk_score: 0,
      fraud_score: 0,
      features: {},
      top_signals: [],
    };
  }
}


// ---------------------------------------------------------------------------
// Loader helpers (Chrome extension context)
// ---------------------------------------------------------------------------

/**
 * Load weights from a URL (use chrome.runtime.getURL in the extension).
 *
 * In background.js:
 *   const scorer = await loadScorer(chrome.runtime.getURL('weights.json'));
 */
async function loadScorer(weightsUrl = './weights.json') {
  const resp = await fetch(weightsUrl);
  const weights = await resp.json();
  return new Scorer(weights);
}

/**
 * Convenience: score a DOM document's readable text.
 * Uses a simple Readability-like extractor (no dependency).
 */
function extractPageText(doc = document) {
  // Remove noise elements
  const noise = ['script','style','nav','footer','header','aside','form',
                 'button','input','select','noscript','iframe'];
  const clone = doc.body ? doc.body.cloneNode(true) : null;
  if (!clone) return '';
  noise.forEach(tag => clone.querySelectorAll(tag).forEach(el => el.remove()));

  // Prefer <article> or <main> if present
  const main = clone.querySelector('article') || clone.querySelector('main') || clone;
  return (main.innerText || main.textContent || '')
    .replace(/\s+/g, ' ')
    .trim()
    .slice(0, 8000); // cap at 8k chars for performance
}


// ---------------------------------------------------------------------------
// Export
// ---------------------------------------------------------------------------

// CommonJS / global fallback (for extension content scripts without bundler)
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { Scorer, loadScorer, extractFeatures, extractPageText };
}
if (typeof self !== 'undefined') {
  self.MisinfoScorer = { Scorer, loadScorer, extractFeatures, extractPageText };
}
if (typeof window !== 'undefined') {
  window.MisinfoScorer = { Scorer, loadScorer, extractFeatures, extractPageText };
}
