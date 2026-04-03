const TrendService = {
  FIELD_LIMITS: {
    category: 180,
    core: 700,
    reason: 700,
    terms: 600,
    question: 120,
    source: 900,
  },

  TOPIC_LABELS: {
    'foundation-models': '파운데이션 모델',
    'vision-perception': '비전 인지',
    'multimodal-agents': '멀티모달 에이전트',
    'generation-creative': '생성·크리에이티브',
    'systems-efficiency': '시스템 효율화',
    other: '기타',
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
      const generated = this.normalizeTrendOutput(OpenAIService.generateTrendBrief(prompt), paper, topicTag);
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
    const seen = [];
    for (let i = 0; i < papers.length; i += 1) {
      const paper = papers[i];
      if (HistoryService.hasSeenPaper(Utils.normalizeArxivUrl(paper.url))) {
        seen.push(paper);
        continue;
      }
      selected.push(paper);
      if (selected.length >= topN) {
        break;
      }
    }
    if (selected.length < topN) {
      for (let i = 0; i < seen.length; i += 1) {
        selected.push(seen[i]);
        if (selected.length >= topN) {
          break;
        }
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
      '영어는 논문을 읽으며 이해가 필요한 기술용어에만 제한적으로 사용하라.',
      '영어를 쓸 경우 반드시 English(한국어) 형식으로 병기하라.',
      '일반 문장, 평가 문장, 시사점 문장에는 영어를 섞지 마라.',
      '예: alignment(정렬), quantization(양자화), retrieval(검색)',
      '반드시 JSON으로만 답하라.',
      '필수 키: title, core_explanation, why_it_matters, quick_terms, discussion_prompt',
      '과장된 일반론, 뜬금없는 시사점, 출처에 없는 주장 금지.',
      'title: 뉴스 스타일 제목, 50자 이내',
      'core_explanation: 2~3문장, 350자 이내',
      'why_it_matters: 2~3문장, 350자 이내',
      'quick_terms: 2~3개 bullet, 220자 이내, 어려운 기술용어만 English(한국어) 형식으로 설명',
      'discussion_prompt: 1문장, 100자 이내',
      'discussion_prompt는 아래 관점 중 하나를 골라 구체적으로 작성하라:',
      '- 실제 적용 가능성',
      '- 성능과 비용 사이의 trade-off',
      '- 데이터 요구사항',
      '- 평가 방식의 한계',
      '- 안전성 또는 신뢰성',
      'discussion_prompt에서 너무 일반적인 질문은 금지한다.',
      '예: "이 논문이 실제 적용에 미칠 영향은 무엇일까?" 같은 반복 문장은 쓰지 마라.',
      '논문 제목/초록에 나온 핵심 개념을 직접 반영한 질문으로 작성하라.',
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

  normalizeTrendOutput(response, paper, topicTag) {
    const rawText = this.extractOutputText(response);
    const parsed = JSON.parse(rawText);
    const normalized = this.normalizeGeneratedFields(parsed, paper, topicTag);
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

  normalizeGeneratedFields(data, paper, topicTag) {
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
      normalized.why_it_matters = '이 연구가 실제 AI 시스템 설계와 응용 방향에 어떤 영향을 줄지 추가 확인이 필요합니다.';
    }
    if (!normalized.quick_terms) {
      normalized.quick_terms = this.buildQuickTermsFallback(paper, topicTag);
    }
    if (!normalized.discussion_prompt && normalized.title) {
      normalized.discussion_prompt = `${normalized.title}가 실제 적용에 미칠 영향은 무엇일까?`;
    }
    return normalized;
  },

  buildQuickTermsFallback(paper, topicTag) {
    const text = `${paper.title}\n${paper.abstract || ''}`.toLowerCase();
    const fallbackMap = {
      'foundation-models': [
        'alignment(정렬): 모델 응답을 사람 의도와 기준에 맞추는 과정',
        'post-training(사후 학습): 사전학습 뒤 실제 사용 목적에 맞게 추가로 학습하는 단계',
        'reasoning(추론): 여러 단계를 거쳐 답을 도출하는 능력',
      ],
      'vision-perception': [
        'segmentation(분할): 이미지에서 물체나 영역의 경계를 픽셀 단위로 나누는 작업',
        'detection(검출): 이미지 안에서 물체가 어디 있는지 찾아내는 작업',
        'panoptic(파놉틱): 검출과 분할을 함께 다루는 통합 시각 이해 설정',
      ],
      'multimodal-agents': [
        'vision-language-action(비전-언어-행동): 시각·언어 입력을 받아 행동까지 결정하는 모델 구조',
        'embodied agent(체화 에이전트): 실제 환경에서 지각하고 행동하는 에이전트',
        'multimodal reasoning(멀티모달 추론): 이미지·텍스트 등 여러 형식을 함께 보고 판단하는 능력',
      ],
      'generation-creative': [
        'diffusion(확산 모델): 점진적으로 노이즈를 제거하며 이미지를 생성하는 방식',
        'editing(편집): 기존 이미지나 영상을 조건에 맞게 바꾸는 작업',
        'avatar(아바타): 사람이나 캐릭터를 디지털 형태로 재현한 대상',
      ],
      'systems-efficiency': [
        'quantization(양자화): 모델 수치 표현을 더 작은 비트로 줄여 효율을 높이는 기법',
        'distillation(지식 증류): 큰 모델의 지식을 작은 모델로 옮기는 학습 방법',
        'throughput(처리량): 일정 시간 동안 시스템이 처리할 수 있는 작업량',
      ],
      other: [
        'benchmark(벤치마크): 모델 성능을 비교하기 위한 평가 기준',
        'pipeline(파이프라인): 여러 처리 단계를 연결한 작업 흐름',
        'modality(모달리티): 텍스트·이미지·음성처럼 입력 데이터의 형식',
      ],
    };

    let terms = fallbackMap[topicTag] || fallbackMap.other;

    if (text.includes('retrieval')) {
      terms = ['retrieval(검색): 필요한 정보를 외부 저장소에서 찾아오는 과정', ...terms.slice(0, 2)];
    }
    if (text.includes('agent')) {
      terms = ['agent(에이전트): 목표를 위해 판단하고 행동하는 시스템', ...terms.slice(0, 2)];
    }
    if (text.includes('token')) {
      terms = ['token(토큰): 모델이 입력을 잘게 나눠 처리하는 최소 단위', ...terms.slice(0, 2)];
    }

    return terms.slice(0, 3).map((term) => `- ${term}`).join('\n');
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
      embeds: [
        {
          title: Utils.safeTruncateText(`이번주 AI 뉴스 || ${section.generated.title}`, 220),
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
              value: this.formatLinePreservingField(section.generated.quick_terms, this.FIELD_LIMITS.terms),
              inline: false,
            },
            {
              name: '생각해볼 질문',
              value: Utils.safeTruncateText(section.generated.discussion_prompt, this.FIELD_LIMITS.question),
              inline: false,
            },
            {
              name: '출처',
              value: this.formatLinePreservingField(`- ${section.paper.title}: ${section.paper.url}`, this.FIELD_LIMITS.source),
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

  formatLinePreservingField(text, limit) {
    const lines = String(text || '')
      .split('\n')
      .map((line) => line.trim())
      .filter(Boolean);
    if (!lines.length) {
      return '';
    }

    const accepted = [];
    let currentLength = 0;
    for (let i = 0; i < lines.length; i += 1) {
      const line = lines[i];
      const normalizedLine = Utils.safeTruncateText(line, Math.min(limit, 300));
      const candidateLength = currentLength === 0
        ? normalizedLine.length
        : currentLength + 1 + normalizedLine.length;
      if (candidateLength > limit) {
        break;
      }
      accepted.push(normalizedLine);
      currentLength = candidateLength;
    }

    if (!accepted.length) {
      return Utils.safeTruncateText(lines[0], limit);
    }
    return accepted.join('\n');
  },
};
