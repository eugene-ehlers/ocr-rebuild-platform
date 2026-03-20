def placeholder_response(domain, action):
    return {
        "success": True,
        "status": "placeholder",
        "domain": domain,
        "action": action,
        "message": f"{domain}:{action} scaffold created"
    }
