import gradio as gr
from langchain.memory import FileChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
import os
from llm_config import get_llm
from typing import List, Tuple
import json
import uuid
from datetime import datetime

# Initialize the LLM
llm = get_llm(temperature=0.7)

# Create a directory for storing chat histories if it doesn't exist
CHAT_HISTORY_DIR = "chat_histories"
os.makedirs(CHAT_HISTORY_DIR, exist_ok=True)

def save_chat_history(session_id: str, history: List[Tuple[str, str]]):
    """Save chat history to a JSON file."""
    history_file = os.path.join(CHAT_HISTORY_DIR, f"{session_id}.json")
    chat_data = {
        "session_id": session_id,
        "last_updated": datetime.now().isoformat(),
        "messages": [
            {
                "human": msg[0],
                "assistant": msg[1],
                "timestamp": datetime.now().isoformat()
            }
            for msg in history
        ]
    }
    
    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump(chat_data, f, indent=2, ensure_ascii=False)

def load_chat_history(session_id: str) -> List[Tuple[str, str]]:
    """Load chat history from a JSON file."""
    history_file = os.path.join(CHAT_HISTORY_DIR, f"{session_id}.json")
    if os.path.exists(history_file):
        with open(history_file, 'r', encoding='utf-8') as f:
            chat_data = json.load(f)
            return [(msg["human"], msg["assistant"]) for msg in chat_data["messages"]]
    return []

def list_chat_sessions() -> List[dict]:
    """List all available chat sessions."""
    sessions = []
    for filename in os.listdir(CHAT_HISTORY_DIR):
        if filename.endswith('.json'):
            with open(os.path.join(CHAT_HISTORY_DIR, filename), 'r', encoding='utf-8') as f:
                chat_data = json.load(f)
                sessions.append({
                    "session_id": chat_data["session_id"],
                    "last_updated": chat_data["last_updated"],
                    "message_count": len(chat_data["messages"])
                })
    return sorted(sessions, key=lambda x: x["last_updated"], reverse=True)

def chat(message: str, history: List[Tuple[str, str]], session_id: str) -> Tuple[str, List[Tuple[str, str]]]:
    """Main chat function."""
    try:
        # Convert history to LangChain format for context
        messages = []
        for human_msg, ai_msg in history:
            messages.append(HumanMessage(content=human_msg))
            messages.append(AIMessage(content=ai_msg))
        
        # Add current message
        messages.append(HumanMessage(content=message))
        
        # Get response from LLM
        response = llm.invoke(messages)
        
        # Update history
        history.append((message, response.content))
        
        # Save chat history
        save_chat_history(session_id, history)
        
        return response.content, history
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        history.append((message, error_message))
        save_chat_history(session_id, history)
        return error_message, history

def create_gradio_interface():
    # Generate a unique session ID
    session_id = str(uuid.uuid4())
    
    with gr.Blocks(css="""
        .container {display: flex; height: 100vh;}
        .sidebar {width: 260px; height: 100%; border-right: 1px solid rgba(0,0,0,0.1); padding: 1rem;}
        .main-content {flex-grow: 1; height: 100%; display: flex; flex-direction: column;}
        .chat-container {flex-grow: 1; overflow-y: auto; padding: 2rem;}
        .input-container {padding: 2rem; border-top: 1px solid rgba(0,0,0,0.1);}
        .history-button {margin-bottom: 0.5rem; text-align: left; padding: 0.5rem; border-radius: 0.5rem;}
        .history-button:hover {background-color: rgba(0,0,0,0.1);}
        #component-0 {height: 100%;}
    """) as demo:
        with gr.Row(elem_classes="container"):
            # Sidebar
            with gr.Column(elem_classes="sidebar"):
                gr.Markdown("### Chat History")
                new_chat = gr.Button("+ New Chat", variant="primary")
                session_list = gr.Dropdown(
                    label="Previous Sessions",
                    choices=[s["session_id"] for s in list_chat_sessions()],
                    value=session_id,
                    visible=False  # Hide the dropdown, we'll use buttons instead
                )
                chat_history_container = gr.Column()  # Container for chat history buttons
                refresh_sessions = gr.Button("Refresh", size="sm")

            # Main Content
            with gr.Column(elem_classes="main-content"):
                with gr.Column(elem_classes="chat-container"):
                    chatbot = gr.Chatbot(height="100%", elem_classes="chatbot")
                
                with gr.Column(elem_classes="input-container"):
                    msg = gr.Textbox(
                        label="",
                        placeholder="Type your message here...",
                        lines=2
                    )
                    with gr.Row():
                        clear = gr.Button("Clear Chat", size="sm")
                        submit = gr.Button("Send", variant="primary")

        state = gr.State([])  # For storing chat history
        session_state = gr.State(session_id)  # For storing session ID

        def update_chat_history_buttons():
            sessions = list_chat_sessions()
            buttons_html = ""
            for session in sessions:
                # Format the timestamp
                timestamp = datetime.fromisoformat(session["last_updated"]).strftime("%Y-%m-%d %H:%M")
                buttons_html += f"""<button class='history-button'>{timestamp}<br>Messages: {session["message_count"]}</button>"""
            return gr.HTML(buttons_html)

        def respond(message, history, session_id):
            if not message:
                return "", history
            bot_message, new_history = chat(message, history, session_id)
            return "", new_history

        def clear_chat():
            return [], []

        def load_session(session_id):
            history = load_chat_history(session_id)
            return history, session_id

        def create_new_chat():
            new_session_id = str(uuid.uuid4())
            return [], new_session_id, update_chat_history_buttons()

        # Event handlers
        msg.submit(respond, [msg, state, session_state], [msg, chatbot])
        submit.click(respond, [msg, state, session_state], [msg, chatbot])
        clear.click(clear_chat, None, [msg, chatbot], queue=False)
        session_list.change(load_session, [session_list], [chatbot, session_state])
        refresh_sessions.click(update_chat_history_buttons, None, [chat_history_container])
        new_chat.click(create_new_chat, None, [chatbot, session_state, chat_history_container])

        # Initialize chat history buttons
        demo.load(update_chat_history_buttons, None, [chat_history_container])

    return demo

if __name__ == "__main__":
    demo = create_gradio_interface()
    demo.launch(share=False) 
    
