from itsdangerous import URLSafeSerializer
from django.conf import settings
from .models import LogEntry

def generate_token(data):
    serializer = URLSafeSerializer(settings.SECRET_KEY)
    return serializer.dumps(data)

def verify_token(token):
    serializer = URLSafeSerializer(settings.SECRET_KEY)
    try:
        return serializer.loads(token)
    except Exception:
        return None

def create_log_entry(key, txt, session, ipaddr, app="PBL01LOGS"):
    LogEntry.objects.create(
        key=key,
        txt=txt,
        session=session,
        ipaddr=ipaddr,
        app=app
    )

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip