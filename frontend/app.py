import streamlit as st

from orchestrator.main import run_startup_pipeline

st.set_page_config(page_title="AI Startup Builder", page_icon="🚀")
st.title("🚀 AI Startup-in-a-Box")

# --- State Management ---
# Initialize session state variables if they don't exist yet
if "agent_question" not in st.session_state:
    st.session_state["agent_question"] = None
if "pending_user_idea" not in st.session_state:
    st.session_state["pending_user_idea"] = None

# --- UI Logic ---
# STATE 1: PAUSED (Agent needs clarification)
if st.session_state["agent_question"]:
    st.warning("⚠️ The Market Analyst needs more information to proceed.")
    st.markdown(st.session_state["agent_question"])
    user_reply = st.text_input("Your clarification")

    if st.button("Submit Clarification"):
        idea = st.session_state.get("pending_user_idea") or ""
        if not idea.strip():
            st.error("Original idea missing from session. Start over from the home screen.")
        elif not user_reply.strip():
            st.warning("Please enter a clarification.")
        else:
            with st.spinner("Resuming research..."):
                result = run_startup_pipeline(idea, clarification=user_reply.strip())

            if result["status"] == "success":
                st.session_state["agent_question"] = None
                st.session_state["pending_user_idea"] = None
                st.success("✅ Created successfully!")
                st.markdown("---")
                st.markdown(result["data"])
            elif result["status"] == "paused":
                st.session_state["agent_question"] = result["data"]
                st.rerun()
            elif result["status"] == "error":
                st.error(result.get("data", "Unknown error"))

# STATE 2: START (Initial prompt)
else:
    user_idea = st.text_input("Describe your startup idea:")
    
    if st.button("Generate Pitch Deck"):
        if user_idea:
            with st.spinner("Agents are researching..."):
                result = run_startup_pipeline(user_idea)
                
                if result["status"] == "paused":
                    st.session_state["agent_question"] = result["data"]
                    st.session_state["pending_user_idea"] = user_idea
                    st.rerun()
                elif result["status"] == "success":
                    st.session_state["pending_user_idea"] = None
                    st.success("✅ Created successfully!")
                    st.markdown("---")
                    st.markdown(result["data"])
                elif result["status"] == "error":
                    st.error(result.get("data", "Unknown error"))
        else:
            st.warning("Please enter an idea first.")