import json
import re
from typing import List
import openai
from memory_management import (
    load_persistent_memory,
    save_persistent_memory,
    update_memory_display
)

def chat_with_memory(user_input: str, history: List[dict], model: str) -> (str, str):
    # Load persistent memory
    persistent_memory = load_persistent_memory()

    # Prepare conversation history for the model
    conversation = [
        {"role": "system", "content": f"""
You are an assistant with the ability to manipulate a persistent memory system. You can create, update, and delete entries in the persistent memory. The persistent memory is a dictionary of key-value pairs.

When you want to manipulate the memory, you should output commands in the following JSON format on a single line:

<BEGIN COMMANDS>
{{
    "commands": [
        {{
            "action": "add",
            "key": "some key",
            "value": "some value"
        }},
        {{
            "action": "update",
            "key": "some key",
            "value": "new value"
        }},
        {{
            "action": "delete",
            "key": "some key"
        }}
    ]
}}
<END COMMANDS>

After the commands, continue your response to the user as usual. Do not mention the commands in your user-facing text.

Current persistent memory entries:

{json.dumps(persistent_memory, indent=2)}
"""}
    ]

    # Add conversation history
    conversation.extend(history)

    # Append the user's latest input
    conversation.append({"role": "user", "content": user_input})

    # Call OpenAI API
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=conversation
        )
        assistant_reply = response.choices[0].message['content']
    except Exception as e:
        assistant_reply = f"Sorry, I encountered an error: {str(e)}"
        return assistant_reply, update_memory_display()

    # Extract and process commands from the assistant's reply
    # We'll look for JSON between <BEGIN COMMANDS> and <END COMMANDS>
    command_pattern = r"<BEGIN COMMANDS>(.*?)<END COMMANDS>"
    match = re.search(command_pattern, assistant_reply, re.DOTALL)
    if match:
        commands_json = match.group(1).strip()
        try:
            commands_data = json.loads(commands_json)
            commands = commands_data.get("commands", [])
            for command in commands:
                action = command.get("action")
                key = command.get("key")
                value = command.get("value", "")
                if action == "add" or action == "update":
                    # Add or update the entry
                    persistent_memory[key] = value
                elif action == "delete":
                    # Delete the entry with the given key
                    persistent_memory.pop(key, None)
            # Save the updated persistent memory
            save_persistent_memory(persistent_memory)
        except json.JSONDecodeError:
            assistant_reply += "\n\n[Error processing commands: Invalid JSON.]"
        except Exception as e:
            assistant_reply += f"\n\n[Error processing commands: {str(e)}]"
        # Remove the commands from the assistant's reply
        assistant_reply = re.sub(command_pattern, '', assistant_reply, flags=re.DOTALL).strip()

    # Return assistant reply and persistent memory for display
    memory_html = update_memory_display()
    return assistant_reply, memory_html