import os
from supabase import create_client, Client

url: str = os.environ.get("https://txsgstwieumgupxasmho.supabase.co")
key: str = os.environ.get("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR4c2dzdHdpZXVtZ3VweGFzbWhvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTc0NDM5NzgsImV4cCI6MjAzMzAxOTk3OH0.anWWbzncvaQybZO82ZNovX4AIpoSkjqieEITzo4dWP8")
supabase: Client = create_client(url, key)