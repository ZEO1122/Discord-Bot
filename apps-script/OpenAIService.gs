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
      '라벨 후보: llm, detection-segmentation, vision-language, other',
      'few-shot 예시:',
      '입력: title=Preference Alignment of Vision-Language-Action Model / abstract=운전자의 선호를 반영한 비전-언어-행동 모델',
      '출력: llm',
      '입력: title=Panoptic Segmentation for Medical Imaging / abstract=병변 분할과 검출을 함께 다룬다',
      '출력: detection-segmentation',
      '입력: title=Vision-Language Model for Image Captioning / abstract=이미지와 텍스트 표현 정렬',
      '출력: vision-language',
      'JSON으로만 답하라.',
      '{"topic":"llm"}',
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
