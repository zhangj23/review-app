from google import genai
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from google.genai import types

class ProConResponse(BaseModel):
    pros: list[str]
    cons: list[str]
    rating: float
    
load_dotenv()
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

response = client.models.generate_content(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
        system_instruction=f"You are reviewing a product and are figuring out the pros and cons of whether to buy a product titled"),
    contents="Given these reviews ",
    config={
        "response_mime_type": "application/json",
        "response_schema": ProConResponse,
    },
)

print(response.text)