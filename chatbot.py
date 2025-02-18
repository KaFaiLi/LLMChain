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
        
        # Get response from LLM
        response = llm.invoke({
            "input": message,
            "chat_history": messages
        })
        
        # Update history
        history.append((message, response["output"]))
        
        # Save chat history
        save_chat_history(session_id, history)
        
        return response["output"], history
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        history.append((message, error_message))
        save_chat_history(session_id, history)
        return error_message, history

def create_gradio_interface():
    # Generate a unique session ID
    session_id = str(uuid.uuid4())
    
    with gr.Blocks() as demo:
        gr.Markdown("# Chat Interface")
        
        with gr.Row():
            with gr.Column(scale=3):
                chatbot = gr.Chatbot(height=600)
                msg = gr.Textbox(label="Message", placeholder="Type your message here...")
                with gr.Row():
                    submit = gr.Button("Send")
                    clear = gr.Button("Clear")
            
            with gr.Column(scale=1):
                session_list = gr.Dropdown(
                    label="Previous Sessions",
                    choices=[s["session_id"] for s in list_chat_sessions()],
                    value=session_id
                )
                refresh_sessions = gr.Button("Refresh Sessions")
        
        state = gr.State([])  # For storing chat history
        session_state = gr.State(session_id)  # For storing session ID
        
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
        
        def refresh_session_list():
            sessions = list_chat_sessions()
            return gr.Dropdown(choices=[s["session_id"] for s in sessions])
        
        # Event handlers
        msg.submit(respond, [msg, state, session_state], [msg, chatbot])
        submit.click(respond, [msg, state, session_state], [msg, chatbot])
        clear.click(clear_chat, None, [msg, chatbot], queue=False)
        session_list.change(load_session, [session_list], [chatbot, session_state])
        refresh_sessions.click(refresh_session_list, None, [session_list])
    
    return demo

if __name__ == "__main__":
    demo = create_gradio_interface()
    demo.launch(share=False) 