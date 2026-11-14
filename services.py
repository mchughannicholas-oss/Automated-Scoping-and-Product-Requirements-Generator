from google import genai
from google.genai import types
from schemas import ProductRequirementsDocument

def generate_prd(api_key: str, raw_input_text: str) -> ProductRequirementsDocument:
    """Initializes the GenAI client and generates a structured PRD without reasoning stalls."""
    if not api_key or not api_key.strip():
        raise ValueError("A valid API key is required to initialize the GenAI client.")

    try:
        client = genai.Client(
            api_key=api_key.strip(),
            http_options=types.HttpOptions(timeout=90000)  # 90 seconds in ms
        )

        system_instruction = (
            "You are an expert Principal Technical Product Manager. "
            "Analyze the user's input and convert it into a concise, actionable "
            "Product Requirements Document (PRD) matching the required schema."
        )

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=raw_input_text,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                response_schema=ProductRequirementsDocument,
                temperature=0.2,
                # Disable extended thinking so structured JSON generation starts immediately
                thinking_config=types.ThinkingConfig(thinking_budget=0),
            ),
        )

        if not response.parsed:
            raise ValueError("The model returned an empty parsed response structure.")

        return response.parsed

    except Exception as e:
        raise RuntimeError(f"Gemini API generation failed: {str(e)}")