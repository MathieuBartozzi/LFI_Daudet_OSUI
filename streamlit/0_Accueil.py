import streamlit as st
import os
from PIL import Image
import hashlib



# Configuration de la mise en page
st.set_page_config(
    page_title='Audit LFIAD 2024',
    layout='wide')


# Domaine autorisé pour l'authentification
DOMAINE_AUTORISE = "@mlfmonde.org"

# Mot de passe commun (à sécuriser dans secrets.toml)
MOT_DE_PASSE_COMMUN = st.secrets["mot_de_passe_commun"]

# Fonction pour hacher le mot de passe
def hacher_mot_de_passe(mot_de_passe):
    return hashlib.sha256(mot_de_passe.encode()).hexdigest()

# Initialiser la variable de session pour l'état de connexion
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# Fonction pour charger les images
@st.cache_data
def load_images():
    # Obtenir le chemin absolu du fichier courant
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Construire les chemins vers les images
    logo_path = os.path.join(current_dir, "logo.jpg")
    image_path = os.path.join(current_dir, "image_daudet.jpeg")

    # Charger les images si elles existent
    logo_image = Image.open(logo_path) if os.path.exists(logo_path) else None
    daudet_image = Image.open(image_path) if os.path.exists(image_path) else None

    return logo_image, daudet_image

def login():
    st.title("Connexion à l'application")
    email = st.text_input("Adresse e-mail")
    mot_de_passe = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):
        if email.endswith(DOMAINE_AUTORISE) and hacher_mot_de_passe(mot_de_passe) == hacher_mot_de_passe(MOT_DE_PASSE_COMMUN):
            st.session_state.logged_in = True
            st.session_state.email = email
            st.success("Connexion réussie ! Utilisez le menu pour naviguer.")
            st.rerun()
        else:
            st.error("Adresse e-mail ou mot de passe incorrect.")

# Vérification de l'état de connexion
if not st.session_state.logged_in:
    login()
else:

    # Appel de la fonction pour charger les images
    logo_image, daudet_image = load_images()

    # Affichage du logo
    if logo_image:
        st.logo(logo_image)
    else:
        st.warning("Le logo n'a pas pu être chargé.")

    # Affichage du contenu principal
    if daudet_image:
        # Deux colonnes si l'image Daudet est disponible
        col1, col2 = st.columns([2, 1])
        with col1:
            st.title("Audit LFIAD 2024 : Analyse des résultats et enquêtes")
            st.markdown("""
            Dans le cadre de notre **analyse des performances pédagogiques** au **LFIAD**, nous avons collecté et croisé plusieurs sources de données :
            - Les informations issues de **Pronote** (base 2023-2024).
            - Les résultats des **enquêtes individuelles**.
            - Les échanges et conclusions des **réunions d'équipes** organisées à la fin du mois de septembre 2024.

            Ce document vous présente une **synthèse** de ce travail, ainsi que des **pistes de réflexion** pour renforcer les pratiques pédagogiques.
            """)
        with col2:
            st.image(daudet_image, width=400)
    else:
        # Organisation normale avec une seule colonne si l'image Daudet n'est pas disponible
        st.title("Audit LFIAD 2024 : Analyse des résultats et enquêtes")
        st.markdown("""
        Dans le cadre de notre **analyse des performances pédagogiques** au **LFIAD**, nous avons collecté et croisé plusieurs sources de données :
        - Les informations issues de **Pronote** (base 2023-2024).
        - Les résultats des **enquêtes individuelles**.
        - Les échanges et conclusions des **réunions d'équipes** organisées à la fin du mois de septembre 2024.

        Ce document vous présente une **synthèse** de ce travail, ainsi que des **pistes de réflexion** pour renforcer les pratiques pédagogiques.
        """)



    st.markdown("""

    #### 🎯 Objectifs de l'analyse

    Cette analyse vise à offrir une **vue d'ensemble** des dynamiques pédagogiques et des profils d'élèves afin de :
    - **Identifier des tendances** dans les pratiques pédagogiques des équipes.
    - **Mettre en lumière les points forts** et les initiatives prometteuses.
    - **Repérer des pistes d'amélioration** pour accompagner et renforcer les pratiques.
    - **Mieux comprendre les élèves** et les facteurs de leur réussite.

    Ces indicateurs ne sont pas conçus pour évaluer ou juger les équipes, mais pour **stimuler une réflexion collective** et **encourager un dialogue constructif**.

    ---

    #### 🔍 Perspectives

    Cette analyse constitue une **première étape** dans la valorisation des données pédagogiques.
    Nous nous engageons à :
    - Rester **transparents** sur la manière dont les données sont collectées et analysées.
    - **Améliorer continuellement les indicateurs** afin qu'ils reflètent fidèlement la diversité des pratiques pédagogiques.
    - **Adapter nos outils d'analyse** pour mieux tenir compte des spécificités de chaque équipe et des contextes variés.

    Votre retour est essentiel pour affiner cette démarche et faire évoluer nos outils.

    ---

    #### 💡 Votre contribution

    Nous croyons fermement que ces analyses, bien qu’imparfaites, peuvent être un **levier puissant** pour mieux comprendre les dynamiques pédagogiques au sein de nos établissements.

    Toutefois, pour maximiser leur impact, **vos retours et suggestions** sont essentiels.

    💬 **Partagez vos remarques, idées ou questions** afin que nous puissions construire ensemble des outils pertinents et adaptés à vos besoins.

    """)


    st.divider()

    st.write('**Bonne navigation !**')
