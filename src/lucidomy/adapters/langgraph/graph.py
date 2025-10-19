from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import add_messages
from langgraph.prebuilt import ToolExecutor

from src.lucidomy.adapters.langgraph.callbacks import CostLoggingCallbackHandler
from src.lucidomy.core.logic import send_email, update_database
from src.lucidomy.core.tools import SendEmail, UpdateDatabase


class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    requires_human_approval: bool
    tool_to_approve: dict | None


send_email_tool = tool(args_schema=SendEmail)(send_email)
update_database_tool = tool(args_schema=UpdateDatabase)(update_database)

tools = [send_email_tool, update_database_tool]
tool_executor = ToolExecutor(tools)

cost_callback = CostLoggingCallbackHandler()
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest")
llm_with_tools = llm.bind_tools(tools)


def call_model(state: AgentState):
    """
    Invokes the LLM with the current state's messages.

    Args:
        state: The current state of the agent, containing messages.

    Returns:
        A dictionary with the LLM's response message.
    """
    messages = state["messages"]
    response = llm_with_tools.invoke(messages, config={"callbacks": [cost_callback]})
    return {"messages": [response]}


def call_tool_node(state: AgentState):
    """
    Executes tool calls requested by the LLM.

    Args:
        state: The current state of the agent, containing messages with tool calls.

    Returns:
        A dictionary with the tool's output messages.
    """
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        tool_messages = tool_executor.invoke(last_message.tool_calls)
        return {"messages": tool_messages}
