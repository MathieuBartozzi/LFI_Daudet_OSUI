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

    with st.popover("**Utilisation des données** : méthodologie et limites"):
        st.markdown("""

### 1. Grandes étapes de la méthodologie et du code

L’analyse des données pédagogiques au LFIAD a suivi une méthodologie rigoureuse, mise en œuvre à travers plusieurs étapes clés :

1. **Extraction des données**
   - Les données ont été exportées depuis **Pronote** pour l’année 2023-2024 sous forme de fichiers CSV.
   - Toutefois, les résultats des évaluations par compétences pour les classes de **6e, 5e et 4e** n’ont pas pu être inclus en raison de la structuration insuffisante des données dans Pronote.

2. **Anonymisation**
   - Toutes les données personnelles (noms, prénoms) ont été remplacées par des **identifiants uniques** pour respecter le RGPD :
     - Les élèves sont identifiés par un champ `eleve_id`.
     - Les professeurs sont identifiés par un champ `prof_id`.
   - Les fichiers anonymisés sont irréversibles et séparés des fichiers de réidentification réservés à une vérification restreinte.

3. **Nettoyage et structuration des données**
   - **Normalisation des colonnes** : formatage des dates, coefficients et notes.
   - **Uniformisation des matières** : noms standardisés pour faciliter l’analyse (ex. : "ARABE LV SECTION" → "Arabe").
   - **Traitement des valeurs manquantes et doublons**, avec catégorisation par niveau (ex. : "collège" pour les niveaux inclus).

4. **Analyse et modélisation**
   - **Clustering (KNN)** : segmentation des élèves selon leurs performances et comportements.
   - **Sentiment analysis (VADER)** : évaluation des appréciations des professeurs.
   - **Scoring avancé (GPT-4o Mini)** : extraction d’indicateurs sur le travail, le comportement et l’engagement des élèves.

5. **Visualisation**
   - Une application **Streamlit sécurisée** (voir Section 3) a été développée pour offrir des tableaux de bord dynamiques.
   - Les visualisations incluent :
     - Profils d’élèves croisés (moyennes, retards, punitions, etc.).
     - Répartition des notes par matières et genres.
     - Analyse des appréciations et corrélations avec les performances académiques.

---

### 2. Données publiques

Un sous-ensemble des données, nettoyées et anonymisées, est disponible sur [un dépôt GitHub](https://github.com/MathieuBartozzi/LFI_Daudet_OSUI).
- Ce dépôt contient :
  - Les fichiers anonymisés utilisés dans l’application.
  - Les scripts Python utilisés pour l’anonymisation, le nettoyage et les analyses.
  - Un guide de reproduction des analyses et des visualisations.

---

### 3. Sécurisation de l’application

L'application Streamlit a été conçue avec une attention particulière à la sécurité :
- **Accès restreint** : réservé aux utilisateurs disposant d’une adresse e-mail **@mlfmonde.org** et d’un mot de passe unique.
- **Données anonymisées** : seules les informations strictement nécessaires aux analyses sont intégrées dans l'application.
- **Fichiers de réidentification** : conservés séparément, non accessibles depuis l’application.
- **Journalisation des accès** : pour surveiller et limiter les utilisations abusives.

---

### 4. Limites et vigilances

Malgré le soin apporté à cette analyse, plusieurs limites doivent être prises en compte :

1. **Qualité et véracité des données**
   - Les données exportées depuis Pronote peuvent contenir des erreurs ou être incomplètes, notamment pour les évaluations par compétences des classes de **6e, 5e et 4e**, qui ne sont pas intégrées.
   - Les informations issues de Pronote nécessitent parfois une validation manuelle ou des corrections préalables.

2. **Travail et méthodologie perfectibles**
   - Bien que la méthodologie suive des standards rigoureux, certaines étapes peuvent comporter des imperfections, comme des biais introduits lors du nettoyage ou du clustering.
   - Les choix de paramètres dans les modèles (par ex. : nombre de clusters pour KNN) peuvent affecter les résultats.

3. **Limites des modèles utilisés**
   - **VADER** : Performant pour des phrases simples, il peut mal interpréter des appréciations complexes ou nuancées.
   - **GPT-4o Mini** : Bien qu’efficace, il peut manquer de sensibilité face à des textes ambigus ou atypiques. Une adaptation plus fine aux contextes éducatifs serait nécessaire.

---

### 5. Conclusion

Ce projet a permis de développer un cadre rigoureux pour l’analyse des données pédagogiques, tout en respectant le RGPD. L’application fournit des informations utiles pour le pilotage pédagogique, mais il est important de considérer les limites mentionnées pour interpréter les résultats de manière éclairée.


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
