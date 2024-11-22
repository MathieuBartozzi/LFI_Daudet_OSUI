import streamlit as st

# Configuration de la mise en page
st.set_page_config(
    page_title='Audit LFIAD 2024',
    layout='wide')

# st.sidebar.success("Selectionner une page.")

# st.logo('logo.jpg')


# # Titre de l'application
# col1, col2=st.columns([2,1])
# with col1:
#     st.title("Audit LFIAD 2024 : Analyse des résultats et enquêtes")
#     st.markdown("""
# Dans le cadre de notre **analyse des performances pédagogiques** au **LFIAD**, nous avons collecté et croisé plusieurs sources de données :
# - Les informations issues de **Pronote** (base 2023-2024).
# - Les résultats des **enquêtes individuelles**.
# - Les échanges et conclusions des **réunions d'équipes** organisées à la fin du mois de septembre 2024.

# Ce document vous présente une **synthèse** de ce travail, ainsi que des **pistes de réflexion** pour renforcer les pratiques pédagogiques.
# """)

# with col2:
#     st.image("image_daudet.jpeg",width=400)


# Introduction

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
