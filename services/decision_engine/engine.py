def route_payload(service_name, payload):
    """
    Stub routing for services. Returns which service was called.
    """
    if service_name == "financial_management":
        return {"status": "called financial_management ECS"}
    elif service_name == "fica_compliance":
        return {"status": "called fica_compliance ECS"}
    elif service_name == "credit_decision":
        return {"status": "called credit_decision ECS"}
    else:
        return {"error": "Unknown service"}
