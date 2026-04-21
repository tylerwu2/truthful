# Truthful

A Chrome extension that detects and highlights potential misinformation on web pages using heuristics and AI analysis.

## Features

- **Heuristics-based detection**: Identifies phishing attempts, manipulative content, conspiracy theories, and spam
- **AI integration**: Supports Groq API (Llama 3.3), Google Gemini, and local Ollama
- **Content highlighting**: Highlights suspicious text spans with color-coded borders and tooltips
- **Risk gauge**: Visual indicator showing overall risk level
- **Caching**: Stores analysis results to avoid re-processing the same pages
- **Popup interface**: Quick access to risk scores and scan functionality
- **Options page**: Configure analysis provider, API keys, and thresholds

## Installation

1. Clone or download this repository
2. Open Chrome and go to `chrome://extensions/`
3. Enable "Developer mode" in the top right
4. Click "Load unpacked" and select the `misinformation-detector` folder
5. The extension should now be installed

## Usage

1. Navigate to any webpage
2. Click the extension icon in the toolbar
3. View the risk score and gauge in the popup
4. Review the list of flagged claims
5. Suspicious content will be highlighted on the page with tooltips
6. Use the "Scan This Page" button to re-analyze

## Configuration

Access the options page by right-clicking the extension icon and selecting "Options", or go to `chrome://extensions/` and click "Details" > "Extension options".

### Providers

- **Heuristics Only**: No API required, works offline
- **Groq API**: Fast, free tier available (Llama 3.3 70B)
- **Google Gemini**: Free tier with 1M tokens/day
- **Ollama**: Run locally for complete privacy

## Development

### Project Structure

```
misinformation-detector/
├── manifest.json          # Extension manifest
├── background.js          # Service worker
├── content.js             # Content script for highlighting
├── heuristics.js          # Pattern-based detection
├── utils/
│   ├── storage.js         # Storage utilities
│   └── scorer.js          # Risk scoring
├── popup/
│   ├── popup.html
│   ├── popup.js
│   └── popup.css
├── options/
│   ├── options.html
│   └── options.js
└── test.html              # Test page
```

### Testing

Open `test.html` in a browser to test the heuristics engine.

## Privacy

- No user data is stored externally
- Analysis results are cached locally in `chrome.storage.local`
- API keys are stored locally and only used for analysis requests
- Extension only analyzes text content from web pages you visit

## License

MIT License
