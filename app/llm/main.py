import google.generativeai as genai
import os
import json
from dotenv import load_dotenv
from pydantic import BaseModel
from google.generativeai.types import GenerationConfig # Import GenerationConfig

# Your Pydantic model is now a "tool" for the AI
class ProConResponse(BaseModel):
    """
    A tool to structure the analysis of product reviews.
    """
    pros: list[str]
    cons: list[str]
    rating: float

# --- Setup ---
load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

class GeminiHandler():
    def __init__(self):
        # 1. Define the tool based on your Pydantic model
        self.analysis_tool = genai.protos.Tool(
            function_declarations=[
                genai.protos.FunctionDeclaration(
                    name="product_review_analysis",
                    description="Saves the pros, cons, and rating from a set of product reviews.",
                    # The model will use this schema for its parameters
                    parameters=genai.protos.Schema(
                        type=genai.protos.Type.OBJECT,
                        properties={
                            "pros": genai.protos.Schema(type=genai.protos.Type.ARRAY, items=genai.protos.Schema(type=genai.protos.Type.STRING)),
                            "cons": genai.protos.Schema(type=genai.protos.Type.ARRAY, items=genai.protos.Schema(type=genai.protos.Type.STRING)),
                            "rating": genai.protos.Schema(type=genai.protos.Type.NUMBER, format="float")
                        },
                        required=["pros", "cons", "rating"]
                    )
                )
            ]
        )
        
        # 2. Create the model instance
        self.gemini_model = genai.GenerativeModel("gemini-1.5-flash-latest")
        
    def _get_cluster_topic(self, reviews_sample: list, sentiment_type: str):
        """Uses Gemini to generate a short title for a cluster, with sentiment context."""

        # Dynamically set the connotation based on the sentiment type
        if sentiment_type == "pro":
            connotation = "positive feature (pro)"
        else:
            connotation = "negative issue (con)"

        prompt = (
                f"You are a product analyst summarizing customer feedback. The following reviews all discuss a common {connotation}. "
                f"Your task is to identify the specific product feature or attribute being described.\n\n"
                f"Summarize this feature into a concise, 2-4 word title. "
                f"Be specific. For example, instead of a generic title like 'Good Design', use a specific one like 'Stylish Color Options' or 'Comfortable Typing Feel'.\n\n"
                f"REVIEWS:\n{reviews_sample}"
            )
                
        try:
            response = self.gemini_model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error generating topic: {e}")
            return "General Feedback"
    def generate_final_report(self, pros_list, cons_list):
        final_prompt = (
            "You are a product analyst summarizing customer feedback. Based on the following key topics, "
            "write a final, clean summary report. Combine any redundant or very similar points. "
            "Present the result as a simple list of 'Top Pros' and 'Top Cons'.\n\n"
            f"Pros Topics: {pros_list}\n"
            f"Cons Topics: {cons_list}"
        )

        # Make a simple, final call to the LLM
        final_report = self.gemini_model.generate_content(final_prompt)
        return final_report.text

    def generate_pros_cons(self, reviews: list[str], product: str):
        # 3. Define the System Instruction and User Prompt
        system_instruction = (
            "You are an expert product review analyst. Your task is to analyze a list of user reviews for a product. "
            "Based on the reviews, call the `product_review_analysis` tool to save the common pros, cons, and estimated overall rating."
        )

        review_text = "\n".join(reviews)
        prompt = (
            f"Please analyze the following reviews for the product '{product}' and call the required tool:\n\n"
            f"--- REVIEWS ---\n{review_text}\n--- END REVIEWS ---"
        )
        
        try:
            # 4. Call the API with the tool
            response = self.gemini_model.generate_content(
                [system_instruction, prompt],
                tools=[self.analysis_tool] # Pass the tool to the API
            )
            
            # 5. Extract the arguments the model wants to pass to your "function"
            tool_call = response.candidates[0].content.parts[0].function_call
            if tool_call.name == "product_review_analysis":
                args = tool_call.args
                # Convert the model's arguments into a dictionary
                response_data = {
                    "pros": list(args.get("pros", [])),
                    "cons": list(args.get("cons", [])),
                    "rating": float(args.get("rating", 0.0))
                }
                # Validate with Pydantic
                validated_response = ProConResponse(**response_data)
                return validated_response
            else:
                return None

        except Exception as e:
            print(f"An error occurred: {e}")
            return None
