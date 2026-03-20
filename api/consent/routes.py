from .handlers import placeholder_response

def capture():
    return placeholder_response("consent", "capture")

def validate():
    return placeholder_response("consent", "validate")

def retrieve():
    return placeholder_response("consent", "retrieve")

def revoke():
    return placeholder_response("consent", "revoke")

def proof():
    return placeholder_response("consent", "proof")
