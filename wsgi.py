"""
WSGI entry point for production deployment
"""
from app import server

# This is the WSGI application that Gunicorn will use
application = server

if __name__ == "__main__":
    application.run()
