# ai.py
import ollama

def get_fast_study_buddy_stream(messages):
    """
    Streams the response from Ollama token-by-token for maximum speed.
    """
    model_name = 'qwen2.5:3b' 
    
    system_prompt = {
        'role': 'system',
        'content': (
            "You are a warm, kind, and incredibly patient best friend who happens to "
            "be an expert in all academic studies, school subjects, and learning techniques. "
            "Your goal is to make the user feel supported, smart, and less stressed. "
            "Respond instantly, break down complex study topics into simple, encouraging terms, "
            "and always maintain a friendly, warm, peer-to-peer tone. Keep answers concise so you are fast."
        )
    }
    
    if not messages or messages[0].get('role') != 'system':
        messages.insert(0, system_prompt)
        
    try:
        # Enable streaming mode for instant responses
        response_stream = ollama.chat(model=model_name, messages=messages, stream=True)
        for chunk in response_stream:
            yield chunk['message']['content']
    except Exception as e:
        yield f"Oh no, I ran into a small error! Let's try again. Error: {e}"
