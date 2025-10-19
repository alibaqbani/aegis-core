"""
Core business logic for tools.

This module contains the framework-agnostic business logic for the tools
defined in `lucidomy.core.tools`. Adapters will call these functions.
"""

from typing import Any, Dict

from src.lucidomy.core.tools import SendEmail, UpdateDatabase


def send_email(params: SendEmail) -> Dict[str, Any]:
    """
    Simulates sending an email.

    In a real application, this function would integrate with an email service
    like SendGrid or AWS SES. For this example, it just prints the details.
    """
    print(
        f"[LOGIC] Sending email to {params.recipient} "
        f"with subject '{params.subject}'..."
    )
    return {"status": "email_sent", "recipient": params.recipient}


def update_database(params: UpdateDatabase) -> Dict[str, Any]:
    """
    Simulates executing a database query with a dry-run safety mechanism.

    This function demonstrates the "Blast Radius" principle by defaulting to
    a safe (dry_run) mode.
    """
    if params.dry_run:
        print(f"[LOGIC] DRY RUN: Would execute query: {params.query}")
        return {"status": "dry_run", "query": params.query}
    else:
        print(f"[LOGIC] EXECUTING: {params.query}")
        return {"status": "executed", "query": params.query}
