from config import model
from langchain.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
from agents import  SearchAgent
import streamlit as st
            
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

class FutureWorksAgent:
    def __init__(self):
        self.model = model
        self.prompt = """
            Analyze the current state of research and suggest promising future directions based on the following context and prior conversation.

            ### Previous Conversation:
            {chat_history}

            ### Current Research Context:
            {context}

            ### Guidelines:
            1. **Identify gaps** in the existing research landscape.
            2. **Propose specific research directions** that address these gaps.
            3. Consider **technical challenges** that might arise in pursuing these directions.
            4. Suggest **methodological improvements** to advance the field.
            5. Discuss **potential applications** and their real-world impact.

            Focus on providing **concrete, actionable research directions**, offering clear steps forward rather than general or broad suggestions.
            """

    def solve(self, query):
            
        # Load vector store
        vector_db_chunks = FAISS.load_local("vector_db_chunks", embeddings, index_name="base_and_adjacent", allow_dangerous_deserialization=True)
        
        # Get chat history
        history = st.session_state.get("chat_history", [])
        history_text = "\n".join([f"{sender}: {msg}" for sender, msg in history[-5:]])
        
        # Get relevant chunks
        retrieved = vector_db_chunks.as_retriever().get_relevant_documents(query)
        context = "\n".join([doc.page_content for doc in retrieved])
        
        # Generate response
        full_prompt = self.prompt.format(
            chat_history=history_text,
            context=context
        )
        response = self.model.generate_content(full_prompt)
        return response.text