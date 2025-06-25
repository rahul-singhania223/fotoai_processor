from supabase import create_client, Client

import os
from dotenv import load_dotenv

load_dotenv()

supabase_url: str = os.getenv("SUPABASE_URL")
supabase_key: str = os.getenv("SUPABASE_KEY")

print(supabase_url)
print("\n")
print(supabase_key)


supabase: Client = create_client(supabase_url, supabase_key)

