import streamlit as st
from libs.supabase_client import get_supabase_client

def main():
    st.title("First Page")
    st.write("First Page")

    supabase = get_supabase_client()

    # データ取得例
    data = supabase.table("tags").select("*").execute()

    st.write("✅ Data from Supabase:")
    st.json(data.data)

if __name__ == "__main__":
    main()
