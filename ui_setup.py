def get_custom_css():
    return """
    /* Custom CSS for enhanced styling */

    html, body {
        height: 100%;
        margin: 0;
        padding: 0;
    }

    body {
        background-color: #1e1e1e;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #f5f5f5;
        display: flex;
        flex-direction: column;
    }

    /* Main container wrapping all components */
    #component-0 {
        flex: 1;
        display: flex;
        flex-direction: column;
    }

    /* Main layout containing sidebar and chat interface */
    #main-layout {
        flex: 1;
        display: flex;
        overflow: hidden;
    }

    /* Sidebar styles */
    .sidebar {
        max-width: 350px;
        background-color: #2e2e2e;
        padding: 20px;
        border-radius: 12px;
        overflow-y: auto;
    }

    /* Chat interface styles */
    .chat-interface {
        flex: 1;
        display: flex;
        flex-direction: column;
        padding: 10px;
        border-radius: 12px;
        overflow: hidden;
    }

    /* Chatbot styles */
    #chatbot {
        flex: 1;
        display: flex;
        flex-direction: column;
        background-color: #2e2e2e;
        border: none;
        border-radius: 8px;
        margin-bottom: 10px;
        overflow: hidden;
        /* Override inline height */
        height: auto !important;
        min-height: 0; /* For Flexbox to calculate height properly */
    }

    /* Bubble wrap containing messages */
    .bubble-wrap {
        flex: 1;
        overflow-y: auto;
        padding: 10px;
        display: flex;
        flex-direction: column;
    }

    /* Message wrap styles */
    .message-wrap {
        display: flex;
        flex-direction: column;
    }

    /* Individual message styles */
    .message-row {
        margin-bottom: 5px;
    }

    .message.user, .message.bot {
        padding: 10px;
        border-radius: 8px;
        background-color: #3a3a3a;
        color: #ffffff;
        font-size: 14px;
    }

    /* User input area */
    #user-input {
        margin-top: 10px;
    }

    #user-input textarea {
        width: 100%;
        padding: 10px;
        border: 1px solid #444;
        border-radius: 8px;
        background-color: #3a3a3a;
        color: #ffffff;
        font-size: 16px;
        resize: none;
    }

    /* Send button */
    #send-button {
        background-color: #ff5722;
        color: white;
        border: none;
        padding: 10px 18px;
        font-size: 16px;
        border-radius: 8px;
        cursor: pointer;
        transition: background-color 0.3s;
        margin-top: 5px;
    }

    #send-button:hover {
        background-color: #e64a19;
    }

    /* Clear buttons */
    .clear-buttons {
        background-color: #c0392b;
        color: white;
        border: none;
        padding: 10px 18px;
        font-size: 16px;
        border-radius: 8px;
        cursor: pointer;
        transition: background-color 0.3s;
        margin: 5px 2px;
    }

    .clear-buttons:hover {
        background-color: #b71c1c;
    }

    /* Token Count Display */
    #token-count-display {
        margin-bottom: 10px;
        font-size: 16px;
    }

    /* Adjustments for mobile view */
    @media (max-width: 768px) {
        .sidebar {
            max-width: 100%;
        }
        .chat-interface {
            max-width: 100%;
        }
    }
    """