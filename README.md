Question-answering (QA) systems are designed to automatically provide answers to questions posed in natural language. Traditional QA systems often relied on structured databases or information retrieval techniques to find relevant information. However, the advent of LLMs has revolutionized this field. LLMs can understand the nuances of human language, enabling them to process a wider range of questions and provide more accurate and contextually appropriate answers.
Vector databases play a crucial role in modern LLM-powered QA systems. These databases store word or document embeddings, which are numerical representations of text that capture semantic meaning. By converting both the query and the stored information into embeddings, the system can efficiently identify the most relevant information using similarity search algorithms. This combination of LLMs for language understanding and vector databases for efficient retrieval has significantly improved the performance and capabilities of QA systems, enabling them to handle complex queries and large volumes of data.
This project leverages the power of generative AI and LLMs to address the challenge of accessing efficient technical support within e-learning environments.


An **AI-powered Question Answering System** that uses **LangChain, FAISS, and Google PaLM/Gemini** to answer questions from web-scraped content.

---

##  Features
- Scrapes FAQ or content from websites (e.g., GeeksforGeeks, StackOverflow, Javatpoint).
- Converts content into **vector embeddings** using HuggingFace.
- Stores embeddings in **FAISS vector database**.
- Uses **LangChain RetrievalQA** pipeline for question answering.
- Interactive **Streamlit web app** UI.

---

## Tech Stack
- **Python** (LangChain, BeautifulSoup, FAISS, HuggingFace)
- **Google PaLM/Gemini LLM**
- **Streamlit** (for UI)
- **Libraries**: requests, bs4, langchain, faiss, transformers

---

## Setup Instructions
```bash
# Clone repo
git clone https://github.com/diptisneha04/SmartScrape-QA.git
cd SmartScrape-QA

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app_enh.py
