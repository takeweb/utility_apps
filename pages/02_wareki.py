import streamlit as st
from supabase import Client
from libs.supabase_client import get_supabase_client
import tools.wareki as wareki


def main():
    wareki.display_streamlit_app()

if __name__ == "__main__":
    main()
