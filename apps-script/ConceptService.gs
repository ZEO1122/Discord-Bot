const ConceptService = {
  runDailyConcept() {
    const manifest = GitHubService.fetchJson(ConfigService.getConceptManifestPath());
    const progress = HistoryService.getConceptProgress();
    const nextIndex = progress.lastIndex + 1;
    if (!manifest.order || nextIndex >= manifest.order.length) {
      Logger.log('No remaining concepts to post');
      return;
    }

    const nextPath = manifest.order[nextIndex];
    const markdown = GitHubService.fetchText(nextPath);
    const parsed = ConceptService.parseConceptMarkdown(markdown);
    const payload = ConceptService.buildConceptEmbed(parsed);
    DiscordService.sendWebhook(ConfigService.getConceptWebhookUrl(), payload);

    HistoryService.setConceptProgress({
      lastIndex: nextIndex,
      lastPath: nextPath,
      lastBriefingKey: parsed.briefing_key,
      lastPostedAt: Utils.nowIso(),
    });
  },

  parseConceptMarkdown(markdown) {
    const { frontmatterText, body } = Utils.parseFrontmatter(markdown);
    const meta = frontmatterText;
    const sections = Utils.parseMarkdownSections(body);
    return {
      briefing_key: /briefing_key:\s*(.+)/.exec(meta)?.[1]?.trim() || '',
      title: /title:\s*(.+)/.exec(meta)?.[1]?.trim() || '',
      one_line: /one_line:\s*(.+)/.exec(meta)?.[1]?.trim() || '',
      sections,
    };
  },

  buildConceptEmbed(parsed) {
    const embed = {
      title: parsed.title,
      description: parsed.one_line,
      color: 3447003,
      fields: parsed.sections.map((section) => ({
        name: section.heading === 'source' ? '출처' : section.heading,
        value: section.value,
        inline: false,
      })),
    };
    return { embeds: [embed] };
  }
};
