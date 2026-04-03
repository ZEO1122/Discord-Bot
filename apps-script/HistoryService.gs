const HistoryService = {
  getConceptProgress() {
    const properties = PropertiesService.getScriptProperties();
    return {
      lastIndex: Number(properties.getProperty('CONCEPT_LAST_INDEX') || -1),
      lastPath: properties.getProperty('CONCEPT_LAST_PATH'),
      lastBriefingKey: properties.getProperty('CONCEPT_LAST_BRIEFING_KEY'),
      lastPostedAt: properties.getProperty('CONCEPT_LAST_POSTED_AT'),
    };
  },

  setConceptProgress(progress) {
    const properties = PropertiesService.getScriptProperties();
    properties.setProperty('CONCEPT_LAST_INDEX', String(progress.lastIndex));
    properties.setProperty('CONCEPT_LAST_PATH', progress.lastPath || '');
    properties.setProperty('CONCEPT_LAST_BRIEFING_KEY', progress.lastBriefingKey || '');
    properties.setProperty('CONCEPT_LAST_POSTED_AT', progress.lastPostedAt || '');
  },

  getTrendSheet() {
    const sheet = SpreadsheetApp.openById(ConfigService.getTrendHistorySheetId()).getSheetByName(ConfigService.getTrendHistorySheetName());
    if (!sheet) {
      throw new Error('Trend history sheet not found');
    }
    return sheet;
  },

  appendTrendHistoryRow(row) {
    this.getTrendSheet().appendRow([
      row.paper_id,
      row.title,
      row.canonical_url,
      row.published_at,
      row.citation_count,
      row.topic_tag,
      row.posted_at,
      row.brief_title,
    ]);
  },

  getTrendHistory() {
    const values = this.getTrendSheet().getDataRange().getValues();
    if (values.length <= 1) {
      return [];
    }
    const rows = values.slice(1);
    return rows.map((row) => ({
      paper_id: row[0],
      title: row[1],
      canonical_url: row[2],
      published_at: row[3],
      citation_count: row[4],
      topic_tag: row[5],
      posted_at: row[6],
      brief_title: row[7],
    }));
  },

  hasSeenPaper(canonicalUrl) {
    return this.getTrendHistory().some((row) => row.canonical_url === canonicalUrl);
  }
};
