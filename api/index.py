"""
Vercel serverless function for Dash app
"""
import sys
import os

# Add the parent directory to the path so we can import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

# Vercel expects a handler function
def handler(request, response):
    return app.server(request, response)

# For Vercel compatibility
app = app.server
