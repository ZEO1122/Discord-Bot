const ConfigService = {
  getScriptProperty(key) {
    return PropertiesService.getScriptProperties().getProperty(key);
  },

  getJsonFromProperty(key) {
    const raw = this.getScriptProperty(key);
    if (!raw) {
      throw new Error(`Missing Script Property: ${key}`);
    }
    try {
      return JSON.parse(raw);
    } catch (error) {
      return this.parseSimpleYamlMap(raw);
    }
  },

  parseSimpleYamlMap(raw) {
    const lines = String(raw)
      .split('\n')
      .map((line) => line.trim())
      .filter((line) => line && !line.startsWith('#'));
    const result = {};
    lines.forEach((line) => {
      const idx = line.indexOf(':');
      if (idx === -1) {
        return;
      }
      const key = line.slice(0, idx).trim();
      const value = line.slice(idx + 1).trim();
      if (key && value) {
        result[key] = value;
      }
    });
    if (!Object.keys(result).length) {
      throw new Error('Failed to parse JSON/YAML Script Property');
    }
    return result;
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
