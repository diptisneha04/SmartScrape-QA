import streamlit as st
from main import get_quesans_chain, timed_chain_query, summarize_if_requested
import html

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
st.set_page_config(
    page_title="SmartScrape QA System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with ultra-modern aesthetics
st.markdown("""
<style>
    /* Global Styles */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #1e1e2e 0%, #2d2b42 100%);
        color: #e0e0ff;
    }
    
    [data-testid="stHeader"] {
        background-color: rgba(0,0,0,0.2);
        backdrop-filter: blur(10px);
    }
    
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    
    /* Typography */
    h1, h2, h3, h4, h5 {
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        color: #fff;
    }
    
    p, div, span {
        font-family: 'Inter', sans-serif;
    }
    
    /* Header Styles */
    .main-header {
        background: linear-gradient(90deg, #4158D0, #C850C0, #FFCC70);
        padding: 2rem;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 100%);
        z-index: 1;
    }
    
    .main-header h1 {
        font-size: 3rem;
        margin-bottom: 0.5rem;
        font-weight: 800;
        background: linear-gradient(to right, #fff, #e0e0ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0px 2px 4px rgba(0,0,0,0.1);
        position: relative;
        z-index: 2;
    }
    
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.9;
        max-width: 600px;
        margin: 0 auto;
        position: relative;
        z-index: 2;
    }
    
    /* Memory Section */
    .memory-title {
        background: linear-gradient(90deg, #4158D0, #C850C0);
        color: white;
        padding: 1rem;
        border-radius: 12px 12px 0 0;
        font-weight: bold;
        text-align: center;
        font-size: 1.2rem;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .memory-title::after {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #FFCC70, #C850C0, #4158D0);
    }
    
    .memory-container {
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-top: none;
        border-radius: 0 0 12px 12px;
        margin-bottom: 1.5rem;
        background-color: rgba(30, 30, 46, 0.6);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(8px);
        padding-bottom: 1rem;
    }
    
    .memory-empty {
        text-align: center;
        padding: 2rem;
        color: rgba(255, 255, 255, 0.6);
        font-style: italic;
    }
    
    .memory-card {
        background: rgba(255, 255, 255, 0.05);
        margin: 0.75rem;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s;
        border-left: 4px solid #C850C0;
        position: relative;
        overflow: hidden;
    }
    
    .memory-card::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(45deg, rgba(65, 88, 208, 0.05) 0%, rgba(200, 80, 192, 0.05) 100%);
        z-index: -1;
    }
    
    .memory-card:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15);
        border-left: 4px solid #FFCC70;
    }
    
    .memory-question {
        font-weight: 600;
        color: #C850C0;
        margin-bottom: 0.5rem;
    }
    
    .memory-answer {
        color: rgba(255, 255, 255, 0.8);
        font-size: 0.9rem;
        white-space: pre-wrap;
    }
    
    /* Chat Section */
    .chat-container {
        background: rgba(30, 30, 46, 0.6);
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .chat-container::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #4158D0, #C850C0, #FFCC70);
    }
    
    /* Input Styles */
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.08) !important;
        color: white !important;
        border-radius: 50px !important;
        padding: 1rem 1.5rem !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        box-shadow: none !important;
        transition: all 0.3s;
        font-size: 1rem !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: rgba(255, 255, 255, 0.5) !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #C850C0 !important;
        box-shadow: 0 0 15px rgba(200, 80, 192, 0.3) !important;
        background-color: rgba(255, 255, 255, 0.12) !important;
    }
    
    /* Button Styles */
    .stButton > button {
        background: linear-gradient(90deg, #4158D0, #C850C0) !important;
        color: white !important;
        border-radius: 50px !important;
        padding: 0.75rem 2.5rem !important;
        font-weight: bold !important;
        border: none !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(65, 88, 208, 0.3) !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton > button::before {
        content: "" !important;
        position: absolute !important;
        top: 0 !important;
        left: -100% !important;
        width: 100% !important;
        height: 100% !important;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent) !important;
        transition: all 0.5s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 25px rgba(65, 88, 208, 0.4) !important;
    }
    
    .stButton > button:hover::before {
        left: 100% !important;
    }
    
    /* Answer Box */
    .answer-box {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 1.5rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .answer-box::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(to bottom, #4158D0, #C850C0, #FFCC70);
    }
    
    .answer-box strong {
        color: #FFCC70;
    }
    
    .answer-divider {
        height: 1px;
        background: linear-gradient(to right, rgba(255, 255, 255, 0), rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0));
        margin: 1rem 0;
    }
    
    /* Text content */
    .text-content {
        white-space: pre-wrap;
        word-wrap: break-word;
    }
    
    /* Feedback Section */
    .feedback-title {
        text-align: center;
        margin: 1.5rem 0 1rem;
        color: rgba(255, 255, 255, 0.9);
        font-weight: 600;
    }
    
    .feedback-container {
        display: flex;
        justify-content: center;
        gap: 1.5rem;
        margin-top: 0.5rem;
    }
    
    .feedback-button {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 50px;
        padding: 0.75rem 2rem;
        cursor: pointer;
        transition: all 0.3s;
        display: flex;
        align-items: center;
        gap: 8px;
        font-weight: 600;
    }
    
    .feedback-button.positive {
        color: #8aff80;
    }
    
    .feedback-button.negative {
        color: #ff80bf;
    }
    
    .feedback-button.selected {
        background-color: rgba(255, 255, 255, 0.1);
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    }
    
    .feedback-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    }
    
    /* Success/Error Messages */
    .success-box {
        background: rgba(138, 255, 128, 0.1);
        color: #8aff80;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin-top: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        border: 1px solid rgba(138, 255, 128, 0.3);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .warning-box {
        background: rgba(255, 128, 191, 0.1);
        color: #ff80bf;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin-top: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        border: 1px solid rgba(255, 128, 191, 0.3);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .error-box {
        background: rgba(255, 100, 100, 0.1);
        color: #ff6464;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin-top: 1.5rem;
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
        border: 1px solid rgba(255, 100, 100, 0.3);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        animation: shake 0.5s cubic-bezier(0.36, 0.07, 0.19, 0.97) both;
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
        20%, 40%, 60%, 80% { transform: translateX(5px); }
    }
    
    .error-details {
        font-size: 0.85rem;
        opacity: 0.8;
        margin-top: 0.5rem;
    }
    
    /* Spinner/Loading */
    .loading {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2rem 0;
    }
    
    .loading-spinner {
        width: 50px;
        height: 50px;
        border: 5px solid rgba(255, 255, 255, 0.1);
        border-radius: 50%;
        border-top-color: #C850C0;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Animation for glowing effect */
    @keyframes glow {
        0% { box-shadow: 0 0 5px rgba(200, 80, 192, 0.3); }
        50% { box-shadow: 0 0 20px rgba(200, 80, 192, 0.5); }
        100% { box-shadow: 0 0 5px rgba(200, 80, 192, 0.3); }
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border-radius: 8px !important;
        color: rgba(255, 255, 255, 0.9) !important;
        padding: 0.75rem 1rem !important;
    }
    
    .streamlit-expanderHeader:hover {
        background-color: rgba(255, 255, 255, 0.1) !important;
    }
    
    div[data-testid="stExpander"] {
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Empty state illustrations */
    .empty-state {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 2rem;
        color: rgba(255, 255, 255, 0.6);
    }
    
    .empty-state-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        color: rgba(200, 80, 192, 0.5);
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(200, 80, 192, 0.5);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(200, 80, 192, 0.7);
    }
    
    /* Text area styling */
    .stTextArea textarea {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: rgba(255, 255, 255, 0.9) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
    }
</style>

<!-- Import Google Fonts -->
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">

<!-- Font Awesome for icons -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
""", unsafe_allow_html=True)

# Main layout
st.markdown('''
<div class="main-header">
    <h1>SmartScrape QA</h1>
    <p>Ask questions about your data and get intelligent, accurate answers powered by AI</p>
</div>
''', unsafe_allow_html=True)

col1, col2 = st.columns([1, 2])

# MEMORY SECTION
with col1:
    st.markdown('<div class="memory-title"><i class="fas fa-history"></i> Recent Conversations</div>', unsafe_allow_html=True)
    st.markdown('<div class="memory-container">', unsafe_allow_html=True)
    
    if not st.session_state.memory:
        st.markdown('''
        <div class="empty-state">
            <div class="empty-state-icon"><i class="fas fa-comments"></i></div>
            <div>No conversation history yet</div>
            <div style="font-size: 0.9rem; margin-top: 0.5rem;">Your recent questions will appear here</div>
        </div>
        ''', unsafe_allow_html=True)
    else:
        for i, qa in enumerate(st.session_state.memory[-6:][::-1], 1):
            question_preview = qa['question'][:40] + ('...' if len(qa['question']) > 40 else '')
            
            with st.expander(f"Q: {question_preview}"):
                st.markdown(f'''
                <div class="memory-card">
                    <div class="memory-question"><i class="fas fa-question-circle"></i> {html.escape(qa['question'])}</div>
                    <div class="answer-divider"></div>
                    <div class="memory-answer"><i class="fas fa-robot"></i> {html.escape(qa['answer'])}</div>
                </div>
                ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# CHATBOT SECTION
with col2:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Question input with icon
    st.markdown('<label for="question_input" style="font-weight: 600; color: rgba(255,255,255,0.9); margin-bottom: 0.5rem; display: block;"><i class="fas fa-search"></i> Ask your question</label>', unsafe_allow_html=True)
    question = st.text_input("", placeholder="What would you like to know about your data?", key="question_input")
    
    # Get Answer button
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
    with col_btn2:
        get_answer_btn = st.button("Get Answer", use_container_width=True)
    
    if get_answer_btn:
        if question.strip():
            with st.spinner(""):
                st.markdown('''
                <div class="loading">
                    <div class="loading-spinner"></div>
                </div>
                ''', unsafe_allow_html=True)
                
                chain = st.session_state.chain
                result = timed_chain_query(chain, question)
                answer = summarize_if_requested(result["result"], question)

                # Save to memory as Q&A pair
                st.session_state.memory.append({"question": question, "answer": answer})
                st.session_state.last_qa = {"question": question, "answer": answer}
                st.session_state.show_answer = True
                st.session_state.feedback = None  # reset feedback
                
                # Remove spinner - this is a hack since Streamlit doesn't allow direct DOM manipulation
                st.markdown('<style>.loading { display: none !important; }</style>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="warning-box"><i class="fas fa-exclamation-triangle"></i> Please enter a valid question.</div>', unsafe_allow_html=True)

    if st.session_state.show_answer and st.session_state.last_qa:
        # Display the answer directly with Streamlit components instead of HTML
        st.markdown("### <i class='fas fa-question-circle'></i> Question:", unsafe_allow_html=True)
        st.markdown(f"<div class='text-content'>{html.escape(st.session_state.last_qa['question'])}</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='answer-divider'></div>", unsafe_allow_html=True)
        
        st.markdown("### <i class='fas fa-robot'></i> Answer:", unsafe_allow_html=True)
        st.markdown(f"<div class='text-content'>{html.escape(st.session_state.last_qa['answer'])}</div>", unsafe_allow_html=True)

        # Error message container (hidden by default)
        st.markdown('''
        <div id="error-message" class="error-box" style="display: none;">
            <i class="fas fa-exclamation-triangle"></i>
            <div>
                <strong>Error:</strong> <span id="error-text"></span>
                <div class="error-details">Please try again or contact support if the issue persists.</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)

        st.markdown('<div class="feedback-title"><i class="fas fa-thumbs-up"></i> Was this answer helpful?</div>', unsafe_allow_html=True)
        
        col_yes, col_no = st.columns([1, 1])
        with col_yes:
            if st.button("👍 Yes, it helped!", key="yes_btn", use_container_width=True):
                st.session_state.feedback = "Yes"
        with col_no:
            if st.button("👎 Not quite", key="no_btn", use_container_width=True):
                st.session_state.feedback = "No"

        if st.session_state.feedback == "Yes":
            st.markdown('<div class="success-box"><i class="fas fa-check-circle"></i> Thank you for your feedback! Feel free to ask another question.</div>', unsafe_allow_html=True)
        elif st.session_state.feedback == "No":
            st.markdown('<div class="warning-box"><i class="fas fa-exclamation-circle"></i> Sorry about that! Please try rephrasing your question or provide more details.</div>', unsafe_allow_html=True)
            
    # Demo error message that can be triggered
    if question == "show error":
        st.markdown('''
        <div class="error-box">
            <i class="fas fa-exclamation-triangle"></i>
            <div>
                <strong>Error Processing Request:</strong> Unable to generate a response due to a processing error.
                <div class="error-details">Error code: E-2025-SC4. Please try again with a different question or contact support if the issue persists.</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    
    # Add tips section
    st.markdown('''
    <div style="margin-top: 2rem; background: rgba(30, 30, 46, 0.6); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.1);">
        <h3 style="margin-bottom: 1rem; font-size: 1.2rem;"><i class="fas fa-lightbulb" style="color: #FFCC70;"></i> Tips for better results</h3>
        <ul style="margin-left: 1.5rem; color: rgba(255, 255, 255, 0.8);">
            <li>Be specific in your questions</li>
            <li>Include relevant data points or time periods</li>
            <li>For complex questions, break them down into simpler parts</li>
            <li>Use "summarize" in your query if you want a concise answer</li>
        </ul>
    </div>
    ''', unsafe_allow_html=True)