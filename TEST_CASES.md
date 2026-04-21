# Test Cases for Misinformation Detector

This document outlines the test cases to validate the extension functionality.

## Test Case 1: Reuters/AP News Article
**Input:** Load a legitimate news article from Reuters or AP
**Expected:** Risk 0-30, no highlights, "safe" verdict
**Status:** [ ]

## Test Case 2: Known Conspiracy Text
**Input:** Page with text like "vaccines contain microchips" or "5G causes COVID"
**Expected:** Risk 70+, 3+ claims flagged as false
**Status:** [ ]

## Test Case 3: Phishing Email
**Input:** Email-like content with "verify your account immediately" and suspicious domain
**Expected:** Fraud signal 70+, phishing category, red banner
**Status:** [ ]

## Test Case 4: AI-Generated Spam
**Input:** Content like "make $10k/month from home guaranteed"
**Expected:** Risk 60+, ai_generated + misleading tags
**Status:** [ ]

## Test Case 5: Satire Article
**Input:** The Onion or similar satirical content
**Expected:** Risk stays below 50 — should not over-flag opinion
**Status:** [ ]

## Test Case 6: Page with No Body Text
**Input:** Login page, image-only page, or empty content
**Expected:** Graceful no-op, no popup errors
**Status:** [ ]

## Test Case 7: Very Long Article
**Input:** Article with 10,000+ words
**Expected:** Chunking works, no API timeout
**Status:** [ ]

## Test Case 8: Groq API Key Invalid
**Input:** Set invalid/expired Groq API key in options
**Expected:** Clear error in popup, falls back to heuristics
**Status:** [ ]

## Test Case 9: Ollama Not Running
**Input:** Select Ollama provider but don't start Ollama
**Expected:** Error message with setup instructions
**Status:** [ ]

## Test Case 10: Same URL Revisited
**Input:** Visit a previously scanned URL
**Expected:** Result loads from cache, no duplicate API call
**Status:** [ ]

## Test Case 11: User Changes Risk Threshold
**Input:** Change threshold in options from 40 to 60
**Expected:** Highlights update immediately on active tab
**Status:** [ ]

## Test Case 12: Extension on Gmail
**Input:** Use extension on Gmail inbox
**Expected:** Scans email body only, not UI chrome
**Status:** [ ]

## Test Case 13: Heuristics Fallback
**Input:** Disable all AI providers, use only heuristics
**Expected:** Fast analysis using pattern matching
**Status:** [ ]

## Test Case 14: Multiple Claims on Page
**Input:** Page with several different types of suspicious content
**Expected:** All claims highlighted with appropriate colors
**Status:** [ ]

## Test Case 15: Edge Case - Special Characters
**Input:** Content with emojis, special characters, or non-English text
**Expected:** Handles gracefully without crashing
**Status:** [ ]

## Running Tests

1. Load the extension in Chrome developer mode
2. Visit each test URL or create test pages
3. Check popup results and page highlighting
4. Verify badge updates correctly
5. Test settings changes

## Test URLs

Create local HTML files or use these public examples:
- Safe content: Any major news site (reuters.com, apnews.com)
- Conspiracy: Search for "vaccines microchip conspiracy"
- Phishing: Create a test page with urgent account verification text
- Spam: Any get-rich-quick site
- Satire: theonion.com
- Long content: Wikipedia articles
- Gmail: mail.google.com (after logging in)