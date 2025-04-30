import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.docstore.document import Document
from transformers import pipeline
doc = Document(page_content="Hello", metadata={"source": "test"})
print(doc)

from langchain.chains import RetrievalQA

from bs4 import BeautifulSoup
import requests
import time
from dotenv import load_dotenv
import os


load_dotenv()
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

embeddings = HuggingFaceEmbeddings(model_name="hkunlp/instructor-large")
db_path ="faiss_index" # Path to save the FAISS index

llm=GoogleGenerativeAI(api_key=os.environ["GOOGLE_API_KEY"], model="gemini-2.0-flash", temperature=0)
def gfg_scrape():
    root = 'https://www.geeksforgeeks.org'
    url = f'{root}/technical-interview-questions/#programming-language-tools-technologies-interview-questions'

    r = requests.get(url)
    time.sleep(2)
    content = r.text
    soup = BeautifulSoup(content, 'html.parser')

    redirect_divs = soup.find_all('div', class_='redirect')

    links = []
    for div in redirect_divs:
        for link in div.find_all('a', href=True):
            links.append(link['href'])

    print("Extracted links:", links)

    scraped_data = []  #store data in list instead of files

    for link in links:
        full_url = f'{root}{link}' if link.startswith('/') else link
        r = requests.get(full_url)
        time.sleep(2)
        sub_content = r.text
        sub_soup = BeautifulSoup(sub_content, 'html.parser')

        main_content = sub_soup.find('div', class_='entry-content')
        if not main_content:
            main_content = sub_soup.find('article')
        if not main_content:
            main_content = sub_soup.find('div', id='content')

        if main_content:
            title_tag = sub_soup.find(['h1', 'h2'])
            title = title_tag.get_text(strip=True) if title_tag else "untitled"
            transcript = main_content.get_text(strip=True, separator=' ')

            scraped_data.append({ 
                'title': title,
                'url': full_url,
                'content': transcript
            })
        else:
            print(f"No main content found for {full_url}")

    return scraped_data  

def javatpoint_scrape():
    root = 'https://www.tpointtech.com'
    html_file_path = 'c:/Users/user/Desktop/Tpoint Tech - Free Online Tutorials.html'

    # Check if the file exists
    if not os.path.exists(html_file_path):
        print(f"File not found: {html_file_path}. Skipping Javatpoint scrape.")
        return []

    with open(html_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    soup = BeautifulSoup(content, 'html.parser')
    btech_mca_section = soup.find('h3', string='B.Tech/MCA')

    scraped_data = [] 

    if btech_mca_section:
        print("B.Tech/MCA section found.")
        links_container = btech_mca_section.find_next('div', class_='courses-grid')
        if links_container:
            links = links_container.find_all('a', href=True)
            print(f"Found {len(links)} links in the B.Tech/MCA section.")

            for link in links:
                href = link['href']
                full_url = f'{root}{href}' if href.startswith('/') else href
                print(f"Processing link: {full_url}")

                try:
                    response = requests.get(full_url)
                    response.raise_for_status()
                    time.sleep(2)
                    sub_soup = BeautifulSoup(response.text, 'html.parser')

                    main_content = sub_soup.find('div', class_='entry-content')
                    if not main_content:
                        main_content = sub_soup.find('div', id='content')

                    if main_content:
                        text_content = main_content.get_text(strip=True, separator='\n')
                    else:
                        text_content = sub_soup.get_text(strip=True, separator='\n')
                        print(f"Using fallback to extract all text for {full_url}")

                    title_tag = sub_soup.find(['h1', 'h2'])
                    title = title_tag.get_text(strip=True) if title_tag else "untitled"

                    scraped_data.append({  
                        'title': title,
                        'url': full_url,
                        'content': text_content
                    })
                    print(f"Content stored for {full_url}")
                except requests.exceptions.RequestException as e:
                    print(f"Failed to fetch {full_url}: {e}")
        else:
            print("No links container found in the B.Tech/MCA section.")
    else:
        print("B.Tech/MCA section not found in the HTML file.")

    return scraped_data  

def bbs4():
    url = 'https://www.crummy.com/software/BeautifulSoup/bs4/doc/'
    res = requests.get(url)
    time.sleep(2)

    soup = BeautifulSoup(res.text, 'html.parser')

    print("Available <h1> headings:")
    for h1 in soup.find_all('h1'):
        print(h1.get_text(strip=True))

    print("Available <h3> headings:")
    for h3 in soup.find_all('h3'):
        print(h3.get_text(strip=True))

    headings = soup.find_all(['h1', 'h3'])

    scraped_data = []  

    if headings:
        for i, heading in enumerate(headings):
            content = []
            for element in heading.find_all_next():
                if element in headings[i + 1:]:
                    break
                content.append(element.get_text(strip=True))

            extracted_content = '\n'.join(content)

            title = heading.get_text(strip=True).replace('¶', '').replace(' ', '_')

            scraped_data.append({  
                'title': title,
                'content': extracted_content
            })
            print(f"Content stored for heading: {title}")
    else:
        print("No headings found in the document.")

    return scraped_data  

def create_vector_db():

    if os.path.exists(db_path):
        print("FAISS index already exists. Skipping vector DB creation.")
        return  #  Skip regeneration if already exists

    print("Creating FAISS vector database. This may take a while...")
    # Load all text files safely using utf-8
    gfg_data = gfg_scrape()
    javatpoint_data = javatpoint_scrape()
    bbs4_data = bbs4()

    # Combine all scraped data into a single list
    all_scraped_data = gfg_data + javatpoint_data + bbs4_data

    documents = []
    for item in all_scraped_data:
        documents.append(
            Document(
                page_content=item.get('content', ''),
                metadata={
                    "source": item.get('url', 'no_url'),
                    "title": item.get('title', 'untitled')
                }
            )
        )

    # Split into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    docs = text_splitter.split_documents(documents)

    # Create FAISS vector DB
    vectordb = FAISS.from_documents(documents=docs, embedding=embeddings)
    vectordb.save_local(db_path)


def get_quesans_chain():
    vectordb = FAISS.load_local(db_path, embeddings, allow_dangerous_deserialization=True)
    retriever = vectordb.as_retriever(score_threshold=0.5, search_kwargs={"k": 5})

    prompt_template = """You are an expert assistant. Given the following context and a question, your task is to extract the most relevant answer from the context.
    Use the exact text from the context as much as possible. If the answer is not found in the context, reply with: "Sorry, I don't know." Do not guess or fabricate an answer.

    CONTEXT: {context}

    QUESTION: {question}

    ANSWER:"""

    PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",  # Changed to 'stuff' for direct context usage
        retriever=retriever,
        input_key="query",
        return_source_documents=True,
        chain_type_kwargs={"prompt": PROMPT}  # Updated to use 'prompt' instead of 'question_prompt'
    )
    return chain

# Updated timed_chain_query to log retrieved documents for debugging
def timed_chain_query(chain, query):
    if isinstance(query, dict):
        query = query.get("query", "")  # Extract the query string if it's a dictionary

    start = time.time()
    result = chain.invoke({"query": query})
    end = time.time()
    print(f"\n Query took {end - start:.2f} seconds.")

    # Log retrieved documents for debugging
    print("\n📥 Retrieved Document Chunks:")
    source_docs = result.get('source_documents', [])
    if not source_docs:
        print("No documents retrieved.")
    for i, doc in enumerate(source_docs):
        print(f"\n--- Retrieved Doc #{i+1} ---")
        print("Title:", doc.metadata.get('title'))
        print("Source URL:", doc.metadata.get('source'))
        print("Content Preview:\n", doc.page_content[:500], "...\n")

    return result

# Memory Management to keep track of last 6 questions
context_memory = []
def update_memory(question):
    context_memory = []
    context_memory.append(question)
    if len(context_memory) > 6:
        context_memory.pop(0)
    return context_memory

#Answer Summarization for Long Responses
summarizer = pipeline("summarization")
def summarize_if_requested(answer, user_input):
    if "short" in user_input.lower() or "brief" in user_input.lower():
        if len(answer.split()) > 30:
            summary = summarizer(answer, max_length=50, min_length=20, do_sample=False)[0]['summary_text']
            return summary
    return answer

#Feedback Collection
def collect_feedback():
    feedback = input("Was this answer helpful? (yes/no): ").strip().lower()
    if feedback == "yes":
        print("Thank you!  I'm glad it helped.You can ask me anything else.")
    elif feedback == "no":
        print("Sorry, I’ll try to improve next time. Please let me know how I can help you better.")
    else:
        print("Feedback not recognized. Try again later.")

# Session History
chat_log = []

def log_interaction(question, answer):
    chat_log.append((question, answer))

def display_chat_history():
    print("\n--- Chat History ---")
    for i, (q, a) in enumerate(chat_log):
        print(f"{i+1}. Q: {q}\n   A: {a}\n")


if __name__ == "__main__":
   
    create_vector_db()
    chain = get_quesans_chain()

    user_query = "What is the difference between supervised and unsupervised learning"  # keep as a string
    result = timed_chain_query(chain, user_query)

    answer = result['result']
    summarized_answer = summarize_if_requested(answer, user_query)

    print(f"\nAnswer: {summarized_answer}")

    update_memory(user_query)
    log_interaction(user_query, summarized_answer)
    display_chat_history()
    collect_feedback()
