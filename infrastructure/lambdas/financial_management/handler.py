from services.financial_management.service_runner import run


def lambda_handler(event, context):
    return run(event)
