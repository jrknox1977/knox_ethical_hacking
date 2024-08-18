
import os
from dotenv import load_dotenv
from openai import OpenAI
from groq import Groq
import anthropic
import google.generativeai as genai
load_dotenv()

# Pip command to install requirements:
# pip install python-dotenv openai groq anthropic google-generativeai

# -----( OPENAI )-----------------------------------------------

def generate_openai_response(
        model="gpt-4o", 
        system_role="You are a helpful assistant", 
        user_prompt="How are you today? Please introduce yourself.", 
        temperature=1, 
        max_tokens=1000, 
        top_p=1, 
        frequency_penalty=0, 
        presence_penalty=0,
        messages=None
        ):
    
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    if messages is None:
        messages = [
            {"role": "system", "content": system_role},
            {"role": "user", "content": user_prompt}
        ]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty
    )
    return response.choices[0].message.content

# -----( GROQ )-----------------------------------------------

def generate_groq_response(
        model="llama-3.1-70b-versatile", 
        system_role="You are a helpful assistant", 
        user_prompt="How are you today? Please introduce yourself.", 
        temperature=0.7, 
        max_tokens=1000,
        messages=None
        ):
    
    client = Groq(
        api_key=os.getenv("GROQ_API_KEY"),
    )
    
    if messages is None:
        messages = [
            {"role": "system", "content": system_role},
            {"role": "user", "content": user_prompt}
        ]
    
    chat_completion = client.chat.completions.create(
        messages=messages,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return chat_completion.choices[0].message.content

# -----( GEMINI )-----------------------------------------------

def generate_gemini_response(
        model="gemini-1.5-pro", 
        system_role="You are a helpful assistant", 
        user_prompt="How are you today? Please introduce yourself.", 
        temperature=0.7, 
        max_tokens=1000
        ):
    
    import google.generativeai as genai
    
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    
    model = genai.GenerativeModel(model)
    
    prompt_parts = [
        system_role,
        user_prompt
    ]
    
    response = model.generate_content(
        prompt_parts,
        generation_config=genai.types.GenerationConfig(
            max_output_tokens=max_tokens,
            temperature=temperature
        )
    )

    return response.text
    
# -----( ANTHROPIC )-----------------------------------------------

def generate_anthropic_response(
        model="claude-3-sonnet-20240229", 
        system_role="You are a helpful assistant", 
        user_prompt="How are you today? Please introduce yourself.", 
        temperature=0.7, 
        max_tokens=1000,
        messages=None
        ):
    
    client = anthropic.Anthropic(
        api_key=os.getenv("ANTHROPIC_API_KEY"),
    )

    if messages is None:
        messages = [
            {"role": "user", "content": user_prompt}
        ]

    message = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        system=system_role,
        messages=messages
    )

    return message.content[0].text

if __name__ == "__main__":
    # print("\n")
    # print("-" * 80)
    # response = generate_openai_response()
    # print(response)
    # print("-" * 80)
    # response = generate_groq_response()
    # print(response)
    # print("-" * 80)
    # response = generate_anthropic_response()
    # print(response)
    # print("-" * 80)
    response = generate_gemini_response()
    print(response)
    print("-" * 80)