import random
import streamlit as st

st.set_page_config(page_title="영단어 게임", page_icon="📚")

WORD_BANK = [
    {"word": "friend", "meaning": "친구"},
    {"word": "beautiful", "meaning": "아름다운"},
    {"word": "travel", "meaning": "여행하다"},
    {"word": "library", "meaning": "도서관"},
    {"word": "important", "meaning": "중요한"},
    {"word": "exercise", "meaning": "운동"},
    {"word": "dangerous", "meaning": "위험한"},
    {"word": "imagine", "meaning": "상상하다"},
    {"word": "decide", "meaning": "결정하다"},
    {"word": "celebrate", "meaning": "축하하다"},
]


def make_questions():
    questions = []
    selected = random.sample(WORD_BANK, 8)
    for item in selected:
        distractors = [w["word"] for w in WORD_BANK if w["word"] != item["word"]]
        options = [item["word"], *random.sample(distractors, 3)]
        random.shuffle(options)
        questions.append(
            {
                "word": item["word"],
                "meaning": item["meaning"],
                "options": options,
                "answer": item["word"],
            }
        )
    return questions


def reset_game():
    st.session_state.questions = make_questions()
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.show_result = False
    st.session_state.finished = False
    st.session_state.feedback = ""


if "questions" not in st.session_state:
    reset_game()

st.title("📚 영어 공부 앱")
st.write("영단어 게임과 BTS 소개를 함께 즐겨보세요!")

word_tab, bts_tab = st.tabs(["📖 영단어 게임", "🎤 BTS 소개"])

with word_tab:
    st.subheader("영단어 퀴즈")
    st.write("뜻을 보고 영어 단어를 고르는 간단한 퀴즈입니다.")

    st.button("🔄 새 게임 시작", on_click=reset_game)

    if st.session_state.finished:
        st.success(f"게임 끝! 점수: {st.session_state.score}/{len(st.session_state.questions)}")
        st.write("다시 시작해서 더 많이 맞혀 보세요!")
    else:
        current = st.session_state.questions[st.session_state.index]
        st.progress((st.session_state.index + 1) / len(st.session_state.questions))
        st.subheader(f"문제 {st.session_state.index + 1}")
        st.write(f"뜻: {current['meaning']}")

        if not st.session_state.show_result:
            choice = st.radio(
                "정답을 선택하세요",
                current["options"],
                key=f"choice_{st.session_state.index}",
            )

            if st.button("✅ 정답 확인"):
                if choice is None:
                    st.warning("답을 선택해 주세요.")
                else:
                    if choice == current["answer"]:
                        st.session_state.score += 1
                        st.session_state.feedback = "정답입니다! 👍"
                    else:
                        st.session_state.feedback = f"아쉽네요. 정답은 {current['answer']}입니다."
                    st.session_state.show_result = True
        else:
            if st.session_state.feedback.startswith("정답"):
                st.success(st.session_state.feedback)
            else:
                st.error(st.session_state.feedback)

            if st.session_state.index < len(st.session_state.questions) - 1:
                if st.button("➡️ 다음 문제"):
                    st.session_state.index += 1
                    st.session_state.show_result = False
            else:
                if st.button("🏁 결과 보기"):
                    st.session_state.finished = True

with bts_tab:
    st.subheader("BTS 소개")
    st.write("BTS는 방탄소년단으로, 한국의 대표적인 보이 그룹입니다.")
    st.write("멤버들은 함께 음악과 춤으로 많은 사람들에게 힘이 되는 메시지를 전합니다.")

    st.markdown("### BTS의 특징")
    st.write("- 멤버: RM, 진, 슈가, 제이홉, 지민, 뷔, 정국")
    st.write("- 유명한 곡: Dynamite, Butter, Boy With Luv")
    st.write("- 특별한 점: 멋진 춤과 감동적인 노래가 매력입니다")

    st.info("BTS는 세계적으로 큰 인기를 얻었고, 많은 팬들에게 사랑받고 있습니다.")
