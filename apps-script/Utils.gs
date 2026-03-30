const Utils = {
  nowIso() {
    return new Date().toISOString();
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
