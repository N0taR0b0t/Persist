import json
import re
from typing import List
import openai
import gradio as gr
from ui_setup import get_custom_css
from chat_functions import chat_with_memory
from memory_management import (
    update_memory_display,
    load_conversation_memory,
    save_conversation_memory,
    load_persistent_memory,
    save_persistent_memory,
    get_token_count  # Import the new function
)

def create_app():
    # Load conversation history in 'messages' format
    history = load_conversation_memory()
    if not history:
        history = []

    # Ensure history is in the correct format (list of dicts with 'role' and 'content')
    def ensure_history_format(history):
        formatted_history = []
        for message in history:
            if isinstance(message, dict) and 'role' in message and 'content' in message:
                formatted_history.append(message)
            elif isinstance(message, list) or isinstance(message, tuple):
                # Convert from old list/tuple format to new dict format
                if len(message) == 2:
                    user_msg, assistant_msg = message
                    formatted_history.append({"role": "user", "content": user_msg})
                    formatted_history.append({"role": "assistant", "content": assistant_msg})
            else:
                # Skip or handle unexpected formats
                pass
        return formatted_history

    history = ensure_history_format(history)

    with gr.Blocks(css=get_custom_css()) as demo:
        gr.Markdown("""
        <h1 style='text-align: center; color: #6c757d;'>Persistent Memory Chatbot</h1>
        """)

        with gr.Row(equal_height=False, elem_id="main-layout"):
            # Sidebar for persistent memory display
            with gr.Column(scale=1, elem_classes="sidebar"):
                gr.Markdown("<h2 style='color: #6c757d;'>Persistent Memory</h2>")
                memory_display = gr.HTML(value=update_memory_display())
                clear_persistent_memory_button = gr.Button(
                    "Clear Persistent Memory",
                    elem_id="clear-persistent-memory-button",
                    variant="primary",
                    interactive=True
                )

                # Add model selection toggle
                gr.Markdown("<h3 style='color: #6c757d;'>Model Selection</h3>")
                model_selector = gr.Radio(
                    choices=["gpt-4o-mini", "gpt-4o"],
                    value="gpt-4o-mini",
                    label="Select Model",
                    interactive=True
                )

            # Chat interface with improved layout and style
            with gr.Column(scale=3, elem_classes="chat-interface"):
                gr.Markdown("<h2 style='color: #6c757d;'>Chat Interface</h2>")
                
                # New: Display Token Count
                token_display = gr.Markdown(
                    value=f"*Context Tokens: {get_token_count()}*",
                    elem_id="token-count-display"
                )
                
                chatbot = gr.Chatbot(value=history, elem_id="chatbot", type="messages")

                # Input and send button aligned vertically
                with gr.Column():
                    user_input = gr.Textbox(
                        label="Your Message",
                        placeholder="Type your message here...",
                        lines=3,
                        max_lines=10,
                        interactive=True,
                        elem_id="user-input-textbox",  # Changed elem_id
                        container=False,
                    )

                send_button = gr.Button("Send", elem_id="send-button", variant="primary")

                # Clear conversation button with confirmation
                with gr.Row(elem_id="clear-conversation-row"):
                    clear_memory_button = gr.Button(
                        "Clear Conversation",
                        elem_id="clear-conversation-button",
                        variant="secondary",
                        size="small"
                    )
                    confirm_clear_button = gr.Button(
                        "Confirm Clear",
                        elem_id="confirm-clear-button",
                        variant="secondary",
                        visible=False,
                        size="small"
                    )

        # Inject JavaScript to handle Enter for submit and Shift+Enter for newline
        gr.HTML("""
            <script>
                document.addEventListener("DOMContentLoaded", function() {
                    // Function to attach the Enter and Shift+Enter behaviors
                    function attachEnterBehavior() {
                        const textbox = document.querySelector('#user-input-textbox textarea');
                        const sendButton = document.querySelector('#send-button');

                        // Attach event listener if elements are found
                        if (textbox && sendButton) {
                            textbox.removeEventListener('keydown', handleEnterKey); // Prevent duplicate listeners
                            textbox.addEventListener('keydown', handleEnterKey);
                        }
                    }

                    // Define the Enter and Shift+Enter behavior
                    function handleEnterKey(e) {
                        if (e.key === 'Enter') {
                            if (e.shiftKey) {
                                // Shift+Enter: add newline, do nothing
                                e.stopPropagation();
                            } else {
                                // Enter: trigger send
                                e.preventDefault();
                                document.querySelector('#send-button').click();
                            }
                        }
                    }

                    // Set up a MutationObserver to reapply listeners if elements are re-rendered
                    const observer = new MutationObserver(attachEnterBehavior);
                    observer.observe(document.body, { childList: true, subtree: true });

                    // Initial call to attach behaviors
                    attachEnterBehavior();
                });
            </script>
        """)

        # Define the main function with persistent memory
        def gradio_chat(user_message, history, model):
            # Append the user's message to the history
            history.append({"role": "user", "content": user_message})

            # Generate the assistant's response using chat_with_memory
            assistant_reply, memory_html = chat_with_memory(user_message, history, model)

            # Append the assistant's message to the history
            history.append({"role": "assistant", "content": assistant_reply})

            # Save the conversation history in the correct format
            save_conversation_memory(history)

            # Calculate the new token count
            token_count = get_token_count()

            return history, memory_html, f"**Tokens in context window:** {token_count}", ""  # Clear the input textbox

        # Toggle visibility for clear conversation confirmation
        def toggle_clear_confirmation():
            return gr.update(visible=False), gr.update(visible=True)

        # Clear conversation memory functionality with confirmation
        def clear_conversation_memory():
            history = []
            save_conversation_memory(history)
            token_count = get_token_count()
            return history, update_memory_display(), f"**Tokens in context window:** {token_count}", gr.update(visible=False), gr.update(visible=False)

        # Clear persistent memory functionality
        def clear_persistent_memory():
            persistent_memory = {}
            save_persistent_memory(persistent_memory)
            memory_html = update_memory_display()
            token_count = get_token_count()
            return history, memory_html, f"**Tokens in context window:** {token_count}", ""

        # Link the input and output to Gradio functions
        send_button.click(
            gradio_chat,
            inputs=[user_input, chatbot, model_selector],
            outputs=[chatbot, memory_display, token_display, user_input]
        )
        user_input.submit(
            gradio_chat,
            inputs=[user_input, chatbot, model_selector],
            outputs=[chatbot, memory_display, token_display, user_input]
        )

        # Toggle visibility when clicking "Clear Conversation"
        clear_memory_button.click(
            toggle_clear_confirmation,
            inputs=None,
            outputs=[clear_memory_button, confirm_clear_button]
        )

        # Perform clearing action upon confirmation
        confirm_clear_button.click(
            clear_conversation_memory,
            inputs=None,
            outputs=[chatbot, memory_display, token_display, clear_memory_button, confirm_clear_button]
        )

        clear_persistent_memory_button.click(
            clear_persistent_memory,
            inputs=None,
            outputs=[chatbot, memory_display, token_display, user_input]
        )

    return demo