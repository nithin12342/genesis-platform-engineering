import azure.functions as func
import logging
import json
import random

app = func.FunctionApp()

@app.route(route="status", auth_level=func.AuthLevel.ANONYMOUS)
def status(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Fetching status for 01 Infrastructure as Code Terraform.')
    data = {"status": "Active", "uptime": "99.9%", "requests": random.randint(10, 100)}
    return func.HttpResponse(json.dumps(data), mimetype="application/json")
