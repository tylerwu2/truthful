// scorer.js - Risk score to color/label mapping

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
    case 'high_risk': return 'High Risk - Exercise Caution';
    case 'medium_risk': return 'Medium Risk - Verify Information';
    case 'low_risk': return 'Low Risk - Appears Safe';
    default: return 'Unknown';
  }
}

// Export functions
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { getRiskLevel, getRiskColor, getRiskLabel, getVerdictText };
}