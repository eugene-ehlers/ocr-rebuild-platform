from .handlers import placeholder_response

def catalog():
    return placeholder_response("requests_results", "catalog")

def create():
    return placeholder_response("requests_results", "create")

def status():
    return placeholder_response("requests_results", "status")

def remediation():
    return placeholder_response("requests_results", "remediation")

def result():
    return placeholder_response("requests_results", "result")

def rerun():
    return placeholder_response("requests_results", "rerun")
