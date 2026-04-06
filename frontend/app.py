import streamlit as st

from orchestrator.main import run_startup_pipeline

st.set_page_config(page_title="AI Startup Builder", page_icon="🚀")
st.title("🚀 AI Startup-in-a-Box")

# --- Session state ---
if "agent_question" not in st.session_state:
    st.session_state["agent_question"] = None
if "pending_user_idea" not in st.session_state:
    st.session_state["pending_user_idea"] = None
if "completed_deck" not in st.session_state:
    st.session_state["completed_deck"] = None


def _reset_session_for_new_pitch() -> None:
    st.session_state["agent_question"] = None
    st.session_state["pending_user_idea"] = None
    st.session_state["completed_deck"] = None
    for k in ("user_idea", "clarification_reply"):
        st.session_state.pop(k, None)


# --- After success: show deck only; pipeline caches already cleared on server ---
if st.session_state["completed_deck"]:
    st.success(
        "✅ Pitch deck generated. Pipeline caches were cleared—your next run starts fresh."
    )
    st.markdown("---")
    st.markdown(st.session_state["completed_deck"])
    if st.button("Create another pitch"):
        _reset_session_for_new_pitch()
        st.rerun()
    st.stop()

# --- Paused: market analyst needs clarification ---
if st.session_state["agent_question"]:
    st.warning("⚠️ The Market Analyst needs more information to proceed.")
    st.markdown(st.session_state["agent_question"])
    user_reply = st.text_input("Your clarification", key="clarification_reply")

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
                st.session_state["completed_deck"] = result["data"]
                st.session_state.pop("clarification_reply", None)
                st.rerun()
            elif result["status"] == "paused":
                st.session_state["agent_question"] = result["data"]
                st.rerun()
            elif result["status"] == "error":
                st.error(result.get("data", "Unknown error"))

# --- Initial ---
else:
    user_idea = st.text_input("Describe your startup idea:", key="user_idea")

    if st.button("Generate Pitch Deck"):
        if user_idea:
            with st.spinner("Agents are researching..."):
                result = run_startup_pipeline(user_idea)

            if result["status"] == "paused":
                st.session_state["agent_question"] = result["data"]
                st.session_state["pending_user_idea"] = user_idea
                st.rerun()
            elif result["status"] == "success":
                st.session_state["agent_question"] = None
                st.session_state["pending_user_idea"] = None
                st.session_state["completed_deck"] = result["data"]
                st.session_state.pop("user_idea", None)
                st.rerun()
            elif result["status"] == "error":
                st.error(result.get("data", "Unknown error"))
        else:
            st.warning("Please enter an idea first.")
