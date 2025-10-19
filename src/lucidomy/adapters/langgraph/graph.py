from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages


class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    requires_human_approval: bool
    tool_to_approve: dict | None
