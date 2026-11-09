"""Think Fast, Talk Smart - 즉흥 스피치 아이디어 생성기.

갑자기 말해야 하는 상황(회의, 면접, 건배사, 질의응답 등)에서
말할 구조와 핵심 포인트, 예시 스크립트를 빠르게 만들어 줍니다.
"""

import os
import random
import time

import anthropic
import streamlit as st

MODEL = "claude-opus-5-5"

STRUCTURES = {
    "What - So What - Now What": "무엇인가(사실) → 왜 중요한가(의미) → 이제 무엇을 할까(다음 행동)",
    "Problem - Solution - Benefit": "문제 → 해결책 → 기대 효과",
    "PREP": "주장(Point) → 이유(Reason) → 예시(Example) → 주장 반복(Point)",
    "과거 - 현재 - 미래": "예전에는 → 지금은 → 앞으로는",
    "Yes, and...": "상대의 말을 인정하고(Yes) → 내 생각을 더한다(and)",
}

SITUATIONS = ["회의 중 즉석 의견", "면접 질문 답변", "건배사 / 축사", "Q&A 질문 응답", "자기소개", "스몰토크", "기타"]

PRACTICE_PROMPTS = [
    "지난주에 배운 것 중 가장 유용했던 것은?",
    "우리 팀의 가장 큰 강점을 1분 안에 설명해 보세요.",
    "실패에서 배운 경험을 이야기해 주세요.",
    "재택근무와 출근, 어느 쪽이 더 생산적인가요?",
    "동료의 승진을 축하하는 건배사를 해 주세요.",
    "AI가 우리 업무를 어떻게 바꿀까요?",
    "가장 좋아하는 책을 추천해 주세요.",
    "고객이 가격이 비싸다고 할 때 어떻게 답하시겠어요?",
    "5년 뒤 당신은 어떤 모습일까요?",
    "오늘 회의에서 결정된 사항을 요약해 주세요.",
]

SYSTEM_PROMPT = """당신은 즉흥 스피치 코치입니다. 사용자가 준비할 시간 없이 바로 말해야 하는 상황에서
짧고 명확하게 말할 수 있도록 돕습니다. 원칙:
- 완벽함보다 연결: 청중이 바로 이해할 수 있는 쉬운 말을 씁니다.
- 구조가 자유를 줍니다: 선택된 말하기 구조를 그대로 따릅니다.
- 짧게: 지정된 길이에 맞추고, 군더더기를 뺍니다.

다음 마크다운 형식으로 한국어로 답하세요:
### 핵심 메시지
(한 문장)
### 구조별 말하기 포인트
(구조의 각 단계마다 1~2개의 짧은 bullet)
### 예시 스크립트
(실제로 소리 내어 말할 수 있는 문장, 지정 길이에 맞춤)
### 대안 아이디어
(다른 각도의 오프닝 또는 포인트 3개)
"""


def get_api_key() -> str | None:
    try:
        if "ANTHROPIC_API_KEY" in st.secrets:
            return st.secrets["ANTHROPIC_API_KEY"]
    except Exception:
        pass
    return os.environ.get("ANTHROPIC_API_KEY") or st.session_state.get("api_key") or None


def generate(client: anthropic.Anthropic, user_prompt: str):
    """Claude 응답을 스트리밍으로 생성합니다. (텍스트 조각을 yield)"""
    with client.beta.messages.stream(
        model=MODEL,
        max_tokens=16000,
        system=SYSTEM_PROMPT,
        output_config={"effort": "low"},
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
        messages=[{"role": "user", "content": user_prompt}],
    ) as stream:
        for text in stream.text_stream:
            yield text
        final = stream.get_final_message()
        if final.stop_reason == "refusal":
            yield "\n\n> 요청을 처리할 수 없습니다. 주제를 바꿔 다시 시도해 주세요."


# ---------------- UI ----------------
st.set_page_config(page_title="Think Fast, Talk Smart", page_icon="🎤")
st.title("🎤 Think Fast, Talk Smart")
st.caption("즉흥 스피치 아이디어 생성기 - 갑자기 말해야 할 때, 구조부터 잡아 드립니다.")

with st.sidebar:
    st.header("설정")
    if not get_api_key():
        st.text_input("Anthropic API Key", type="password", key="api_key")
    st.markdown("**말하기 구조**")
    for name, desc in STRUCTURES.items():
        st.markdown(f"- **{name}**: {desc}")

tab_gen, tab_practice = st.tabs(["💡 아이디어 생성", "⏱️ 즉흥 연습"])

with tab_gen:
    topic = st.text_area("무엇에 대해 말해야 하나요?", placeholder="예: 신규 프로젝트 일정이 2주 늦어진 이유를 팀장님께 설명")
    col1, col2 = st.columns(2)
    situation = col1.selectbox("상황", SITUATIONS)
    structure = col2.selectbox("말하기 구조", list(STRUCTURES.keys()))
    col3, col4 = st.columns(2)
    audience = col3.text_input("청중", placeholder="예: 팀장님, 면접관, 동료들")
    length = col4.select_slider("말하는 시간", options=["30초", "1분", "2분", "3분"], value="1분")

    if st.button("아이디어 생성", type="primary", disabled=not topic.strip()):
        api_key = get_api_key()
        if not api_key:
            st.error("사이드바에 Anthropic API Key를 입력해 주세요.")
        else:
            client = anthropic.Anthropic(api_key=api_key)
            prompt = (
                f"상황: {situation}\n주제: {topic}\n청중: {audience or '일반 청중'}\n"
                f"말하기 구조: {structure} ({STRUCTURES[structure]})\n길이: {length}"
            )
            try:
                st.write_stream(generate(client, prompt))
            except anthropic.AuthenticationError:
                st.error("API Key가 올바르지 않습니다.")
            except anthropic.RateLimitError:
                st.error("요청이 너무 많습니다. 잠시 후 다시 시도해 주세요.")
            except anthropic.APIStatusError as e:
                st.error(f"API 오류 ({e.status_code}): {e.message}")
            except anthropic.APIConnectionError:
                st.error("네트워크 연결을 확인해 주세요.")

with tab_practice:
    st.write("무작위 질문을 받고, 구조를 떠올려 바로 말해 보세요.")
    if st.button("🎲 새 질문 뽑기"):
        st.session_state.practice_q = random.choice(PRACTICE_PROMPTS)
        st.session_state.practice_s = random.choice(list(STRUCTURES.keys()))
    if "practice_q" in st.session_state:
        st.subheader(st.session_state.practice_q)
        s = st.session_state.practice_s
        st.info(f"추천 구조: **{s}** - {STRUCTURES[s]}")
        secs = st.slider("타이머(초)", 30, 180, 60, step=30)
        if st.button("▶️ 시작"):
            bar = st.progress(0, text=f"{secs}초")
            for i in range(secs):
                time.sleep(1)
                bar.progress((i + 1) / secs, text=f"남은 시간 {secs - i - 1}초")
            st.success("끝! 핵심 메시지가 한 문장으로 전달됐나요?")
