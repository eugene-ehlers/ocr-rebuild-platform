from .handlers import placeholder_response

def create():
    return placeholder_response("annotations", "create")

def update():
    return placeholder_response("annotations", "update")

def history():
    return placeholder_response("annotations", "history")

def status():
    return placeholder_response("annotations", "status")

def reprocess():
    return placeholder_response("annotations", "reprocess")
