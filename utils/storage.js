// storage.js - chrome.storage.local read/write wrapper

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

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
  module.exports = StorageManager;
}
