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
    'foundation-models': 'LLM과 추론',
    'vision-perception': '이미지·영상 이해',
    'multimodal-agents': '멀티모달·에이전트',
    'speech-audio': '음성·오디오 AI',
    'retrieval-search': '검색·RAG',
    'robotics-embodied': '로봇·자율행동',
    'generation-creative': '이미지·영상 생성',
    'data-training': '데이터·학습 방법',
    'systems-efficiency': '모델 경량화·서빙',
    other: '기타 AI 연구',
  },

  SELECTION_WEIGHTS: {
    recency: 10,
    impact: 15,
    reproducibility: 20,
    experimental_depth: 20,
    research_fit: 20,
    implementation_signal: 15,
  },

  RESEARCH_FIT_KEYWORDS: [
    'llm',
    'language model',
    'reasoning',
    'alignment',
    'benchmark',
    'evaluation',
    'dataset',
    'generalization',
    'robustness',
    'vision',
    'segmentation',
    'detection',
    'multimodal',
    'vision-language',
    'agent',
    'retrieval',
    'rag',
    'diffusion',
    'generation',
    'quantization',
    'distillation',
    'serving',
    'pretraining',
    'fine-tuning',
    'training',
    'optimization',
  ],

  EVALUATION_SIGNAL_KEYWORDS: [
    'benchmark',
    'evaluation',
    'ablation',
    'baseline',
    'compare',
    'comparison',
    'generalization',
    'robustness',
    'error analysis',
    'human evaluation',
    'leaderboard',
    'dataset',
  ],

  IMPLEMENTATION_SIGNAL_KEYWORDS: [
    'open source',
    'open-source',
    'github',
    'code available',
    'code release',
    'released',
    'reproducible',
    'checkpoint',
  ],

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
          'speech-audio',
          'retrieval-search',
          'robotics-embodied',
          'generation-creative',
          'data-training',
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
        url: item.primary_location?.landing_page_url || item.best_oa_location?.landing_page_url || item.ids?.openalex || '',
        published_at: item.publication_date || '',
        citation_count: Utils.toNumber(item.cited_by_count, 0),
        fwci: Utils.toNumber(item.fwci, 0),
        citation_percentile: Utils.toNumber(item.citation_normalized_percentile?.value, 0),
        is_retracted: Boolean(item.is_retracted),
        has_fulltext: Boolean(item.open_access?.any_repository_has_fulltext),
        is_oa: Boolean(item.open_access?.is_oa),
        doi: item.ids?.doi || item.doi || '',
        openalex_topic: item.primary_topic?.display_name || '',
        arxiv_id: Utils.extractArxivId(item.primary_location?.landing_page_url || item.ids?.doi || item.doi || ''),
      }))
      .filter((item) => item.title && item.url)
      .sort((a, b) => String(b.published_at).localeCompare(String(a.published_at)));
  },

  selectWeeklyPapers(papers, topN) {
    const ranked = this.rankWeeklyPapers(papers);
    const unseen = [];
    const seen = [];
    ranked.forEach((paper) => {
      if (HistoryService.hasSeenPaper(Utils.normalizeArxivUrl(paper.url))) {
        seen.push(paper);
        return;
      }
      unseen.push(paper);
    });

    const selected = unseen.slice(0, topN);
    if (selected.length < topN) {
      seen.slice(0, topN - selected.length).forEach((paper) => selected.push(paper));
    }
    selected.forEach((paper) => Logger.log(this.formatSelectionLogLine(paper)));
    return selected;
  },

  rankWeeklyPapers(papers) {
    const ranked = [];
    papers.forEach((paper) => {
      const enriched = this.enrichPaperForSelection(paper);
      if (enriched.is_retracted) {
        return;
      }
      ranked.push(enriched);
    });
    ranked.sort((a, b) => {
      if (b.selection_score !== a.selection_score) {
        return b.selection_score - a.selection_score;
      }
      if (String(b.published_at) !== String(a.published_at)) {
        return String(b.published_at).localeCompare(String(a.published_at));
      }
      return String(a.title).localeCompare(String(b.title));
    });
    return ranked;
  },

  enrichPaperForSelection(paper) {
    const enriched = Object.assign({}, paper);
    const community = this.fetchHuggingFaceMetadata(enriched.arxiv_id);
    Object.assign(enriched, community);
    const breakdown = this.buildSelectionBreakdown(enriched);
    enriched.selection_breakdown = breakdown;
    enriched.selection_score = this.roundScore(
      breakdown.recency +
        breakdown.impact +
        breakdown.reproducibility +
        breakdown.experimental_depth +
        breakdown.research_fit +
        breakdown.implementation_signal,
    );
    return enriched;
  },

  buildSelectionBreakdown(paper) {
    return {
      recency: this.scoreRecency(paper.published_at),
      impact: this.scoreImpact(paper),
      reproducibility: this.scoreReproducibility(paper),
      experimental_depth: this.scoreExperimentalDepth(paper),
      research_fit: this.scoreResearchFit(paper),
      implementation_signal: this.scoreImplementationSignal(paper),
    };
  },

  scoreRecency(publishedAt) {
    const date = this.parsePublishedDate(publishedAt);
    if (!date) {
      return 0;
    }
    const today = new Date();
    const ageDays = Math.max(Math.floor((today.getTime() - date.getTime()) / (24 * 60 * 60 * 1000)), 0);
    if (ageDays <= 1) {
      return this.SELECTION_WEIGHTS.recency;
    }
    if (ageDays <= 3) {
      return this.roundScore(this.SELECTION_WEIGHTS.recency * 0.8);
    }
    if (ageDays <= 7) {
      return this.roundScore(this.SELECTION_WEIGHTS.recency * 0.6);
    }
    if (ageDays >= 8) {
      return 0;
    }
    return 0;
  },

  scoreImpact(paper) {
    const percentileScore = Math.min(8, Utils.toNumber(paper.citation_percentile, 0) * 8);
    const fwciScore = Math.min(4, (Utils.toNumber(paper.fwci, 0) / 20) * 4);
    const citationScore = Math.min(3, (Utils.toNumber(paper.citation_count, 0) / 100) * 3);
    return this.roundScore(percentileScore + fwciScore + citationScore);
  },

  scoreReproducibility(paper) {
    if (paper.is_retracted) {
      return 0;
    }
    const text = this.buildPaperText(paper);
    let score = 0;
    if (paper.doi) {
      score += 4;
    }
    if (paper.has_fulltext) {
      score += 5;
    }
    if (paper.is_oa) {
      score += 3;
    }
    if ((paper.abstract || '').length >= 400) {
      score += 3;
    }
    if (this.countKeywordMatches(text, this.IMPLEMENTATION_SIGNAL_KEYWORDS) > 0 || Utils.toNumber(paper.hf_github_stars, 0) > 0) {
      score += 5;
    }
    return this.roundScore(Math.min(this.SELECTION_WEIGHTS.reproducibility, score));
  },

  scoreExperimentalDepth(paper) {
    const text = this.buildPaperText(paper);
    const matches = this.countKeywordMatches(text, this.EVALUATION_SIGNAL_KEYWORDS);
    let score = 4 + Math.min(10, matches * 2);
    if ((paper.abstract || '').length >= 800) {
      score += 2;
    }
    if (text.includes('ablation')) {
      score += 2;
    }
    if (text.includes('benchmark') || text.includes('dataset')) {
      score += 2;
    }
    return this.roundScore(Math.min(this.SELECTION_WEIGHTS.experimental_depth, score));
  },

  scoreResearchFit(paper) {
    const text = this.buildPaperText(paper);
    const matches = this.countKeywordMatches(text, this.RESEARCH_FIT_KEYWORDS);
    let score = 4 + Math.min(14, matches * 1.5);
    if (paper.openalex_topic) {
      score += 2;
    }
    return this.roundScore(Math.min(this.SELECTION_WEIGHTS.research_fit, score));
  },

  scoreImplementationSignal(paper) {
    const text = this.buildPaperText(paper);
    const upvoteScore = Math.min(3, (Utils.toNumber(paper.hf_upvotes, 0) / 150) * 3);
    const githubScore = Math.min(8, (Utils.toNumber(paper.hf_github_stars, 0) / 30000) * 8);
    let dailyRankScore = 0;
    const dailyRank = Utils.toNumber(paper.hf_daily_rank, 0);
    if (dailyRank === 1) {
      dailyRankScore = 2;
    } else if (dailyRank > 1 && dailyRank <= 5) {
      dailyRankScore = 1.5;
    } else if (dailyRank > 5 && dailyRank <= 10) {
      dailyRankScore = 1;
    }
    const keywordBonus = this.countKeywordMatches(text, this.IMPLEMENTATION_SIGNAL_KEYWORDS) > 0 ? 2 : 0;
    return this.roundScore(Math.min(this.SELECTION_WEIGHTS.implementation_signal, upvoteScore + githubScore + dailyRankScore + keywordBonus));
  },

  buildPaperText(paper) {
    return `${paper.title || ''} ${paper.abstract || ''}`.toLowerCase();
  },

  countKeywordMatches(text, keywords) {
    return keywords.filter((keyword) => text.includes(keyword)).length;
  },

  fetchHuggingFaceMetadata(arxivId) {
    if (!arxivId) {
      return { hf_upvotes: 0, hf_github_stars: 0, hf_daily_rank: 0 };
    }

    const cache = CacheService.getScriptCache();
    const cacheKey = `hf-paper:${arxivId}`;
    const cached = cache.get(cacheKey);
    if (cached) {
      return JSON.parse(cached);
    }

    try {
      const response = UrlFetchApp.fetch(`https://huggingface.co/papers/${encodeURIComponent(arxivId)}`, {
        muteHttpExceptions: true,
        headers: { 'User-Agent': 'Mozilla/5.0' },
      });
      if (response.getResponseCode() !== 200) {
        return { hf_upvotes: 0, hf_github_stars: 0, hf_daily_rank: 0 };
      }

      const html = response.getContentText();
      const metadata = {
        hf_github_stars: this.extractHtmlNumber(html, /githubStars&quot;:(\d+)/i),
        hf_daily_rank: this.extractHtmlNumber(html, /dailyPaperRank&quot;:(\d+)/i),
        hf_upvotes: this.extractHtmlNumber(html, /Upvote[^0-9]{0,20}(\d+)/i),
      };
      cache.put(cacheKey, JSON.stringify(metadata), 6 * 60 * 60);
      return metadata;
    } catch (error) {
      Logger.log(`TrendService:hf_fetch_failed arxiv_id=${arxivId} error=${error}`);
      return { hf_upvotes: 0, hf_github_stars: 0, hf_daily_rank: 0 };
    }
  },

  extractHtmlNumber(text, regex) {
    const match = String(text || '').match(regex);
    return match && match[1] ? Utils.toNumber(match[1], 0) : 0;
  },

  parsePublishedDate(value) {
    if (!value) {
      return null;
    }
    const date = new Date(String(value));
    return Number.isNaN(date.getTime()) ? null : date;
  },

  roundScore(value) {
    return Math.round(Utils.toNumber(value, 0) * 100) / 100;
  },

  formatSelectionLogLine(paper) {
    const breakdown = paper.selection_breakdown || {};
    const breakdownText = Object.keys(breakdown)
      .sort()
      .map((key) => `${key}=${breakdown[key]}`)
      .join(',');
    return `TrendService:selection score=${paper.selection_score || 0} title=${paper.title} breakdown=${breakdownText}`;
  },

  tagPaperTopic(paper, taxonomy) {
    const text = `${paper.title}\n${paper.abstract || ''}`.toLowerCase();
    const heuristicRules = [
      {
        topic: 'robotics-embodied',
        keywords: ['robot', 'robotics', 'manipulation', 'locomotion', 'navigation', 'policy learning', 'sim2real'],
      },
      {
        topic: 'multimodal-agents',
        keywords: ['vision-language-action', 'vision language action', 'multimodal', 'embodied', 'vlm', 'vla', 'agent'],
      },
      {
        topic: 'speech-audio',
        keywords: ['speech', 'audio', 'voice', 'asr', 'tts', 'speaker', 'sound event', 'speech recognition'],
      },
      {
        topic: 'retrieval-search',
        keywords: ['retrieval', 'rag', 'search', 'rerank', 'reranker', 'dense retrieval', 'knowledge base', 'indexing'],
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
        topic: 'data-training',
        keywords: ['dataset', 'data curation', 'synthetic data', 'preference data', 'curriculum', 'data mixture', 'annotation'],
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
      '- 후속 실험 설계',
      '- 평가 방식의 공백',
      '- 재현에 필요한 조건',
      '- 데이터 또는 계산 자원 제약',
      '- 기존 baseline과의 비교 한계',
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
      'speech-audio': [
        'automatic speech recognition(음성 인식): 사람 음성을 텍스트로 바꾸는 작업',
        'text-to-speech(음성 합성): 텍스트를 자연스러운 음성으로 생성하는 기술',
        'speaker representation(화자 표현): 화자의 특성을 벡터 형태로 담아내는 방식',
      ],
      'retrieval-search': [
        'retrieval(검색): 필요한 정보를 외부 저장소에서 찾아오는 과정',
        'reranking(재정렬): 검색된 후보를 더 정확한 기준으로 다시 순서화하는 단계',
        'indexing(색인화): 빠른 검색을 위해 문서를 검색 가능한 구조로 저장하는 작업',
      ],
      'robotics-embodied': [
        'manipulation(조작): 로봇이 물체를 잡고 옮기고 다루는 능력',
        'navigation(이동 계획): 환경 안에서 목적지까지 경로를 정하고 움직이는 과정',
        'sim2real(시뮬레이션-현실 전이): 가상 환경에서 학습한 정책을 실제 환경에 적용하는 문제',
      ],
      'generation-creative': [
        'diffusion(확산 모델): 점진적으로 노이즈를 제거하며 이미지를 생성하는 방식',
        'editing(편집): 기존 이미지나 영상을 조건에 맞게 바꾸는 작업',
        'avatar(아바타): 사람이나 캐릭터를 디지털 형태로 재현한 대상',
      ],
      'data-training': [
        'dataset curation(데이터 큐레이션): 학습 목적에 맞게 데이터를 선별하고 정리하는 과정',
        'synthetic data(합성 데이터): 실제 수집 대신 생성 방식으로 만든 학습용 데이터',
        'curriculum learning(커리큘럼 학습): 쉬운 예시부터 어려운 예시로 점차 학습하는 전략',
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
