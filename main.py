
import streamlit as st

# CSS ciblé uniquement sur la sidebar
st.markdown("""
    <style>
        /* Masquer uniquement la sidebar */
        [data-testid="stSidebar"] {
            display: none !important;
            width: 0 !important;
            height: 0 !important;
            position: fixed !important;
            left: -999px !important;
            top: -999px !important;
        }

        /* Masquer le bouton hamburger */
        button[kind="secondary"],
        [data-testid="baseButton-secondary"] {
            display: none !important;
        }

        /* Assurer que le contenu principal utilise toute la largeur */
        .main .block-container {
            max-width: 100% !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
    </style>
""", unsafe_allow_html=True)

# Configuration de la page
# #st.set_page_config(
#     page_title="My App",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

import pandas as pd
from pages.login import login_page
from pages.forgot_pw import forgot_password
from pages.sign_up_client import sign_up
from pages.home_page import account_management, home # Import the home page
from pages.Create_account import sign_up_page
from pages.display_user_list import display_users_list
from pages.update_account import edit_user_page, fetch_user_details
from pages.view_profil import view_profil




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

    if "page" not in st.session_state:
        st.session_state.page = "login"
        st.switch_page("pages/login.py")  

    # # Rediriger automatiquement vers la page de connexion si l'utilisateur n'est pas connecté
    # if "identifier" not in st.session_state:
    #     if st.session_state.page != "login":
    #         st.session_state.page = "login"

    #     # Vérifie si le formulaire de login n'a pas encore été affiché
    #     if "login_form_rendered" not in st.session_state:
    #         login_page()
    #         st.session_state.login_form_rendered = True




    # if "identifier" not in st.session_state:
    #     st.session_state.page = "login"
    # else:
    #     #  Afficher la sidebar uniquement après connexion
    #     with st.sidebar:
    #         identifier = st.session_state.identifier
    #         user_details = fetch_user_details(identifier)
    #         if user_details is not None and isinstance(user_details, pd.Series):
    #             client_name = user_details["ClientName"]
    #             st.sidebar.write(f"Welcome, :violet[{client_name}]!")
    #         else:
    #             st.sidebar.error("Impossible de récupérer les informations de l'utilisateur.")

        # Gear button at the top right if logged in
        # Gear button at the top right if logged in
        #if "identifier" in st.session_state:
            
        #     col1, col2 = st.columns([8, 1])
        # with col2:
        #     st.button("⚙️", key="gear_button")
             
            # if st.sidebar.button("Home", key="home_button"):
            #     st.session_state.view = "home"


            # #if st.sidebar.button("View Profil"):
            #     #st.session_state.view = "display"
            #     #display_users_list()



            # if st.sidebar.button("↩️Log Out"):
            #     st.session_state.view = "login" # Met à jour la vue actuelle
            #     st.switch_page("pages/login.py")  
            #     st.session_state.pop("identifier", None)  # Supprime les infos utilisateur
            #     st.session_state.pop("client_name", None)
            #     st.session_state.pop("role_name", None)
            #     st.rerun()  # Recharge l'interface pour rediriger vers la page de login














    # Afficher la page actuelle
    st.write(f"Current page: {st.session_state.page}")

    # Logique pour afficher la bonne page
    if st.session_state.page == "login":
        login_page()  # Ta fonction de connexion
    elif st.session_state.page == "sign_up":
        sign_up_page()  # Page d'inscription
    elif st.session_state.page == "home":
        home()  # Dashboard principal
    elif st.session_state.page == "sign_upp":
        sign_up()
    elif st.session_state.page == "display":
         display_users_list()
    elif st.session_state.page == "forgot_password":
        forgot_password()
    elif st.session_state.page == "update":
        identifier = st.session_state.get("edit_user_identifier", None)
        if identifier:
            edit_user_page(identifier)
        else:
            st.error("No user selected for modification.")
    elif st.session_state.page == "view":
        identifier = st.session_state.get("edit_user_identifier", None)
        if identifier:
            view_profil(identifier)
        else:
            st.error("No user selected for modification.")
    else:
        st.write("Unexpected page state")

if __name__ == "__main__":
    main()
