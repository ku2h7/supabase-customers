# app/controllers/customers_route.py

from flask import Blueprint, jsonify, request
from app.utils.supabase_client import get_supabase_client  # Import fungsi untuk mendapatkan client Supabase

# Membuat blueprint untuk route customers
customers_blueprint = Blueprint('customers', __name__)
supabase = get_supabase_client()  # Dapatkan client Supabase

# Route untuk memeriksa koneksi ke database
@customers_blueprint.route('/check-db', methods=['GET'])
def check_db():
    try:
        # Mengembalikan status jika terhubung ke database
        return jsonify({"status": "success", "message": "Connected to database."}), 200
    except Exception as e:
        # Mengembalikan pesan kesalahan jika terjadi kesalahan
        return jsonify({"status": "error", "message": str(e)}), 500

# Route untuk mengambil semua pelanggan
@customers_blueprint.route('/customers', methods=['GET'])
def get_customers():
    try:
        # Mengambil semua pelanggan dan mengurutkan berdasarkan id
        response = supabase.from_("customers").select("*").order("id").execute()
        return jsonify({"status": "success", "data": response.data}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": "Failed to fetch customers."}), 500


# Route untuk mengambil pelanggan tertentu berdasarkan ID
@customers_blueprint.route('/customers/<int:customer_id>', methods=['GET'])
def get_specific_customer(customer_id):
    try:
        # Mengambil data pelanggan berdasarkan ID yang diberikan
        response = supabase.from_("customers").select("*").eq('id', customer_id).execute()
        if response.data:
            # Mengembalikan data pelanggan jika ditemukan
            return jsonify({"status": "success", "data": response.data[0]}), 200
        else:
            # Mengembalikan pesan kesalahan jika pelanggan tidak ditemukan
            return jsonify({"status": "error", "message": "Customer not found."}), 404
    except Exception as e:
        # Mengembalikan pesan kesalahan jika terjadi kesalahan
        return jsonify({"status": "error", "message": str(e)}), 500

# Route untuk membuat pelanggan baru
@customers_blueprint.route('/customers', methods=['POST'])
def create_customer():
    try:
        # Mendapatkan data dari body permintaan
        data = request.get_json()

        # Validasi apakah name dan email ada
        if not data or 'name' not in data or 'email' not in data:
            return jsonify({"status": "error", "message": "Name and email are required."}), 400

        # Pengecekan apakah email sudah ada
        existing_customer = supabase.from_("customers").select("*").eq("email", data["email"]).execute()

        if existing_customer.data:
            return jsonify({"status": "error", "message": "Customer with this email already exists."}), 409

        # Insert customer baru
        new_customer = {
            "name": data["name"],
            "email": data["email"]
        }
        response = supabase.from_("customers").insert(new_customer).execute()

        # Return jika sukses
        return jsonify({"status": "success", "data": response.data}), 201

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Route untuk memperbarui data pelanggan berdasarkan ID
@customers_blueprint.route('/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    data = request.json  # Mengambil data dari request JSON
    try:
        # Memperbarui data pelanggan berdasarkan ID yang diberikan
        response = supabase.from_("customers").update(data).eq('id', customer_id).execute()
        return jsonify({"status": "success", "data": response.data}), 200  # Mengembalikan data pelanggan yang diperbarui
    except Exception as e:
        # Mengembalikan pesan kesalahan jika terjadi kesalahan
        return jsonify({"status": "error", "message": str(e)}), 500

# Route untuk menghapus pelanggan berdasarkan ID
@customers_blueprint.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    try:
        # Menghapus pelanggan berdasarkan ID yang diberikan
        response = supabase.from_("customers").delete().eq('id', customer_id).execute()
        return jsonify({"status": "success", "data": response.data}), 200  # Mengembalikan status penghapusan
    except Exception as e:
        # Mengembalikan pesan kesalahan jika terjadi kesalahan
        return jsonify({"status": "error", "message": str(e)}), 500
