# WSGI entry point for production deployment
from web_invoice_app_production import create_app
import os

app = create_app('production')

if __name__ == "__main__":
    app.run()
