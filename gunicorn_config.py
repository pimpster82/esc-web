import os

# Bind to PORT environment variable, fallback to 8080
bind = f"0.0.0.0:{os.environ.get('PORT', '8080')}"
workers = 2
timeout = 120
