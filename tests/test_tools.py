from app.tools import check_order_status, create_ticket, escalate_to_human


def test_order_found():
    result = check_order_status("#1042")
    assert result["found"] is True
    assert result["status"] == "delayed"


def test_order_not_found():
    result = check_order_status("9999")
    assert result["found"] is False


def test_create_ticket():
    ticket = create_ticket("Customer charged twice", "high")
    assert ticket["status"] == "open"
    assert ticket["urgency"] == "high"


def test_escalate():
    result = escalate_to_human("Angry customer")
    assert result["escalated"] is True