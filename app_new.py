import streamlit as st
from g4f.client import Client

# All Text Models
TEXT_MODELS = [
    "gpt-3.5-turbo", "gpt-4", "gpt-4-turbo", "gpt-4o", "gpt-4o-mini", 
    "llama-2-7b", "llama-3.1-8b", "llama-3.1-70b", "llama-3.1-405b", 
    "llama-3.3-70b", "mixtral-7b", "mixtral-8x7b", "mistral-large", 
    "hermes-2-dpo", "hermes-2-pro", "gemini-flash", "gemini-pro", 
    "gemma-2b", "claude-3-haiku", "claude-3.5-sonnet", "blackboxai", 
    "blackboxai-pro", "command-r", "qwen-2.5-coder-32b", "qwq-32b", 
    "deepseek-chat", "deepseek-coder", "openchat-3.5", "openhermes-2.5", 
    "lfm-40b", "german-7b", "zephyr-7b", "neural-7b", "dbrx-instruct", 
    "evil", "turbo", "unity", "rtist"
]


# All Image Models
IMAGE_MODELS = [
    "sdxl", "sd-3", "playground-v2.5", "flux", "flux-pro", "flux-dev", 
    "flux-realism", "flux-cablyai", "flux-anime", "flux-3d", 
    "flux-disney", "flux-pixel", "flux-4o", "dall-e-3", 
    "midjourney", "any-dark"
]


# Supported Output Languages
OUTPUT_LANGUAGES = [
    "English", "Spanish", "French", "German", "Chinese", "Japanese", "Korean", "Hindi", "Arabic", "Portuguese", "Bengali"
]

# Streamlit App
st.title("AI Model Interaction App")
st.write("Choose the type of generation (text/image), model, and other options to interact.")

# Input fields for type and model selection
generation_type = st.selectbox("Select Generation Type", ["text", "image"])
model = st.selectbox("Select Model", TEXT_MODELS if generation_type == "text" else IMAGE_MODELS)

if generation_type == "text":
    output_language = st.selectbox("Select Output Language", OUTPUT_LANGUAGES, index=0)

# Input field for text or image prompt
user_input = st.text_area(f"Enter {'message' if generation_type == 'text' else 'prompt'}:", height=200)

if st.button("Generate"):
    if user_input.strip():
        try:
            client = Client()
            if generation_type == "text":
                # Append language instruction to the input
                user_input_with_language = f"Respond in {output_language}: {user_input}"
                response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": user_input_with_language}],
                    web_search=False
                )
                st.success(response.choices[0].message.content)
            elif generation_type == "image":
                response = client.images.generate(
                    model=model,
                    prompt=user_input,
                    response_format="url"
                )
                image_url = response.data[0].url
                st.markdown(f"[Generated Image URL]({image_url})")
                st.image(image_url, caption="Generated Image")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning(f"Please enter a {'message' if generation_type == 'text' else 'prompt'} before generating.")
