import streamlit as st
from supabase import create_client, Client

@st.cache_resource
def get_supabase_client() -> Client:
    """Supabaseクライアントを初期化してキャッシュ"""
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["publishable_key"]
    return create_client(url, key)
