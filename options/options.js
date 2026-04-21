// options.js - Options page script

document.addEventListener('DOMContentLoaded', async () => {
  const providerSelect = document.getElementById('provider');
  const apiKeyInput = document.getElementById('apiKey');
  const apiKeyGroup = document.getElementById('apiKeyGroup');
  const thresholdInput = document.getElementById('threshold');
  const thresholdValue = document.getElementById('thresholdValue');
  const autoScanCheckbox = document.getElementById('autoScan');
  const saveBtn = document.getElementById('saveBtn');
  const statusDiv = document.getElementById('status');

  // Load current settings
  await loadSettings();

  // Update threshold display
  thresholdInput.addEventListener('input', () => {
    thresholdValue.textContent = thresholdInput.value;
  });

  // Show/hide API key field
  providerSelect.addEventListener('change', () => {
    const needsApiKey = ['groq', 'gemini'].includes(providerSelect.value);
    apiKeyGroup.style.display = needsApiKey ? 'block' : 'none';
  });

  // Save settings
  saveBtn.addEventListener('click', async () => {
    const settings = {
      provider: providerSelect.value,
      apiKey: apiKeyInput.value,
      threshold: parseInt(thresholdInput.value),
      autoScan: autoScanCheckbox.checked
    };

    try {
      await chrome.storage.local.set({ settings });
      showStatus('Settings saved successfully!', 'success');
    } catch (error) {
      showStatus('Error saving settings: ' + error.message, 'error');
    }
  });

  async function loadSettings() {
    try {
      const result = await chrome.storage.local.get('settings');
      const settings = result.settings || {
        provider: 'heuristics',
        apiKey: '',
        threshold: 40,
        autoScan: true
      };

      providerSelect.value = settings.provider;
      apiKeyInput.value = settings.apiKey;
      thresholdInput.value = settings.threshold;
      thresholdValue.textContent = settings.threshold;
      autoScanCheckbox.checked = settings.autoScan;

      // Trigger change event to show/hide API key field
      providerSelect.dispatchEvent(new Event('change'));
    } catch (error) {
      console.error('Load settings error:', error);
    }
  }

  function showStatus(message, type) {
    statusDiv.textContent = message;
    statusDiv.className = `status ${type}`;
    statusDiv.style.display = 'block';

    setTimeout(() => {
      statusDiv.style.display = 'none';
    }, 3000);
  }
});