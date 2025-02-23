import pandas as pd
import streamlit as st
import re
from dbConnection import get_connection
import hashlib
from sqlalchemy import text
from update_account import fetch_user_details

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

def home():
    st.write(f"Role Name: {st.session_state.get('role_name', 'Unknown')}")
    st.title("Dashboard")
    st.write("Ici, vous pouvez voir vos données et graphiques.")

def account_management():
    st.title("Account Management")
    st.write("Gérez votre compte ici.")

def main():
    st.sidebar.title("Navigation")
    if st.sidebar.button("Dashboard"):
        st.session_state.page = "Dashboard"
    if st.sidebar.button("Account Management"):
        st.session_state.page = "Account Management"
    
    if st.session_state.page == "Dashboard":
        home()
    elif st.session_state.page == "Account Management":
        account_management()

if __name__ == "__main__":
    main()
