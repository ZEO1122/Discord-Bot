const TrendService = {
  runWeeklyTrends() {
    const config = GitHubService.fetchJson(ConfigService.getChannelMapPath());
    const webhookMap = ConfigService.getTrendWebhookMap();
    const channels = (config.channels || []).filter((channel) => channel.enabled);

    channels.forEach((channel) => {
      const sections = [];
      (channel.interests || []).slice(0, channel.max_topics || 1).forEach((interest) => {
        const sources = TrendService.fetchSourcesForInterest(interest, 3);
        const freshSources = sources.filter(
          (source) => !HistoryService.hasSeenSource(channel.channel_id, interest, Utils.normalizeArxivUrl(source.url))
        );
        if (!freshSources.length) {
          return;
        }

        const prompt = TrendService.buildPrompt(interest, freshSources);
        const response = OpenAIService.generateTrendBrief(prompt);
        const generated = TrendService.normalizeTrendOutput(response);
        sections.push({ interest, generated, sources: freshSources });
      });

      if (!sections.length) {
        Logger.log(`No fresh trend sections for ${channel.channel_key}`);
        return;
      }

      const payload = TrendService.buildTrendEmbed(channel.channel_key, sections);
      DiscordService.sendWebhook(webhookMap[channel.webhook_key], payload);

      sections.forEach((section) => {
        section.sources.forEach((source) => {
          HistoryService.appendTrendHistoryRow({
            channel_key: channel.channel_key,
            channel_id: channel.channel_id,
            interest: section.interest,
            source_url: Utils.normalizeArxivUrl(source.url),
            source_title: source.title,
            published_at: source.published_at,
            posted_at: Utils.nowIso(),
            brief_title: section.generated.title,
          });
        });
      });
    });
  },

  fetchSourcesForInterest(interest, maxResults) {
    throw new Error(`Not implemented yet: fetchSourcesForInterest(${interest}, ${maxResults})`);
  },

  buildPrompt(interest, sources) {
    const sourceLines = sources
      .map((source) => `- ${source.title} | ${source.url} | ${source.published_at || ''}`)
      .join('\n');
    return [
      '당신은 AI 학술동아리용 브리핑 에디터다.',
      `트랙: ${interest}`,
      '아래 출처만 근거로 한국어 브리핑을 작성하라.',
      '반드시 JSON으로만 답하라.',
      '필수 키: title, core_explanation, why_it_matters, quick_terms, discussion_prompt',
      '{"title":"...","core_explanation":"...","why_it_matters":"...","quick_terms":"- 용어: 설명\\n- 용어: 설명","discussion_prompt":"..."}',
      '출처를 바꾸거나 추가하지 마라.',
      '',
      '출처 목록:',
      sourceLines,
    ].join('\n');
  },

  normalizeTrendOutput(response) {
    throw new Error('Not implemented yet: normalizeTrendOutput(response)');
  },

  buildTrendEmbed(channelKey, sections) {
    const fields = [];
    sections.forEach((section) => {
      fields.push({ name: '주제', value: section.generated.title, inline: false });
      fields.push({ name: '핵심 설명', value: section.generated.core_explanation, inline: false });
      fields.push({ name: '왜 중요한가', value: section.generated.why_it_matters, inline: false });
      fields.push({ name: '용어 빠르게 이해하기', value: section.generated.quick_terms, inline: false });
      fields.push({ name: '생각해볼 질문', value: section.generated.discussion_prompt, inline: false });
      fields.push({
        name: '출처',
        value: section.sources.map((source) => `- ${source.title}: ${source.url}`).join('\n'),
        inline: false,
      });
    });
    fields.push({
      name: '주의',
      value: '주의: 이 브리핑은 최신 source를 바탕으로 GPT가 요약한 내용입니다. 해석 오류나 누락 가능성이 있으니 원문 출처를 함께 확인하세요.',
      inline: false,
    });

    return {
      embeds: [
        {
          title: `이번 주 관심분야 브리핑 | ${channelKey}`,
          color: 15844367,
          fields,
        },
      ],
    };
  }
};
