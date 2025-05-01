import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.document_loaders import DirectoryLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
import os

load_dotenv()
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

embeddings = HuggingFaceEmbeddings(model_name="hkunlp/instructor-large")
db_path ="faiss_index" # Path to save the FAISS index

llm=GoogleGenerativeAI(api_key=os.environ["GOOGLE_API_KEY"], model="gemini-2.0-flash")

def create_vector_db():
    
        # Load all text files safely using utf-8
        loader = DirectoryLoader(
            'scraped_content',
            glob="**/*.txt",
            loader_cls=lambda path: TextLoader(path, encoding='utf-8')
        )

        data = loader.load()
        
        # Split the documents into smaller chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        docs = text_splitter.split_documents(data)
        
        # Create the FAISS vector database
        vectordb = FAISS.from_documents(documents=docs, embedding=embeddings)
        vectordb.save_local(db_path)
        
def get_quesans_chain():
        vectordb = FAISS.load_local(db_path, embeddings,allow_dangerous_deserialization=True)
        retriever = vectordb.as_retriever(score_threshold = 0.7)
        prompt_template = """Given the following context and a question, generate an answer based on this context only.
        In the answer try to provide as much text as possible from "response" section in the source document context without making much changes.
        If the answer is not found in the context, kindly state "Sorry,I don't know." Don't try to make up an answer.

        CONTEXT: {context}

        QUESTION: {question}"""


        PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
        )
        chain_type_kwargs = {"question_prompt": PROMPT}

        GoogleGenerativeAI(api_key=os.environ["GOOGLE_API_KEY"], model="gemini-2.0-flash")


        chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="map_reduce",
            retriever=retriever,
            input_key="query",
            return_source_documents=True,
            chain_type_kwargs=chain_type_kwargs
        )
        return chain


    

if __name__ == "__main__":
    #create_vector_db()
    chain= get_quesans_chain()
    print(chain("What is the difference between supervised and unsupervised learning?"))
    


