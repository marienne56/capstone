import streamlit as st

# Simulation de récupération des utilisateurs
def fetch_total_users():
    # Remplacer ceci par la logique réelle pour obtenir le nombre total d'utilisateurs
    return 50  # Exemple avec 50 utilisateurs

# Exemple de fonction pour récupérer les utilisateurs d'une page spécifique
def fetch_users(page_number, page_size):
    # Simulation de la récupération des utilisateurs par page
    start = (page_number - 1) * page_size
    end = start + page_size
    # Retourner une liste fictive d'utilisateurs
    return [f"User {i}" for i in range(start + 1, end + 1)]

# Pagination sans radio button
PAGE_SIZE = 10  # Nombre d'utilisateurs par page
page_number = st.session_state.get("page_number", 1)
search_query = st.text_input("Search an user :", "").strip().lower()

# Calculer le nombre total de pages
total_users = fetch_total_users()
total_pages = (total_users // PAGE_SIZE) + (1 if total_users % PAGE_SIZE > 0 else 0)

# Affichage des utilisateurs
users = fetch_users(page_number, PAGE_SIZE)
st.write(f"Page {page_number}/{total_pages} :")
for user in users:
    st.write(user)

# Gestion de la pagination
if total_pages > 1:
    col1, col2, col3 = st.columns([1, 6, 1])

    # Bouton Précédent
    with col1:
        if page_number > 1:
            if st.button("⬅️ Previous"):
                st.session_state.page_number -= 1
                st.rerun()

    # Affichage des numéros de pages
    with col2:
        page_buttons = []
        for i in range(1, total_pages + 1):
            if st.button(f"{i}", key=f"page_{i}", on_click=lambda i=i: go_to_page(i)):

                # Change page when button is clicked
                st.session_state.page_number = i
                st.rerun()

    # Bouton Suivant
    with col3:
        if page_number < total_pages:
            if st.button("➡️ Next"):
                st.session_state.page_number += 1
                st.rerun()

# Logique de redirection pour changer de page
def go_to_page(page):
    st.session_state.page_number = page
    st.rerun()

st.title("Pagination Example")
