from google import genai
from google.genai import types
from schemas import ProductRequirementsDocument

def generate_prd(api_key: str, raw_input_text: str) -> ProductRequirementsDocument:
    """Initializes the GenAI client with a valid key and safety timeout."""
    if not api_key or not api_key.strip():
        raise ValueError("A valid API key is required to initialize the GenAI client.")

    try:
        # Initialize client explicitly with the provided key
        client = genai.Client(
            api_key=api_key.strip(),
            http_options=types.HttpOptions(timeout=60000) # 60 second timeout
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
        raise RuntimeError(f"Gemini API generation failed: {str(e)}")