alembic upgrade head
uvicorn openstadia_hub.main:app --proxy-headers --forwarded-allow-ips='*' --host 0.0.0.0 --port 8000