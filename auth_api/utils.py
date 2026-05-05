import json, os, requests, logging

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST


MAILEROO_URL = "https://smtp.maileroo.com/api/v2/emails" # Para enviar correos
logger = logging.getLogger(__name__)

# url api/email/send/

@csrf_exempt
@require_POST
def send_email(request):
    data = json.loads(request.body)
    to = data["to"]
    subject = data["subject"]
    text = data["text"]

    headers = {
        "X-API-Key": os.getenv("MAILEROO_TOKEN", ""),
        "Content-Type": "application/json"
    }

    payload = {
        "from": {"address": os.getenv("MAILEROO_FROM_ADDRESS", "")},
        "to": [{"address": to}],
        "subject": subject,
        "plain": text
    }

    try:
        r = requests.post(MAILEROO_URL, headers=headers, json=payload, timeout=10)

    except requests.RequestException:
        return JsonResponse({
            "error": "external_service_unavailable",
        }, status=503)

    if r.status_code >= 400:
        logger.error('send_email: external_service_error to="%s" status=%s body="%s"', to, r.status_code, r.text[:200])
        return JsonResponse({
            "message": "external_service_error",
        }, status=502)
    
    logger.info('send_email: ok to="%s" status=%s', to, r.status_code, r.text[:200])
    return JsonResponse({
        "ok": True
    }, status=200)

def send_email_service(to, subject, text):
    headers = {
        "X-API-Key": os.getenv("MAILEROO_TOKEN", ""),
        "Content-Type": "application/json"
    }

    payload = {
        "from": {"address": os.getenv("MAILEROO_FROM_ADDRESS", "")},
        "to": [{"address": to}],
        "subject": subject,
        "plain": text
    }

    return requests.post(MAILEROO_URL, headers=headers, json=payload, timeout=10)