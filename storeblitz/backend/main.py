from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load small models locally
generator = pipeline("text2text-generation", model="google/flan-t5-small")

translators = {
    "hindi": pipeline("translation", model="Helsinki-NLP/opus-mt-en-hi"),
    "tamil": pipeline("translation", model="Helsinki-NLP/opus-mt-en-ta"),
    "bengali": pipeline("translation", model="Helsinki-NLP/opus-mt-en-bn"),
    "marathi": pipeline("translation", model="Helsinki-NLP/opus-mt-en-mr"),
}

class ContentRequest(BaseModel):
    business_name: str
    category: str
    content_type: str
    language: str
    detail: str

@app.post("/generate")
async def generate_content(data: ContentRequest):
    # Step 1: Generate marketing content in English
    prompt = (
        f"Write a short and engaging {data.content_type} in English "
        f"for a business called '{data.business_name}' in the {data.category} industry. "
        f"Include this detail: '{data.detail}'. "
        f"Make it persuasive and suitable for Indian audiences."
    )
    gen_output = generator(prompt, max_length=80, num_return_sequences=1)
    english_text = gen_output[0]["generated_text"].strip()

    # Step 2: Translate if needed
    lang = data.language.lower()
    if lang in translators:
        translated = translators[lang](english_text, max_length=80)
        final_text = translated[0]["translation_text"].strip()
    else:
        final_text = english_text  # default English if no translator

    return {"content": final_text}
