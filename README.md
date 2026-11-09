# 🎤 Think Fast, Talk Smart

즉흥 스피치 아이디어 생성기. 회의 중 갑작스런 의견 요청, 면접 질문, 건배사, Q&A 등
**준비 없이 말해야 하는 순간**에 말하기 구조와 핵심 포인트, 예시 스크립트를 만들어 줍니다.

## 기능
- **💡 아이디어 생성**: 주제 · 상황 · 청중 · 길이 · 말하기 구조를 고르면 Claude가 핵심 메시지, 구조별 포인트, 예시 스크립트, 대안 아이디어를 생성 (스트리밍)
- **⏱️ 즉흥 연습**: 무작위 질문 + 추천 구조 + 타이머로 즉흥 말하기 연습 (API 불필요)

## 말하기 구조
| 구조 | 흐름 |
|---|---|
| What - So What - Now What | 사실 → 의미 → 다음 행동 |
| Problem - Solution - Benefit | 문제 → 해결책 → 효과 |
| PREP | 주장 → 이유 → 예시 → 주장 |
| 과거 - 현재 - 미래 | 예전 → 지금 → 앞으로 |
| Yes, and... | 인정 → 덧붙이기 |

## 실행

### Windows: 더블클릭 실행
`run.bat` 을 더블클릭하세요. 처음 한 번은 가상환경 생성과 패키지 설치를 자동으로 하고, 이후에는 바로 브라우저에서 앱이 열립니다.
앱을 끄려면 검은 콘솔 창을 닫으면 됩니다. (Python 3.10+ 필요)

### 직접 실행
```bash
pip install -r requirements.txt
cp .streamlit/secrets.toml.example .streamlit/secrets.toml   # API 키 입력
streamlit run app.py
```
API 키는 `.streamlit/secrets.toml`, 환경변수 `ANTHROPIC_API_KEY`, 또는 앱 사이드바 입력 중 하나로 설정할 수 있습니다.

## 기술 스택
- Streamlit
- Anthropic Claude API (`claude-opus-5-5`)
