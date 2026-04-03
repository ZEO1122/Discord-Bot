const Utils = {
  OPENALEX_API_URL: 'https://api.openalex.org/works',

  nowIso() {
    return new Date().toISOString();
  },

  formatUtcDate(date) {
    return Utilities.formatDate(date, 'UTC', 'yyyy-MM-dd');
  },

  parseFrontmatter(markdown) {
    if (!markdown.startsWith('---\n')) {
      throw new Error('Markdown must start with YAML frontmatter');
    }
    const parts = markdown.split('\n---\n');
    if (parts.length < 2) {
      throw new Error('Markdown frontmatter split failed');
    }
    const frontmatterText = parts[0].replace(/^---\n/, '');
    const body = parts.slice(1).join('\n---\n').trim();
    return { frontmatterText, body };
  },

  normalizeArxivUrl(url) {
    const trimmed = String(url).trim();
    if (!trimmed.includes('/abs/')) {
      return trimmed;
    }
    const parts = trimmed.split('/abs/');
    let arxivId = parts[1].split('?')[0];
    if (/v\d+$/.test(arxivId)) {
      arxivId = arxivId.replace(/v\d+$/, '');
    }
    return `${parts[0]}/abs/${arxivId}`;
  },

  buildOpenAlexUrl(config) {
    const toDate = new Date();
    const fromDate = new Date(toDate.getTime() - Number(config.lookback_days || 7) * 24 * 60 * 60 * 1000);
    const filters = [
      `from_publication_date:${this.formatUtcDate(fromDate)}`,
      `to_publication_date:${this.formatUtcDate(toDate)}`,
    ].join(',');
    const params = [
      `search=${encodeURIComponent(config.search_query || 'artificial intelligence')}`,
      `filter=${encodeURIComponent(filters)}`,
      'sort=cited_by_count:desc',
      `per-page=${Math.max(Number(config.top_papers || 3) * 10, 30)}`,
    ].join('&');
    return `${this.OPENALEX_API_URL}?${params}`;
  },

  truncateText(text, limit) {
    const value = String(text || '').trim();
    if (value.length <= limit) {
      return value;
    }
    if (limit <= 1) {
      return value.slice(0, limit);
    }
    return value.slice(0, limit).trim();
  },

  safeTruncateText(text, limit) {
    const value = String(text || '').trim();
    if (value.length <= limit) {
      return value;
    }
    const searchWindow = value.slice(0, limit);
    const boundaries = ['. ', '.\n', '다.', '요.', '! ', '? ', '\n', ' ']
      .map((token) => searchWindow.lastIndexOf(token))
      .filter((index) => index >= 0);
    const cut = boundaries.length ? Math.max(...boundaries) : -1;
    if (cut < Math.floor(limit * 0.6)) {
      return this.truncateText(value, limit);
    }
    return searchWindow.slice(0, cut + 1).trim();
  },

  rebuildOpenAlexAbstract(invertedIndex) {
    if (!invertedIndex) {
      return '';
    }
    const tokens = [];
    Object.keys(invertedIndex).forEach((word) => {
      invertedIndex[word].forEach((position) => {
        tokens[position] = word;
      });
    });
    return tokens.filter(Boolean).join(' ');
  },

  parseMarkdownSections(body) {
    const lines = String(body).split('\n');
    const sections = [];
    let currentHeading = null;
    let currentLines = [];

    lines.forEach((line) => {
      if (line.startsWith('## ')) {
        if (currentHeading) {
          sections.push({ heading: currentHeading, value: currentLines.join('\n').trim() });
        }
        currentHeading = line.replace(/^##\s+/, '').trim();
        currentLines = [];
      } else {
        currentLines.push(line);
      }
    });

    if (currentHeading) {
      sections.push({ heading: currentHeading, value: currentLines.join('\n').trim() });
    }

    return sections.filter((section) => section.value);
  }
};
