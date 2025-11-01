import toml
from supabase import create_client

def get_client():
    secrets = toml.load("secrets.toml")
    url = secrets["supabase"]["url"]
    key = secrets["supabase"]["key"]
    return create_client(url, key)

supabase = get_client()
