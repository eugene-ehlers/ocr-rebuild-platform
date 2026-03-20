def lambda_handler(event, context):
    """
    Financial Management Service Lambda.
    Performs transaction parsing, category classification, and cashflow evaluation.
    """
    # Extract payload
    transactions = event.get("transactions", [])

    # Example processing (placeholder)
    parsed = [{"id": t.get("id"), "amount": t.get("amount"), "category": "uncategorized"} for t in transactions]

    # Return structured output
    return {
        "status": "success",
        "service": "financial_management",
        "parsed_transactions": parsed,
        "summary": {"total_transactions": len(parsed)}
    }
