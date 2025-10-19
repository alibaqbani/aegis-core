import os

import google.generativeai as genai
from dotenv import load_dotenv

# Gemini 1.5 Pro cost per token
GEMINI_PRO_COST_PER_INPUT_TOKEN = 0.0000035
GEMINI_PRO_COST_PER_OUTPUT_TOKEN = 0.0000105


def get_instrumented_client():
    """
    Initializes and returns an instrumented generative AI client.

    This function loads the Google API key from environment variables,
    configures the generative AI client, and returns a generative model
    instance.

    Returns:
        genai.GenerativeModel: An instance of the generative model.
    """
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables.")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-1.5-pro-latest")


def generate_content_with_cost_logging(model, prompt):
    """
    Generates content using the provided model and logs the cost.

    This function sends a prompt to the generative model, calculates the
    cost of the API call based on token usage, logs the cost, and returns
    the model's response.

    Args:
        model: An instance of the generative model.
        prompt (str): The prompt to send to the model.

    Returns:
        The response from the generative model.
    """
    response = model.generate_content(prompt)
    input_tokens = response.usage_metadata.prompt_token_count
    output_tokens = response.usage_metadata.candidates_token_count
    total_tokens = response.usage_metadata.total_token_count

    input_cost = input_tokens * GEMINI_PRO_COST_PER_INPUT_TOKEN
    output_cost = output_tokens * GEMINI_PRO_COST_PER_OUTPUT_TOKEN
    total_cost = input_cost + output_cost

    print(
        f"[METRIC] LLM Call complete. Tokens: {total_tokens}. Cost: ${total_cost:.8f}"
    )
    return response
