# Truthful

A Chrome extension that detects and highlights potential misinformation, phishing, and AI-generated spam on web pages using a trained ML classifier, heuristics, and optional AI APIs.

## Features

- **ML-powered detection**: Trained logistic regression classifier on 123 labeled examples across 4 categories (safe, misinformation, phishing, AI spam)
- **26 linguistic features**: Syntactic, statistical, discourse, phishing, and AI-generation indicators
- **Heuristics fallback**: Pattern-based detection when classifier unavailable or fails
- **API integration**: Optional Groq (Llama 3.3), Google Gemini, or local Ollama for enhanced analysis
- **Smart text extraction**: Extracts main content while filtering nav/footer/forms to reduce false positives
- **Content highlighting**: Color-coded marks with risk tooltips
- **Risk gauge**: Visual 0-100 risk indicator
- **Caching**: 1-hour analysis cache to avoid re-processing
- **Popup UI**: Modern CRM dashboard-inspired interface
- **Options page**: Configure provider, API keys, scan threshold, and auto-scan

## Installation

1. Clone or download this repository
2. Open Chrome and go to `chrome://extensions/`
3. Enable "Developer mode" in the top right
4. Click "Load unpacked" and select the extension folder
5. The extension icon should appear in your toolbar

## Usage

1. Navigate to any webpage
2. Click the **Truthful** extension icon
3. View the risk score, gauge, and verdict
4. Click **"Scan This Page"** to manually trigger analysis
5. Suspicious content will be highlighted with color-coded marks:
   - 🟢 **Green**: Low risk
   - 🟡 **Yellow**: Medium risk  
   - 🔴 **Red**: High risk
6. Hover over highlighted text for claim details

## Configuration

Right-click the extension icon → **Options** (or `chrome://extensions/` → Details → Extension options)

### Analysis Providers

| Provider | Speed | Cost | Accuracy | Privacy |
|----------|-------|------|----------|---------|
| **Classifier** (default) | Instant | Free | Good | ✅ Local |
| **Heuristics** (fallback) | Instant | Free | Fair | ✅ Local |
| **Groq API** | Fast | Free tier | Better | ⚠️ Cloud |
| **Gemini API** | Fast | Free tier | Better | ⚠️ Cloud |
| **Ollama** | Varies | Free | Better | ✅ Local |

### Settings

- **Analysis Provider**: Choose detection method (classifier is recommended)
- **API Key**: Required for Groq/Gemini (optional for Ollama)
- **Risk Threshold**: Only show claims above this score (0-100)
- **Auto-scan**: Automatically analyze pages on load

## Architecture

### Classifier

- **Model**: Logistic regression (sklearn)
- **Features**: 26 linguistic + structural indicators
- **Classes**: safe, misinformation, phishing, ai_spam
- **Training data**: 123 labeled examples
- **Performance**: Cross-validation accuracy ~82%

### Fallback Chain

1. Try configured provider (Groq/Gemini/Ollama)
2. Fall back to ML classifier
3. Fall back to heuristics
4. Default to safe if all fail

## Project Structure

```
truthful/
├── manifest.json              # MV3 manifest
├── background.js              # Service worker + analysis logic
├── content.js                 # DOM highlighting
├── scorer.js                  # ML classifier (trained weights)
├── weights.json               # Trained model weights
├── train.py                   # Training script
├── feature_extractor.py       # Feature engineering
├── training_data.py           # 123 labeled examples
├── popup/
│   ├── popup.html            # Modern UI
│   ├── popup.js              # Analysis & display logic
│   └── popup.css             # CRM dashboard styling
├── options/
│   ├── options.html          # Settings page
│   └── options.js
├── test-pages/               # Test content
│   ├── conspiracy.html
│   ├── phishing.html
│   ├── spam.html
│   ├── safe-news.html
│   └── ...
├── utils/
│   └── storage.js            # Chrome storage utilities
├── README.md
└── .gitignore
```

## Development

### Training the Classifier

```bash
cd truthful
python3 train.py
```

This generates:
- `weights.json` - Trained model weights
- `report.txt` - Cross-validation metrics

### Testing

1. Load extension in Chrome (Dev mode)
2. Open `test-pages/` in a browser tab
3. Click extension icon → **Scan This Page**
4. Check console (F12) for debug logs

### Key Files

| File | Purpose |
|------|---------|
| `background.js` | Handles analysis requests, manages fallback chain |
| `scorer.js` | ML classifier inference, feature extraction |
| `content.js` | DOM text extraction and highlighting |
| `popup/popup.js` | UI logic, tab communication |
| `train.py` | Generates `weights.json` from `training_data.py` |

## Privacy & Security

- ✅ **Local inference**: ML classifier runs entirely in the browser
- ✅ **No tracking**: No analytics or user data collection
- ✅ **Configurable storage**: Results cached locally only
- ⚠️ **API usage**: Groq/Gemini/Ollama sends text to external services (if configured)
- 🔒 **API keys**: Stored locally in `chrome.storage.local`, never sent to third parties

## Known Limitations

- Text extraction may miss content in iframes or shadow DOM
- Very short pages (<200 chars) are marked as low risk
- Classifier optimized for English text
- API costs apply if using Groq/Gemini (free tiers available)

## Troubleshooting

### Extension won't load
- Check `manifest.json` syntax
- Verify all script files exist
- Clear Chrome cache and reload

### High false positives
- Increase risk threshold in settings
- Switch to Groq/Gemini for higher accuracy
- Check console for debug logs

### Classifier scoring fails
- Check `weights.json` is present
- Verify `scorer.js` loads successfully
- Extension falls back to heuristics automatically

## Future Improvements

- [ ] Multi-language support
- [ ] Real-time fact-checking API integration
- [ ] User feedback loop for model retraining
- [ ] Browser sync for settings
- [ ] Dark mode UI
- [ ] Content source reputation scoring
- [ ] Source verification integration

## License

MIT License

## Credits

Built with:
- Chrome Extensions API (MV3)
- scikit-learn (model training)
- Logistic Regression (classifier)
