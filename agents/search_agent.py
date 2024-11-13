
from config import model
import urllib.request as libreq
import xml.etree.ElementTree as ET
import requests
import os
from langchain.document_loaders import PDFMinerLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import FAISS
from langchain_community.document_loaders import ArxivLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
            
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
index = faiss.IndexFlatL2(len(embeddings.embed_query("hello world")))

text_splitter   =   RecursiveCharacterTextSplitter(
            chunk_size=700,
            chunk_overlap=0,
            length_function=len
        )





class SearchAgent:
    def __init__(self):
     
        self.model = model
        self.p = """
            You are an assistant tasked with extracting research topics or titles from user queries. When a user asks about a specific area of research, identify the core subject of their query and provide a concise, clear title or topic related to that area. If the query refers to a specific research paper, include the paper's title, author(s), and publication year.

            ### Instructions:

            - **General Topics**: If the query refers to a general research area or topic without mentioning a specific paper, identify the primary research field or topic. For instance, if the query is "What are the recent trends in neural network architectures?" your response should be "Neural Network Architectures."

            - **Specific Research Papers**: If the query refers to a particular paper, extract the paper's title, authors, and publication year. For example, for the query "What does the paper 'Improving NLP with Transformers by Sarah Lee, 2020' discuss?" your response should be "'Improving NLP with Transformers' (Sarah Lee, 2020)."

            - **Abstract or General Inquiries**: If the query is a general or high-level question about a field or topic, return the central theme or title related to that field. For example, "What are the latest advancements in reinforcement learning?" would result in "Reinforcement Learning Advancements."

            ### Example Queries and Expected Responses:

            - **User Query**: "Tell me about the latest developments in quantum computing."  
            **Response**: "Quantum Computing Advancements."

            - **User Query**: "Can you summarize the paper 'Neural Networks for Object Recognition by John Doe, 2021'?"  
            **Response**: "'Neural Networks for Object Recognition' (John Doe, 2021)."

            - **User Query**: "What are the key findings in the paper 'AI in Healthcare by Maria Gonzalez, 2022'?"  
            **Response**: "'AI in Healthcare' (Maria Gonzalez, 2022)."

            - **User Query**: "What does the research on text-to-image generation by Alex Turner in 2023 focus on?"  
            **Response**: "'Text-to-Image Generation' (Alex Turner, 2023)."
            """


    def solve(self, task):
        print(f"Searching for information on: {task}")
        response = model.generate_content(self.p+task)
        query =  response.text.strip()

        r=query.split(" ")
        query="%20".join(r)
        
        with libreq.urlopen(f'''http://export.arxiv.org/api/query?search_query=all:{query}&sortBy=relevance&sortOrder=descending&start=0&max_results=5''') as url:
            r = url.read()
            
            

        xml_content = r
        root = ET.fromstring(xml_content)
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        ids = [entry.find('atom:id', ns).text for entry in root.findall('atom:entry', ns)]
        pdf_urls = [url.replace("abs", "pdf") for url in ids]

        # Create list to store paper information
        papers = []
        
        # Extract information for each paper
        for entry in root.findall('atom:entry', ns):
            paper_info = {}
            
            # Get paper title
            title = entry.find('atom:title', ns).text
            paper_info['title'] = title
            
            # Get paper ID and create PDF link
            paper_id = entry.find('atom:id', ns).text
            pdf_link = paper_id.replace("abs", "pdf")
            paper_info['link'] = pdf_link
            
            # Get publication year from published date
            published = entry.find('atom:published', ns).text
            year = published[:4]  # Extract year from date string
            paper_info['year'] = year
            
            papers.append(paper_info)

        adjacents_papers_numbers = []

        def download_pdf_paper_from_url(url):
            paper_number = os.path.basename(url).strip(".pdf")
            res = requests.get(url)
            pdf_path = f"papers/{paper_number}.pdf"
            with open(pdf_path, 'wb') as f:
                f.write(res.content)
            return paper_number
            
        for paper in papers:
            paper_number = download_pdf_paper_from_url(paper['link'])
            adjacents_papers_numbers.append(paper_number)
            # Add paper number to paper info
            paper['paper_number'] = paper_number

        vector_db_chunks = FAISS(
            embedding_function=embeddings,
            index=index,
            docstore=InMemoryDocstore(),
            index_to_docstore_id={}
        )
        
        for pdf_number in adjacents_papers_numbers:
            docs = ArxivLoader(query=pdf_number)
            docs = PDFMinerLoader(f"papers/{pdf_number}.pdf").load()
            docs = text_splitter.split_documents(docs)
            vector_db_chunks.add_documents(docs)
        
        vector_db_chunks.save_local("vector_db_chunks", index_name="base_and_adjacent")
        
        return papers , papers
     

