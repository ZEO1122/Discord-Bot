const OpenAIService = {
  generateTrendBrief(prompt) {
    const apiKey = ConfigService.getOpenAiKey();
    const model = ConfigService.getOpenAiModel();
    Logger.log(`OpenAIService:request model=${model} prompt_length=${String(prompt).length}`);
    const response = UrlFetchApp.fetch('https://api.openai.com/v1/responses', {
      method: 'post',
      contentType: 'application/json',
      headers: {
        Authorization: `Bearer ${apiKey}`,
      },
      payload: JSON.stringify({
        model,
        input: prompt,
        text: {
          format: { type: 'json_object' },
        },
      }),
      muteHttpExceptions: true,
    });
    const status = response.getResponseCode();
    Logger.log(`OpenAIService:response status=${status}`);
    if (status < 200 || status >= 300) {
      throw new Error(`OpenAI response failed: ${status} ${response.getContentText()}`);
    }
    return JSON.parse(response.getContentText());
  },

  classifyPaperTopic(inputText) {
    const apiKey = ConfigService.getOpenAiKey();
    const model = ConfigService.getOpenAiModel();
    const prompt = [
      '당신은 AI 논문 분류기다.',
      '아래 논문 제목과 초록을 읽고 정확히 하나의 라벨만 반환하라.',
      '라벨 후보: foundation-models, vision-perception, multimodal-agents, generation-creative, systems-efficiency, other',
      'few-shot 예시:',
      '입력: title=Preference Alignment of Large Language Models / abstract=alignment, post-training, agent behavior, reasoning',
      '출력: foundation-models',
      '입력: title=Panoptic Segmentation for Medical Imaging / abstract=segmentation, detection, scene understanding',
      '출력: vision-perception',
      '입력: title=Vision-Language-Action Model for Driving / abstract=vision-language-action, multimodal reasoning, embodied agent',
      '출력: multimodal-agents',
      '입력: title=Diffusion-based Video Editing / abstract=video generation and editing',
      '출력: generation-creative',
      '입력: title=Efficient LLM Serving with Quantization / abstract=serving latency throughput optimization',
      '출력: systems-efficiency',
      'JSON으로만 답하라.',
      '{"topic":"foundation-models"}',
      '',
      '입력:',
      inputText,
    ].join('\n');

    Logger.log(`OpenAIService:classify request model=${model} prompt_length=${String(prompt).length}`);
    const response = UrlFetchApp.fetch('https://api.openai.com/v1/responses', {
      method: 'post',
      contentType: 'application/json',
      headers: {
        Authorization: `Bearer ${apiKey}`,
      },
      payload: JSON.stringify({
        model,
        input: prompt,
        text: {
          format: { type: 'json_object' },
        },
      }),
      muteHttpExceptions: true,
    });
    const status = response.getResponseCode();
    Logger.log(`OpenAIService:classify response status=${status}`);
    if (status < 200 || status >= 300) {
      throw new Error(`OpenAI classify failed: ${status} ${response.getContentText()}`);
    }
    return JSON.parse(response.getContentText());
  }
};
