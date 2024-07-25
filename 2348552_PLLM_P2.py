import os
from groq import Groq

api_key = "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"
client = Groq(api_key=api_key)


def get_chat_response(client, messages):
    chat_completion = client.chat.completions.create(
        messages=messages,
        model="llama3-8b-8192", 
        temperature=1, 
        max_tokens=2048, 
        top_p=1, 
        stop=None,
    )
    return chat_completion.choices[0].message.content


def chatbot():
    print("Welcome to the chatbot! Type 'exit' to end the conversation.")
    messages = []
    memory = {}
    
    while True:
        user_message = input("You: ")
        if user_message.lower() == 'exit': 
            print("Goodbye!")
            break
        
        
        messages.append({"role": "user", "content": user_message})
        
        
        if "my name is" in user_message.lower():
            name = user_message.split("my name is")[-1].strip()
            memory["name"] = name # storing the users name in the memory
            response = f"Nice to meet you, {name}!"
        
        
        elif "remember" in user_message.lower():
            key_value = user_message.split("remember")[-1].strip().split(" as ")
            if len(key_value) == 2:
                key, value = key_value
                memory[key.strip()] = value.strip()
                response = f"Got it! I'll remember that {key.strip()} is {value.strip()}."
            else:
                response = "I didn't quite catch that. Could you please clarify?"
            
        
        elif "what is" in user_message.lower() and any(mem_key in user_message.lower() for mem_key in memory):
            mem_key = next(mem_key for mem_key in memory if mem_key in user_message.lower())
            response = f"{mem_key} is {memory[mem_key]}."
        else:
            try:
                # Get chatbot response
                response = get_chat_response(client, messages)
                messages.append({"role": "assistant", "content": response})
            except Exception as e:
                response = f"An error occurred: {str(e)}"
        
        print("Bot:", response)

if __name__ == "__main__":
    chatbot()
