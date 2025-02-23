import pandas as pd
import streamlit as st
from login import login_page
from forgot_pw import forgot_password
from sign_up_client import sign_up
from home_page import account_management, home # Import the home page
from Create_account import sign_up_page
from display_user_list import display_users_list
from update_account import edit_user_page, fetch_user_details
from view_profil import view_profil
# Set page configuration
#st.set_page_config(page_title="User Registration", layout="centered")

# Central page control

    

if "page" not in st.session_state or st.session_state.page not in ["sign_up", "login", "home", "sign_upp", "display", "update", "view", "forgot_password"]:
        st.session_state.page = "login"  # On force la page par défaut
        st.rerun()  # On recharge pour appliquer la correction immédiatement


# Injecter du CSS et JavaScript plus agressif pour cacher le bouton Deploy mais garder le menu avec les trois points
st.markdown("""
    <style>
        /* Masquer le bouton Deploy */
        .st-emotion-cache-1wbqy5l,
        [data-testid="stDeployButton"],
        button[kind="primary"],
        .stDeployButton,
        iframe[title="Deploy"],
        div[data-testid="stToolbar"] button {
            display: none !important;
            width: 0 !important;
            height: 0 !important;
            padding: 0 !important;
            margin: 0 !important;
            border: none !important;
            pointer-events: none !important;
            position: absolute !important;
            top: -9999px !important;
            left: -9999px !important;
            opacity: 0 !important;
            visibility: hidden !important;
            clip: rect(0 0 0 0) !important;
            overflow: hidden !important;
        }

        /* Cibler le bouton de menu avec les trois points et garder visible */
        div[data-testid="stToolbar"] button[aria-label="Options"] {
            visibility: visible !important;
            opacity: 1 !important;
            position: relative !important;
            top: auto !important;
            left: auto !important;
            pointer-events: all !important;
        }

        /* S'assurer que le bouton de menu reste interactif */
        div[data-testid="stToolbar"] button[aria-label="Options"]:hover {
            background-color: #f4f4f4; /* Peut être personnalisé */
        }
    </style>
    
    <script>
        function forceDisableButton() {
            const selectors = [
                '.st-emotion-cache-1wbqy5l',
                '[data-testid="stDeployButton"]',
                'button[kind="primary"]',
                '.stDeployButton',
                'iframe[title="Deploy"]',
                'div[data-testid="stToolbar"] button'
            ];
            
            selectors.forEach(selector => {
                const elements = document.querySelectorAll(selector);
                elements.forEach(element => {
                    if (element) {
                        // Supprimer complètement l'élément du DOM
                        element.remove();
                    }
                });
            });

            // Bloquer également les event listeners au niveau document
            document.addEventListener('click', function(e) {
                const target = e.target;
                if (target && 
                    (target.matches(selectors.join(',')) || 
                     target.closest(selectors.join(',')))) {
                    e.preventDefault();
                    e.stopPropagation();
                    return false;
                }
            }, true);
        }

        // Exécuter immédiatement
        forceDisableButton();
        
        // Continuer à exécuter pour attraper les nouveaux rendus
        const observer = new MutationObserver(forceDisableButton);
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
        
        // Backup avec setInterval
        setInterval(forceDisableButton, 100);
    </script>
""", unsafe_allow_html=True)




def main():
    #st.write("DEBUG - Session State:", st.session_state)

    if "page" not in st.session_state or st.session_state.page not in ["sign_up", "login", "home", "sign_upp", "display", "update", "view", "forgot_password"]:
        st.session_state.page = "login"  # On force la page par défaut
        st.rerun()  # On recharge pour appliquer la correction immédiatement


    if "identifier" not in st.session_state:
        st.session_state.page = "login"
    else:
        #  Afficher la sidebar uniquement après connexion
        with st.sidebar:
            identifier = st.session_state.identifier
            user_details = fetch_user_details(identifier)
            if user_details is not None and isinstance(user_details, pd.Series):
                client_name = user_details["ClientName"]
                st.sidebar.write(f"Welcome, :violet[{client_name}]!")
            else:
                st.sidebar.error("Impossible de récupérer les informations de l'utilisateur.")

        # Gear button at the top right if logged in
        # Gear button at the top right if logged in
        if "identifier" in st.session_state:
            
            col1, col2 = st.columns([8, 1])
        with col2:
            st.button("⚙️", key="gear_button")
             
        if st.sidebar.button("Dashboard"):
            st.session_state.page = "home"
            st.rerun()
        
        if st.sidebar.button("View profil"):
            st.session_state.page = "display"  # Affichage de la liste des utilisateurs
            st.rerun()

        if st.sidebar.button("Log Out"):
                # Réinitialiser l'état de session pour déconnecter l'utilisateur
            st.session_state.page = "login"
            st.session_state.pop("identifier", None)
            st.session_state.pop("client_name", None)
            st.session_state.pop("role_name", None)
            st.rerun()

    st.write(f"Current page: {st.session_state.page}")
            
    if st.session_state.page == "sign_up":
        sign_up_page()  # Directly call the sign up page function
    elif st.session_state.page == "login":
        login_page()  # Directly call the login page function

    elif st.session_state.page == "home":
        home()
      
    elif st.session_state.page == "sign_upp":
        sign_up()
    elif st.session_state.page == "display":
        display_users_list()
        
    elif st.session_state.page == "forgot_password":
        forgot_password()
      
    elif st.session_state.page == "update":
        identifier = st.session_state.get("edit_user_identifier", None)  # Récupérer l'identifiant
        if identifier:
            edit_user_page(identifier)  # Passer l'identifiant à la fonction
        else:
            st.error("No user selected for modification.")  # Afficher un message d'erreur si aucun identifiant   
    elif st.session_state.page == "view":
        identifier = st.session_state.get("edit_user_identifier", None)  # Récupérer l'identifiant
        if identifier:
            view_profil(identifier)  # Passer l'identifiant à la fonction
        else:
            st.error("No user selected for modification.")  # Afficher un message d'erreur si aucun identifiant   
    else:
        st.write("Unexpected page state")  # Handle unexpected states

if __name__ == "__main__":
    main()
