<!-- FILE: dl-concept-001-perceptron.md -->
---
briefing_key: "dl-concept-001-perceptron"
track: "dl-basics"
mode: "concept"
title: "퍼셉트론"
one_line: "퍼셉트론은 입력의 가중합을 기준으로 두 범주를 나누는 가장 기본적인 인공 뉴런 모델이다."
discussion_prompt: "복잡한 신경망을 이해할 때 퍼셉트론의 단순한 결정 방식이 여전히 중요한 이유는 무엇일까?"
---

## 핵심 설명
- 퍼셉트론은 입력값에 가중치를 곱해 더한 뒤, 그 값이 기준을 넘는지에 따라 출력을 정하는 모델이다. 가장 단순한 이진 분류기의 형태로 볼 수 있다.
- 이 개념은 신경망이 입력을 선형 결합해 판단한다는 출발점을 보여 준다. 복잡한 모델도 기본적으로는 이런 연산을 여러 층에 걸쳐 반복한다.
- 한 개의 퍼셉트론은 직선이나 평면 같은 선형 경계만 만들 수 있다. 그래서 XOR처럼 선형적으로 나눌 수 없는 문제는 단독으로 풀기 어렵다.
- 퍼셉트론은 오늘날의 깊은 신경망보다 단순하지만, 가중치 학습과 결정 경계라는 핵심 아이디어를 이해하는 데 매우 유용하다.

## 직관
- 여러 개의 체크 항목에 점수를 매기고, 총점이 기준 이상이면 합격이라고 판단하는 방식과 비슷하다.
- 문 앞 경비원이 여러 조건을 빠르게 합쳐 들어올 수 있는지 없는지를 판단하는 규칙으로 생각할 수 있다.

## 헷갈리기 쉬운 점
- 퍼셉트론이 곧 모든 신경망을 뜻하는 것은 아니다. 퍼셉트론은 신경망을 이루는 아주 기본적인 출발점에 가깝다.
- 퍼셉트론이 학습한다고 해서 모든 패턴을 배울 수 있는 것은 아니다. 한 개의 퍼셉트론은 비선형 관계를 직접 표현하지 못한다.

## 셀프 체크 퀴즈
1. 퍼셉트론이 선형 분류기라고 불리는 이유는 무엇인가?
2. 한 개의 퍼셉트론으로 XOR 문제를 풀기 어려운 이유는 무엇인가?
3. 퍼셉트론에서 가중치와 기준값이 결정에 어떤 역할을 하는가?

## source
- Frank Rosenblatt / The Perceptron: A Probabilistic Model for Information Storage and Organization in the Brain / 1958
- Ian Goodfellow, Yoshua Bengio, Aaron Courville / Deep Learning / 2016
- Stanford / CS231n Course Notes on Linear Classification and Neural Networks

<!-- FILE: dl-concept-002-neural-network.md -->
---
briefing_key: "dl-concept-002-neural-network"
track: "dl-basics"
mode: "concept"
title: "인공신경망"
one_line: "인공신경망은 여러 뉴런 층을 연결해 입력으로부터 복잡한 패턴을 배우는 함수 근사 모델이다."
discussion_prompt: "인공신경망이 단순한 규칙 모음이 아니라 표현을 스스로 학습하는 도구라고 볼 수 있는 이유는 무엇일까?"
---

## 핵심 설명
- 인공신경망은 입력층, 은닉층, 출력층으로 이루어진 여러 연산 단계를 통해 데이터를 변환한다. 각 층은 이전 층의 출력을 받아 더 추상적인 표현을 만든다.
- 중요한 점은 사람이 특징을 일일이 설계하지 않아도, 모델이 학습 과정에서 유용한 표현을 스스로 찾는다는 것이다.
- 은닉층이 늘고 비선형 활성화가 들어가면 단순한 직선 구분을 넘어 매우 복잡한 함수를 근사할 수 있다.
- 이미지, 텍스트, 음성처럼 구조가 복잡한 데이터에서 인공신경망은 입력을 단계적으로 해석하는 데 자주 쓰인다.

## 직관
- 공장에서 원재료가 여러 공정을 거치며 완제품으로 바뀌듯이, 입력 데이터도 층을 지날수록 더 해석하기 쉬운 표현으로 바뀐다.
- 첫 번째 층은 작은 단서만 보고, 뒤쪽 층은 그것들을 조합해 더 큰 의미를 알아보는 팀 작업처럼 생각할 수 있다.

## 헷갈리기 쉬운 점
- 층이 많다고 자동으로 좋은 모델이 되는 것은 아니다. 데이터, 구조, 학습 방법이 함께 맞아야 성능이 나온다.
- 인공신경망이 사람 뇌를 그대로 흉내 내는 것은 아니다. 이름은 유사성에서 왔지만 실제 동작은 수학적 최적화에 더 가깝다.

## 셀프 체크 퀴즈
1. 인공신경망에서 은닉층은 왜 필요한가?
2. 비선형 활성화가 없으면 여러 층을 쌓아도 표현력이 제한되는 이유는 무엇인가?
3. 인공신경망이 입력에서 표현을 학습한다는 말은 무엇을 뜻하는가?

## source
- Ian Goodfellow, Yoshua Bengio, Aaron Courville / Deep Learning / 2016
- Christopher M. Bishop / Pattern Recognition and Machine Learning / 2006
- Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola / Dive into Deep Learning

<!-- FILE: dl-concept-003-weights-and-biases.md -->
---
briefing_key: "dl-concept-003-weights-and-biases"
track: "dl-basics"
mode: "concept"
title: "가중치와 편향"
one_line: "가중치와 편향은 신경망이 입력을 해석하는 방식을 정하는 기본 학습 파라미터다."
discussion_prompt: "같은 입력을 받아도 가중치와 편향이 다르면 전혀 다른 판단이 나오는 이유는 무엇일까?"
---

## 핵심 설명
- 가중치는 각 입력이 결과에 얼마나 큰 영향을 주는지 정한다. 어떤 입력은 크게 반영하고 어떤 입력은 거의 무시하도록 학습될 수 있다.
- 편향은 전체 출력을 일정하게 이동시키는 역할을 한다. 입력이 모두 0이어도 뉴런이 특정 기준에서 출발할 수 있게 해 준다.
- 학습이란 결국 손실을 줄이는 방향으로 가중치와 편향을 조금씩 조정하는 과정이다. 모델의 지식은 이 파라미터 안에 저장된다고 볼 수 있다.
- 가중치만 있고 편향이 없다면 표현력이 불필요하게 제한될 수 있다. 편향은 결정 경계를 더 유연하게 움직이게 만든다.

## 직관
- 가중치는 각 재료의 비율이고, 편향은 기본 간의 세기처럼 생각할 수 있다. 같은 재료라도 기본 간이 다르면 전체 맛이 달라진다.
- 가중치는 투표권의 크기, 편향은 출발 점수와 비슷하다. 어떤 항목은 큰 표를 갖고, 전체 판단은 기본 점수에서 시작한다.

## 헷갈리기 쉬운 점
- 가중치가 크다고 항상 좋은 특징이라는 뜻은 아니다. 데이터의 스케일과 다른 파라미터와의 관계까지 함께 봐야 한다.
- 편향은 단순한 보정값 이상이다. 편향이 있어야 뉴런이 원점을 지나지 않는 다양한 함수를 표현하기 쉬워진다.

## 셀프 체크 퀴즈
1. 가중치와 편향은 각각 어떤 역할을 하는가?
2. 편향이 없으면 결정 경계 표현에 어떤 제약이 생길 수 있는가?
3. 학습 과정에서 모델의 지식이 가중치와 편향에 저장된다고 말하는 이유는 무엇인가?

## source
- Ian Goodfellow, Yoshua Bengio, Aaron Courville / Deep Learning / 2016
- Christopher M. Bishop / Pattern Recognition and Machine Learning / 2006
- Stanford / CS231n Neural Networks Part 1

<!-- FILE: dl-concept-004-activation-functions.md -->
---
briefing_key: "dl-concept-004-activation-functions"
track: "dl-basics"
mode: "concept"
title: "활성화 함수"
one_line: "활성화 함수는 뉴런의 가중합에 비선형성을 넣어 신경망이 복잡한 패턴을 표현하게 만든다."
discussion_prompt: "신경망에서 활성화 함수가 없다면 층을 여러 개 쌓는 의미가 왜 크게 줄어들까?"
---

## 핵심 설명
- 활성화 함수는 뉴런의 선형 결합 결과를 바로 내보내지 않고 한 번 변환한다. 이 비선형성이 있어야 신경망은 복잡한 관계를 표현할 수 있다.
- 시그모이드, 탄흐, ReLU(Rectified Linear Unit) 같은 함수는 출력 범위와 기울기 특성이 서로 다르다. 그래서 쓰임새와 학습 안정성도 달라진다.
- 은닉층에서는 ReLU 계열이 널리 쓰이고, 출력층에서는 문제 종류에 따라 다른 함수가 선택된다. 예를 들어 이진 분류는 시그모이드, 다중 분류는 소프트맥스를 자주 쓴다.
- 활성화 함수의 선택은 기울기 흐름, 학습 속도, 표현 방식에 영향을 준다. 따라서 단순한 형식 요소가 아니라 핵심 설계 요소다.

## 직관
- 선형 연산만 계속하면 아무리 단계를 나눠도 결국 하나의 큰 직선 계산과 비슷해진다. 활성화 함수는 그 흐름에 굴곡을 만든다.
- 같은 재료를 그냥 섞기만 하는 것이 아니라, 가열하거나 발효해 새로운 성질을 만드는 과정과 비슷하다.

## 헷갈리기 쉬운 점
- 활성화 함수는 항상 클수록 좋은 출력을 만드는 장치가 아니다. 출력의 크기보다 비선형성의 도입과 기울기 특성이 더 중요하다.
- ReLU가 많이 쓰인다고 해서 모든 층과 모든 문제에 최선인 것은 아니다. 출력층은 과제에 맞는 함수가 따로 필요하다.

## 셀프 체크 퀴즈
1. 활성화 함수가 비선형성을 제공한다는 말은 무엇을 뜻하는가?
2. 은닉층과 출력층에서 활성화 함수 선택이 달라질 수 있는 이유는 무엇인가?
3. 시그모이드와 ReLU는 학습에 어떤 차이를 만들 수 있는가?

## source
- Ian Goodfellow, Yoshua Bengio, Aaron Courville / Deep Learning / 2016
- Vinod Nair, Geoffrey E. Hinton / Rectified Linear Units Improve Restricted Boltzmann Machines / 2010
- Stanford / CS231n Neural Networks Part 1

<!-- FILE: dl-concept-005-forward-pass.md -->
---
briefing_key: "dl-concept-005-forward-pass"
track: "dl-basics"
mode: "concept"
title: "순전파"
one_line: "순전파는 입력이 네트워크를 통과하며 예측값으로 변환되는 계산 과정이다."
discussion_prompt: "학습 전에 먼저 순전파를 이해해야 역전파와 손실 계산도 자연스럽게 연결되는 이유는 무엇일까?"
---

## 핵심 설명
- 순전파는 입력 데이터를 첫 층부터 마지막 층까지 차례대로 통과시키며 출력을 계산하는 과정이다. 예측값은 이 단계에서 만들어진다.
- 각 층은 이전 층의 출력을 받아 가중합과 활성화 함수를 적용한다. 이런 변환이 반복되면서 원시 입력이 의미 있는 예측으로 바뀐다.
- 손실 함수는 순전파의 최종 결과와 정답을 비교해 계산된다. 그래서 학습의 출발점은 항상 순전파라고 볼 수 있다.
- 추론 단계에서는 보통 순전파만 수행한다. 즉 이미 학습된 파라미터를 이용해 새로운 입력에 대한 출력을 계산한다.

## 직관
- 공장 컨베이어 벨트에서 물건이 공정을 지나며 점점 완성품에 가까워지는 흐름과 비슷하다.
- 문제를 풀 때 중간 계산을 차례대로 적어 최종 답을 얻는 과정처럼, 순전파는 네트워크의 계산 기록이다.

## 헷갈리기 쉬운 점
- 순전파는 단순히 데이터를 앞으로 보내는 이동이 아니다. 각 층에서 실제 수치 변환이 일어난다.
- 순전파만으로 학습이 끝나는 것은 아니다. 예측이 얼마나 틀렸는지 계산하고, 그 정보를 바탕으로 파라미터를 수정해야 학습이 진행된다.

## 셀프 체크 퀴즈
1. 순전파에서 각 층은 이전 층의 출력을 어떻게 사용해 다음 출력을 만드는가?
2. 손실 함수 계산이 순전파 이후에 이루어지는 이유는 무엇인가?
3. 추론 단계에서 순전파는 어떤 의미를 가지는가?

## source
- Ian Goodfellow, Yoshua Bengio, Aaron Courville / Deep Learning / 2016
- Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola / Dive into Deep Learning
- Stanford / CS231n Neural Networks Part 1

<!-- FILE: dl-concept-006-loss-function.md -->
---
briefing_key: "dl-concept-006-loss-function"
track: "dl-basics"
mode: "concept"
title: "손실 함수"
one_line: "손실 함수는 모델의 예측이 정답과 얼마나 다른지를 하나의 수치로 나타내는 기준이다."
discussion_prompt: "좋은 손실 함수를 고르는 일이 모델 구조를 고르는 것만큼 중요한 이유는 무엇일까?"
---

## 핵심 설명
- 손실 함수는 예측값과 정답 사이의 차이를 수치화한다. 학습은 이 값을 줄이는 방향으로 진행된다.
- 같은 모델이라도 어떤 손실 함수를 쓰느냐에 따라 무엇을 잘 맞추려 하는지가 달라진다. 즉 손실 함수는 학습 목표를 구체적으로 정의한다.
- 회귀에서는 평균제곱오차, 분류에서는 교차엔트로피처럼 문제 유형에 맞는 손실 함수가 널리 쓰인다.
- 손실 함수가 미분 가능하거나 안정적으로 최적화될 수 있어야 기울기 기반 학습이 원활하게 작동한다.

## 직관
- 시험 채점 기준이 바뀌면 같은 답안도 평가 결과가 달라진다. 손실 함수는 모델에게 무엇이 실수인지 알려 주는 채점표와 같다.
- 길찾기에서 목적지까지의 거리를 재는 방식이 달라지면 어느 길이 좋은지 달라지는 것과 비슷하다.

## 헷갈리기 쉬운 점
- 손실 함수와 평가 지표는 항상 같은 것이 아니다. 학습에는 손실 함수를 쓰고, 최종 성능 평가는 다른 지표를 쓸 수 있다.
- 손실 값이 작다고 실제 서비스 목적에 꼭 맞는 것은 아니다. 문제에서 중요한 비용 구조가 손실 함수에 잘 반영되어야 한다.

## 셀프 체크 퀴즈
1. 손실 함수는 학습 과정에서 어떤 역할을 하는가?
2. 회귀와 분류에서 자주 쓰이는 손실 함수가 다른 이유는 무엇인가?
3. 손실 함수와 평가 지표를 구분해야 하는 이유는 무엇인가?

## source
- Ian Goodfellow, Yoshua Bengio, Aaron Courville / Deep Learning / 2016
- Christopher M. Bishop / Pattern Recognition and Machine Learning / 2006
- Kevin P. Murphy / Machine Learning: A Probabilistic Perspective / 2012

<!-- FILE: dl-concept-007-mean-squared-error.md -->
---
briefing_key: "dl-concept-007-mean-squared-error"
track: "dl-basics"
mode: "concept"
title: "평균제곱오차"
one_line: "평균제곱오차는 예측값과 정답의 차이를 제곱해 평균낸 회귀용 손실 함수다."
discussion_prompt: "오차를 그냥 평균내지 않고 제곱해서 평균내는 방식이 어떤 장점과 한계를 만들까?"
---

## 핵심 설명
- 평균제곱오차는 각 예측 오차를 제곱한 뒤 평균내는 방식이다. 오차가 0에 가까울수록 손실도 작아진다.
- 오차를 제곱하므로 큰 실수에 더 큰 벌점을 준다. 그래서 큰 편차를 강하게 줄이고 싶은 회귀 문제에서 자주 쓰인다.
- 미분이 간단하고 연속적이라 기울기 기반 최적화와 잘 맞는다. 선형 회귀부터 신경망 회귀까지 폭넓게 사용된다.
- 반대로 이상치가 있으면 손실이 크게 흔들릴 수 있다. 따라서 데이터 특성에 따라 평균절대오차 같은 다른 선택도 고려한다.

## 직관
- 작은 흠집보다 큰 흠집에 훨씬 더 엄격한 감점을 주는 채점 방식과 비슷하다.
- 거리를 제곱해 계산하면 멀리 벗어난 점이 훨씬 더 눈에 띄는 것처럼, 큰 오차가 더 강조된다.

## 헷갈리기 쉬운 점
- 평균제곱오차는 분류 문제의 기본 선택이 아니다. 확률을 다루는 분류에서는 교차엔트로피가 더 잘 맞는 경우가 많다.
- 오차를 제곱한다고 해서 항상 더 공정한 것은 아니다. 이상치가 많으면 일부 샘플이 학습을 지나치게 끌고 갈 수 있다.

## 셀프 체크 퀴즈
1. 평균제곱오차가 큰 오차에 더 민감한 이유는 무엇인가?
2. 회귀 문제에서 평균제곱오차가 자주 쓰이는 이유는 무엇인가?
3. 이상치가 많은 데이터에서 평균제곱오차가 불리할 수 있는 이유는 무엇인가?

## source
- Christopher M. Bishop / Pattern Recognition and Machine Learning / 2006
- Ian Goodfellow, Yoshua Bengio, Aaron Courville / Deep Learning / 2016
- Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola / Dive into Deep Learning

<!-- FILE: dl-concept-008-cross-entropy.md -->
---
briefing_key: "dl-concept-008-cross-entropy"
track: "dl-basics"
mode: "concept"
title: "교차엔트로피"
one_line: "교차엔트로피는 예측한 확률분포가 정답 분포와 얼마나 다른지를 측정하는 분류용 손실 함수다."
discussion_prompt: "분류 문제에서 정답을 맞혔는지뿐 아니라 얼마나 확신했는지도 중요하게 보는 이유는 무엇일까?"
---

## 핵심 설명
- 교차엔트로피는 모델이 정답 클래스에 얼마나 높은 확률을 주는지를 평가한다. 정답에 낮은 확률을 줄수록 손실이 커진다.
- 이 손실은 확률분포를 다루므로 분류 문제와 잘 맞는다. 다중 분류에서는 보통 소프트맥스 출력과 함께 사용된다.
- 틀린 예측 중에서도 확신이 큰 오답에 강한 벌점을 준다. 그래서 단순 정확도보다 더 풍부한 학습 신호를 제공한다.
- 확률을 잘 보정하고 로그 가능도를 최적화하는 관점과도 연결되어 있어, 현대 분류 모델에서 널리 쓰인다.

## 직관
- 시험 답을 틀렸을 때도 애매하게 틀린 경우와 아주 자신 있게 틀린 경우를 다르게 감점하는 방식과 비슷하다.
- 정답 상자에 얼마나 많은 확률 질량을 담아 두었는지를 보는 측정 도구라고 생각할 수 있다.

## 헷갈리기 쉬운 점
- 교차엔트로피는 정확도와 같은 개념이 아니다. 정확도가 같아도 확률 분포가 다르면 교차엔트로피 값은 달라질 수 있다.
- 출력이 확률처럼 해석되도록 설계되지 않았다면 교차엔트로피를 그대로 쓰기 어렵다. 보통 소프트맥스나 시그모이드와 함께 본다.

## 셀프 체크 퀴즈
1. 교차엔트로피가 분류 문제에 잘 맞는 이유는 무엇인가?
2. 확신이 큰 오답이 교차엔트로피에서 더 큰 손실을 만드는 이유는 무엇인가?
3. 정확도와 교차엔트로피가 서로 다른 정보를 주는 이유는 무엇인가?

## source
- Christopher M. Bishop / Pattern Recognition and Machine Learning / 2006
- Kevin P. Murphy / Machine Learning: A Probabilistic Perspective / 2012
- Ian Goodfellow, Yoshua Bengio, Aaron Courville / Deep Learning / 2016

<!-- FILE: dl-concept-009-gradient-descent.md -->
---
briefing_key: "dl-concept-009-gradient-descent"
track: "dl-basics"
mode: "concept"
title: "경사하강법"
one_line: "경사하강법은 손실을 줄이기 위해 기울기의 반대 방향으로 파라미터를 반복해서 갱신하는 최적화 방법이다."
discussion_prompt: "경사하강법이 단순해 보여도 딥러닝 학습의 중심 원리로 남아 있는 이유는 무엇일까?"
---

## 핵심 설명
- 경사하강법은 현재 위치에서 손실이 가장 가파르게 증가하는 방향의 반대로 조금 이동하는 방법이다. 이 과정을 반복하면 더 작은 손실 지점으로 접근한다.
- 신경망의 파라미터 수는 매우 많기 때문에 손으로 방향을 정할 수 없다. 기울기는 각 파라미터를 어떻게 바꿔야 하는지 알려 주는 핵심 정보다.
- 학습률, 초기화, 손실 지형에 따라 수렴 속도와 안정성이 달라진다. 따라서 경사하강법은 원리는 단순하지만 실제 동작은 여러 요소와 얽혀 있다.
- 딥러닝의 다양한 옵티마이저는 대부분 경사하강법을 더 빠르고 안정적으로 만들기 위한 변형이라고 볼 수 있다.

## 직관
- 산에서 가장 가파른 내리막 방향을 따라 조금씩 내려가는 것과 비슷하다.
- 눈을 가린 채 바닥의 기울기만 느끼며 낮은 곳을 찾는 게임처럼 생각할 수 있다.

## 헷갈리기 쉬운 점
- 기울기의 반대 방향으로 간다고 해서 항상 전역 최솟값에 도달하는 것은 아니다. 중간에 평평한 구간이나 지역적인 낮은 지점이 있을 수 있다.
- 한 번의 갱신으로 학습이 끝나는 것은 아니다. 손실이 줄어들도록 매우 많은 반복이 필요하다.

## 셀프 체크 퀴즈
1. 경사하강법에서 기울기는 어떤 정보를 제공하는가?
2. 학습률이 너무 크면 어떤 문제가 생길 수 있는가?
3. 모멘텀이나 Adam 같은 방법을 경사하강법의 변형으로 볼 수 있는 이유는 무엇인가?

## source
- Ian Goodfellow, Yoshua Bengio, Aaron Courville / Deep Learning / 2016
- Léon Bottou, Frank E. Curtis, Jorge Nocedal / Optimization Methods for Large-Scale Machine Learning / 2018
- Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola / Dive into Deep Learning

<!-- FILE: dl-concept-010-stochastic-gradient-descent.md -->
---
briefing_key: "dl-concept-010-stochastic-gradient-descent"
track: "dl-basics"
mode: "concept"
title: "확률적 경사하강법"
one_line: "확률적 경사하강법은 일부 데이터만 사용해 기울기를 근사하며 자주 파라미터를 갱신하는 학습 방법이다."
discussion_prompt: "기울기를 정확히 계산하지 않고 일부 데이터만 써도 학습이 잘 되는 이유는 무엇일까?"
---

## 핵심 설명
- 확률적 경사하강법은 전체 데이터 대신 한 개 샘플이나 작은 묶음을 사용해 기울기를 추정한다. 계산량을 줄이면서 더 자주 갱신할 수 있다.
- 매번 보는 데이터가 달라 기울기에 잡음이 섞이지만, 이 잡음이 오히려 평평하지 않은 손실 지형을 탐색하는 데 도움을 주기도 한다.
- 대규모 데이터셋에서는 전체 배치를 매번 쓰는 방식보다 훨씬 실용적이다. 현대 딥러닝 학습의 기본 흐름이 사실상 이 방식에 가깝다.
- 실무에서는 한 샘플만 쓰는 순수한 SGD보다 미니배치를 이용한 형태가 더 흔하다. 그래도 개념적으로는 모두 확률적 경사하강법 계열이다.

## 직관
- 전체 여론조사를 매번 하지 않고 일부 표본만 보고 대략적인 방향을 잡는 것과 비슷하다.
- 지도 전체를 매번 펼치지 않고 주변 정보만 보며 빠르게 이동하는 방식으로 이해할 수 있다.

## 헷갈리기 쉬운 점
- 확률적이라는 말이 무작위로 아무 방향이나 간다는 뜻은 아니다. 일부 데이터에서 계산한 기울기를 이용해 방향을 정한다.
- 잡음이 있다고 해서 항상 나쁜 것은 아니다. 때로는 너무 일찍 특정 지점에 갇히는 것을 줄이는 데 도움이 된다.

## 셀프 체크 퀴즈
1. 확률적 경사하강법이 전체 배치 방식보다 실용적인 이유는 무엇인가?
2. SGD의 기울기에 잡음이 생기는 이유는 무엇인가?
3. 실무에서 순수한 한 샘플 SGD보다 미니배치 SGD가 많이 쓰이는 이유는 무엇인가?

## source
- Herbert Robbins, Sutton Monro / A Stochastic Approximation Method / 1951
- Léon Bottou / Large-Scale Machine Learning with Stochastic Gradient Descent / 2010
- Ian Goodfellow, Yoshua Bengio, Aaron Courville / Deep Learning / 2016

<!-- FILE: dl-concept-011-momentum.md -->
---
briefing_key: "dl-concept-011-momentum"
track: "dl-basics"
mode: "concept"
title: "모멘텀"
one_line: "모멘텀은 이전 기울기 방향을 누적해 경사하강법이 더 빠르고 덜 흔들리게 만드는 최적화 기법이다."
discussion_prompt: "현재 기울기만 보는 것보다 과거의 이동 방향을 함께 보는 것이 왜 학습에 도움이 될까?"
---

## 핵심 설명
- 모멘텀은 현재 기울기뿐 아니라 이전 업데이트 방향도 함께 반영한다. 그래서 같은 방향이 반복되면 더 빠르게 나아갈 수 있다.
- 손실 지형이 좁고 긴 골짜기처럼 생겼을 때, 단순 경사하강법은 좌우로 흔들리기 쉽다. 모멘텀은 이런 진동을 줄이고 진행 방향을 유지하는 데 도움을 준다.
- 물리학의 속도 개념처럼 이전 움직임이 다음 움직임에 영향을 준다고 이해할 수 있다. 그래서 평평한 구간을 통과할 때도 더 안정적으로 전진한다.
- 모멘텀은 SGD와 자주 함께 쓰이며, 많은 최적화 기법의 기본 구성 요소가 된다.

## 직관
- 언덕을 굴러 내려가는 공은 한 번 속도가 붙으면 작은 요철에 덜 흔들린다. 모멘텀도 비슷하게 이전 속도를 이용한다.
- 쇼핑 카트를 한 번 밀면 바로 멈추지 않고 관성으로 조금 더 나아가는 모습으로 생각할 수 있다.

## 헷갈리기 쉬운 점
- 모멘텀이 있다고 해서 무조건 더 정확한 지점에 도달하는 것은 아니다. 학습률과 함께 조절하지 않으면 지나치게 튈 수도 있다.
- 모멘텀은 기울기를 없애는 장치가 아니다. 기울기 정보를 더 부드럽고 일관되게 사용하는 방식이다.

## 셀프 체크 퀴즈
1. 모멘텀이 진동을 줄이는 이유는 무엇인가?
2. 모멘텀을 속도나 관성에 비유하는 이유는 무엇인가?
3. 모멘텀과 학습률을 함께 고려해야 하는 이유는 무엇인가?

## source
- Boris T. Polyak / Some Methods of Speeding up the Convergence of Iteration Methods / 1964
- Ian Goodfellow, Yoshua Bengio, Aaron Courville / Deep Learning / 2016
- Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola / Dive into Deep Learning

<!-- FILE: dl-concept-012-adam-optimizer.md -->
---
briefing_key: "dl-concept-012-adam-optimizer"
track: "dl-basics"
mode: "concept"
title: "Adam 옵티마이저"
one_line: "Adam 옵티마이저는 모멘텀과 적응적 학습률을 결합해 각 파라미터를 유연하게 갱신하는 방법이다."
discussion_prompt: "Adam이 널리 쓰이는데도 모든 문제에서 자동으로 최선의 선택이 아닌 이유는 무엇일까?"
---

## 핵심 설명
- Adam은 1차 모멘트와 2차 모멘트를 추적해, 각 파라미터마다 다른 크기의 업데이트를 적용한다. 쉽게 말해 방향의 평균과 변화 규모를 함께 본다.
- 희소한 특징이나 스케일이 다른 파라미터가 섞여 있을 때도 비교적 안정적으로 학습하는 편이라 기본 선택으로 많이 쓰인다.
- 초기 학습이 빠르고 튜닝 부담이 적다는 장점이 있지만, 모든 문제에서 최종 일반화 성능이 가장 좋은 것은 아니다.
- Adam도 학습률과 배치 크기 같은 설정에 영향을 받는다. 편하다고 해서 무조건 무조정으로 써도 된다는 뜻은 아니다.

## 직관
- 모든 학생을 같은 속도로 가르치는 대신, 이해 속도에 맞춰 설명 속도를 조금씩 조절하는 교사와 비슷하다.
- 울퉁불퉁한 길을 달릴 때 속도와 노면 상태를 함께 보며 바퀴마다 다른 힘을 주는 자동차처럼 생각할 수 있다.

## 헷갈리기 쉬운 점
- Adam이 자동 조정 기능을 갖고 있어도 학습률이 완전히 중요하지 않은 것은 아니다. 기본값이 잘 맞지 않는 상황도 많다.
- Adam이 SGD를 완전히 대체하는 것은 아니다. 어떤 문제에서는 단순한 SGD 계열이 더 좋은 일반화 성능을 보이기도 한다.

## 셀프 체크 퀴즈
1. Adam이 파라미터마다 다른 업데이트 크기를 적용할 수 있는 이유는 무엇인가?
2. Adam이 기본 선택으로 자주 쓰이는 이유는 무엇인가?
3. Adam을 쓸 때도 학습률을 점검해야 하는 이유는 무엇인가?

## source
- Diederik P. Kingma, Jimmy Ba / Adam: A Method for Stochastic Optimization / 2015
- Ian Goodfellow, Yoshua Bengio, Aaron Courville / Deep Learning / 2016
- Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola / Dive into Deep Learning

<!-- FILE: dl-concept-013-learning-rate.md -->
---
briefing_key: "dl-concept-013-learning-rate"
track: "dl-basics"
mode: "concept"
title: "학습률"
one_line: "학습률은 한 번의 업데이트에서 파라미터를 얼마나 크게 움직일지를 정하는 핵심 하이퍼파라미터다."
discussion_prompt: "모델 구조가 좋아도 학습률 설정이 잘못되면 학습이 무너질 수 있는 이유는 무엇일까?"
---

## 핵심 설명
- 학습률은 기울기 방향으로 얼마만큼 이동할지 정하는 계수다. 같은 기울기라도 학습률이 다르면 업데이트 크기가 달라진다.
- 값이 너무 크면 최솟값 근처를 지나치거나 발산할 수 있다. 반대로 너무 작으면 학습이 매우 느리거나 좋은 지점에 도달하기 전에 멈춘 것처럼 보일 수 있다.
- 학습 초반과 후반에 서로 다른 학습률이 더 적합할 수 있다. 그래서 스케줄링이나 warmup 같은 기법이 함께 사용되기도 한다.
- 학습률은 옵티마이저, 배치 크기, 정규화 방식과 상호작용한다. 단독 숫자 하나가 아니라 전체 학습 전략의 일부다.

## 직관
- 계단을 내려갈 때 보폭이 너무 크면 헛디디고, 너무 작으면 오래 걸린다. 학습률은 그 보폭과 비슷하다.
- 차를 주차할 때 한 번에 너무 많이 꺾으면 지나치고, 너무 조금 움직이면 제자리에서만 수정하는 상황과 닮아 있다.

## 헷갈리기 쉬운 점
- 학습률이 작다고 해서 항상 안전한 것은 아니다. 너무 작으면 사실상 학습이 거의 진행되지 않는다.
- 좋은 학습률은 데이터셋마다 다를 수 있다. 다른 실험의 숫자를 그대로 가져오면 잘 맞지 않을 수 있다.

## 셀프 체크 퀴즈
1. 학습률이 너무 크면 왜 발산이나 진동이 생길 수 있는가?
2. 학습률이 너무 작을 때 학습이 느려지는 이유는 무엇인가?
3. 학습률 스케줄링이 필요한 상황은 어떤 경우인가?

## source
- Ian Goodfellow, Yoshua Bengio, Aaron Courville / Deep Learning / 2016
- Léon Bottou, Frank E. Curtis, Jorge Nocedal / Optimization Methods for Large-Scale Machine Learning / 2018
- Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola / Dive into Deep Learning

<!-- FILE: dl-concept-014-mini-batch.md -->
---
briefing_key: "dl-concept-014-mini-batch"
track: "dl-basics"
mode: "concept"
title: "미니배치"
one_line: "미니배치는 한 번의 파라미터 업데이트에 함께 사용하는 작은 데이터 묶음이다."
discussion_prompt: "한 샘플도 아니고 전체 데이터도 아닌 작은 묶음을 쓰는 방식이 왜 딥러닝의 기본이 되었을까?"
---

## 핵심 설명
- 미니배치는 전체 데이터셋을 여러 작은 묶음으로 나눈 것이다. 모델은 한 묶음을 보고 손실과 기울기를 계산한 뒤 파라미터를 갱신한다.
- 이 방식은 전체 배치보다 메모리 부담이 적고, 한 샘플 방식보다 계산이 안정적이다. 그래서 속도와 안정성 사이의 균형점으로 자주 선택된다.
- GPU 같은 병렬 하드웨어를 효율적으로 활용하기에도 적합하다. 한 번에 너무 적지도 많지도 않은 양을 처리할 수 있기 때문이다.
- 미니배치 크기는 학습 신호의 잡음, 메모리 사용량, 일반화 성능에 영향을 줄 수 있다.

## 직관
- 반 전체를 한 번에 가르치지도, 학생 한 명씩만 가르치지도 않고 소그룹 수업을 하는 방식과 비슷하다.
- 택배를 하나씩 보내면 비효율적이고, 창고 전체를 한 번에 옮기면 부담이 크다. 적당한 묶음으로 보내는 방식이 미니배치다.

## 헷갈리기 쉬운 점
- 미니배치가 크다고 항상 더 좋은 것은 아니다. 계산은 안정적일 수 있지만 메모리 부담과 일반화 특성이 달라질 수 있다.
- 미니배치는 단순한 데이터 분할이 아니라 업데이트 단위를 정하는 핵심 학습 설정이다.

## 셀프 체크 퀴즈
1. 미니배치가 한 샘플 학습과 전체 배치 학습의 중간 형태라고 볼 수 있는 이유는 무엇인가?
2. 미니배치 크기가 메모리 사용과 학습 신호에 어떤 영향을 주는가?
3. GPU 학습에서 미니배치가 자주 쓰이는 이유는 무엇인가?

## source
- Ian Goodfellow, Yoshua Bengio, Aaron Courville / Deep Learning / 2016
- Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola / Dive into Deep Learning
- Léon Bottou / Large-Scale Machine Learning with Stochastic Gradient Descent / 2010

<!-- FILE: dl-concept-015-epoch-iteration-step.md -->
---
briefing_key: "dl-concept-015-epoch-iteration-step"
track: "dl-basics"
mode: "concept"
title: "에폭·이터레이션·스텝"
one_line: "에폭, 이터레이션, 스텝은 학습이 얼마나 진행되었는지를 서로 다른 기준으로 나타내는 용어다."
discussion_prompt: "학습 로그를 읽을 때 이 세 용어를 구분하지 못하면 어떤 오해가 생길까?"
---

## 핵심 설명
- 에폭은 전체 학습 데이터를 한 번 모두 사용하는 주기를 뜻한다. 데이터셋을 처음부터 끝까지 한 바퀴 돈 셈이다.
- 이터레이션이나 스텝은 보통 한 번의 파라미터 업데이트를 가리킨다. 미니배치를 하나 처리할 때마다 1스텝이 늘어난다고 보면 된다.
- 한 에폭 안에는 여러 스텝이 들어간다. 스텝 수는 보통 데이터 개수를 배치 크기로 나눈 값과 연결된다.
- 논문이나 프레임워크에 따라 iteration이라는 단어를 약간 다르게 쓰는 경우가 있어, 문맥을 함께 확인하는 습관이 중요하다.

## 직관
- 책 한 권을 끝까지 읽는 것이 에폭이라면, 한 페이지를 읽고 메모하는 단위는 스텝에 가깝다.
- 운동에서 전체 코스를 한 바퀴 도는 것이 에폭이고, 중간중간 한 세트씩 수행하는 것이 스텝이라고 생각할 수 있다.

## 헷갈리기 쉬운 점
- 에폭과 스텝은 같은 단위가 아니다. 배치 크기가 바뀌면 같은 에폭 수라도 스텝 수는 달라질 수 있다.
- iteration이 항상 에폭과 같은 뜻으로 쓰이는 것은 아니다. 자료마다 정의를 확인해야 한다.

## 셀프 체크 퀴즈
1. 에폭과 스텝은 어떻게 다른가?
2. 배치 크기가 바뀌면 한 에폭 안의 스텝 수는 어떻게 달라지는가?
3. iteration이라는 용어를 문맥으로 확인해야 하는 이유는 무엇인가?

## source
- Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola / Dive into Deep Learning
- Ian Goodfellow, Yoshua Bengio, Aaron Courville / Deep Learning / 2016
- PyTorch / Training Loop Tutorials and Documentation

<!-- FILE: dl-concept-016-backpropagation.md -->
---
briefing_key: "dl-concept-016-backpropagation"
track: "dl-basics"
mode: "concept"
title: "역전파"
one_line: "역전파는 출력의 오차가 각 파라미터에 얼마나 책임이 있는지 효율적으로 계산하는 방법이다."
discussion_prompt: "수많은 파라미터의 기울기를 따로따로 구하지 않고도 학습이 가능한 이유는 무엇일까?"
---

## 핵심 설명
- 역전파는 손실에서 시작해 출력층에서 입력층 방향으로 기울기를 전파하는 알고리즘이다. 미분의 연쇄법칙을 이용해 각 파라미터의 기여도를 계산한다.
- 같은 중간 계산 결과를 재사용하므로, 모든 파라미터에 대한 기울기를 훨씬 효율적으로 구할 수 있다. 현대 딥러닝이 실용화된 핵심 이유 중 하나다.
- 순전파가 예측값을 만드는 과정이라면, 역전파는 그 예측이 틀린 이유를 각 층에 배분하는 과정이라고 볼 수 있다.
- 역전파로 얻은 기울기는 경사하강법 계열 옵티마이저의 입력이 된다. 즉 학습의 수정 신호를 만드는 역할을 한다.

## 직관
- 팀 프로젝트 결과가 좋지 않을 때, 마지막 결과만 보고 끝내지 않고 각 단계가 얼마나 영향을 줬는지 거꾸로 추적하는 것과 비슷하다.
- 최종 점수에서 출발해 어떤 계산이 점수를 올리거나 내렸는지 거슬러 올라가는 계산 감사 과정으로 생각할 수 있다.

## 헷갈리기 쉬운 점
- 역전파는 데이터를 거꾸로 흘려보내는 과정이 아니다. 오차 자체보다 기울기 정보를 뒤쪽에서 앞쪽으로 전달하는 것이다.
- 역전파가 있다고 해서 기울기 소실 문제가 자동으로 없어지는 것은 아니다. 네트워크 구조와 활성화 함수 선택이 함께 중요하다.

## 셀프 체크 퀴즈
1. 역전파가 연쇄법칙과 어떤 관련이 있는가?
2. 역전파가 각 파라미터의 기울기를 효율적으로 계산할 수 있는 이유는 무엇인가?
3. 순전파와 역전파의 역할은 어떻게 다른가?

## source
- David E. Rumelhart, Geoffrey E. Hinton, Ronald J. Williams / Learning Representations by Back-Propagating Errors / 1986
- Ian Goodfellow, Yoshua Bengio, Aaron Courville / Deep Learning / 2016
- Christopher M. Bishop / Pattern Recognition and Machine Learning / 2006

<!-- FILE: dl-concept-017-weight-initialization.md -->
---
briefing_key: "dl-concept-017-weight-initialization"
track: "dl-basics"
mode: "concept"
title: "가중치 초기화"
one_line: "가중치 초기화는 학습 시작점의 파라미터 값을 정해 기울기 흐름과 학습 안정성에 큰 영향을 준다."
discussion_prompt: "학습은 결국 데이터를 보고 바뀌는 과정인데도 시작값이 중요한 이유는 무엇일까?"
---

## 핵심 설명
- 가중치 초기화는 학습 전에 파라미터를 어떤 값으로 시작할지 정하는 일이다. 시작점이 다르면 학습 경로와 수렴 속도가 달라질 수 있다.
- 모든 가중치를 같은 값으로 두면 뉴런들이 같은 일을 하게 되어 대칭성이 깨지지 않는다. 그래서 보통 작은 무작위 값으로 초기화한다.
- 너무 큰 값이나 너무 작은 값은 층을 거치며 신호와 기울기를 폭발시키거나 사라지게 만들 수 있다. Xavier 초기화와 He 초기화는 이런 문제를 완화하려는 대표 방법이다.
- 초기화는 단순 준비 단계가 아니라, 깊은 네트워크가 실제로 학습되게 만드는 핵심 조건 중 하나다.

## 직관
- 여러 사람이 같은 출발선에서 똑같은 방향만 보면 협업이 안 되듯이, 뉴런도 처음부터 조금씩 다른 역할을 시작해야 한다.
- 건물을 세울 때 기초가 기울어 있으면 위층 공사가 어려워지는 것처럼, 초기화가 나쁘면 뒤 학습이 힘들어진다.

## 헷갈리기 쉬운 점
- 가중치를 0으로 시작하면 깔끔해 보이지만 대부분의 층에서 좋지 않다. 뉴런들이 서로 구별되지 않기 때문이다.
- 좋은 초기화가 학습을 대신해 주는 것은 아니다. 다만 학습이 가능하고 안정적으로 진행되도록 돕는다.

## 셀프 체크 퀴즈
1. 모든 가중치를 같은 값으로 초기화하면 왜 문제가 생길 수 있는가?
2. 가중치 초기화가 기울기 소실이나 폭발과 연결되는 이유는 무엇인가?
3. Xavier 초기화와 He 초기화는 어떤 문제를 완화하려는가?

## source
- Xavier Glorot, Yoshua Bengio / Understanding the Difficulty of Training Deep Feedforward Neural Networks / 2010
- Kaiming He, Xiangyu Zhang, Shaoqing Ren, Jian Sun / Delving Deep into Rectifiers / 2015
- Ian Goodfellow, Yoshua Bengio, Aaron Courville / Deep Learning / 2016

<!-- FILE: dl-concept-018-input-normalization.md -->
---
briefing_key: "dl-concept-018-input-normalization"
track: "dl-basics"
mode: "concept"
title: "입력 정규화"
one_line: "입력 정규화는 특징들의 스케일을 맞춰 학습을 더 빠르고 안정적으로 만드는 전처리 과정이다."
discussion_prompt: "입력값의 단위를 맞추는 단순한 전처리가 왜 학습 결과에 큰 차이를 만들 수 있을까?"
---

## 핵심 설명
- 입력 정규화는 각 특징의 크기나 분포를 일정한 범위나 평균과 분산 기준으로 맞추는 과정이다. 대표적으로 평균을 빼고 표준편차로 나누는 표준화가 많이 쓰인다.
- 특징마다 값의 스케일이 크게 다르면 어떤 입력은 기울기를 지배하고, 어떤 입력은 거의 반영되지 않을 수 있다. 정규화는 이런 불균형을 줄여 준다.
- 정규화된 입력은 최적화가 더 안정적으로 진행되게 만들고, 학습률 선택도 덜 까다롭게 하는 경우가 많다.
- 이미지, 표 데이터, 음성 등 거의 모든 영역에서 입력 스케일링은 기본적인 출발점으로 여겨진다.

## 직관
- 키는 센티미터로, 몸무게는 킬로그램으로 적은 표를 그대로 비교하면 한쪽 숫자가 더 커 보일 수 있다. 단위를 맞추면 비교가 쉬워진다.
- 모두 비슷한 크기의 블록으로 정리해 두면 조립이 쉬워지는 것처럼, 입력 스케일을 맞추면 학습이 편해진다.

## 헷갈리기 쉬운 점
- 입력 정규화는 데이터 누수를 조심해야 한다. 평균과 분산은 보통 학습 데이터에서만 계산해 검증과 테스트에 적용한다.
- 입력 정규화가 모든 문제를 해결하는 것은 아니다. 모델 구조나 손실 함수의 문제는 별도로 다뤄야 한다.

## 셀프 체크 퀴즈
1. 입력 특징의 스케일 차이가 크면 학습에 어떤 문제가 생길 수 있는가?
2. 정규화 통계를 학습 데이터에서만 계산해야 하는 이유는 무엇인가?
3. 입력 정규화가 학습률 선택을 덜 까다롭게 만들 수 있는 이유는 무엇인가?

## source
- Yann LeCun, Léon Bottou, Genevieve B. Orr, Klaus-Robert Müller / Efficient BackProp / 1998
- Ian Goodfellow, Yoshua Bengio, Aaron Courville / Deep Learning / 2016
- Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola / Dive into Deep Learning

<!-- FILE: dl-concept-019-train-validation-test-split.md -->
---
briefing_key: "dl-concept-019-train-validation-test-split"
track: "dl-basics"
mode: "concept"
title: "학습·검증·테스트 분할"
one_line: "학습·검증·테스트 분할은 모델 학습, 설정 조정, 최종 평가를 분리해 일반화 성능을 공정하게 확인하는 방법이다."
discussion_prompt: "좋은 성능을 주장하려면 왜 데이터를 나눠서 서로 다른 역할을 맡겨야 할까?"
---

## 핵심 설명
- 학습 세트는 파라미터를 실제로 학습하는 데 사용된다. 모델이 데이터를 보고 패턴을 익히는 구간이다.
- 검증 세트는 하이퍼파라미터 조정, 모델 선택, 조기 종료 판단 등에 사용된다. 학습에는 직접 포함되지 않지만 개발 과정에서 자주 참고한다.
- 테스트 세트는 마지막에 한 번만 써서 최종 일반화 성능을 확인하는 용도다. 개발 중 반복해서 보면 사실상 검증 세트처럼 오염된다.
- 이 분할은 모델이 본 데이터와 처음 보는 데이터에서 각각 어떻게 행동하는지 구분해 보게 해 준다.

## 직관
- 문제집으로 공부하고, 모의고사로 전략을 조정하고, 실제 시험으로 최종 실력을 확인하는 구조와 비슷하다.
- 요리 연습, 중간 시식, 손님에게 내는 마지막 접시를 구분하는 것처럼 역할을 분리하는 과정이다.

## 헷갈리기 쉬운 점
- 검증 세트와 테스트 세트는 같은 역할이 아니다. 둘 다 평가용처럼 보여도 개발 중 사용할 수 있는지는 크게 다르다.
- 테스트 점수를 자주 확인하면 그 점수에 맞춰 모델을 고르게 된다. 그러면 최종 평가는 더 이상 공정하지 않다.

## 셀프 체크 퀴즈
1. 학습 세트, 검증 세트, 테스트 세트는 각각 어떤 역할을 하는가?
2. 테스트 세트를 개발 중 반복해서 보면 왜 문제가 되는가?
3. 검증 세트 없이 모델을 조정하면 어떤 위험이 생길 수 있는가?

## source
- Christopher M. Bishop / Pattern Recognition and Machine Learning / 2006
- Ian Goodfellow, Yoshua Bengio, Aaron Courville / Deep Learning / 2016
- scikit-learn / Model Selection and Evaluation Documentation

<!-- FILE: dl-concept-020-overfitting.md -->
---
briefing_key: "dl-concept-020-overfitting"
track: "dl-basics"
mode: "concept"
title: "과적합"
one_line: "과적합은 모델이 학습 데이터에는 지나치게 맞지만 새로운 데이터에서는 잘 일반화하지 못하는 상태다."
discussion_prompt: "훈련 성능이 높아 보이는데도 실제로는 좋은 모델이 아닐 수 있는 이유는 무엇일까?"
---

## 핵심 설명
- 과적합은 모델이 학습 데이터의 일반적인 패턴뿐 아니라 우연한 잡음과 예외까지 지나치게 외우는 상태를 뜻한다.
- 이 경우 학습 손실은 낮고 정확도는 높을 수 있지만, 검증이나 테스트 성능은 기대보다 낮게 나온다. 즉 기억은 잘했지만 이해는 부족한 상태다.
- 모델이 너무 복잡하거나 데이터가 부족할 때, 또는 정규화가 약할 때 과적합이 잘 생긴다.
- 과적합을 줄이기 위해 데이터 증강, 드롭아웃, 가중치 감쇠, 조기 종료 같은 방법을 함께 사용한다.

## 직관
- 기출문제 답을 외워서 모의고사에는 강하지만 새로운 유형에는 약한 공부 방식과 비슷하다.
- 지도에서 모든 작은 얼룩까지 길로 착각해 기억하면 원래 지형을 이해하지 못하는 상황으로 볼 수 있다.

## 헷갈리기 쉬운 점
- 과적합은 학습이 많이 됐다는 뜻과 같지 않다. 충분히 학습한 뒤에도 일반화가 나쁘면 과적합일 수 있다.
- 복잡한 모델만 과적합하는 것은 아니다. 단순한 모델도 데이터가 매우 적거나 검증 절차가 나쁘면 과적합처럼 보일 수 있다.

## 셀프 체크 퀴즈
1. 과적합이 발생했을 때 학습 성능과 검증 성능은 보통 어떻게 보이는가?
2. 과적합을 외워 버린 상태에 비유하는 이유는 무엇인가?
3. 과적합을 줄이기 위해 사용할 수 있는 방법에는 무엇이 있는가?

## source
- Ian Goodfellow, Yoshua Bengio, Aaron Courville / Deep Learning / 2016
- Christopher M. Bishop / Pattern Recognition and Machine Learning / 2006
- Kevin P. Murphy / Machine Learning: A Probabilistic Perspective / 2012

<!-- FILE: dl-concept-021-underfitting.md -->
---
briefing_key: "dl-concept-021-underfitting"
track: "dl-basics"
mode: "concept"
title: "과소적합"
one_line: "과소적합은 모델이 데이터의 중요한 패턴조차 충분히 배우지 못해 학습과 일반화 모두가 낮은 상태다."
discussion_prompt: "새로운 데이터를 못 맞히는 것뿐 아니라 학습 데이터도 잘 못 맞히는 상태를 왜 따로 구분해야 할까?"
---

## 핵심 설명
- 과소적합은 모델이 너무 단순하거나 학습이 부족해, 학습 데이터에서도 성능이 충분히 오르지 않는 상태다.
- 이 경우 학습 세트와 검증 세트 모두에서 성능이 낮게 나타나는 경우가 많다. 아직 문제의 구조를 제대로 잡지 못한 것이다.
- 원인으로는 모델 표현력 부족, 너무 강한 정규화, 학습 부족, 부적절한 특징 표현 등이 있다.
- 과소적합을 해결하려면 모델을 더 유연하게 만들거나, 더 오래 학습하거나, 입력 표현을 개선하는 접근이 필요하다.

## 직관
- 시험 범위를 제대로 공부하지 않아 기출문제도 새 문제도 모두 못 푸는 상태와 비슷하다.
- 지도에서 큰 도로조차 표시하지 못한 단순한 스케치라면, 세부 길찾기는 당연히 어렵다.

## 헷갈리기 쉬운 점
- 과소적합과 과적합은 둘 다 성능 문제지만 원인이 다르다. 과적합은 지나치게 외운 상태이고, 과소적합은 아직 충분히 배우지 못한 상태다.
- 검증 성능이 낮다고 해서 항상 과적합은 아니다. 학습 성능도 함께 봐야 과소적합인지 구분할 수 있다.

## 셀프 체크 퀴즈
1. 과소적합일 때 학습 성능과 검증 성능은 보통 어떻게 나타나는가?
2. 과소적합의 대표 원인에는 무엇이 있는가?
3. 과소적합을 해결하기 위해 시도할 수 있는 방법은 무엇인가?

## source
- Ian Goodfellow, Yoshua Bengio, Aaron Courville / Deep Learning / 2016
- Christopher M. Bishop / Pattern Recognition and Machine Learning / 2006
- Kevin P. Murphy / Machine Learning: A Probabilistic Perspective / 2012

<!-- FILE: dl-concept-022-regularization.md -->
---
briefing_key: "dl-concept-022-regularization"
track: "dl-basics"
mode: "concept"
title: "정규화(Regularization)"
one_line: "정규화는 모델이 학습 데이터를 지나치게 외우지 않도록 제약을 주어 일반화를 돕는 방법들의 묶음이다."
discussion_prompt: "더 잘 맞히게 만드는 것이 아니라 덜 과하게 맞히게 만드는 전략이 왜 중요할까?"
---

## 핵심 설명
- 정규화는 모델 복잡도나 파라미터 크기를 조절해, 새로운 데이터에서도 잘 작동하도록 돕는 방법이다.
- 가중치 감쇠, 드롭아웃, 조기 종료, 데이터 증강 등 다양한 기법이 넓은 의미의 정규화에 포함된다.
- 핵심 아이디어는 학습 데이터에서만 통하는 지나치게 섬세한 규칙 대신, 더 단순하고 안정적인 패턴을 배우게 만드는 것이다.
- 정규화가 강하면 과적합은 줄일 수 있지만, 너무 강하면 과소적합이 생길 수 있다. 그래서 적절한 균형이 중요하다.

## 직관
- 시험 답안을 한 문제에만 맞춘 비법 대신, 여러 문제에 통하는 기본 원리를 익히게 만드는 훈련과 비슷하다.
- 조각칼을 너무 날카롭게 세우면 작은 흠집까지 새기게 된다. 정규화는 그 칼날을 적당히 둔하게 만들어 큰 형태를 우선 보게 한다.

## 헷갈리기 쉬운 점
- 정규화는 데이터 전처리의 정규화와 다른 문맥으로 쓰일 수 있다. 여기서는 일반화를 위한 제약이라는 의미다.
- 정규화가 많을수록 무조건 좋은 것은 아니다. 너무 강하면 학습 자체가 충분히 일어나지 않을 수 있다.

## 셀프 체크 퀴즈
1. 정규화의 목적은 무엇인가?
2. 가중치 감쇠와 드롭아웃을 모두 정규화 기법으로 보는 이유는 무엇인가?
3. 정규화가 너무 강할 때 어떤 문제가 생길 수 있는가?

## source
- Ian Goodfellow, Yoshua Bengio, Aaron Courville / Deep Learning / 2016
- Christopher M. Bishop / Pattern Recognition and Machine Learning / 2006
- Kevin P. Murphy / Machine Learning: A Probabilistic Perspective / 2012

<!-- FILE: dl-concept-023-dropout.md -->
---
briefing_key: "dl-concept-023-dropout"
track: "dl-basics"
mode: "concept"
title: "드롭아웃"
one_line: "드롭아웃은 학습 중 일부 뉴런을 무작위로 끄며 특정 연결에 과하게 의존하지 않게 하는 정규화 기법이다."
discussion_prompt: "학습 중 일부 뉴런을 일부러 꺼 버리는 방식이 오히려 일반화에 도움이 되는 이유는 무엇일까?"
---

## 핵심 설명
- 드롭아웃은 학습 과정에서 일부 뉴런의 출력을 무작위로 0으로 만든다. 그래서 네트워크가 특정 뉴런 조합에 지나치게 의존하지 못하게 한다.
- 이 방법은 여러 부분 네트워크를 번갈아 학습하는 효과를 내어, 더 튼튼한 표현을 만들도록 유도한다.
- 학습 때와 추론 때의 동작이 다르다는 점이 중요하다. 추론 시에는 모든 뉴런을 사용하되, 학습 시의 평균 효과를 반영하도록 스케일을 조정한다.
- 드롭아웃은 특히 완전연결층에서 널리 쓰였고, 현재도 상황에 따라 유용한 정규화 방법으로 사용된다.

## 직관
- 축구 연습에서 특정 선수 몇 명이 빠져도 팀이 돌아가도록 훈련하는 것과 비슷하다.
- 매번 다른 도구 몇 개를 빼고 작업해도 결과를 내야 한다면, 한 도구에만 의존하지 않는 습관이 생긴다.

## 헷갈리기 쉬운 점
- 드롭아웃은 추론 단계에서도 계속 뉴런을 끄는 것이 아니다. 보통 학습 때만 무작위 제거를 적용한다.
- 드롭아웃이 항상 성능을 올리는 것은 아니다. 배치 정규화나 구조 자체의 특성에 따라 효과가 크지 않을 수도 있다.

## 셀프 체크 퀴즈
1. 드롭아웃이 특정 뉴런에 대한 과의존을 줄이는 이유는 무엇인가?
2. 학습 단계와 추론 단계에서 드롭아웃 동작이 다른 이유는 무엇인가?
3. 드롭아웃이 여러 부분 네트워크를 학습하는 효과를 낸다고 말하는 이유는 무엇인가?

## source
- Nitish Srivastava et al. / Dropout: A Simple Way to Prevent Neural Networks from Overfitting / 2014
- Ian Goodfellow, Yoshua Bengio, Aaron Courville / Deep Learning / 2016
- Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola / Dive into Deep Learning

<!-- FILE: dl-concept-024-batch-normalization.md -->
---
briefing_key: "dl-concept-024-batch-normalization"
track: "dl-basics"
mode: "concept"
title: "배치 정규화"
one_line: "배치 정규화는 중간층의 활성값을 배치 기준으로 정규화해 학습을 더 안정적으로 만드는 기법이다."
discussion_prompt: "입력이 아니라 중간 표현을 정규화하는 방식이 왜 깊은 네트워크 학습에 도움이 될까?"
---

## 핵심 설명
- 배치 정규화는 층의 입력이나 활성값을 미니배치의 평균과 분산으로 정규화한 뒤, 다시 학습 가능한 스케일과 이동을 적용한다.
- 이 과정은 각 층으로 들어가는 값의 분포가 지나치게 흔들리는 것을 줄여, 더 큰 학습률에서도 안정적으로 학습되게 도울 수 있다.
- 배치 정규화는 종종 학습 속도를 높이고 초기화 민감도를 줄여 준다. 하지만 효과는 모델 구조와 배치 크기에 따라 달라진다.
- 추론 단계에서는 현재 배치 통계가 아니라 학습 중 누적한 평균과 분산을 사용한다는 점이 중요하다.

## 직관
- 조립 라인마다 들어오는 부품 크기를 비슷하게 맞춰 두면 다음 공정이 덜 흔들리는 것과 비슷하다.
- 각 반 학생의 점수를 바로 쓰지 않고 평균과 분산을 고려해 기준을 맞춘 뒤 평가하는 방식으로 이해할 수 있다.

## 헷갈리기 쉬운 점
- 배치 정규화는 과적합을 막는 정규화 효과가 일부 있을 수 있지만, 주목적은 학습 안정화다.
- 배치 크기가 매우 작으면 통계가 불안정해질 수 있다. 그래서 모든 상황에서 같은 효과를 기대하긴 어렵다.

## 셀프 체크 퀴즈
1. 배치 정규화는 각 층의 어떤 값을 정규화하는가?
2. 학습 단계와 추론 단계에서 사용하는 통계가 다른 이유는 무엇인가?
3. 배치 크기가 매우 작을 때 배치 정규화가 까다로울 수 있는 이유는 무엇인가?

## source
- Sergey Ioffe, Christian Szegedy / Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift / 2015
- Ian Goodfellow, Yoshua Bengio, Aaron Courville / Deep Learning / 2016
- Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola / Dive into Deep Learning

<!-- FILE: dl-concept-025-residual-connection.md -->
---
briefing_key: "dl-concept-025-residual-connection"
track: "dl-basics"
mode: "concept"
title: "잔차 연결"
one_line: "잔차 연결은 입력을 몇 개 층을 건너뛰어 더해 주어 깊은 네트워크의 학습을 쉽게 만드는 구조다."
discussion_prompt: "깊이를 늘리면 표현력이 커질 수 있는데도 실제 학습은 오히려 어려워지는 이유를 잔차 연결이 어떻게 완화할까?"
---

## 핵심 설명
- 잔차 연결은 어떤 블록의 입력을 그 블록의 출력에 직접 더해 주는 구조다. 그래서 블록은 전체 함수를 처음부터 배우기보다 변화량만 배우면 된다.
- 깊은 네트워크에서는 층을 더 쌓았는데도 최적화가 어려워 성능이 나빠지는 일이 생길 수 있다. 잔차 연결은 이런 문제를 줄이는 데 큰 역할을 했다.
- 입력이 그대로 흐를 수 있는 우회 경로가 생기면 기울기 전달도 쉬워진다. 그래서 매우 깊은 모델도 비교적 안정적으로 학습된다.
- 대표적인 예가 ResNet이며, 이후 많은 모델 구조에 잔차 아이디어가 널리 퍼졌다.

## 직관
- 새 내용을 덧붙이는 편집 작업처럼, 전체 문서를 다시 쓰기보다 기존 내용에서 무엇을 바꿀지만 적는 방식과 비슷하다.
- 계단 대신 완만한 경사로를 하나 더 놓아 이동을 쉽게 만드는 구조로 생각할 수 있다.

## 헷갈리기 쉬운 점
- 잔차 연결이 있다고 해서 모든 깊은 모델 문제가 자동으로 사라지는 것은 아니다. 그래도 최적화 난도를 크게 낮춘 중요한 구조다.
- 잔차 연결은 단순한 출력 복사가 아니다. 본래 변환 결과와 입력을 함께 사용해 학습을 돕는 방식이다.

## 셀프 체크 퀴즈
1. 잔차 연결에서 블록이 변화량을 배운다고 말하는 이유는 무엇인가?
2. 잔차 연결이 깊은 네트워크의 기울기 흐름에 어떤 도움을 주는가?
3. ResNet이 딥러닝 역사에서 중요한 이유는 무엇인가?

## source
- Kaiming He, Xiangyu Zhang, Shaoqing Ren, Jian Sun / Deep Residual Learning for Image Recognition / 2016
- Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola / Dive into Deep Learning
- Stanford / CS231n Convolutional Neural Networks Notes

<!-- FILE: dl-concept-026-convolution.md -->
---
briefing_key: "dl-concept-026-convolution"
track: "dl-basics"
mode: "concept"
title: "합성곱"
one_line: "합성곱은 작은 필터를 입력 위로 이동시키며 지역 패턴을 찾는 연산이다."
discussion_prompt: "이미지 전체를 한 번에 보지 않고 작은 창을 움직이며 보는 방식이 왜 효과적일까?"
---

## 핵심 설명
- 합성곱은 작은 커널 또는 필터를 입력 위로 슬라이드하며 각 위치에서 가중합을 계산하는 연산이다. 이미지에서는 가장자리나 질감 같은 지역 패턴을 잘 포착한다.
- 같은 필터를 여러 위치에 공유하므로 파라미터 수가 크게 줄어든다. 이 덕분에 완전연결층보다 공간 구조를 더 효율적으로 다룰 수 있다.
- 합성곱층은 위치가 조금 달라도 비슷한 특징을 감지할 수 있다. 그래서 이미지처럼 인접한 픽셀 관계가 중요한 데이터에 잘 맞는다.
- 현대의 이미지 모델에서 합성곱은 핵심 기반 연산으로 널리 사용되어 왔다.

## 직관
- 돋보기를 들고 그림 전체를 훑으면서 특정 무늬가 있는지 찾는 것과 비슷하다.
- 벽지를 볼 때 전체 벽을 한 번에 보기보다 작은 구역의 반복 패턴을 살피는 방식으로 이해할 수 있다.

## 헷갈리기 쉬운 점
- 합성곱이 이미지를 완전히 이해하는 것은 아니다. 지역 특징을 쌓아 가며 더 큰 의미를 뒤쪽 층에서 조합한다.
- 필터가 공유된다고 해서 모든 위치를 똑같이 취급하는 것은 아니다. 입력 내용에 따라 각 위치의 반응은 달라진다.

## 셀프 체크 퀴즈
1. 합성곱에서 필터를 여러 위치에 공유하는 장점은 무엇인가?
2. 합성곱이 이미지의 지역 패턴을 잘 잡는 이유는 무엇인가?
3. 완전연결층과 비교할 때 합성곱층이 공간 구조를 다루는 방식은 어떻게 다른가?

## source
- Yann LeCun et al. / Gradient-Based Learning Applied to Document Recognition / 1998
- Ian Goodfellow, Yoshua Bengio, Aaron Courville / Deep Learning / 2016
- Stanford / CS231n Convolutional Neural Networks Notes

<!-- FILE: dl-concept-027-padding.md -->
---
briefing_key: "dl-concept-027-padding"
track: "dl-basics"
mode: "concept"
title: "패딩"
one_line: "패딩은 입력 가장자리에 값을 덧붙여 출력 크기와 가장자리 정보 손실을 조절하는 기법이다."
discussion_prompt: "합성곱 전에 가장자리에 여유 공간을 두는 단순한 조치가 왜 중요한 역할을 할까?"
---

## 핵심 설명
- 패딩은 입력의 바깥쪽에 0 같은 값을 둘러 추가하는 방식이다. 합성곱을 적용할 때 가장자리 정보가 너무 빨리 줄어드는 것을 막아 준다.
- 패딩이 없으면 필터가 움직일 때 출력의 공간 크기가 줄어든다. 여러 층을 거치면 입력의 테두리 정보가 빠르게 사라질 수 있다.
- 적절한 패딩을 사용하면 출력 크기를 입력과 같게 유지하는 것도 가능하다. 이는 네트워크 설계를 더 단순하게 만든다.
- 패딩은 커널 크기, 스트라이드와 함께 출력 크기를 결정하는 핵심 요소다.

## 직관
- 그림을 자르기 전에 가장자리에 여백 종이를 붙여 두면 원래 내용이 덜 잘리는 것과 비슷하다.
- 운동장에서 선 밖으로 한 걸음 더 설 공간을 만들어 두면 가장자리에서도 동작을 더 자유롭게 할 수 있다.

## 헷갈리기 쉬운 점
- 패딩은 단순히 크기 맞추기용 장식이 아니다. 가장자리 픽셀도 충분히 활용하도록 돕는 중요한 설계 요소다.
- 항상 0 패딩만 쓰는 것은 아니다. 문제에 따라 다른 패딩 방식이 사용될 수 있다.

## 셀프 체크 퀴즈
1. 패딩이 없을 때 합성곱 출력 크기는 왜 줄어드는가?
2. 패딩이 가장자리 정보 보존에 도움이 되는 이유는 무엇인가?
3. 커널 크기와 스트라이드 외에 패딩도 출력 크기에 영향을 주는 이유는 무엇인가?

## source
- Ian Goodfellow, Yoshua Bengio, Aaron Courville / Deep Learning / 2016
- Stanford / CS231n Convolutional Neural Networks Notes
- Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola / Dive into Deep Learning

<!-- FILE: dl-concept-028-stride.md -->
---
briefing_key: "dl-concept-028-stride"
track: "dl-basics"
mode: "concept"
title: "스트라이드"
one_line: "스트라이드는 필터가 입력 위를 이동할 때 한 번에 건너뛰는 칸 수를 뜻한다."
discussion_prompt: "필터를 촘촘히 움직일지 성큼성큼 움직일지의 선택이 모델 표현과 계산량에 어떤 차이를 만들까?"
---

## 핵심 설명
- 스트라이드는 합성곱 필터나 풀링 창이 이동하는 간격이다. 값이 1이면 한 칸씩, 2이면 두 칸씩 움직인다.
- 스트라이드가 커질수록 출력의 공간 크기는 작아지고 계산량도 줄어든다. 대신 세부 정보는 더 많이 생략될 수 있다.
- 즉 스트라이드는 다운샘플링의 한 방법으로 볼 수 있다. 합성곱층 자체에서 해상도를 줄이는 역할을 하기도 한다.
- 커널 크기, 패딩과 함께 스트라이드는 특징 맵의 해상도와 수용영역 성장 속도에 영향을 준다.

## 직관
- 사진을 검사할 때 한 칸씩 꼼꼼히 볼지, 두세 칸씩 건너뛰며 빠르게 볼지 정하는 것과 비슷하다.
- 돋보기를 움직일 때 조금씩 이동하면 자세히 보고, 크게 이동하면 빨리 훑지만 놓치는 부분이 생길 수 있다.

## 헷갈리기 쉬운 점
- 스트라이드가 크다고 무조건 나쁜 것은 아니다. 계산 효율과 추상화 수준을 위해 의도적으로 크게 설정할 때가 많다.
- 풀링에만 스트라이드가 있는 것은 아니다. 합성곱층에서도 스트라이드를 사용해 해상도를 줄일 수 있다.

## 셀프 체크 퀴즈
1. 스트라이드가 커질수록 출력 크기와 계산량은 어떻게 달라지는가?
2. 스트라이드가 큰 설정이 세부 정보 손실과 연결되는 이유는 무엇인가?
3. 합성곱층에서 스트라이드를 이용해 어떤 역할을 수행할 수 있는가?

## source
- Stanford / CS231n Convolutional Neural Networks Notes
- Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola / Dive into Deep Learning
- Ian Goodfellow, Yoshua Bengio, Aaron Courville / Deep Learning / 2016

<!-- FILE: dl-concept-029-pooling.md -->
---
briefing_key: "dl-concept-029-pooling"
track: "dl-basics"
mode: "concept"
title: "풀링"
one_line: "풀링은 주변 값들을 요약해 특징 맵의 크기를 줄이고 중요한 반응을 강조하는 연산이다."
discussion_prompt: "세부 값을 모두 남기지 않고 요약하는 과정이 왜 이미지 인식에서 유용할까?"
---

## 핵심 설명
- 풀링은 작은 영역의 값을 하나로 요약하는 연산이다. 최대값을 고르는 최대 풀링과 평균을 내는 평균 풀링이 대표적이다.
- 이 연산은 공간 크기를 줄여 계산량과 메모리 사용량을 낮춘다. 동시에 작은 위치 변화에 덜 민감한 특징 표현을 만들 수 있다.
- 풀링은 어디에 강한 반응이 있었는지를 요약해 다음 층이 더 큰 패턴에 집중하도록 돕는다.
- 최근에는 모든 곳에서 풀링을 쓰기보다, 스트라이드 합성곱이나 글로벌 평균 풀링처럼 목적에 맞게 변형해 사용한다.

## 직관
- 동네별 최고 점수만 남기고 세부 점수표를 줄이는 방식과 비슷하다.
- 큰 지도를 축약본으로 만들 때 작은 구역의 대표 정보만 남기는 과정으로 생각할 수 있다.

## 헷갈리기 쉬운 점
- 풀링이 항상 정보를 버리는 나쁜 연산은 아니다. 필요한 정보를 압축해 다음 단계가 더 큰 구조를 보게 만드는 역할을 한다.
- 최대 풀링과 평균 풀링은 같은 결과를 주지 않는다. 무엇을 강조할지에 따라 의미가 달라진다.

## 셀프 체크 퀴즈
1. 최대 풀링과 평균 풀링은 어떤 차이가 있는가?
2. 풀링이 작은 위치 변화에 덜 민감한 표현을 만드는 이유는 무엇인가?
3. 최근 모델에서 전통적인 풀링을 다른 방식으로 대체하기도 하는 이유는 무엇인가?

## source
- Ian Goodfellow, Yoshua Bengio, Aaron Courville / Deep Learning / 2016
- Stanford / CS231n Convolutional Neural Networks Notes
- Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola / Dive into Deep Learning

<!-- FILE: dl-concept-030-receptive-field.md -->
---
briefing_key: "dl-concept-030-receptive-field"
track: "dl-basics"
mode: "concept"
title: "수용영역"
one_line: "수용영역은 특정 뉴런의 출력에 영향을 주는 입력 영역의 범위를 뜻한다."
discussion_prompt: "깊은 층으로 갈수록 더 넓은 문맥을 볼 수 있다는 말을 수용영역으로 어떻게 설명할 수 있을까?"
---

## 핵심 설명
- 수용영역은 특징 맵의 한 위치가 원래 입력의 어느 범위를 참고해 계산되었는지를 나타낸다.
- 초기 층의 뉴런은 작은 지역만 보지만, 층이 깊어질수록 여러 지역 특징이 합쳐져 더 넓은 입력 범위를 보게 된다.
- 수용영역이 충분히 크지 않으면 모델은 전체 물체나 긴 문맥을 파악하기 어렵다. 반대로 너무 빠르게 커지면 세밀한 정보가 약해질 수 있다.
- 커널 크기, 스트라이드, 풀링, 네트워크 깊이는 모두 수용영역의 크기와 성장 방식에 영향을 준다.

## 직관
- 돋보기로 아주 작은 부분만 보면 점 하나만 보이고, 점점 멀리서 보면 모양 전체가 보이는 것과 비슷하다.
- 한 사람이 주변 두세 명의 말만 들을 때와, 여러 단계를 거쳐 회의 전체 맥락을 듣는 상황의 차이로 이해할 수 있다.

## 헷갈리기 쉬운 점
- 특징 맵의 해상도가 작다고 해서 항상 수용영역이 충분히 크다는 뜻은 아니다. 어떤 연산을 거쳤는지가 중요하다.
- 이론적 수용영역과 실제로 강하게 활용되는 영역은 다를 수 있다. 개념적으로는 입력 영향 범위를 보는 도구다.

## 셀프 체크 퀴즈
1. 수용영역은 무엇을 설명하는 개념인가?
2. 깊은 층으로 갈수록 수용영역이 커지는 이유는 무엇인가?
3. 수용영역이 너무 작으면 어떤 종류의 정보를 놓치기 쉬운가?

## source
- Vincent Dumoulin, Francesco Visin / A Guide to Convolution Arithmetic for Deep Learning / 2016
- Ian Goodfellow, Yoshua Bengio, Aaron Courville / Deep Learning / 2016
- Stanford / CS231n Convolutional Neural Networks Notes

<!-- FILE: dl-concept-031-embedding.md -->
---
briefing_key: "dl-concept-031-embedding"
track: "dl-basics"
mode: "concept"
title: "임베딩"
one_line: "임베딩은 단어나 항목 같은 이산 대상을 연속적인 벡터로 바꿔 의미적 관계를 표현하는 방법이다."
discussion_prompt: "단순한 번호표처럼 보이는 토큰을 왜 굳이 벡터 공간에 옮겨 놓아야 할까?"
---

## 핵심 설명
- 임베딩은 이산적인 항목을 고정 길이의 실수 벡터로 나타내는 표현 방식이다. 신경망은 이런 벡터를 입력으로 받아 관계를 계산하기 쉽다.
- 원-핫 벡터와 달리 임베딩은 차원을 줄이면서도 항목 간 유사성을 반영할 수 있다. 비슷한 의미나 역할을 가진 항목은 비슷한 위치에 놓일 수 있다.
- 자연어 처리에서는 단어 임베딩이 대표적이지만, 추천 시스템의 상품, 사용자, 범주형 변수 등에도 널리 쓰인다.
- 임베딩 벡터는 사람이 직접 정하지 않고 학습을 통해 얻는 경우가 많다. 따라서 과제에 맞는 의미 구조를 스스로 형성할 수 있다.

## 직관
- 사람 이름 목록을 숫자 번호로만 적어 두면 관계를 알기 어렵지만, 지도로 배치하면 가까운 사람끼리 비슷하다고 볼 수 있다. 임베딩은 이런 지도와 비슷하다.
- 도서관 책을 제목 순 번호로 두는 대신 주제별로 배치하면 관련 책을 더 쉽게 찾을 수 있다.

## 헷갈리기 쉬운 점
- 임베딩의 각 축이 사람에게 바로 해석되는 의미를 가지는 것은 아니다. 중요한 것은 전체 벡터의 관계 구조다.
- 임베딩은 단어 뜻을 완벽히 고정해 저장하는 사전이 아니다. 학습 데이터와 과제에 따라 표현이 달라질 수 있다.

## 셀프 체크 퀴즈
1. 임베딩이 원-핫 표현보다 유용한 이유는 무엇인가?
2. 비슷한 항목이 임베딩 공간에서 가깝게 놓인다는 말은 무엇을 뜻하는가?
3. 자연어 외의 영역에서도 임베딩을 사용할 수 있는 이유는 무엇인가?

## source
- Tomas Mikolov et al. / Efficient Estimation of Word Representations in Vector Space / 2013
- Ian Goodfellow, Yoshua Bengio, Aaron Courville / Deep Learning / 2016
- Stanford / CS224n Course Notes on Word Vectors

<!-- FILE: dl-concept-032-sequence-modeling.md -->
---
briefing_key: "dl-concept-032-sequence-modeling"
track: "dl-basics"
mode: "concept"
title: "시퀀스 모델링"
one_line: "시퀀스 모델링은 순서가 있는 데이터에서 앞뒤 관계를 고려해 다음 정보나 전체 구조를 예측하는 문제다."
discussion_prompt: "데이터가 같은 요소 집합이어도 순서가 달라지면 의미가 바뀌는 상황을 모델은 어떻게 다뤄야 할까?"
---

## 핵심 설명
- 시퀀스 모델링은 시간이나 위치에 따라 나열된 데이터의 의존관계를 다루는 문제다. 텍스트, 음성, 주가, 센서 데이터가 대표적 예다.
- 이런 데이터에서는 같은 요소라도 순서가 바뀌면 의미가 달라질 수 있다. 따라서 각 항목을 독립적으로 보는 모델로는 한계가 생긴다.
- 모델은 과거 정보, 현재 입력, 때로는 미래 문맥까지 이용해 다음 토큰 예측, 번역, 태깅, 분류 같은 작업을 수행한다.
- RNN, LSTM, GRU, 트랜스포머는 모두 시퀀스 모델링을 위한 대표 구조들이다.

## 직관
- 문장에서 단어 주머니만 보는 것과, 단어 순서를 따라 읽는 것은 이해 수준이 다르다. 시퀀스 모델링은 후자를 다룬다.
- 멜로디는 같은 음이라도 순서가 바뀌면 전혀 다른 곡이 된다. 순서 정보가 핵심인 데이터라고 볼 수 있다.

## 헷갈리기 쉬운 점
- 시퀀스 모델링이 꼭 시간 데이터만 뜻하는 것은 아니다. 위치나 토큰 순서처럼 순차 구조가 있으면 모두 해당된다.
- 모든 시퀀스 작업이 다음 값 예측만 하는 것은 아니다. 전체 문장 분류처럼 시퀀스 전체를 하나의 출력으로 요약하는 문제도 있다.

## 셀프 체크 퀴즈
1. 시퀀스 모델링에서 순서 정보가 중요한 이유는 무엇인가?
2. 텍스트와 음성을 모두 시퀀스 데이터로 보는 공통 이유는 무엇인가?
3. 시퀀스 모델링의 출력 형태가 항상 다음 값 예측만은 아닌 이유는 무엇인가?

## source
- Ian Goodfellow, Yoshua Bengio, Aaron Courville / Deep Learning / 2016
- Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola / Dive into Deep Learning
- Stanford / CS224n Course Materials

<!-- FILE: dl-concept-033-rnn.md -->
---
briefing_key: "dl-concept-033-rnn"
track: "dl-basics"
mode: "concept"
title: "순환신경망"
one_line: "순환신경망은 이전 시점의 상태를 현재 계산에 반영해 시퀀스 정보를 처리하는 신경망이다."
discussion_prompt: "입력을 한 번에 보지 않고 순서대로 읽어 가며 상태를 갱신하는 방식은 어떤 장점과 한계를 가질까?"
---

## 핵심 설명
- 순환신경망은 현재 입력과 이전 은닉 상태를 함께 사용해 새로운 은닉 상태를 계산한다. 그래서 과거 정보를 요약하며 시퀀스를 처리할 수 있다.
- 같은 파라미터를 모든 시점에 공유하므로 길이가 다른 시퀀스에도 적용하기 쉽다. 텍스트, 음성, 시계열에 널리 사용되었다.
- 하지만 시퀀스가 길어지면 오래전 정보가 약해지기 쉽고, 역전파 과정에서 기울기 소실이나 폭발 문제가 생길 수 있다.
- 이 한계를 보완하기 위해 LSTM과 GRU 같은 게이트 구조가 제안되었다.

## 직관
- 문장을 읽을 때 앞에서 읽은 내용을 머릿속에 간단히 요약해 두고 다음 단어를 이해하는 방식과 비슷하다.
- 릴레이 달리기처럼 이전 주자의 정보를 배턴 하나에 담아 다음 단계로 넘기는 구조로 볼 수 있다.

## 헷갈리기 쉬운 점
- 순환신경망이 과거를 본다고 해서 긴 문맥을 항상 잘 기억하는 것은 아니다. 기본 RNN은 멀리 떨어진 의존관계에 약할 수 있다.
- 시퀀스 길이가 가변적이라는 이유만으로 RNN이 항상 최선은 아니다. 병렬화와 장기 의존성 측면에서 다른 구조가 더 유리할 수 있다.

## 셀프 체크 퀴즈
1. 순환신경망에서 은닉 상태는 어떤 역할을 하는가?
2. 기본 RNN이 긴 시퀀스 처리에서 어려움을 겪는 이유는 무엇인가?
3. LSTM과 GRU가 등장한 배경은 무엇인가?

## source
- Jeffrey L. Elman / Finding Structure in Time / 1990
- Ian Goodfellow, Yoshua Bengio, Aaron Courville / Deep Learning / 2016
- Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola / Dive into Deep Learning

<!-- FILE: dl-concept-034-lstm.md -->
---
briefing_key: "dl-concept-034-lstm"
track: "dl-basics"
mode: "concept"
title: "LSTM"
one_line: "LSTM은 게이트와 셀 상태를 사용해 긴 시퀀스의 정보를 더 오래 유지하도록 설계된 순환신경망이다."
discussion_prompt: "기억을 지울지, 쓸지, 꺼낼지를 나누어 조절하는 구조가 왜 긴 문맥 처리에 유리할까?"
---

## 핵심 설명
- LSTM(Long Short-Term Memory)은 입력 게이트, 망각 게이트, 출력 게이트를 이용해 정보 흐름을 조절한다.
- 핵심은 셀 상태라는 비교적 안정적인 경로를 두어, 오래 유지할 정보와 버릴 정보를 구분한다는 점이다. 이 덕분에 기본 RNN보다 긴 의존관계를 다루기 쉽다.
- 번역, 음성 인식, 시계열 예측 등에서 오랫동안 중요한 기본 구조로 쓰였다.
- 구조가 더 복잡하고 계산량도 늘지만, 장기 기억을 다루는 능력 때문에 기본 RNN의 한계를 크게 보완했다.

## 직관
- 노트를 그냥 한 장만 들고 다니는 대신, 보관함과 필터가 있는 다이어리를 쓰는 것과 비슷하다.
- 중요한 메모는 남기고, 불필요한 메모는 지우고, 필요한 순간에만 꺼내 읽는 비서 시스템으로 생각할 수 있다.

## 헷갈리기 쉬운 점
- LSTM이 모든 긴 문맥 문제를 완벽히 해결하는 것은 아니다. 매우 긴 시퀀스나 병렬 계산 측면에서는 다른 구조가 더 유리할 수 있다.
- 게이트가 많다고 무조건 더 좋은 것은 아니다. 과제와 자원에 따라 더 단순한 GRU가 충분할 때도 있다.

## 셀프 체크 퀴즈
1. LSTM의 셀 상태는 기본 RNN의 은닉 상태와 어떤 차이를 가지는가?
2. 망각 게이트는 왜 중요한가?
3. LSTM이 기본 RNN보다 장기 의존관계를 더 잘 다룰 수 있는 이유는 무엇인가?

## source
- Sepp Hochreiter, Jürgen Schmidhuber / Long Short-Term Memory / 1997
- Ian Goodfellow, Yoshua Bengio, Aaron Courville / Deep Learning / 2016
- Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola / Dive into Deep Learning

<!-- FILE: dl-concept-035-gru.md -->
---
briefing_key: "dl-concept-035-gru"
track: "dl-basics"
mode: "concept"
title: "GRU"
one_line: "GRU는 LSTM보다 간단한 게이트 구조로 시퀀스 의존관계를 학습하는 순환신경망이다."
discussion_prompt: "비슷한 목적을 가지면서도 구조를 더 단순하게 만든 GRU는 어떤 상황에서 매력적일까?"
---

## 핵심 설명
- GRU(Gated Recurrent Unit)는 업데이트 게이트와 리셋 게이트를 사용해 정보 유지와 갱신을 조절한다.
- LSTM보다 구조가 단순해 파라미터 수가 적고 계산이 가벼운 편이다. 그럼에도 긴 의존관계를 다루는 능력을 상당 부분 유지한다.
- 데이터 크기, 과제 특성, 자원 제약에 따라 LSTM보다 더 실용적인 선택이 될 수 있다.
- 결국 GRU와 LSTM의 우열은 절대적이지 않다. 실제 성능과 효율을 함께 비교해 선택하는 경우가 많다.

## 직관
- 복잡한 서류 보관함 대신, 자주 쓰는 두 개 버튼만 있는 간단한 정리함으로도 충분히 일을 잘할 수 있는 상황과 비슷하다.
- 자동차의 기능을 줄였지만 핵심 주행 성능은 유지한 경량 모델처럼 생각할 수 있다.

## 헷갈리기 쉬운 점
- GRU가 LSTM보다 단순하다고 해서 항상 성능이 낮은 것은 아니다. 어떤 데이터에서는 비슷하거나 더 잘 작동할 수도 있다.
- 게이트 구조가 단순해도 기본 RNN보다 훨씬 안정적일 수 있다. 단순함과 약함은 같은 뜻이 아니다.

## 셀프 체크 퀴즈
1. GRU가 LSTM보다 구조적으로 단순한 이유는 무엇인가?
2. GRU가 실무에서 매력적인 선택이 될 수 있는 이유는 무엇인가?
3. GRU와 LSTM 중 어느 쪽이 더 낫다고 일반화하기 어려운 이유는 무엇인가?

## source
- Kyunghyun Cho et al. / Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation / 2014
- Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola / Dive into Deep Learning
- Stanford / CS224n Sequence Modeling Materials

<!-- FILE: dl-concept-036-attention.md -->
---
briefing_key: "dl-concept-036-attention"
track: "dl-basics"
mode: "concept"
title: "어텐션"
one_line: "어텐션은 모델이 입력 전체를 똑같이 보지 않고 현재 필요한 부분에 더 큰 가중치를 두게 하는 메커니즘이다."
discussion_prompt: "모든 정보를 같은 비중으로 처리하지 않고 중요한 부분만 더 주목하는 전략이 왜 효과적일까?"
---

## 핵심 설명
- 어텐션은 현재 작업에 관련 있는 입력이나 은닉 상태에 더 큰 가중치를 부여해 정보를 읽는 방식이다.
- 이 메커니즘 덕분에 모델은 고정 길이 벡터 하나에 모든 정보를 억지로 압축하지 않고, 필요할 때 필요한 부분을 다시 참조할 수 있다.
- 기계 번역에서는 현재 생성 중인 단어와 관련된 입력 위치를 더 강하게 볼 수 있어 성능 향상에 큰 기여를 했다.
- 어텐션은 이후 셀프 어텐션과 트랜스포머로 확장되며 현대 딥러닝의 핵심 아이디어가 되었다.

## 직관
- 긴 문서를 읽을 때 모든 문장을 같은 비중으로 기억하지 않고, 현재 질문과 관련된 부분만 다시 찾아보는 것과 비슷하다.
- 발표를 들으며 지금 말하는 주제와 직접 연결된 슬라이드에 눈이 더 가는 상황으로 생각할 수 있다.

## 헷갈리기 쉬운 점
- 어텐션은 단순한 중요도 표시가 아니다. 가중치를 이용해 실제로 어떤 정보를 얼마나 섞어 읽을지를 결정한다.
- 어텐션이 있다고 해서 문맥을 완벽히 이해하는 것은 아니다. 그래도 관련 부분을 선택적으로 참고하게 만든다는 점이 핵심이다.

## 셀프 체크 퀴즈
1. 어텐션이 고정 길이 압축의 한계를 완화하는 이유는 무엇인가?
2. 기계 번역에서 어텐션이 특히 유용한 이유는 무엇인가?
3. 어텐션 가중치는 모델의 어떤 행동을 바꾸는가?

## source
- Dzmitry Bahdanau, Kyunghyun Cho, Yoshua Bengio / Neural Machine Translation by Jointly Learning to Align and Translate / 2015
- Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola / Dive into Deep Learning
- Stanford / CS224n Attention Notes

<!-- FILE: dl-concept-037-self-attention.md -->
---
briefing_key: "dl-concept-037-self-attention"
track: "dl-basics"
mode: "concept"
title: "셀프 어텐션"
one_line: "셀프 어텐션은 시퀀스의 각 위치가 같은 시퀀스 안의 다른 위치들을 참고해 자신의 표현을 업데이트하는 방식이다."
discussion_prompt: "문장 안의 각 단어가 다른 모든 단어를 직접 바라볼 수 있게 하면 어떤 이점이 생길까?"
---

## 핵심 설명
- 셀프 어텐션에서는 각 토큰이 같은 입력 시퀀스의 다른 토큰들과의 관련도를 계산한다. 이를 통해 문맥을 반영한 새로운 표현을 만든다.
- 먼 거리의 단어 사이 관계도 직접 연결할 수 있어, 긴 의존관계를 다루는 데 유리하다. 또한 모든 위치를 병렬로 계산하기 쉬워 효율적이다.
- 각 토큰의 의미가 주변 토큰에 따라 달라지는 자연어 처리에서 특히 강력하다. 같은 단어도 문맥에 따라 다른 표현으로 바뀔 수 있다.
- 셀프 어텐션은 트랜스포머의 핵심 구성 요소이며, 현대 언어 모델의 기반이 된다.

## 직관
- 회의에서 각 사람이 한 명만 따라 듣는 것이 아니라, 방 안 모든 사람의 말을 함께 듣고 자기 발언을 정리하는 모습과 비슷하다.
- 문장 속 단어가 서로를 참고해 의미를 다시 정리하는 협업 회의라고 생각할 수 있다.

## 헷갈리기 쉬운 점
- 셀프 어텐션은 순서 정보를 자동으로 아는 것이 아니다. 별도의 위치 정보가 없으면 토큰 순서를 구분하기 어렵다.
- 모든 토큰이 서로를 본다고 해서 모든 관계가 똑같이 중요한 것은 아니다. 학습을 통해 관련도 가중치가 달라진다.

## 셀프 체크 퀴즈
1. 셀프 어텐션이 긴 의존관계를 다루기 쉬운 이유는 무엇인가?
2. 셀프 어텐션이 병렬 계산에 유리한 이유는 무엇인가?
3. 위치 정보가 별도로 필요한 이유는 무엇인가?

## source
- Ashish Vaswani et al. / Attention Is All You Need / 2017
- Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola / Dive into Deep Learning
- Stanford / CS224n Transformer Notes

<!-- FILE: dl-concept-038-transformer.md -->
---
briefing_key: "dl-concept-038-transformer"
track: "dl-basics"
mode: "concept"
title: "트랜스포머"
one_line: "트랜스포머는 셀프 어텐션과 피드포워드 층을 중심으로 시퀀스를 병렬 처리하는 모델 구조다."
discussion_prompt: "트랜스포머가 시퀀스 모델링의 표준이 된 배경에는 어떤 구조적 강점이 있을까?"
---

## 핵심 설명
- 트랜스포머는 반복 구조 없이 셀프 어텐션으로 토큰 간 관계를 계산한다. 그래서 긴 시퀀스도 병렬로 처리하기 쉽다.
- 기본 블록은 멀티헤드 어텐션, 위치별 피드포워드 네트워크, 잔차 연결, 정규화 등으로 이루어진다.
- 번역에서 시작했지만, 이후 언어 모델, 비전, 음성 등 매우 넓은 영역으로 확장되었다.
- 장기 의존성 처리와 병렬화의 장점 덕분에 RNN 계열을 크게 대체하는 핵심 구조가 되었다.

## 직관
- 한 줄씩 순서대로 일하는 공정 대신, 필요한 관계를 한꺼번에 비교해 병렬로 일하는 공장과 비슷하다.
- 문장 전체를 동시에 펼쳐 놓고 단어들 사이의 관계선을 바로 그리는 방식으로 생각할 수 있다.

## 헷갈리기 쉬운 점
- 트랜스포머가 반복 구조를 쓰지 않는다고 해서 문맥을 무시하는 것은 아니다. 문맥은 셀프 어텐션을 통해 적극적으로 반영된다.
- 트랜스포머가 모든 상황에서 비용이 적은 것은 아니다. 시퀀스 길이가 매우 길면 어텐션 계산량이 부담이 될 수 있다.

## 셀프 체크 퀴즈
1. 트랜스포머가 RNN보다 병렬 처리에 유리한 이유는 무엇인가?
2. 트랜스포머의 핵심 구성 요소에는 무엇이 있는가?
3. 트랜스포머가 다양한 영역으로 확장된 배경은 무엇인가?

## source
- Ashish Vaswani et al. / Attention Is All You Need / 2017
- Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola / Dive into Deep Learning
- Stanford / CS224n Transformer Materials

<!-- FILE: dl-concept-039-positional-encoding.md -->
---
briefing_key: "dl-concept-039-positional-encoding"
track: "dl-basics"
mode: "concept"
title: "위치 인코딩"
one_line: "위치 인코딩은 트랜스포머가 토큰의 순서를 알 수 있도록 위치 정보를 입력 표현에 더하는 방법이다."
discussion_prompt: "셀프 어텐션이 순서에 민감하지 않다면 위치 정보를 어떤 식으로 보완해야 할까?"
---

## 핵심 설명
- 트랜스포머의 셀프 어텐션은 기본적으로 입력 집합의 순서를 직접 알지 못한다. 그래서 각 토큰에 위치 정보를 함께 제공해야 한다.
- 위치 인코딩은 토큰 임베딩에 더해지는 별도의 위치 벡터로 구현할 수 있다. 사인과 코사인 기반의 고정 방식이나, 학습 가능한 위치 임베딩이 대표적이다.
- 이 정보 덕분에 모델은 단어의 종류뿐 아니라 어디에 놓였는지도 함께 고려할 수 있다. 같은 단어라도 위치가 바뀌면 다른 역할을 할 수 있기 때문이다.
- 위치 표현 방식은 모델이 상대적 거리와 순서를 얼마나 잘 다루는지에 영향을 준다.

## 직관
- 같은 재료 카드라도 줄서기 번호가 없으면 순서를 알 수 없다. 위치 인코딩은 각 카드에 붙는 번호표와 비슷하다.
- 회의 발언 기록에서 누가 무슨 말을 했는지만 있고 순서가 없다면 대화 흐름을 이해하기 어렵다. 위치 정보는 그 순서 기록이다.

## 헷갈리기 쉬운 점
- 위치 인코딩은 단어 의미 자체를 바꾸는 것이 아니라, 의미가 놓인 자리 정보를 함께 제공하는 것이다.
- 고정된 사인 파형 방식만 가능한 것은 아니다. 학습 가능한 방식이나 상대 위치 방식도 널리 연구되고 사용된다.

## 셀프 체크 퀴즈
1. 트랜스포머에 위치 인코딩이 필요한 이유는 무엇인가?
2. 고정형 위치 인코딩과 학습형 위치 표현은 어떤 공통 목적을 가지는가?
3. 같은 단어라도 위치 정보가 중요할 수 있는 이유는 무엇인가?

## source
- Ashish Vaswani et al. / Attention Is All You Need / 2017
- Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola / Dive into Deep Learning
- Stanford / CS224n Transformer Notes

<!-- FILE: dl-concept-040-encoder-decoder.md -->
---
briefing_key: "dl-concept-040-encoder-decoder"
track: "dl-basics"
mode: "concept"
title: "인코더-디코더 구조"
one_line: "인코더-디코더 구조는 입력을 표현으로 바꾼 뒤 그 표현을 바탕으로 출력을 생성하는 틀이다."
discussion_prompt: "입력을 이해하는 단계와 출력을 만들어 내는 단계를 나누면 어떤 종류의 문제를 더 잘 다룰 수 있을까?"
---

## 핵심 설명
- 인코더는 입력 시퀀스나 데이터를 받아 의미 있는 내부 표현으로 바꾼다. 디코더는 그 표현을 바탕으로 원하는 출력 시퀀스를 생성한다.
- 입력과 출력의 길이가 다를 수 있는 문제에 특히 잘 맞는다. 번역, 요약, 음성 인식, 이미지 캡셔닝이 대표적이다.
- 초기에는 RNN 기반 구조가 많았고, 이후 어텐션과 트랜스포머 기반 인코더-디코더가 널리 쓰였다.
- 핵심 아이디어는 이해와 생성의 역할을 분리해, 입력을 해석한 뒤 그 정보를 활용해 출력을 순차적으로 만들게 하는 것이다.

## 직관
- 통역사가 먼저 원문을 이해하고 머릿속에 정리한 뒤, 그것을 다른 언어로 말해 주는 과정과 비슷하다.
- 요리법을 읽고 핵심을 머릿속에 정리한 다음, 실제 요리를 차례대로 만들어 내는 흐름으로 볼 수 있다.

## 헷갈리기 쉬운 점
- 인코더가 반드시 하나의 고정 길이 벡터만 만들어야 하는 것은 아니다. 어텐션 이후에는 입력의 여러 위치 표현을 계속 참조할 수 있다.
- 디코더는 단순한 출력층이 아니다. 이전에 생성한 결과와 인코더 정보를 함께 보며 다음 출력을 결정하는 구조일 수 있다.

## 셀프 체크 퀴즈
1. 인코더와 디코더는 각각 어떤 역할을 하는가?
2. 입력과 출력 길이가 다른 문제에서 인코더-디코더 구조가 유용한 이유는 무엇인가?
3. 어텐션이 인코더-디코더 구조를 더 강력하게 만든 이유는 무엇인가?

## source
- Ilya Sutskever, Oriol Vinyals, Quoc V. Le / Sequence to Sequence Learning with Neural Networks / 2014
- Dzmitry Bahdanau, Kyunghyun Cho, Yoshua Bengio / Neural Machine Translation by Jointly Learning to Align and Translate / 2015
- Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola / Dive into Deep Learning

<!-- FILE: dl-concept-041-pretraining.md -->
---
briefing_key: "dl-concept-041-pretraining"
track: "dl-basics"
mode: "concept"
title: "사전학습"
one_line: "사전학습은 큰 데이터와 일반적인 목표로 먼저 학습해 넓은 패턴을 익히는 단계다."
discussion_prompt: "목표 과제를 바로 배우지 않고 먼저 넓은 데이터로 준비 운동을 하는 방식이 왜 강력할까?"
---

## 핵심 설명
- 사전학습은 대규모 데이터에서 비교적 일반적인 목표를 사용해 모델이 기본 표현을 먼저 익히게 하는 과정이다.
- 이 단계에서 모델은 언어 규칙, 시각적 패턴, 구조적 통계처럼 여러 과제에 재사용 가능한 지식을 배울 수 있다.
- 이후 특정 과제용 데이터가 적더라도, 사전학습된 표현을 바탕으로 더 빠르고 안정적으로 적응할 수 있다.
- 현대 대형 언어 모델과 비전 모델의 성능 향상에서 사전학습은 매우 중요한 기반이 되었다.

## 직관
- 전문 훈련 전에 넓은 기초 체력을 먼저 쌓아 두는 것과 비슷하다.
- 새 도시에서 길찾기를 배우기 전에 지도를 읽는 일반 원리를 먼저 익히는 과정으로 생각할 수 있다.

## 헷갈리기 쉬운 점
- 사전학습이 곧 특정 과제 성능을 보장하는 것은 아니다. 목표 과제에 맞는 추가 조정이 여전히 필요할 수 있다.
- 사전학습은 단순히 더 오래 학습하는 것과 다르다. 일반적 목표와 큰 데이터로 재사용 가능한 표현을 만든다는 점이 핵심이다.

## 셀프 체크 퀴즈
1. 사전학습은 어떤 종류의 지식을 먼저 익히게 하는가?
2. 사전학습된 모델이 적은 데이터 환경에서 유리한 이유는 무엇인가?
3. 사전학습과 단순 장시간 학습을 구분해야 하는 이유는 무엇인가?

## source
- Dumitru Erhan et al. / Why Does Unsupervised Pre-training Help Deep Learning? / 2010
- Jacob Devlin et al. / BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding / 2019
- Ian Goodfellow, Yoshua Bengio, Aaron Courville / Deep Learning / 2016

<!-- FILE: dl-concept-042-fine-tuning.md -->
---
briefing_key: "dl-concept-042-fine-tuning"
track: "dl-basics"
mode: "concept"
title: "미세조정"
one_line: "미세조정은 사전학습된 모델을 특정 과제와 데이터에 맞게 추가로 학습시키는 과정이다."
discussion_prompt: "이미 많은 지식을 가진 모델도 왜 목표 과제에 맞는 마지막 조정이 필요할까?"
---

## 핵심 설명
- 미세조정은 사전학습 모델의 파라미터를 초기값으로 사용하고, 목표 과제 데이터로 추가 학습하는 방법이다.
- 사전학습이 일반적인 패턴을 익혔다면, 미세조정은 그 지식을 특정 도메인과 출력 형식에 맞게 다듬는 단계다.
- 전체 파라미터를 모두 조정할 수도 있고, 일부 층만 조정하거나 작은 추가 모듈만 학습할 수도 있다.
- 적은 데이터로도 좋은 출발점을 활용할 수 있어 학습 효율을 높이는 데 매우 유용하다.

## 직관
- 기초 영어를 잘하는 사람이 법률 영어 수업을 추가로 들으며 표현을 다듬는 과정과 비슷하다.
- 이미 기본 지도가 있는 내비게이션에 지역별 상세 정보를 업데이트하는 작업으로 생각할 수 있다.

## 헷갈리기 쉬운 점
- 미세조정은 모델을 처음부터 다시 학습하는 것과 다르다. 기존 지식을 활용해 목표 과제에 맞게 수정한다.
- 전체를 모두 업데이트해야만 미세조정인 것은 아니다. 일부만 조정하는 방식도 넓은 의미의 미세조정에 포함된다.

## 셀프 체크 퀴즈
1. 미세조정은 사전학습과 어떤 관계를 가지는가?
2. 미세조정에서 일부 층만 조정하는 전략을 사용할 수 있는 이유는 무엇인가?
3. 적은 데이터에서 미세조정이 유리한 이유는 무엇인가?

## source
- Jacob Devlin et al. / BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding / 2019
- Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola / Dive into Deep Learning
- Stanford / CS224n Transfer Learning and Fine-tuning Materials

<!-- FILE: dl-concept-043-transfer-learning.md -->
---
briefing_key: "dl-concept-043-transfer-learning"
track: "dl-basics"
mode: "concept"
title: "전이학습"
one_line: "전이학습은 한 과제나 도메인에서 배운 지식을 다른 과제에 옮겨 활용하는 학습 전략이다."
discussion_prompt: "한 문제에서 익힌 지식이 다른 문제에도 도움이 되는 조건은 무엇일까?"
---

## 핵심 설명
- 전이학습은 원본 과제에서 학습한 표현이나 파라미터를 새로운 과제에 재사용하는 접근이다.
- 출발 과제와 목표 과제가 어느 정도 관련이 있다면, 처음부터 배우는 것보다 적은 데이터와 계산으로 더 좋은 성능을 낼 수 있다.
- 사전학습 후 미세조정은 전이학습의 대표 사례다. 하지만 특징 추출기 고정, 도메인 적응 등 더 넓은 방식도 포함된다.
- 핵심은 지식을 버리지 않고 옮긴다는 점이다. 무엇을 얼마나 옮길지는 과제의 유사도에 따라 달라진다.

## 직관
- 피아노를 배운 사람이 다른 악기를 배울 때 리듬감과 악보 읽기 능력을 일부 가져가는 것과 비슷하다.
- 한 도시에서 익힌 길찾기 감각이 비슷한 구조의 다른 도시에서도 도움이 되는 상황으로 생각할 수 있다.

## 헷갈리기 쉬운 점
- 전이학습은 항상 도움이 되지 않는다. 원본 과제와 목표 과제가 너무 다르면 오히려 방해가 되는 음의 전이가 생길 수 있다.
- 전이학습과 미세조정을 같은 뜻으로만 보면 범위가 좁아진다. 미세조정은 전이학습의 한 방식이다.

## 셀프 체크 퀴즈
1. 전이학습이 처음부터 학습하는 것보다 유리할 수 있는 이유는 무엇인가?
2. 미세조정은 왜 전이학습의 한 사례로 볼 수 있는가?
3. 원본 과제와 목표 과제가 너무 다를 때 어떤 문제가 생길 수 있는가?

## source
- Sinno Jialin Pan, Qiang Yang / A Survey on Transfer Learning / 2010
- Jason Yosinski et al. / How Transferable Are Features in Deep Neural Networks? / 2014
- Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola / Dive into Deep Learning

<!-- FILE: dl-concept-044-self-supervised-learning.md -->
---
briefing_key: "dl-concept-044-self-supervised-learning"
track: "dl-basics"
mode: "concept"
title: "자기지도학습"
one_line: "자기지도학습은 데이터 자체에서 학습 목표를 만들어 레이블 없이 표현을 배우는 방법이다."
discussion_prompt: "정답 라벨이 없어도 데이터 안에서 학습 신호를 끌어낼 수 있다는 발상이 왜 중요한가?"
---

## 핵심 설명
- 자기지도학습은 사람이 붙인 정답 라벨 없이, 데이터 내부 구조를 이용해 예측 과제를 만든다. 가려진 단어 맞히기나 서로 맞는 짝 찾기가 대표적이다.
- 이 방식은 대규모 비라벨 데이터를 활용할 수 있어, 값비싼 수작업 라벨링의 부담을 크게 줄여 준다.
- 핵심 목표는 즉시 최종 과제를 푸는 것이 아니라, 이후 다양한 작업에 재사용 가능한 표현을 배우는 것이다.
- 현대 언어 모델과 많은 비전 모델의 기반 학습 전략으로 자기지도학습이 널리 사용된다.

## 직관
- 교사가 문제를 내주지 않아도, 책 일부를 가리고 다음 내용을 예측하며 스스로 공부하는 방식과 비슷하다.
- 퍼즐 조각의 일부를 숨기고 전체 그림을 유추하게 하는 연습으로 이해할 수 있다.

## 헷갈리기 쉬운 점
- 자기지도학습은 완전히 감독이 없는 무작위 학습이 아니다. 목표는 데이터에서 자동으로 만들지만, 분명한 학습 과제가 존재한다.
- 라벨이 없다고 해서 아무 정보도 없는 것은 아니다. 데이터의 순서, 구조, 짝 관계가 중요한 단서가 된다.

## 셀프 체크 퀴즈
1. 자기지도학습이 비라벨 데이터를 활용할 수 있는 이유는 무엇인가?
2. 가려진 단어 예측이 자기지도학습의 예가 되는 이유는 무엇인가?
3. 자기지도학습으로 얻은 표현이 이후 과제에 도움이 되는 이유는 무엇인가?

## source
- Ting Chen et al. / A Simple Framework for Contrastive Learning of Visual Representations / 2020
- Jacob Devlin et al. / BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding / 2019
- Longlong Jing, Yingli Tian / Self-supervised Visual Feature Learning with Deep Neural Networks: A Survey / 2020

<!-- FILE: dl-concept-045-autoencoder.md -->
---
briefing_key: "dl-concept-045-autoencoder"
track: "dl-basics"
mode: "concept"
title: "오토인코더"
one_line: "오토인코더는 입력을 압축한 뒤 다시 복원하도록 학습해 유용한 잠재표현을 배우는 모델이다."
discussion_prompt: "입력을 그대로 출력하게 하는 과제가 단순해 보여도 왜 의미 있는 표현 학습이 가능할까?"
---

## 핵심 설명
- 오토인코더는 인코더가 입력을 잠재표현으로 압축하고, 디코더가 그것을 다시 원래 입력에 가깝게 복원하는 구조다.
- 중간 병목이 충분히 제한되면, 모델은 단순 복사 대신 중요한 구조를 요약하는 표현을 배워야 한다.
- 이 표현은 차원 축소, 잡음 제거, 이상 탐지, 사전학습 등에 활용될 수 있다.
- 핵심은 복원 정확도 자체보다, 복원을 위해 어떤 잠재표현을 배우는가에 있다.

## 직관
- 긴 글을 아주 짧은 메모로 요약했다가 다시 원문을 재구성하려면 핵심 내용을 잘 추려야 한다. 오토인코더도 비슷하다.
- 짐을 작은 가방에 넣었다가 다시 꺼내려면 꼭 필요한 물건 배치를 배워야 하는 상황으로 볼 수 있다.

## 헷갈리기 쉬운 점
- 오토인코더가 입력을 복원한다고 해서 항상 의미 있는 표현을 배우는 것은 아니다. 병목 구조나 제약이 중요하다.
- 오토인코더는 분류 모델이 아니다. 입력 자체를 다시 만드는 것이 직접적인 학습 목표다.

## 셀프 체크 퀴즈
1. 오토인코더에서 병목 구조가 중요한 이유는 무엇인가?
2. 오토인코더의 잠재표현은 어떤 용도로 활용될 수 있는가?
3. 오토인코더의 학습 목표가 분류 모델과 다른 이유는 무엇인가?

## source
- Geoffrey E. Hinton, Ruslan R. Salakhutdinov / Reducing the Dimensionality of Data with Neural Networks / 2006
- Ian Goodfellow, Yoshua Bengio, Aaron Courville / Deep Learning / 2016
- Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola / Dive into Deep Learning

<!-- FILE: dl-concept-046-variational-autoencoder.md -->
---
briefing_key: "dl-concept-046-variational-autoencoder"
track: "dl-basics"
mode: "concept"
title: "변분 오토인코더"
one_line: "변분 오토인코더는 잠재공간을 확률분포로 학습해 새로운 샘플 생성이 가능하도록 만든 오토인코더다."
discussion_prompt: "잠재표현을 점 하나가 아니라 분포로 다루면 생성 모델로서 어떤 이점이 생길까?"
---

## 핵심 설명
- 변분 오토인코더는 입력을 하나의 잠재 벡터로만 보내지 않고, 평균과 분산으로 정의되는 확률분포로 인코딩한다.
- 학습 목표는 복원 손실과 잠재분포 정규화 항을 함께 최적화하는 것이다. 이렇게 하면 잠재공간이 더 매끄럽고 샘플링하기 쉬운 구조를 갖게 된다.
- 학습 후에는 잠재공간에서 표본을 뽑아 새로운 데이터를 생성할 수 있다. 그래서 단순 압축 모델을 넘어 생성 모델로 쓰인다.
- VAE는 확률적 해석이 명확하고 잠재공간 조작이 비교적 쉬워, 생성 모델 개념을 배우는 데 중요한 출발점이다.

## 직관
- 학생의 위치를 한 점으로 찍는 대신, 대략 이 범위에 있을 것이라고 구름처럼 표현하면 새로운 예시도 자연스럽게 뽑아볼 수 있다.
- 지도 위 한 집만 표시하는 것이 아니라 동네 전체 분포를 익혀 두면, 새로운 집 위치를 그럴듯하게 제안할 수 있다.

## 헷갈리기 쉬운 점
- 변분 오토인코더는 일반 오토인코더와 같지 않다. 잠재공간을 분포로 다루고, 생성 가능성을 염두에 둔 정규화가 들어간다.
- 복원 품질만 보면 다른 모델이 더 선명할 수 있다. VAE의 장점은 매끄러운 잠재공간과 확률적 생성 해석에 있다.

## 셀프 체크 퀴즈
1. VAE에서 잠재공간을 분포로 다루는 이유는 무엇인가?
2. VAE의 학습 목표가 일반 오토인코더보다 하나 더 복잡한 이유는 무엇인가?
3. VAE가 새로운 샘플 생성에 적합한 이유는 무엇인가?

## source
- Diederik P. Kingma, Max Welling / Auto-Encoding Variational Bayes / 2014
- Carl Doersch / Tutorial on Variational Autoencoders / 2016
- Ian Goodfellow, Yoshua Bengio, Aaron Courville / Deep Learning / 2016

<!-- FILE: dl-concept-047-gan.md -->
---
briefing_key: "dl-concept-047-gan"
track: "dl-basics"
mode: "concept"
title: "생성적 적대 신경망"
one_line: "생성적 적대 신경망은 생성자와 판별자가 경쟁하며 점점 더 그럴듯한 데이터를 만드는 생성 모델이다."
discussion_prompt: "정답을 직접 맞추는 대신 서로 경쟁하는 두 모델을 붙이면 왜 강한 생성 능력이 생길까?"
---

## 핵심 설명
- GAN(Generative Adversarial Network)은 가짜 데이터를 만드는 생성자와, 진짜와 가짜를 구분하는 판별자가 함께 학습하는 구조다.
- 생성자는 판별자를 속이려 하고, 판별자는 이를 막으려 한다. 이 경쟁 과정에서 생성자는 점점 더 진짜 같은 샘플을 만들게 된다.
- GAN은 매우 선명한 이미지 생성으로 큰 주목을 받았지만, 학습이 불안정하고 모드 붕괴 같은 문제가 생기기 쉽다.
- 따라서 GAN은 강력하지만 다루기 까다로운 생성 모델로 자주 소개된다.

## 직관
- 위조지폐 제작자와 감별사가 서로 실력을 높여 가는 경쟁과 비슷하다.
- 모의 재판에서 공격과 방어가 모두 강해질수록 논리가 정교해지는 구조로 생각할 수 있다.

## 헷갈리기 쉬운 점
- GAN의 판별자는 최종 목적이 아니라 생성자를 훈련시키는 상대 역할이다. 학습 후에는 생성자만 사용하는 경우가 많다.
- GAN이 선명한 샘플을 만들 수 있어도 모든 종류의 생성 문제에서 가장 쉬운 선택은 아니다. 학습 안정성이 큰 과제다.

## 셀프 체크 퀴즈
1. GAN에서 생성자와 판별자는 각각 어떤 역할을 하는가?
2. GAN의 경쟁 구조가 생성 품질 향상에 도움이 되는 이유는 무엇인가?
3. 모드 붕괴는 GAN에서 어떤 문제를 뜻하는가?

## source
- Ian J. Goodfellow et al. / Generative Adversarial Nets / 2014
- Ian Goodfellow, Yoshua Bengio, Aaron Courville / Deep Learning / 2016
- Alec Radford, Luke Metz, Soumith Chintala / Unsupervised Representation Learning with Deep Convolutional Generative Adversarial Networks / 2016

<!-- FILE: dl-concept-048-diffusion-model.md -->
---
briefing_key: "dl-concept-048-diffusion-model"
track: "dl-basics"
mode: "concept"
title: "확산모델"
one_line: "확산모델은 데이터에 점차 노이즈를 더하는 과정을 거꾸로 되돌리며 샘플을 생성하는 모델이다."
discussion_prompt: "데이터를 한 번에 만들어 내지 않고 노이즈 제거를 여러 단계로 나누는 방식은 어떤 장점을 가질까?"
---

## 핵심 설명
- 확산모델은 먼저 데이터에 조금씩 노이즈를 더해 결국 순수한 잡음에 가깝게 만든다고 가정한다. 그런 뒤 학습을 통해 이 과정을 역으로 되돌리는 법을 배운다.
- 생성 단계에서는 무작위 노이즈에서 출발해 여러 번의 복원 단계를 거치며 점점 의미 있는 샘플을 만든다.
- 복잡한 분포를 단계적으로 다루기 때문에 고품질 생성이 가능하다는 장점이 있다. 최근 이미지 생성에서 강력한 성능을 보였다.
- 다만 샘플 생성에 여러 단계가 필요해 속도가 느릴 수 있고, 이를 줄이기 위한 다양한 개선이 연구되었다.

## 직관
- 안개가 낀 사진을 한 번에 선명하게 만드는 대신, 조금씩 잡음을 걷어 내며 그림을 드러내는 방식과 비슷하다.
- 조각상을 한 번에 깎아 내는 대신, 덮인 먼지를 여러 번 털어 내며 형태를 드러내는 과정으로 생각할 수 있다.

## 헷갈리기 쉬운 점
- 확산모델은 단순한 잡음 제거기와 같지 않다. 데이터 분포에서 새로운 샘플을 생성하도록 전체 역과정을 학습한다.
- 여러 단계를 거친다고 해서 무조건 더 좋은 것은 아니다. 품질과 속도 사이의 균형이 중요한 모델 계열이다.

## 셀프 체크 퀴즈
1. 확산모델에서 학습하는 역과정은 무엇을 의미하는가?
2. 확산모델이 노이즈에서 시작해 샘플을 생성할 수 있는 이유는 무엇인가?
3. 확산모델의 대표적인 단점으로 속도가 언급되는 이유는 무엇인가?

## source
- Jascha Sohl-Dickstein et al. / Deep Unsupervised Learning using Nonequilibrium Thermodynamics / 2015
- Jonathan Ho, Ajay Jain, Pieter Abbeel / Denoising Diffusion Probabilistic Models / 2020
- Yang Song et al. / Score-Based Generative Modeling through Stochastic Differential Equations / 2021

<!-- FILE: dl-concept-049-evaluation-metrics.md -->
---
briefing_key: "dl-concept-049-evaluation-metrics"
track: "dl-basics"
mode: "concept"
title: "평가 지표"
one_line: "평가 지표는 모델이 실제로 얼마나 잘 작동하는지 과제 목적에 맞게 수치로 판단하는 기준이다."
discussion_prompt: "손실이 아니라 평가 지표를 따로 챙겨야 하는 이유는 무엇일까?"
---

## 핵심 설명
- 평가 지표는 모델 성능을 해석하는 기준이다. 정확도, 정밀도, 재현율, F1, ROC-AUC, RMSE 같은 지표가 과제에 따라 사용된다.
- 좋은 지표는 실제 목표와 비용 구조를 반영해야 한다. 예를 들어 클래스 불균형이 심하면 정확도만으로는 성능을 오해할 수 있다.
- 손실 함수는 학습을 위한 내부 목표이고, 평가 지표는 결과를 판단하기 위한 외부 기준인 경우가 많다. 둘은 같을 수도 있지만 자주 다르다.
- 따라서 모델 비교에서는 숫자 하나만 보는 것이 아니라, 어떤 지표를 왜 선택했는지 함께 보는 태도가 중요하다.

## 직관
- 운동선수를 평가할 때 점수, 속도, 성공률을 종목별로 다르게 보는 것과 비슷하다. 한 숫자만으로는 충분하지 않다.
- 가게 운영을 볼 때 매출만이 아니라 이익, 재구매율, 반품률을 함께 보는 상황으로 생각할 수 있다.

## 헷갈리기 쉬운 점
- 정확도가 높다고 항상 좋은 모델은 아니다. 희귀 클래스가 중요한 문제에서는 정밀도나 재현율이 더 중요할 수 있다.
- 평가 지표는 많을수록 좋은 것이 아니다. 실제 목표와 가장 잘 맞는 지표를 중심으로 해석해야 한다.

## 셀프 체크 퀴즈
1. 손실 함수와 평가 지표를 구분해야 하는 이유는 무엇인가?
2. 클래스 불균형 문제에서 정확도만 보면 왜 오해가 생길 수 있는가?
3. 평가 지표를 선택할 때 실제 비용 구조를 고려해야 하는 이유는 무엇인가?

## source
- Ian Goodfellow, Yoshua Bengio, Aaron Courville / Deep Learning / 2016
- scikit-learn / Model Evaluation: Quantifying the Quality of Predictions
- Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola / Dive into Deep Learning

<!-- FILE: dl-concept-050-training-vs-inference.md -->
---
briefing_key: "dl-concept-050-training-vs-inference"
track: "dl-basics"
mode: "concept"
title: "학습과 추론"
one_line: "학습은 파라미터를 업데이트하는 과정이고, 추론은 학습된 모델로 새 입력의 출력을 계산하는 과정이다."
discussion_prompt: "같은 모델이라도 학습 모드와 추론 모드가 달라져야 하는 이유는 무엇일까?"
---

## 핵심 설명
- 학습은 손실을 계산하고 역전파를 통해 파라미터를 갱신하는 단계다. 데이터와 정답이 함께 필요하다.
- 추론은 이미 학습된 파라미터를 고정한 채, 새로운 입력에 대한 예측을 계산하는 단계다. 보통 순전파만 수행한다.
- 드롭아웃과 배치 정규화처럼 학습과 추론에서 동작이 달라지는 층이 있기 때문에, 모드를 정확히 전환하는 것이 중요하다.
- 실서비스에서는 추론 속도, 메모리 사용, 지연 시간이 중요해져 학습 때와 다른 최적화 관점이 등장한다.

## 직관
- 수업 시간에 문제를 풀고 피드백을 받으며 실력을 늘리는 과정이 학습이라면, 시험장에서 배운 것으로 답하는 과정이 추론이다.
- 요리 레시피를 계속 수정하며 연습하는 단계와, 손님 앞에서 정해진 레시피로 바로 요리하는 단계의 차이로 볼 수 있다.

## 헷갈리기 쉬운 점
- 추론이 단순히 학습의 마지막 부분은 아니다. 파라미터 업데이트가 없는 별도의 운영 단계다.
- 학습이 끝난 모델이라도 모드를 잘못 두면 드롭아웃이나 배치 정규화 때문에 예측이 흔들릴 수 있다.

## 셀프 체크 퀴즈
1. 학습과 추론의 가장 큰 차이는 무엇인가?
2. 드롭아웃과 배치 정규화가 모드 전환과 관련되는 이유는 무엇인가?
3. 실서비스에서 추론 단계의 관심사가 학습 단계와 다른 이유는 무엇인가?

## source
- Ian Goodfellow, Yoshua Bengio, Aaron Courville / Deep Learning / 2016
- PyTorch / Module Training and Evaluation Modes Documentation
- Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola / Dive into Deep Learning