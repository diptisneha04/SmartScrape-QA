import streamlit as st
from main import get_quesans_chain, timed_chain_query, summarize_if_requested

# Initialize chain
if 'chain' not in st.session_state:
    st.session_state.chain = get_quesans_chain()

# Initialize memory (question-answer pairs)
if 'memory' not in st.session_state:
    st.session_state.memory = []

# Track last interaction state
if 'last_qa' not in st.session_state:
    st.session_state.last_qa = None
if 'show_answer' not in st.session_state:
    st.session_state.show_answer = False
if 'feedback' not in st.session_state:
    st.session_state.feedback = None

# UI setup
st.set_page_config(page_title="SmartScrape QA Assistant", layout="wide")

st.markdown("""
<style>
body {
    background-color: #1a1a1a;
    color: white;
}
input, textarea {
    background-color: #2a2a2a !important;
    color: white !important;
}
.stTextInput > div > div > input {
    background-color: #2a2a2a !important;
    color: white !important;
}
.stTextArea > div > textarea {
    background-color: #2a2a2a !important;
    color: white !important;
}
.memory-box {
    background-color: #2a2a2a;
    padding: 1rem;
    border-radius: 8px;
    margin-bottom: 2rem;
}
.chat-box {
    background-color: #2a2a2a;
    padding: 2rem;
    border-radius: 8px;
}
.warning-box {
    background-color: #3d1f1f;
    padding: 1rem;
    border: 1px solid #aa0000;
    border-radius: 6px;
    color: #ffcccc;
    margin-top: 1rem;
}
label {
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# Layout
col1, col2 = st.columns([1, 2])

# MEMORY SECTION
with col1:
    st.markdown("<div class='memory-box'><h3>MEMORY</h3>", unsafe_allow_html=True)
    for i, qa in enumerate(st.session_state.memory[-6:][::-1], 1):
        with st.expander(f"{i}. Q: {qa['question']}"):
            st.markdown(f"**A:** {qa['answer']}")
    st.markdown("</div>", unsafe_allow_html=True)


# CHATBOT SECTION
with col2:
    st.markdown("<div class='chat-box'>", unsafe_allow_html=True)
    st.markdown("<h2>QUESTION-ANSWER CHATBOT</h2>", unsafe_allow_html=True)

    question = st.text_input("Ask your question:")

    if st.button("Get Answer"):
        if question.strip():
            chain = st.session_state.chain
            result = timed_chain_query(chain, question)
            answer = summarize_if_requested(result["result"], question)

            # Save to memory as Q&A pair
            st.session_state.memory.append({"question": question, "answer": answer})
            st.session_state.last_qa = {"question": question, "answer": answer}
            st.session_state.show_answer = True
            st.session_state.feedback = None  # reset feedback
        else:
            st.warning("Please enter a valid question.")

    if st.session_state.show_answer and st.session_state.last_qa:
        st.text_area("Answer:", value=st.session_state.last_qa["answer"], height=150)

        st.markdown("**Was this answer helpful?**")
        feedback = st.radio("Feedback", ["Yes", "No"], horizontal=True, index=None, key="feedback_radio")

        if feedback == "Yes":
            st.success("Thank you! I'm glad it helped. You can ask me anything else.")
        elif feedback == "No":
            st.markdown("""
            <div class="warning-box">
                ⚠️ Sorry, I’ll try to improve next time.
                <br>Please let me know how I can help better.
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
