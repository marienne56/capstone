import streamlit as st

# Variable d'état pour gérer l'affichage du menu
if 'show_menu' not in st.session_state:
    st.session_state.show_menu = False

# Fonction pour basculer l'affichage du menu
def toggle_menu():
    st.session_state.show_menu = not st.session_state.show_menu

# CSS pour masquer le bouton Deploy et ajouter le bouton engrenage
st.markdown(
    """
    <style>
    /* Cacher le bouton Deploy */
    .stAppDeployButton {
        visibility: hidden;
        position: relative;
    }

    /* Ajouter le bouton engrenage exactement au même endroit */
    .stAppDeployButton::after {
        content: "⚙️";
        visibility: visible;
        font-size: 24px;
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Injection de JavaScript pour rendre le bouton engrenage cliquable
st.markdown(
    """
    <script>
    const setupEngrenage = () => {
        const targetNode = document.querySelector('.stAppDeployButton');
        if (targetNode) {
            targetNode.addEventListener('click', function(e) {
                const buttons = parent.window.document.querySelectorAll('button[kind="formSubmit"]');
                for (let i = 0; i < buttons.length; i++) {
                    const buttonText = buttons[i].textContent.trim();
                    if (buttonText.includes('Toggle Menu')) {
                        buttons[i].click();
                        break;
                    }
                }
            });
        } else {
            setTimeout(setupEngrenage, 300);
        }
    };
    
    if (parent.window.document.readyState === 'complete') {
        setupEngrenage();
    } else {
        parent.window.addEventListener('load', setupEngrenage);
    }
    </script>
    """,
    unsafe_allow_html=True
)

# Bouton caché qui sera déclenché par le JavaScript
st.button("Toggle Menu", on_click=toggle_menu, key="toggle_menu_button", help=None)

# Affichage principal
st.title("Application Principale")
st.write("Contenu principal de l'application.")

# Affichage conditionnel des boutons Streamlit
if st.session_state.show_menu:
    st.write("### Menu")
    if st.button("👨🏼 View profile"):
        st.write("Affichage du profil utilisateur...")
        # Ajouter ici le code pour afficher le profil
    
    if st.button("↩️ Log out"):
        st.write("Déconnexion en cours...")
        # Ajouter ici le code pour la déconnexion

# CSS pour cacher le bouton Toggle Menu
st.markdown(
    """
    <style>
    /* Cacher le bouton Toggle Menu */
    [data-testid="baseButton-secondary"]:has(> div:contains("Toggle Menu")) {
        display: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)