import json

def read_json_and_print(file_path):
    with open(file_path, 'r') as json_file:
        conversation = json.load(json_file)
        user_messages = []
        assistant_messages = []

        for message in conversation:
            role = message.get('role')
            content = message.get('content')

            if role == "user":
                user_messages.append({"role": role, "content": content})
            elif role == "assistant":
                assistant_messages.append({"role": role, "content": content})

        while user_messages or assistant_messages:
            if user_messages:
                user_msg = user_messages.pop(0)
                print(f"Role: {user_msg['role']}")
                print(f"Content: {user_msg['content']}\n")

            if assistant_messages:
                assistant_msg = assistant_messages.pop(0)
                print(f"Role: {assistant_msg['role']}")
                print(f"Content: {assistant_msg['content']}\n")

file_path = "data/messages_self_2024-03-10_81352289.json"
read_json_and_print(file_path)
