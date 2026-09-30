"""
Module 6 Project — AI Dashboard  (STARTER)
==========================================
Run with:
    # Start the backend (when ready):
    uvicorn backend:app --reload --port 8000

    # Start the Streamlit app:
    streamlit run app.py

Your goal: build a full Streamlit dashboard with authentication,
task management, data visualisation, and an AI chat feature.

Required sections (each marked with TODO):
    1. Authentication — login form, JWT in session state, logout
    2. Dashboard view — metrics, task list, chart
    3. Data interaction — add task form, complete task buttons
    4. AI chat feature — chat history, mock responses, streaming
    5. Layout — sidebar, tabs, metrics, error messages

Import the API functions from api_client.py (not requests directly).
Use mock_data.py to test the UI while the backend is being built.
"""

import streamlit as st
from mock_data import MOCK_TASKS, MOCK_STATS, MOCK_USER, MOCK_TOKEN
import api_client 
from api_client import login
import time

# ── Step 1: Page configuration ─────────────────────────────────────────────
# TODO: 
st.set_page_config(
    layout="wide", 
    page_title="AI Dashboard", 
    page_icon="🤖")

# ── Step 2: Session state initialisation ───────────────────────────────────
# TODO: Initialise all session state keys you will need:
#   "token"    → None
#   "username" → None
#   "messages" → []    (chat history)
#   "use_mock" → False (toggle to use mock data instead of the real API)

if "token" not in st.session_state:
    st.session_state["token"] = None

if "username" not in st.session_state:
    st.session_state["username"] = None

if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "use_mock" not in st.session_state:
    st.session_state["use_mock"] = False

if "api_key" not in st.session_state:
    st.session_state["api_key"] = ""

# ════════════════════════════════════════════════════════════════════════════
# SECTION A — AUTHENTICATION
# ════════════════════════════════════════════════════════════════════════════
# TODO: Auth gate — if no token, show login form and st.stop()

# Login form should:
#   - Have username + password fields
#   - Have a "Use Mock Data" checkbox (sets token = MOCK_TOKEN, username = MOCK_USER)
#   - On real login: call api_client.login(username, password)
#   - Store token + username in session state on success
#   - Show st.error on failure
#   - Call st.rerun() after successful login

if not st.session_state["token"]:

    st.title("🤖 AI Dashboard")
    st.subheader("Login")

    use_mock = st.checkbox("Use Mock Data")
    st.session_state["use_mock"] = use_mock

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if use_mock:
            st.session_state["token"] = MOCK_TOKEN
            st.session_state["username"] = MOCK_USER
            st.session_state["use_mock"] = False
            st.rerun()

        else:
            #api login
            #response = api_client.login(username, password)
            access_token, error = login(username, password)

            if access_token:
                st.session_state["token"] = access_token
                st.session_state["username"] = username
                st.session_state["use_mock"] = False
                st.rerun()
          
                

            else:
                st.error()

    st.stop()
 
#════════════════════════════════════════════════════════════════════════════
# SECTION B — SIDEBAR
# ════════════════════════════════════════════════════════════════════════════
# TODO: with st.sidebar:
#   - App title and divider
#   - "Logged in as [username]"
#   - Logout button (clear token/username, st.rerun())
#   - AI Chat settings (API key input, system prompt)
#   - Divider and caption
with st.sidebar:
    st.title("🤖 AI Dashboard")
    st.divider()

    # Show logged-in user
    st.write(f"Logged in as **{st.session_state['username']}**")

    # Logout button
    if st.button("Logout"):
        st.session_state["token"] = None
        st.session_state["username"] = None
        st.session_state["messages"] = []
        st.rerun()

    st.divider()

    # AI Chat settings
    st.subheader("🤖 AI Chat Settings")

    #api_key = st.text_input(
    st.session_state["api_key"] = st.text_input(
        "OpenAI API key",
        type="password",
        placeholder="sk-...(optional)"
    )

    system_prompt = st.text_area(
        "System prompt",
        value="You are a helpful AI assistant.",
        height=100
    )

    st.divider()

    st.caption("AI Dashboard • Module 6")

st.title("Welcome to the AI Dashboard!")

st.write(
    f"Hello, {st.session_state['username']}! "
    "You are successfully logged in."
)
# ════════════════════════════════════════════════════════════════════════════
# SECTION C — MAIN CONTENT (tabs)
# ════════════════════════════════════════════════════════════════════════════
# TODO: Create 3 tabs: "📊 Dashboard", "✅ Tasks", "🤖 AI Chat"
# tab_dash, tab_tasks, tab_chat = st.tabs(["📊 Dashboard", "✅ Tasks", "🤖 AI Chat"])

# ── TAB 1: Dashboard 
tab_dash, tab_tasks, tab_chat = st.tabs(
    ["📊 Dashboard", "✅ Tasks", "🤖 AI Chat"]
)
# ──────────────────────────────────────────────────────
# TODO: with tab_dash:
#   - Load tasks (or use MOCK_TASKS if in mock mode)
#   - Show 3 st.metric() in 3 columns: total, done, pending
#   - Show st.dataframe() with task data
#   - Show a bar chart of done vs pending

with tab_dash:
    st.header("📊 Dashboard")
    if st.session_state["use_mock"]:
        tasks = MOCK_TASKS
    else:
        tasks, error = api_client.get_tasks(
            st.session_state["token"])
        
        if error:
            st.error(error)
            tasks = []

    #if tasks is None:
        #st.error("Could not load tasks from the API.")
        #tasks = []

    total = len(tasks)
    done = sum(1 for task in tasks if task["done"])
    pending = total - done

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Tasks", total)

    with col2:
        st.metric("Completed", done)

    with col3:
        st.metric("Pending", pending)

    st.subheader("My Tasks")

    st.dataframe(
        tasks,
        width="stretch"
    )

    # Show bar chart
    st.subheader("Task Status")

    chart_data = {
        "Status": ["Completed", "Pending"],
        "Count": [done, pending]
    }

    st.bar_chart(
        chart_data,
        x="Status",
        y="Count"
    )
# ── TAB 2: Tasks ──────────────────────────────────────────────────────────
# TODO: with tab_tasks:
#   - Add task form (POST to API or append to mock data)
#   - Task list with Complete buttons (PATCH to API or update mock)
#   - Error handling for API failures

# ── TAB 2: Tasks ────────────────────────────────────────────────────

with tab_tasks:
    st.header("✅ Tasks")

    # Add a new task
    st.subheader("Add a New Task")

    with st.form("add_task_form"):
        title = st.text_input("Task title")
        description = st.text_area("Description")

        submitted = st.form_submit_button("Add Task")

        if submitted:
            if not title.strip():
                st.error("Please enter a task title.")
            else:
                try:
                    if st.session_state["use_mock"]:
                        # Add task to mock data
                        new_task = {
                            "id": len(MOCK_TASKS) + 1,
                            "title": title,
                            "done": False,
                            "created_at": "2026-09-28"
                        }

                        MOCK_TASKS.append(new_task)

                        st.success("Task added successfully!")
                        st.rerun()

                    else:
                        # Add task to real API
                        new_task, error = api_client.create_task(
                            st.session_state["token"],
                            title
                        )

                        if new_task:
                            st.success("Task added successfully!")
                            st.rerun()
                        else:
                            st.error(error)

                except Exception as e:
                    st.error(f"Could not add task: {e}")

    st.divider()

    # Show existing tasks
    st.subheader("My Tasks")

    try:
        if st.session_state["use_mock"]:
            tasks = MOCK_TASKS
        else:
            tasks, error = api_client.get_tasks(
                st.session_state["token"]
            )

            if error:
                st.error(error)
                tasks = []

        # Display each task
        for task in tasks:
            col1, col2 = st.columns([5, 1])

            with col1:
                status = "✅ Completed" if task["done"] else "⏳ Pending"

                st.write(f"**{task['title']}**")
                st.caption(status)

            with col2:
                if not task["done"]:
                    if st.button(
                        "Complete",
                        key=f"complete_{task['id']}"
                    ):
                        try:
                            if st.session_state["use_mock"]:
                                # Update mock task
                                task["done"] = True

                                st.success("Task completed!")
                                st.rerun()

                            else:
                                # Update task through API
                                updated_task, error = api_client.complete_task(
                                    st.session_state["token"],
                                    task["id"]
                                )
                                

                                if updated_task:
                                    st.success("Task completed!")
                                    st.rerun()
                                else:
                                    st.error(error)
                                        
                             
                        except Exception as e:
                            st.error(f"Could not complete task: {e}")

    except Exception as e:
        st.error(f"Could not load tasks: {e}")

    
# ── TAB 3: AI Chat ────────────────────────────────────────────────────────
# TODO: with tab_chat:
#   - Render chat history (st.chat_message for each message)
#   - st.chat_input for user messages
#   - Mock response generator or real OpenAI call
#   - st.write_stream for streaming display
#   - Append both user and assistant messages to session state

# ── TAB 3: AI Chat ─────────────────────────────────────────────────

with tab_chat:
    st.header("🤖 AI Chat")

    # Render previous chat messages
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask me anything..."):

        # Add user's message to session state
        st.session_state["messages"].append(
            {
                "role": "user",
                "content": prompt
            }
        )

        # Display user's message
        with st.chat_message("user"):
            st.write(prompt)

        # Generate AI response
        if st.session_state["use_mock"]:

            def mock_response():
                response = (
                    "This is a mock AI response. "
                    "In the real version, your message will be "
                    "sent to an AI service."
                )

                for word in response.split():
                    yield word + " "

            # Display streaming response
            with st.chat_message("assistant"):
                response = st.write_stream(mock_response())

        else:
            # Real AI response
            try:
                with st.chat_message("assistant"):
                    response = api_client.get_ai_response(
                        st.session_state["token"],
                        prompt
                    )

                    st.write(response)

            except Exception as e:
                st.error(f"AI request failed: {e}")
                response = "Sorry, I couldn't get an AI response."

        # Save assistant response
        st.session_state["messages"].append(
            {
                "role": "assistant",
                "content": response
            }
        )