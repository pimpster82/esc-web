import os
import sys

# Debug: Print environment variables
port = os.environ.get('PORT', '8080')
print(f"[GUNICORN CONFIG] PORT env var: {port}", file=sys.stderr, flush=True)
print(f"[GUNICORN CONFIG] All env vars with PORT: {[k for k in os.environ.keys() if 'PORT' in k.upper()]}", file=sys.stderr, flush=True)

# Bind to PORT environment variable, fallback to 8080
bind = f"0.0.0.0:{port}"
workers = 2
timeout = 120

print(f"[GUNICORN CONFIG] Binding to: {bind}", file=sys.stderr, flush=True)

# Hook: Called after each worker is forked
def post_fork(server, worker):
    """Called after a worker has been forked"""
    print(f"[WORKER {worker.pid}] Worker started, loading knowledge base...", file=sys.stderr, flush=True)

    # Import and load knowledge base
    try:
        from web_api import load_knowledge_base
        load_knowledge_base()
        print(f"[WORKER {worker.pid}] Knowledge base loaded successfully", file=sys.stderr, flush=True)
    except Exception as e:
        print(f"[WORKER {worker.pid}] ERROR loading knowledge base: {e}", file=sys.stderr, flush=True)
