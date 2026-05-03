import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# The backend API URL
API_URL = os.getenv("API_URL", "http://localhost:8000/api")

st.set_page_config(page_title="Multi-Agent Research Assistant", page_icon="🕵️", layout="wide")

st.title("🕵️ Multi-Agent Research Assistant")
st.markdown("""
Enter a topic, and our AI agents will:
1. **Search** the web for information.
2. **Summarize** the findings.
3. **Write** a comprehensive report.
4. **Critique** and revise the report.
""")

topic = st.text_input("What would you like to research?", placeholder="e.g., The impact of quantum computing on cryptography")
max_revisions = st.slider("Max Revisions (for the Critic Agent)", min_value=1, max_value=5, value=2)

if st.button("Start Research", type="primary"):
    if not topic:
        st.warning("Please enter a research topic.")
    else:
        with st.spinner("Agents are working... This may take a minute depending on the topic and revisions."):
            try:
                response = requests.post(
                    f"{API_URL}/research",
                    json={"topic": topic, "max_revisions": max_revisions},
                    timeout=300 # Give it 5 minutes to finish
                )
                response.raise_for_status()
                data = response.json()
                
                st.success("Research Complete!")
                st.info(f"Revisions required by Critic: {data.get('revisions', 0)}")
                
                st.markdown("---")
                st.markdown(data.get("report", "No report generated."))
                
                with st.expander("Raw Output"):
                    st.json(data)
                    
            except requests.exceptions.RequestException as e:
                st.error(f"Error communicating with the backend API: {e}")
                st.info("Make sure the backend server is running on port 8000.")
