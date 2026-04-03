const TrendService = {
  FIELD_LIMITS: {
    category: 180,
    core: 700,
    reason: 700,
    terms: 320,
    question: 120,
    source: 500,
  },

  TOPIC_LABELS: {
    'foundation-models': 'foundation models(파운데이션 모델)',
    'vision-perception': 'vision perception(비전 인지)',
    'multimodal-agents': 'multimodal agents(멀티모달 에이전트)',
    'generation-creative': 'generation creative(생성·크리에이티브)',
    'systems-efficiency': 'systems efficiency(시스템 효율화)',
    other: 'other(기타)',
  },

  CAUTION_MESSAGE:
    '이 브리핑은 최신 논문 source를 바탕으로 생성된 요약입니다. 해석 오류나 누락 가능성이 있으니 원문 논문을 함께 확인하세요.',

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
      const topicTag = this.tagPaperTopic(
        paper,
        config.taxonomy || [
          'foundation-models',
          'vision-perception',
          'multimodal-agents',
          'generation-creative',
          'systems-efficiency',
          'other',
        ],
      );
      const prompt = this.buildPrompt(paper, topicTag);
      const generated = this.normalizeTrendOutput(OpenAIService.generateTrendBrief(prompt));
      Logger.log(`TrendService:paper_generated paper_id=${paper.paper_id} topic=${topicTag} title=${generated.title}`);
      return { paper, topicTag, generated };
    });

    sections.forEach((section, index) => {
      const payload = this.buildTrendPayload(section, index + 1, sections.length);
      DiscordService.sendWebhook(ConfigService.getTrendWebhookUrl(), payload);
      Logger.log(`TrendService:posted paper_index=${index + 1}`);
    });
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
    const text = `${paper.title}\n${paper.abstract || ''}`.toLowerCase();
    const heuristicRules = [
      {
        topic: 'multimodal-agents',
        keywords: ['vision-language-action', 'vision language action', 'multimodal', 'embodied', 'vlm', 'vla', 'agent'],
      },
      {
        topic: 'vision-perception',
        keywords: ['segmentation', 'detection', 'tracking', 'medical imaging', 'scene understanding', 'panoptic', 'instance segmentation'],
      },
      {
        topic: 'generation-creative',
        keywords: ['diffusion', 'generation', 'editing', 'image generation', 'video generation', 'avatar', 'creative'],
      },
      {
        topic: 'systems-efficiency',
        keywords: ['serving', 'latency', 'throughput', 'compression', 'distillation', 'quantization', 'memory', 'efficiency'],
      },
      {
        topic: 'foundation-models',
        keywords: ['llm', 'language model', 'pretraining', 'post-training', 'alignment', 'instruction tuning', 'reasoning'],
      },
    ];

    for (let i = 0; i < heuristicRules.length; i += 1) {
      const rule = heuristicRules[i];
      if (rule.keywords.some((keyword) => text.includes(keyword))) {
        return taxonomy.includes(rule.topic) ? rule.topic : 'other';
      }
    }

    const inputText = [`title=${paper.title}`, `abstract=${paper.abstract || ''}`].join('\n');
    const response = OpenAIService.classifyPaperTopic(inputText);
    const topic = String(response.topic || 'other').trim();
    return taxonomy.includes(topic) ? topic : 'other';
  },

  buildPrompt(paper, topicTag) {
    return [
      '당신은 AI study club용 weekly AI news editor다.',
      '논문을 source로 유지하되, 제목과 서술은 뉴스형(news-style)으로 작성하라.',
      '반드시 아래 논문 정보만 근거로 작성하라.',
      '기본 문장은 한국어로만 작성하라.',
      '영어는 기술용어가 꼭 필요할 때만 쓰고 반드시 English(한국어) 형식으로 병기하라.',
      '반드시 JSON으로만 답하라.',
      '필수 키: title, core_explanation, why_it_matters, quick_terms, discussion_prompt',
      '과장된 일반론, 뜬금없는 시사점, 출처에 없는 주장 금지.',
      'title: 뉴스 스타일 제목, 50자 이내',
      'core_explanation: 2~3문장, 350자 이내',
      'why_it_matters: 2~3문장, 350자 이내',
      'quick_terms: 2~3개 bullet, 220자 이내, 기술용어만 English(한국어) 형식 사용',
      'discussion_prompt: 1문장, 80자 이내',
      '',
      `Category: ${this.TOPIC_LABELS[topicTag] || this.TOPIC_LABELS.other}`,
      `Paper title: ${paper.title}`,
      `Abstract: ${paper.abstract || 'No abstract available'}`,
      `Source: ${paper.url}`,
      `Published at: ${paper.published_at || 'unknown'}`,
      `Citation count: ${paper.citation_count}`,
      '',
      '{"title":"...","core_explanation":"...","why_it_matters":"...","quick_terms":"- term: 설명 (English)\\n- term: 설명 (English)","discussion_prompt":"..."}',
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
      normalized.why_it_matters = 'This work may matter for real-world AI systems. 이 연구가 실제 AI 시스템 설계와 응용에 어떤 영향을 주는지 추가 확인이 필요합니다.';
    }
    if (!normalized.quick_terms) {
      normalized.quick_terms = '- key term | 핵심 용어: 원문 source를 함께 확인하세요.';
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

  buildTrendPayload(section, index, total) {
    return {
      content: `이번 주 AI 뉴스 ${index}/${total}`,
      embeds: [
        {
          title: Utils.safeTruncateText(section.generated.title, 220),
          color: 15844367,
          fields: [
            {
              name: '분야',
              value: Utils.safeTruncateText(this.TOPIC_LABELS[section.topicTag] || this.TOPIC_LABELS.other, this.FIELD_LIMITS.category),
              inline: false,
            },
            {
              name: '핵심 설명',
              value: Utils.safeTruncateText(section.generated.core_explanation, this.FIELD_LIMITS.core),
              inline: false,
            },
            {
              name: '왜 중요한가',
              value: Utils.safeTruncateText(section.generated.why_it_matters, this.FIELD_LIMITS.reason),
              inline: false,
            },
            {
              name: '용어 빠르게 이해하기',
              value: Utils.safeTruncateText(section.generated.quick_terms, this.FIELD_LIMITS.terms),
              inline: false,
            },
            {
              name: '생각해볼 질문',
              value: Utils.safeTruncateText(section.generated.discussion_prompt, this.FIELD_LIMITS.question),
              inline: false,
            },
            {
              name: '출처',
              value: Utils.safeTruncateText(`- ${section.paper.title}: ${section.paper.url}`, this.FIELD_LIMITS.source),
              inline: false,
            },
            {
              name: '인용수',
              value: String(section.paper.citation_count),
              inline: false,
            },
            {
              name: '주의',
              value: this.CAUTION_MESSAGE,
              inline: false,
            },
          ],
        },
      ],
    };
  },
};
