import os
import streamlit as st
from dotenv import load_dotenv
from services import generate_prd

load_dotenv()

st.set_page_config(page_title="Automated PRD Generator", layout="wide")
st.title("Automated Scoping and Product Requirements Generator")
st.markdown('Transform messy feature ideas into a structured Product Requirements Document instantly.')

api_key_input = st.sidebar.text_input("Google AI Studio key", type="password")
api_key = api_key_input or st.secrets.get("GEMINI_API_KEY") or os.getenv("GOOGLE_GENAI_API_KEY")

raw_input_text = st.text_area(
    "Paste your raw feature idea or meeting notes here:",
    height=200,
    placeholder="Example: Build an e-commerce dashboard with real-time inventory tracking."
)

generate_button = st.button("Generate PRD", type="primary")

if generate_button:
    if not api_key:
        st.error("Please provide a valid API key in the sidebar.")
    elif not raw_input_text.strip():
        st.error("Please enter input text.")
    else:
        # Use st.status to provide clear, step-by-step visibility
        with st.status("Running generation pipeline...", expanded=True) as status:
            try:
                status.update(label="Sending payload to Gemini 3.8 Flash...", state="running")
                
                # Call modular service function
                prd = generate_prd(api_key, raw_input_text)
                
                status.update(label="PRD generated successfully!", state="complete", expanded=False)
                st.success("Rendering output below.")

            except Exception as e:
                status.update(label="Generation failed.", state="error")
                st.error(f"{e}")
                st.stop()

        # Render Output
        st.divider()
        st.header(prd.project_title)

        st.subheader("1. Executive Summary")
        st.markdown(f"**Problem Statement:** {prd.problem_statement}")
        st.markdown(f"**Target Audience:** {prd.target_audience}")

        st.subheader("2. Goals and Success Metrics")
        for g in prd.goals_and_kpis:
            st.markdown(f"- **Metric:** {g.metric}, **Target:** {g.target}")

        st.subheader("3. User Stories and Acceptance Criteria")
        for story in prd.user_stories:
            with st.expander(f"**{story.id}**: As a {story.as_a}, I want {story.i_want} so that {story.so_that}"):
                st.markdown("**Acceptance Criteria:**")
                for criteria in story.acceptance_criteria:
                    st.markdown(f"* {criteria}")

        st.subheader("4. Technical Considerations")
        for tech in prd.technical_considerations:
            st.markdown(f"- {tech}")

        st.subheader("5. Scope Boundaries")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**In Scope:**")
            for item in prd.scope.in_scope:
                st.markdown(f"- {item}")
        with col2:
            st.markdown("**Out of Scope:**")
            for item in prd.scope.out_of_scope:
                st.markdown(f"- {item}")

        with st.expander("View Raw PRD JSON Output"):
            st.json(prd.model_dump())
