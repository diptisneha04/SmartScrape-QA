import streamlit as st
from main import get_quesans_chain, timed_chain_query, summarize_if_requested

# Initialize chatbot chain
if 'chain' not in st.session_state:
    st.session_state.chain = get_quesans_chain()

# Initialize memory
if 'memory' not in st.session_state:
    st.session_state.memory = []

# Set page layout
st.set_page_config(page_title="Question-Answer Chatbot", layout="wide")

# Custom CSS for dark-themed UI
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

# Split screen layout
col1, col2 = st.columns([1, 2])

# MEMORY SECTION
with col1:
    st.markdown("<div class='memory-box'><h3>MEMORY</h3>", unsafe_allow_html=True)
    for i, q in enumerate(st.session_state.memory[-6:][::-1], 1):
        st.markdown(f"{i}. {q}")
    st.markdown("</div>", unsafe_allow_html=True)

# CHATBOT SECTION
with col2:
    st.markdown("<div class='chat-box'>", unsafe_allow_html=True)
    st.markdown("<h2>QUESTION-ANSWER CHATBOT</h2>", unsafe_allow_html=True)

    question = st.text_input("Ask your question:")

    if st.button("Get Answer"):
        if question.strip():
            chain = st.session_state.chain
            st.session_state.memory.append(question)
            result = timed_chain_query(chain, question)
            answer = summarize_if_requested(result["result"], question)
            st.session_state.last_answer = answer
        else:
            st.warning("Please enter a valid question.")

    if 'last_answer' in st.session_state:
        st.text_area("Answer:", value=st.session_state.last_answer, height=150)

        st.markdown("**Was this answer helpful?**")
        feedback = st.radio("Feedback", ["Yes", "No"], horizontal=True)

        if feedback == "Yes":
            st.success("Thank you! I'm glad it helped. You can ask me anything else.")
        elif feedback == "No":
            st.markdown("""
            <   div class="warning-box">
                    ⚠️ Sorry, I’ll try to improve next time.
                    <br>Please let me know how I can help better.
                </>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
