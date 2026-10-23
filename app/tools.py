# Fake order database (mock data)
ORDERS = {
    "1042": {"status": "delayed", "expected_delivery": "3 days ago", "item": "Wireless Headphones"},
    "1043": {"status": "shipped", "expected_delivery": "tomorrow", "item": "Phone Case"},
    "1044": {"status": "delivered", "expected_delivery": "delivered yesterday", "item": "Laptop Stand"},
}

# Tickets created during this run are stored here
TICKETS = []


def check_order_status(order_id: str) -> dict:
    """Look up the status of a customer's order using its order number."""
    order_id = order_id.replace("#", "").strip()
    order = ORDERS.get(order_id)
    if order is None:
        return {"found": False, "message": f"No order found with id {order_id}"}
    return {"found": True, "order_id": order_id, **order}


def create_ticket(issue_summary: str, urgency: str) -> dict:
    """Create a support ticket. urgency must be one of: low, medium, high."""
    ticket = {
        "ticket_id": f"T-{len(TICKETS) + 1:04d}",
        "issue_summary": issue_summary,
        "urgency": urgency,
        "status": "open",
    }
    TICKETS.append(ticket)
    return ticket


def escalate_to_human(reason: str) -> dict:
    """Hand the conversation to a human support agent, with a reason."""
    return {"escalated": True, "reason": reason, "message": "A human agent will contact the customer shortly."}