const ConfigService = {
  getScriptProperty(key) {
    return PropertiesService.getScriptProperties().getProperty(key);
  },

  getJsonFromProperty(key) {
    const raw = this.getScriptProperty(key);
    if (!raw) {
      throw new Error(`Missing Script Property: ${key}`);
    }
    return JSON.parse(raw);
  },

  getGithubRawBaseUrl() {
    return this.getScriptProperty('GITHUB_RAW_BASE_URL');
  },

  getConceptManifestPath() {
    return this.getScriptProperty('CONCEPT_MANIFEST_PATH') || 'content/concepts/manifest.json';
  },

  getChannelMapPath() {
    return this.getScriptProperty('CHANNEL_MAP_PATH') || 'config/channel_interest_map.json';
  },

  getConceptWebhookUrl() {
    return this.getScriptProperty('DISCORD_WEBHOOK_URL');
  },

  getTrendWebhookMap() {
    return this.getJsonFromProperty('DISCORD_WEBHOOK_MAP_JSON');
  },

  getOpenAiKey() {
    return this.getScriptProperty('OPENAI_API_KEY');
  },

  getOpenAiModel() {
    return this.getScriptProperty('OPENAI_MODEL') || 'gpt-5.1';
  },

  getTrendHistorySheetId() {
    return this.getScriptProperty('TREND_HISTORY_SHEET_ID');
  },

  getTrendHistorySheetName() {
    return this.getScriptProperty('TREND_HISTORY_SHEET_NAME') || 'trend_history';
  }
};
