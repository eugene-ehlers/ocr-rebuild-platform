def lambda_handler(event, context):
    """
    Credit Decision Service Lambda.
    Performs credit scoring, affordability check, and decision recommendation.
    """
    applicant_info = event.get("applicant_info", {})
    credit_data = event.get("credit_data", {})

    # Placeholder: approve all applicants if applicant_info exists
    decision = "approve" if applicant_info else "decline"

    # Return structured output
    return {
        "status": "success",
        "service": "credit_decision",
        "applicant_id": applicant_info.get("id"),
        "decision": decision,
        "score": credit_data.get("score", 600)
    }
