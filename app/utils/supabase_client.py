import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Memuat variabel lingkungan dari file .env
load_dotenv()

# Membaca konfigurasi dari file .env
SUPABASE_URL = os.getenv('SUPABASE_URL')  # URL Supabase
SUPABASE_KEY = os.getenv('SUPABASE_KEY')  # Kunci Supabase

# Membuat client Supabase
def get_supabase_client() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)