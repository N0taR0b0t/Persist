import json
import os

# Define file paths
conversation_memory_file = "conversation_memory.json"
persistent_memory_file = "persistent_memory.json"

# Load conversation memory from the JSON file if it exists
def load_conversation_memory():
    try:
        with open(conversation_memory_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Save conversation memory to the JSON file
def save_conversation_memory(memory):
    with open(conversation_memory_file, "w") as f:
        json.dump(memory, f, indent=2)

# Load persistent memory
def load_persistent_memory():
    try:
        with open(persistent_memory_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Save persistent memory
def save_persistent_memory(memory):
    with open(persistent_memory_file, "w") as f:
        json.dump(memory, f, indent=2)

# Function to update the memory display with enhanced flashcard styling
def update_memory_display():
    persistent_memory = load_persistent_memory()
    # Create HTML cards for each memory entry with enhanced CSS
    cards_html = '''
    <div class="memory-container">
    '''
    if not persistent_memory:
        cards_html += '<p class="no-entries">No entries in persistent memory.</p>'
    else:
        for key, value in persistent_memory.items():
            cards_html += f'''
            <div class="memory-card">
                <strong>{key}</strong><br>
                {value}
            </div>
            '''
    cards_html += '</div>'
    return cards_html

# New Function: Calculate Token Count
def get_token_count():
    """
    Calculates the token count by taking the number of characters
    in the conversation_memory.json file and dividing by 5.
    """
    if not os.path.exists(conversation_memory_file):
        return 0
    try:
        with open(conversation_memory_file, "r") as f:
            content = f.read()
            char_count = len(content)
            token_count = char_count // 5  # Integer division
            return token_count
    except Exception as e:
        print(f"Error calculating token count: {e}")
        return 0