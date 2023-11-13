alembic upgrade head
uvicorn openstadia_hub.main:app --proxy-headers --forwarded-allow-ips='*' --reload --host 0.0.0.0 --port 8000
