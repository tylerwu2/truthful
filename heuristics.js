// heuristics.js - Standalone pattern engine for misinformation detection

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
    if (risk >= 70) return 'high_risk';
    if (risk >= 40) return 'medium_risk';
    return 'low_risk';
  }
}

// Export for use in background.js
if (typeof module !== 'undefined' && module.exports) {
  module.exports = HeuristicsDetector;
}