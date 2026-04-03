const TrendService = {
  FIELD_LIMITS: {
    topic: 220,
    tag: 100,
    core: 700,
    reason: 700,
    terms: 320,
    question: 120,
    source: 500,
  },

  CAUTION_MESSAGE:
    '주의: 이 브리핑은 최신 source를 바탕으로 GPT가 요약한 내용입니다. 해석 오류나 누락 가능성이 있으니 원문 출처를 함께 확인하세요.',

  runWeeklyTrends() {
    Logger.log('runTrendWeekly:start');
    const config = GitHubService.fetchJson(ConfigService.getTrendConfigPath());
    const papers = this.fetchRecentTopPapers(config);
    Logger.log(`TrendService:recent_papers count=${papers.length}`);

    if (!papers.length) {
      Logger.log('TrendService:no_recent_papers');
      return;
    }

    const topPapers = this.selectWeeklyPapers(papers, config.top_papers || 3);
    Logger.log(`TrendService:top_papers count=${topPapers.length}`);
    if (!topPapers.length) {
      Logger.log('TrendService:no_fresh_top_papers');
      return;
    }

    const sections = topPapers.map((paper) => {
      const topicTag = this.tagPaperTopic(paper, config.taxonomy || ['llm', 'detection-segmentation', 'vision-language', 'other']);
      const prompt = this.buildPrompt(paper, topicTag);
      const generated = this.normalizeTrendOutput(OpenAIService.generateTrendBrief(prompt));
      Logger.log(`TrendService:paper_generated paper_id=${paper.paper_id} topic=${topicTag} title=${generated.title}`);
      return { paper, topicTag, generated };
    });

    const payload = this.buildTrendEmbed(sections);
    DiscordService.sendWebhook(ConfigService.getTrendWebhookUrl(), payload);
    Logger.log(`TrendService:posted sections=${sections.length}`);

    sections.forEach((section) => {
      HistoryService.appendTrendHistoryRow({
        paper_id: section.paper.paper_id,
        title: section.paper.title,
        canonical_url: Utils.normalizeArxivUrl(section.paper.url),
        published_at: section.paper.published_at,
        citation_count: section.paper.citation_count,
        topic_tag: section.topicTag,
        posted_at: Utils.nowIso(),
        brief_title: section.generated.title,
      });
    });
    Logger.log('runTrendWeekly:success');
  },

  fetchRecentTopPapers(config) {
    const response = UrlFetchApp.fetch(Utils.buildOpenAlexUrl(config), {
      muteHttpExceptions: true,
      headers: { 'User-Agent': 'Discord-Bot/1.0 (GAS weekly trend fetch)' },
    });
    const status = response.getResponseCode();
    Logger.log(`TrendService:openalex_status status=${status}`);
    if (status < 200 || status >= 300) {
      throw new Error(`OpenAlex fetch failed: ${status} ${response.getContentText()}`);
    }

    const data = JSON.parse(response.getContentText());
    return (data.results || [])
      .map((item) => ({
        paper_id: item.id || item.doi || item.ids?.openalex || item.primary_location?.landing_page_url || item.title,
        title: item.title || '',
        abstract: Utils.rebuildOpenAlexAbstract(item.abstract_inverted_index),
        url: item.primary_location?.landing_page_url || item.ids?.openalex || '',
        published_at: item.publication_date || '',
        citation_count: Number(item.cited_by_count || 0),
      }))
      .filter((item) => item.title && item.url)
      .sort((a, b) => b.citation_count - a.citation_count);
  },

  selectWeeklyPapers(papers, topN) {
    const selected = [];
    for (let i = 0; i < papers.length; i += 1) {
      const paper = papers[i];
      if (HistoryService.hasSeenPaper(Utils.normalizeArxivUrl(paper.url))) {
        continue;
      }
      selected.push(paper);
      if (selected.length >= topN) {
        break;
      }
    }
    return selected;
  },

  tagPaperTopic(paper, taxonomy) {
    const inputText = [`title=${paper.title}`, `abstract=${paper.abstract || ''}`].join('\n');
    const response = OpenAIService.classifyPaperTopic(inputText);
    const topic = String(response.topic || 'other').trim();
    if (taxonomy.includes(topic)) {
      return topic;
    }
    return 'other';
  },

  buildPrompt(paper, topicTag) {
    return [
      '당신은 AI 학술동아리용 주간 논문 브리핑 에디터다.',
      '반드시 아래 논문 정보만 근거로 한국어 브리핑을 작성하라.',
      '반드시 JSON으로만 답하라.',
      '필수 키: title, core_explanation, why_it_matters, quick_terms, discussion_prompt',
      '과장된 일반론, 뜬금없는 응용 시사점, 출처에 없는 주장, 모호한 미래 예측을 쓰지 마라.',
      '각 필드는 짧고 읽기 쉽게 작성하라.',
      'title: 40자 이내',
      'core_explanation: 2~3문장, 350자 이내',
      'why_it_matters: 2~3문장, 350자 이내',
      'quick_terms: 2~3개 bullet, 총 220자 이내',
      'discussion_prompt: 1문장, 80자 이내',
      '',
      `분야 태그: ${topicTag}`,
      `논문 제목: ${paper.title}`,
      `초록: ${paper.abstract || '초록 없음'}`,
      `출처: ${paper.url}`,
      `발행일: ${paper.published_at || 'unknown'}`,
      `인용수: ${paper.citation_count}`,
      '',
      '{"title":"...","core_explanation":"...","why_it_matters":"...","quick_terms":"- 용어: 설명\\n- 용어: 설명","discussion_prompt":"..."}',
    ].join('\n');
  },

  normalizeTrendOutput(response) {
    const rawText = this.extractOutputText(response);
    const parsed = JSON.parse(rawText);
    const normalized = this.normalizeGeneratedFields(parsed);
    this.validateGeneratedFields(normalized);
    return normalized;
  },

  extractOutputText(response) {
    const outputs = response.output || [];
    for (let i = 0; i < outputs.length; i += 1) {
      const contents = outputs[i].content || [];
      for (let j = 0; j < contents.length; j += 1) {
        if (contents[j].type === 'output_text') {
          return contents[j].text;
        }
      }
    }
    throw new Error('OpenAI response did not contain output_text');
  },

  normalizeGeneratedFields(data) {
    const aliasGroups = {
      title: ['title', '제목'],
      core_explanation: ['core_explanation', 'coreExplanation', 'what_happened', 'summary', '핵심 설명', '핵심 요약'],
      why_it_matters: ['why_it_matters', 'whyItMatters', 'importance', '왜 중요한가', '의미'],
      quick_terms: ['quick_terms', 'quickTerms', 'terms', '용어 빠르게 이해하기', '핵심 용어'],
      discussion_prompt: ['discussion_prompt', 'discussionPrompt', 'question', 'prompt', '생각해볼 질문', '토론 질문'],
    };
    const normalized = {};
    Object.keys(aliasGroups).forEach((target) => {
      const aliases = aliasGroups[target];
      let value = '';
      aliases.some((alias) => {
        const raw = data[alias];
        if (typeof raw === 'string' && raw.trim()) {
          value = raw.trim();
          return true;
        }
        return false;
      });
      normalized[target] = value;
    });

    if (!normalized.why_it_matters && normalized.core_explanation) {
      normalized.why_it_matters = '이 논문이 실제 모델 설계와 응용 방향에 어떤 영향을 주는지 추가 확인이 필요합니다.';
    }
    if (!normalized.quick_terms) {
      normalized.quick_terms = '- 핵심 용어: 원문 출처를 함께 확인하세요.';
    }
    if (!normalized.discussion_prompt && normalized.title) {
      normalized.discussion_prompt = `${normalized.title}가 실제 적용에 미칠 영향은 무엇일까?`;
    }
    return normalized;
  },

  validateGeneratedFields(data) {
    ['title', 'core_explanation', 'why_it_matters', 'quick_terms', 'discussion_prompt'].forEach((field) => {
      if (!data[field]) {
        throw new Error(`Missing generated field: ${field}`);
      }
    });
  },

  buildTrendEmbed(sections) {
    const fields = [];
    sections.forEach((section) => {
      fields.push({ name: '주제', value: Utils.safeTruncateText(section.generated.title, this.FIELD_LIMITS.topic), inline: false });
      fields.push({ name: '분야', value: Utils.safeTruncateText(section.topicTag, this.FIELD_LIMITS.tag), inline: false });
      fields.push({ name: '핵심 설명', value: Utils.safeTruncateText(section.generated.core_explanation, this.FIELD_LIMITS.core), inline: false });
      fields.push({ name: '왜 중요한가', value: Utils.safeTruncateText(section.generated.why_it_matters, this.FIELD_LIMITS.reason), inline: false });
      fields.push({ name: '용어 빠르게 이해하기', value: Utils.safeTruncateText(section.generated.quick_terms, this.FIELD_LIMITS.terms), inline: false });
      fields.push({ name: '생각해볼 질문', value: Utils.safeTruncateText(section.generated.discussion_prompt, this.FIELD_LIMITS.question), inline: false });
      fields.push({
        name: '출처',
        value: Utils.safeTruncateText(`- ${section.paper.title}: ${section.paper.url}`, this.FIELD_LIMITS.source),
        inline: false,
      });
    });
    fields.push({ name: '주의', value: this.CAUTION_MESSAGE, inline: false });

    return {
      embeds: [
        {
          title: '이번 주 인용수 상위 논문 브리핑',
          color: 15844367,
          fields,
        },
      ],
    };
  },
};
