from google import genai
from google.genai import types
from schemas import ProductRequirementsDocument

def generate_prd(api_key: str, raw_input_text: str) -> ProductRequirementsDocument:
    """Initializes the GenAI client with a safety timeout and returns a parsed PRD."""
    try:
        # Pass http_options with a timeout (e.g., 30 seconds) to prevent infinite hanging
        client = genai.Client(
            api_key=api_key,
            http_options=types.HttpOptions(timeout=60000) # timeout in milliseconds (30 seconds)
        )

        system_instruction = (
            "You are an expert Principal Technical Product Manager. "
            "Your job is to analyze raw, unstructured user input and convert it into a "
            "thorough, professional Product Requirements Document (PRD) matching the required schema."
        )

        response = client.models.generate_content(
            model='gemini-3.8-flash',
            contents=raw_input_text,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                response_schema=ProductRequirementsDocument,
                temperature=0.2,
            ),
        )
        
        return response.parsed
        
    except Exception as e:
        # Raise a clean exception that main.py can catch immediately
        raise RuntimeError(f"Gemini API generation failed: {str(e)}")