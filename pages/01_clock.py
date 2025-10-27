import streamlit as st
from libs.supabase_client import get_supabase_client
import tools.clock as clock

def main():
    clock.draw_clock()

if __name__ == "__main__":
    main()
