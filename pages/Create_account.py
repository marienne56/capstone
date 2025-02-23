import streamlit as st
import re
from dbConnection import get_connection
import hashlib
from sqlalchemy import text



def validate_email(email):
    """Validate email format using regex."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone_number):
    """Validate phone number format."""
    pattern = r'^\+?1?\d{9,15}$'
    return re.match(pattern, phone_number) is not None

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


def sign_up_page():
 
 

# Title of the application
 st.title("User Registration Form")

# Create form with clear_on_submit=True
 with st.form("registration_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    
    with col1:
        ClientName = st.text_input("Name").strip()
        username = st.text_input("Username").strip()
        email = st.text_input("Email").strip()
        address = st.text_area("Address").strip()
        is_active = st.selectbox("Is Active?", ["Yes", "No"])
        
    
    with col2:
        
        identifier = st.text_input("Identifier").strip()
        phone_number = st.text_input("Phone Number").strip()
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
    
    role_name = st.selectbox("Role ID (Optional)", ["Client", "Agent", "Admin"])
    #zone_name = st.selectbox("Zone ID (Optional)", ["Zone A", "Zone B", "Zone C"])  # Similarly for Zone ID
    submit_button = st.form_submit_button("Create Account")

 if submit_button:
    # Validate required fields
    required_fields = {
        'Name': ClientName,
        'Username': username,
        'Identifier': identifier,
        'Email': email,
        'Password': password
    }
    
    missing_fields = [field for field, value in required_fields.items() if not value]
    
    if missing_fields:
        st.error(f"Please fill in the following required fields: {', '.join(missing_fields)}")
    else:
        # Validate email format
        if not validate_email(email):
            st.error("Please enter a valid email address")
        # Validate phone number if provided
        elif phone_number and not validate_phone(phone_number):
            st.error("Please enter a valid phone number")
        # Validate password match
        elif password != confirm_password:
            st.error("Passwords do not match!")
        else:
            # Validate password strength
            is_password_strong, password_message = validate_password_strength(password)
            if not is_password_strong:
                st.error(password_message)
            else:
                try:
                    engine = get_connection()
                    with engine.connect() as conn:
                        # Check if identifier, email, or username already exists
                        check_query = text("""
                            SELECT identifier, email, username 
                            FROM users 
                            WHERE identifier = :identifier OR email = :email OR username = :username
                        """)
                        
                        result = conn.execute(
                            check_query,
                            {
                                "identifier": identifier,
                                "email": email,
                                "username": username
                            }
                        ).fetchone()

                        if result:
                            # Provide specific feedback about which field exists
                            if result.identifier == identifier:
                                st.error("This identifier is already registered")
                            elif result.email == email:
                                st.error("This email is already registered")
                            else:
                                st.error("This username is already taken")
                        else:
                            # Get the role_id if role_name doesn't exist, insert it
                            role_id_query = text("SELECT role_id FROM role WHERE role_name = :role_name")
                            role_result = conn.execute(role_id_query, {"role_name": role_name}).fetchone()
                            if not role_result:
                                # Insert new role if not found
                                insert_role_query = text("""
                                    INSERT INTO role (role_name) 
                                    VALUES (:role_name)
                                """)
                                conn.execute(insert_role_query, {"role_name": role_name})
                                conn.commit()
                                role_id = conn.execute(role_id_query, {"role_name": role_name}).fetchone()[0]
                            else:
                                role_id = role_result[0]
                            ''''
                            # Get the zone_id if zone_name doesn't exist, insert it
                            zone_id_query = text("SELECT zone_id FROM zone WHERE zone_name = :zone_name")
                            zone_result = conn.execute(zone_id_query, {"zone_name": zone_name}).fetchone()
                            if not zone_result:
                                # Insert new zone if not found
                                insert_zone_query = text("""
                                    INSERT INTO zone (zone_name) 
                                    VALUES (:zone_name)
                                """)
                                conn.execute(insert_zone_query, {"zone_name": zone_name})
                                conn.commit()
                                zone_id = conn.execute(zone_id_query, {"zone_name": zone_name}).fetchone()[0]
                            else:
                                zone_id = zone_result[0]
                            '''

                            # Insert new user
                            insert_query = text("""
                                INSERT INTO users (
                                    ClientName, username, identifier, 
                                    email, phone_number, address, password_hash, 
                                    is_active, role_id
                                ) VALUES (
                                    :ClientName, :username, :identifier,
                                    :email, :phone_number, :address, :password_hash,
                                    :is_active, :role_id
                                )
                            """)
                            
                            conn.execute(
                                insert_query,
                                {
                                    "ClientName": ClientName,
                                    
                                    "username": username,
                                    "identifier": identifier,
                                    "email": email,
                                    "phone_number": phone_number,
                                    "address": address,
                                    "password_hash": hash_password(password),
                                    "is_active": is_active == "Yes",
                                    
                                    "role_id": role_id
                                }
                            )
                            conn.commit()
                            
                            st.success("Registration successful! You can now log in.")
                            # Form will be cleared automatically due to clear_on_submit=True

                except Exception as e:
                    st.error(f"An error occurred during registration: {str(e)}")
                    st.error("Please try again or contact support if the problem persists.")

                    # Bouton de retour
 if st.button("Retour"):
        st.session_state.page = "display"
        st.switch_page("pages/display_user_list.py")
        st.rerun()

if __name__ == "__main__":
    sign_up_page()