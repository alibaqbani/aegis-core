"""
Core schemas for tools.

This module defines the framework-agnostic data structures for tools
that can be used by any adapter.
"""

from pydantic import BaseModel, Field


class SendEmail(BaseModel):
    """A tool to send an email."""

    recipient: str = Field(..., description="The email address of the recipient.")
    subject: str = Field(..., description="The subject line of the email.")
    body: str = Field(..., description="The body content of the email.")


class UpdateDatabase(BaseModel):
    """
    A tool to execute a query against the database.

    This tool is designed with a "blast radius" principle in mind.
    By default, it runs in a dry-run mode to prevent accidental
    modifications.
    """

    query: str = Field(..., description="The SQL query to execute.")
    dry_run: bool = Field(
        True,
        description=(
            "If True, the query is validated but not executed. "
            "If False, the query is executed."
        ),
    )
