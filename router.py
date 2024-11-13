import streamlit as st
from agents import SearchAgent, QAAgent, FutureWorksAgent
from config import model

class IntentAgent:
    def __init__(self):
        self.model = model
        self.prompt = """
            You are an intent classifier for a research paper assistant. Given a user's query, classify it into one of the following categories:

            - "search": The user is looking for relevant research papers on a specific topic.
            - "qa": The user has questions related to the content or findings of specific research papers.
            - "future_works": The user is interested in exploring future research directions, generating review papers, combining multiple papers, or brainstorming new research ideas.

            ### Example queries and their corresponding intents:
            - "Can you recommend papers on deep reinforcement learning?" → "search"
            - "What does the paper by Smith et al. say about experimental design?" → "qa"
            - "What are some emerging trends in AI research for the next decade?" → "future_works"

            Your response should be limited to the appropriate intent category only.

            Query: {query}
            """
    
    def get_intent(self, query):
        response = self.model.generate_content(self.prompt.format(query=query))
        return response.text.strip().lower()


class Router:
    def __init__(self):
        self.intent_agent = IntentAgent()
        self.agents = {
            "search": SearchAgent(),
            "qa": QAAgent(),
            "future_works": FutureWorksAgent()
        }

    def route_query(self, query):
        st.write(f"Analyzing query to determine intent...")
        intent = self.intent_agent.get_intent(query)
        agent = self.agents.get(intent)
        st.write(f"Using {intent} agent...")
        if agent:
            if intent == "search":
                ans , d = agent.solve(query)
                return ans , d
            return agent.solve(query) , None
        else:
            return "Sorry, I couldn't understand your query." , None
