from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage
from langchain_core.tools import tool
from langgraph.graph import add_messages
from langgraph.prebuilt import ToolExecutor

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
