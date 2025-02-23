import streamlit as st
import re
from dbConnection import get_connection
import hashlib
from sqlalchemy import text

if "page" not in st.session_state:
    st.session_state.page = "forgot_password"  # Page par défaut

def hash_password(password):
    """Hash password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def validate_password_strength(password):
    """
    Validate password strength:
    - At least 8 characters
    - Contains uppercase and lowercase
    - Contains numbers
    - Contains special characters
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r"\d", password):
        return False, "Password must contain at least one number"
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character"
    return True, "Password is strong"

# Add custom CSS
st.markdown("""
    <style>
        .stTextInput > label {font-weight: bold;}
        .stSelectbox > label {font-weight: bold;}
    </style>
""", unsafe_allow_html=True)

def forgot_password():
    if "page" not in st.session_state:
        st.session_state.page = "forgot_password"  # Page par défaut


    st.title("Let's change your password🔑")
    with st.form("Let's change your password🔑", clear_on_submit=True):
        
        identifier = st.text_input("Identifier").strip()
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        submit_button = st.form_submit_button("Change your password")

    if submit_button:
        if not identifier:
            st.error("Please enter your identifier.")
            return

        if new_password != confirm_password:
            st.error("Passwords do not match!")
            return
        
        is_password_strong, password_message = validate_password_strength(new_password)
        if not is_password_strong:
            st.error(password_message)
            return

        try:
         with st.spinner('Registering... Please wait'):
            engine = get_connection()
            with engine.connect() as conn:
                # Vérifier si l'identifier existe dans la table consumption et récupérer ClientName
                check_query = text("SELECT identifier FROM users WHERE identifier = :identifier")


                result = conn.execute(check_query, {"identifier": identifier}).fetchone()

                if not result:
                    st.error("This identifier does not exist in the consumption table.")
                    return
                
                


                # Mettre à jour le mot de passe
                update_query = text("""
                        UPDATE users 
                        SET password_hash = :password_hash 
                        WHERE identifier = :identifier
                    """)

                conn.execute(update_query, {
                        "identifier": identifier,
                        "password_hash": hash_password(new_password),
                    })
                conn.commit()

                st.success("Registration successful! Redirecting to login page...")
               

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.error("Please try again or contact support.")

    # Bouton de retour visible seulement si l'inscription n'est pas en cours
    
    if st.button("🔙Log in"):
        st.session_state.page = "login"
        st.switch_page("pages/login.py")
        st.rerun()

#def main():
    

# Exécuter la fonction
 #forgot_password()

#if __name__ == "__main__":
#main()

if __name__ == "__main__":
    forgot_password()