from flask import Flask, jsonify
from app.controllers.customers_route import customers_blueprint
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)

    # Registrasi blueprint
    app.register_blueprint(customers_blueprint, url_prefix="/v1")

    @app.route('/')
    def home():
        return jsonify({"message": "Welcome to the API!"})

    return app

# Jika Anda ingin menjalankan aplikasi secara langsung
if __name__ == "__main__":
    app = create_app()  # Pastikan aplikasi diinisialisasi dengan create_app
    app.run(host='0.0.0.0', port=5000)