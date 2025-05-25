import os
from supabase import create_client
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Create client
supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
