import streamlit as st
import os
import sys
from router import Router

# Add root directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Initialize the Router only once
router = Router()


def main():
    # Page layout
    st.set_page_config(
        page_title="Academic Research Assistant",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Sidebar for navigation and instructions
    with st.sidebar:
        st.title("📚 Academic Research Assistant")
        st.markdown(
            """
            Welcome! This tool helps you find relevant research papers based on your queries.
            - 💬 **Chat with the Assistant** to ask about research topics.
            - 📄 **View Fetched Papers** from your queries.
            """
        )
        st.markdown("### About")
        st.info(
            """
            This assistant uses intelligent query handling to fetch academic papers.
            Try asking about specific topics like:
            - "Deep learning in medical imaging"
            - "Recent advances in generative models"
            """
        )

    # Initialize session states for chat history and fetched papers
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    if "fetched_papers" not in st.session_state:
        st.session_state["fetched_papers"] = []

    # Header Section
    st.title("💬 Chat with the Academic Assistant")
    st.write("Get started by asking a research-related question below:")

    # Chat Input Section
    with st.container():
        col1, col2 = st.columns([4, 1])
        with col1:
            user_input = st.text_input(
                "Enter your query (e.g., 'Advancements in text-to-SQL')",
                placeholder="Ask a research question...",
                key="user_input"
            )
        with col2:
            send_button = st.button("🔍 Search")

    # Handle user input
    if user_input and send_button:
        # Display user query in chat
        st.session_state["chat_history"].append(("User", user_input))

        # Use Router to handle the query
        response, papers = router.route_query(user_input)

        # Ensure unique papers by paper number
        if papers:
            unique_papers = {paper['paper_number']: paper for paper in papers}
            st.session_state["fetched_papers"] = list(unique_papers.values())

        # Append bot's response to chat history
        if response:
            st.session_state["chat_history"].append(("Assistant", response))
        else:
            st.session_state["chat_history"].append(
                ("Assistant", "No relevant response found. Please try a different query.")
            )

        # Refresh page to display chat update
        st.rerun()

    # Display Chat History
    st.markdown("### 🗨️ Conversation History")
    with st.container():
        if st.session_state["chat_history"]:
            for sender, message in reversed(st.session_state["chat_history"]):
                if sender == "User":
                    st.markdown(f"**👤 User**: {message}")
                else:
                    st.markdown(f"**🤖 Assistant**: {message[0]}")
        else:
            st.info("No conversation yet. Start by entering a query above.")

    st.markdown("---")  # Divider line

    # Display Fetched Papers
    st.markdown("### 📄 Fetched Research Papers")
    if st.session_state["fetched_papers"]:
        for idx, paper in enumerate(st.session_state["fetched_papers"]):
            with st.container():
                col1, col2 = st.columns([5, 1])
                with col1:
                    clean_title = paper.get('title', '').replace('\n', ' ').strip()
                    st.markdown(f"**{idx + 1}. Title**: {clean_title}")
                    st.markdown(f"**Year**: {paper.get('year', 'N/A')}")
                    st.markdown(f"**Paper ID**: {paper.get('paper_number', 'N/A')}")
                    st.markdown(f"**Abstract**: {paper.get('abstract', 'No abstract available.')}")
                with col2:
                    download_link = paper.get('link')
                    if download_link:
                        st.markdown(f"[📥 Download PDF]({download_link})", unsafe_allow_html=True)
                    else:
                        st.markdown("No download link available.")

                st.markdown("---")  # Separator line
    else:
        st.info("No papers fetched yet. Please enter a query to get started.")

# Run the Streamlit app
if __name__ == "__main__":
    main()
