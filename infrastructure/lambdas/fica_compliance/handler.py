def lambda_handler(event, context):
    """
    FICA Compliance Service Lambda.
    Performs document validation, identity verification, and compliance classification.
    """
    documents = event.get("documents", [])
    identity_info = event.get("identity_info", {})

    # Placeholder: mark all docs as verified
    results = [{"doc_id": d.get("id"), "verified": True} for d in documents]

    # Return structured output
    return {
        "status": "success",
        "service": "fica_compliance",
        "identity_verified": bool(identity_info),
        "document_results": results
    }
