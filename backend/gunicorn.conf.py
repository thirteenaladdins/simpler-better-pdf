import os

# Use PORT environment variable if available
bind = "0.0.0.0:" + str(os.environ.get("PORT", 591))
workers = 4  # Number of worker processes
worker_class = "uvicorn.workers.UvicornWorker"  # Use Uvicorn worker class
