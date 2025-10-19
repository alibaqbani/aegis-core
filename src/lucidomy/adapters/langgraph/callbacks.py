from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import LLMResult

from src.lucidomy.core.instrumentation import (
    GEMINI_PRO_COST_PER_INPUT_TOKEN,
    GEMINI_PRO_COST_PER_OUTPUT_TOKEN,
)


class CostLoggingCallbackHandler(BaseCallbackHandler):
    def on_llm_end(self, response: LLMResult, **kwargs) -> None:
        """
        Logs the cost of an LLM call.
        """
        usage_metadata = response.llm_output["usage_metadata"]
        input_tokens = usage_metadata["prompt_token_count"]
        output_tokens = usage_metadata["candidates_token_count"]
        total_tokens = input_tokens + output_tokens

        input_cost = input_tokens * GEMINI_PRO_COST_PER_INPUT_TOKEN
        output_cost = output_tokens * GEMINI_PRO_COST_PER_OUTPUT_TOKEN
        total_cost = input_cost + output_cost

        print(
            f"[METRIC] LangGraph Call. Tokens: {total_tokens}. Cost: ${total_cost:.8f}"
        )
