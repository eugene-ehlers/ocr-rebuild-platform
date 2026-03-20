from .handlers import placeholder_response

def event():
    return placeholder_response("telemetry", "event")

def workflow():
    return placeholder_response("telemetry", "workflow")

def document_handling():
    return placeholder_response("telemetry", "document_handling")

def support():
    return placeholder_response("telemetry", "support")

def remediation():
    return placeholder_response("telemetry", "remediation")
