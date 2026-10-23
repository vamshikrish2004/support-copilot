from app.tools import check_order_status, create_ticket, escalate_to_human

print(check_order_status("#1042"))
print(check_order_status("9999"))
print(create_ticket("Customer charged twice", "high"))
print(escalate_to_human("Customer is angry and wants a manager"))