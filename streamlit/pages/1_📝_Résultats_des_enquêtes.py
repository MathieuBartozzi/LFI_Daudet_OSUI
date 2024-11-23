import streamlit as st
import pandas as pd
import plotly.express as px
import os
import plotly.graph_objects as go


# st.logo('logo.jpg')


@st.cache_data
def load_data():
    # Obtenir le chemin absolu du fichier courant
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Remonter d'un niveau pour atteindre le dossier 'streamlit'
    parent_dir = os.path.dirname(current_dir)

    # Construire le chemin vers 'data_app'
    data_dir = os.path.join(parent_dir, "data_app")

    # Vérifier que le dossier existe
    if not os.path.exists(data_dir):
        st.error(f"Le dossier '{data_dir}' n'existe pas.")
        return None

    # Charger les fichiers
    df_scores_equipes = pd.read_csv(os.path.join(data_dir, "df_scores_equipes.csv"))
    return df_scores_equipes

# Appel de la fonction pour charger les données
df_scores_equipes = load_data()




tab1, tab2 = st.tabs(["**RÉSULTATS GÉNERAUX**", "**ANALYSE PAR ÉQUIPE**"])

with tab1:
    st.write("")
    st.subheader('Analyse générale', divider="gray")

    st.markdown("""
    **1 - Usage du numérique**

    L'usage du numérique semble être bien intégré dans la majorité des matières, avec une moyenne d'utilisation globalement élevée (entre 3,5 et 5). Le Tableau Blanc Interactif (TBI), ainsi que des plateformes comme Pronote, sont les outils numériques les plus fréquemment utilisés et cités comme essentiels pour rendre les cours plus interactifs et engageants. Cependant, il existe une disparité dans la maîtrise des outils selon les matières. Les équipes des matières scientifiques et des langues semblent particulièrement à l'aise avec ces technologies, tandis que certaines équipes des cycles du primaire notent encore des lacunes dans l'exploitation complète des outils numériques.

    👉 **Points à retenir**
    - Continuer de soutenir et de développer les compétences numériques des enseignants dans certaines disciplines (notamment dans le primaire).
    - Favoriser les échanges de pratiques réussies entre matières pour améliorer l'usage du numérique.

    ---

    **2 - Évaluation formative**

    L’évaluation formative est utilisée par presque toutes les équipes avec une forte adhésion (100% dans la plupart des matières). L’objectif est de suivre les progrès des élèves et d’adapter les pratiques pédagogiques en fonction de leurs besoins. Les équipes enseignantes privilégient les évaluations orales et les travaux pratiques pour identifier rapidement les lacunes et proposer des aides personnalisées. Cela est particulièrement vrai pour les matières telles que les langues vivantes et les sciences.

    👉 **Points à retenir**
    - Encourager une plus grande diversification des pratiques d’évaluation formative dans toutes les matières.
    - Renforcer la mutualisation des pratiques évaluatives entre disciplines pour aider les élèves à mieux comprendre leurs progrès.

    ---

    **3 - Collaboration**

    Le niveau de collaboration entre enseignants varie fortement entre les matières. Certaines équipes, comme celles des langues et des sciences humaines, ont mis en place des projets interdisciplinaires qui encouragent les échanges (par exemple, autour de thèmes comme l'esclavage en histoire et anglais). D'autres équipes, particulièrement dans les matières plus techniques ou individuelles (comme la philosophie), éprouvent plus de difficultés à collaborer régulièrement. Il est souvent mentionné que la mise en place de plateformes de partage et de coordination serait bénéfique pour renforcer la collaboration.

    👉 **Points à retenir**
    - Promouvoir davantage de projets inter-matières qui encouragent la coopération pédagogique.
    - Mettre en place des outils et des plateformes pour faciliter la collaboration, en particulier dans les matières plus isolées (comme les matières littéraires ou les disciplines artistiques).

    ---

    **4 - Communication**

    La communication avec la vie scolaire est jugée peu satisfaisante dans l'ensemble, mais plusieurs équipes soulignent la nécessité d'une meilleure structuration des informations. L'utilisation de Pronote pour centraliser les communications est bien accueillie, mais certaines équipes estiment que des procédures devraient être plus claires et partagées de manière plus proactive, notamment concernant les sanctions et le suivi des absences. La création de groupes WhatsApp a aussi été évoquée comme solution de communication rapide.

    👉 **Points à retenir**
    - Améliorer la clarté des communications avec des règles et des procédures plus centralisées et bien partagées (par ex. sanctions, retards).
    - Faciliter l'accès à l'information en continuant à utiliser des outils numériques comme Pronote et en ajoutant des canaux de communication instantanée, si nécessaire.

    ---

    **5 - Bien-être et gestion du déménagement**

    Le déménagement semble avoir un impact modéré sur les équipes, avec des notes de satisfaction moyenne autour de 3 sur 5. Plusieurs améliorations ont été proposées, comme la gestion des salles et des emplois du temps, ainsi que l'amélioration de la communication concernant la maintenance et les problèmes urgents (comme les pannes dans les salles). Bien que des désagréments aient été signalés, il semble que les équipes pédagogiques restent résilientes et comprennent que ces perturbations sont temporaires.

    👉 **Points à retenir**
    - Renforcer la communication en amont concernant les changements logistiques pour éviter les frustrations liées à la maintenance ou à la gestion des espaces.
    - Poursuivre les ajustements liés aux espaces et à la gestion des emplois du temps afin d'améliorer le bien-être au travail.

    ---


    """

    )

    with st.container(border=True):
        st.markdown(
            """**Conclusion générale**
            Les équipes montrent une grande résilience et une forte capacité d'adaptation, notamment à travers l'intégration des outils numériques et des pratiques évaluatives. Cependant, il reste des points de progrès dans la collaboration interdisciplinaire, la structuration de la communication et la gestion du bien-être des enseignants. Il serait pertinent de capitaliser sur les réussites des matières qui intègrent déjà ces bonnes pratiques pour les diffuser au sein des autres équipes. Une meilleure coordination entre les équipes et un accompagnement supplémentaire dans les domaines identifiés comme fragiles seraient des leviers clés pour une amélioration continue."""
        )


with tab2 :
    st.write("")
    st.subheader('Analyse détaillé par équipe', divider="gray")


    st.write("Cette section présente une synthèse des enquêtes individuelles et des réunions d'équipe pour chaque groupe. Pour les équipes de plusieurs enseignants, des graphiques illustrent également les caractéristiques clés de leur fonctionnement. Les **indices** sont calculés à partir de plusieurs indicateurs clés, regroupés en trois dimensions principales ")

    st.markdown("""
    | **Indices**                                     | **Indicateurs**                                                                                                      |
    |-------------------------------------------------|----------------------------------------------------------------------------------------------------------------------|
    | 1. Collaboration pédagogique             | Taux de devoirs communs par enseignant<br>Taux de progressions pédagogiques communes<br>Taux de réunions par enseignant<br>Indice de collaboration perçue<br>Taux de projets interdisciplinaires par enseignant|
    | 2. Innovation pédagogique et numérique    | Indice d'utilisation des outils numériques<br>Indice d'impact perçu des outils numériques<br>Taux de participation aux formations<br>Taux d’utilisation des évaluations formatives|
    | 3. Indice d'engagement et de durabilité pédagogique | Taux de participation aux projets disciplinaires<br>Taux de participation aux projets durables<br>Taux de participation aux réunions pédagogiques<br>Ancienneté moyenne<br>Taux de collaboration avec la vie scolaire |
    """, unsafe_allow_html=True)


    st.markdown(
        """

        L’**indice global** est calculé comme la **moyenne** des trois indices principaux :

        1. **Indice de collaboration pédagogique**
        2. **Indice d’innovation pédagogique et numérique**
        3. **Indice d'engagement et de durabilité pédagogique**

        ⚠️ **Important : Ces indices ne doivent en aucun cas être interprétés comme un jugement absolu ou définitif.**

        Ils sont conçus pour **offrir des points de repère**, stimuler une réflexion collective et encourager un dialogue constructif, et non pour fournir des conclusions figées.
        """
    )




    with st.popover("Cadre et méthodologie"):
        st.markdown("""

    **Méthodologie**

    1. **Collecte et traitement des données**
    - Nous avons extrait les données depuis la base de **Pronote 2023-2024**, qui contiennent des informations sur les devoirs et le nombre de notes.
    - Ces données ont été combinées aux informations que vous avez partagées lors de **réunions d’équipes** ou dans les **formulaires individuels**.

    2. **Calcul des indices**
    - Nous avons calculé des indices **relatifs** pour chaque équipe.
    - Ces indices ne représentent pas des valeurs brutes ou objectives, mais plutôt une **comparaison entre équipes** selon les indicateurs disponibles.

    3. **Interprétation**
    - Les indices sont des **indicateurs comparatifs** et non absolus.
    - Cela signifie que :
        - **Les indices sont relatifs** : Ils montrent comment une équipe se positionne par rapport aux autres sur certains indicateurs (comme les devoirs ou les projets), mais ils ne reflètent pas une "vérité universelle" sur la qualité pédagogique.
        Par exemple, un indice plus bas peut simplement indiquer une méthodologie d'évaluation différente ou un contexte spécifique.
        - **Les données sont subjectives et variables** : Certaines équipes peuvent, par exemple, avoir des indicateurs plus faibles en raison de la nature des matières enseignées (certains cours demandent moins de projets, plus de devoirs individuels, etc.).

    ➡️ **L’indice est donc un point de départ pour la discussion, et non une fin en soi.**

    """)



    def plot_global_scores_sorted_with_gradient(scores_df):
            """
            Crée un diagramme en barres horizontales avec des couleurs graduelles
            pour comparer les scores globaux de toutes les équipes.
            """
            # Trier les équipes par leur moyenne globale (du plus grand au plus petit)
            scores_df_sorted = scores_df.sort_values(by='moyenne globale', ascending=False)

            # Création des couleurs graduelles en fonction des scores
            colors = scores_df_sorted['moyenne globale']

            # Créer un graphique en barres horizontales pour les scores globaux triés
            fig = go.Figure(go.Bar(
                x=scores_df_sorted['moyenne globale'],
                y=scores_df_sorted['équipe'],
                orientation='h',  # Barre horizontale
                marker=dict(
                    color=colors,  # Appliquer les couleurs basées sur les scores
                    colorscale='RdBu',  # Palette de couleurs graduelle Viridis
                    cmin=colors.min(),
                    cmax=colors.max(),
                    colorbar=dict(title="Moyenne")  # Légende pour la barre de couleurs
                ),
                text=[f'{val:.2f}' for val in scores_df_sorted['moyenne globale']],
                textposition='auto'
            ))

            # Mettre à jour les titres et la mise en forme
            fig.update_layout(
                yaxis=dict(categoryorder='total ascending'),  # Ordre des équipes du plus grand au plus petit
                template='plotly_white'
            )

            return fig  # Retourner le graphique pour qu'il soit affiché ou sauvegardé

    st.divider()
    st.write("**Classement global**")

    fig_global = plot_global_scores_sorted_with_gradient(df_scores_equipes)
    st.plotly_chart(fig_global, use_container_width=True)


    def plot_radar_equipe(equipe_name, scores_df):
            """
            Crée un diagramme en araignée pour visualiser les scores détaillés d'une équipe.

            Paramètres:
            - equipe_name : Le nom de l'équipe.
            - scores_df : Le DataFrame contenant les scores pour chaque équipe.
            """
            # Filtrer les scores de l'équipe donnée
            equipe_scores = scores_df[scores_df['équipe'] == equipe_name].iloc[0]

            # Extraire les catégories et les valeurs
            categories = ['Collaboration', 'Innovation pédagogique et numérique', 'Engagement et durabilité']
            valeurs = [
                equipe_scores['indice de collaboration'],
                equipe_scores["indice d'innovation pédagogique et numerique"],
                equipe_scores["indice d'engagement et de durabilite"]
            ]

            # Ajouter la première valeur à la fin pour fermer le cercle du radar
            valeurs += valeurs[:1]
            categories += categories[:1]

            # Créer le graphique radar
            fig = go.Figure(go.Scatterpolar(
                r=valeurs,
                theta=categories,
                fill='toself',
                name=equipe_name,
                marker=dict(
                    colorscale='Viridis'
                )
            ))

            # Mise en forme du graphique
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 0.8])
                ),
                # title=f'Scores détaillés pour l\'équipe : {equipe_name}',
                template='plotly_white'
            )

            return fig


    st.divider()
    st.write("**Detail par équipe disciplinaire**")


    with st.expander("Anglais"):

        fig_anglais = plot_radar_equipe('Anglais', df_scores_equipes)
        st.plotly_chart(fig_anglais, use_container_width=True)

        st.subheader("Informations générales")
        st.markdown("""
        - **Nombre de personnes dans l'équipe** : 6
        - **Ancienneté moyenne** : 3 ans
        """)

        st.subheader("Points positifs")
        st.markdown("""
        - Équipe solidaire malgré des parcours variés.
        - Bonne entente et motivation croissante.
        """)

        st.subheader("Points négatifs")
        st.markdown("""
        - Pratiques pédagogiques classiques par manque d'accompagnement.
        - Difficulté à gérer de nombreux EBEP.
        - Absence de tablettes et salle informatique non identifiée.
        """)

        st.subheader("Actions possibles")
        st.markdown("""
        - Organiser des formations pour évoluer vers des pratiques pédagogiques innovantes.
        - Fournir des outils numériques (tablettes) et créer un espace informatique dédié.
        - Offrir un soutien spécifique pour la gestion des EBEP.
        """)



        # Catégorie : Usage du numérique
        st.markdown("### Usage du numérique")
        st.markdown("""
        - **Fréquence** : 4.5
        - **Impact** : 4.3
        """)
        st.write("Résumé :")
        st.caption("""
        - Les réponses du questionnaire indiquent une utilisation variée et efficace du Tableau Blanc Interactif (TBI) dans l'enseignement.
        - Les enseignants utilisent le TBI pour enregistrer les exercices et les cours, facilitant ainsi leur diffusion sur des plateformes comme Pronote.
        - Ils utilisent également le TBI pour diffuser facilement des audios et des vidéos, rendant les cours plus interactifs et engageants.
        Les élèves sont ainsi actifs et acteurs de leur apprentissage. De plus, le TBI est utilisé pour enseigner et répondre en temps réel
        avec les élèves, leur permettant de voir et d'apprendre.
        """)

        # Catégorie : Évaluation formative
        st.markdown("### Évaluation formative")
        st.markdown("""
        - **Utilisation** : Oui (100%)
        """)
        st.write("Résumé :")
        st.caption("""
        Les réponses au questionnaire mettent en évidence une approche pédagogique différente si les élèves n'ont pas compris les notions enseignées.
        Cette approche est considérée comme essentielle pour identifier les lacunes et suivre les progrès de chaque élève, en particulier ceux qui
        rencontrent des difficultés. Une évaluation orale est utilisée pour observer comment les élèves prononcent les mots ou les phrases, ce qui
        permet d'apporter une aide personnalisée. Cette méthode est également utile pour identifier les erreurs persistantes et les lacunes en
        vocabulaire et en grammaire.
        """)

        # Catégorie : Collaboration
        st.markdown("### Collaboration")
        st.markdown("""
        - **Niveau de collaboration** : 4.3
        """)
        st.write("Résumé :")
        st.caption("""
        L'évaluation de l'équipe, bien que nouvelle, indique une collaboration satisfaisante, notamment grâce à des discussions régulières et informelles.
        Toutefois, l'efficacité de cette collaboration pourrait être améliorée grâce à la mise en place de projets communs sur des thèmes spécifiques,
        comme l'esclavage en 4ème, qui pourrait être abordé non seulement en histoire et en anglais, mais aussi en français et en éducation musicale.
        """)

        # Catégorie : Communication
        st.markdown("### Communication")
        st.markdown("""
        - **Satisfaction vie scolaire** : 3
        """)
        st.write("Résumé :")
        st.caption("""
        Les répondants s'accordent à dire que le moyen de communication doit être rapide et efficace, avec une suggestion d'utilisation de PRONOTE pour
        les discussions. Il est également recommandé de simplifier et de centraliser les procédures via des mails ou PRONOTE, avec des rappels réguliers
        pour garder tout le monde informé.
        """)

        # Catégorie : Bien-être
        st.markdown("### Bien-être")
        st.markdown("""
        - **Impact du déménagement** : 3
        """)
        st.write("Résumé :")
        st.caption("""
        Les réponses au questionnaire soulignent la nécessité de distinguer entre les situations qui nécessitent une intervention urgente et celles qui
        peuvent attendre. Par exemple, les problèmes de poignées cassées, bien que considérés comme des détails, ont causé des désagréments importants,
        entraînant des collègues à être enfermés dans des salles ou dans les couloirs. La maintenance a été alertée mais n'a pas pu intervenir rapidement.
        """)

    with st.expander("Arabe"):

        fig_arabe = plot_radar_equipe('Arabe', df_scores_equipes)
        st.plotly_chart(fig_arabe, use_container_width=True)

        st.subheader("Informations générales")
        st.markdown("""
        - **Nombre de personnes dans l'équipe** : 9
        - **Ancienneté moyenne** : 4.3 ans
        """)

        st.subheader("Points positifs")
        st.markdown("""
        - Équipe dynamique et agréable.
        - Projets annuels et voyages pédagogiques organisés (Paris, Andalousie).
        """)

        st.subheader("Points négatifs")
        st.markdown("""
        Aucun point négatif relevé.
        """)

        st.subheader("Actions possibles")
        st.markdown("""
        - Continuer l’accompagnement des collègues dans les projets et les voyages pédagogiques.
        """)



        # Catégorie : Usage du numérique
        st.markdown("### Usage du numérique")
        st.markdown("""
        - **Fréquence** : 4.1
        - **Impact** : 4.1
        """)
        st.write("Résumé :")
        st.caption("""
        Les réponses du questionnaire mettent en évidence l'importance de divers outils technologiques dans l'enseignement. L'écran interactif est apprécié pour ses nombreuses possibilités d'explication et d'analyse, combinant les fonctionnalités d'un tableau interactif et d'un ordinateur personnel. Des plateformes comme Google Classroom sont plébiscitées pour leur facilité d'organisation des cours, le partage de ressources, le suivi des progrès des étudiants et la centralisation des matériaux pédagogiques. Des outils tels que Wordwall sont utilisés pour rendre les évaluations plus interactives et engageantes.
        """)

        # Catégorie : Évaluation formative
        st.markdown("### Évaluation formative")
        st.markdown("""
        - **Utilisation** : Oui (100%)
        """)
        st.write("Résumé :")
        st.caption("""
        L'évaluation formative est un outil essentiel qui permet de découvrir les faiblesses des élèves, mais aussi de favoriser leur participation active à la construction de leurs apprentissages. Elle permet de faire le point sur les acquis des apprenants tout en favorisant la compréhension des erreurs commises, sans les sanctionner. Cela accélère la progression des apprenants en ciblant des compétences précises et en identifiant les besoins réels des élèves. Cela aide à adapter les pratiques pédagogiques pour chaque élève, afin de les aider à progresser. L'évaluation formative permet également d'identifier les forces.
        """)

        # Catégorie : Collaboration
        st.markdown("### Collaboration")
        st.markdown("""
        - **Niveau de collaboration** : 4.3
        """)
        st.write("Résumé :")
        st.caption("""
        Les réponses au questionnaire mettent en avant l'importance de valoriser et renforcer le travail d'équipe. Cela peut se faire en définissant des objectifs et des responsabilités clairs pour les équipes, en favorisant une communication fluide et multicanale, en encourageant une culture du feedback et en favorisant le développement et le partage des connaissances. Il est également essentiel de choisir les méthodes adaptées pour gérer l'équipe et ses missions. L'amélioration de la collaboration peut être encouragée par des réunions régulières, des ateliers de formation et des projets communs, tous axés sur des échanges.
        """)

        # Catégorie : Communication
        st.markdown("### Communication")
        st.markdown("""
        - **Satisfaction vie scolaire** : 3
        """)
        st.write("Résumé :")
        st.caption("""
        Les réponses du questionnaire soulignent l'importance d'adopter une approche participative dans la vie scolaire. Il est essentiel d'assurer l'accessibilité numérique, en partageant toutes les informations de manière efficace et facilement accessible via Pronote. Pour faciliter l'accessibilité, les procédures de la vie scolaire doivent être expliquées en utilisant un langage simple et des guides visuels ou numériques faciles à consulter devraient être créés. Il est également important d'identifier clairement les personnes référentes pour chaque procédure et niveau. La mise en place d'une plateforme en ligne est suggérée.
        """)

        # Catégorie : Bien-être
        st.markdown("### Bien-être")
        st.markdown("""
        - **Impact du déménagement** : 3
        """)
        st.write("Résumé :")
        st.caption("""
        Suite au déménagement, les enseignants ont souligné l'importance d'une bonne planification et d'une communication efficace pour faciliter le processus. Ils ont également apprécié l'aide offerte et le soutien émotionnel reçu, qui ont rendu la transition plus facile pour eux. Un calendrier détaillé et partagé a été identifié comme un outil utile pour organiser le déménagement.
        """)

    with st.expander("Cycle 1"):

        fig_cycle_1 = plot_radar_equipe('cycle 1', df_scores_equipes)
        st.plotly_chart(fig_cycle_1, use_container_width=True)

        st.subheader("Informations générales")
        st.markdown("""
        - **Nombre de personnes dans l'équipe** : 3
        - **Ancienneté moyenne** : 8 ans
        """)

        st.subheader("Points positifs")
        st.markdown("""
        - Équipe soudée.
        - Volonté d'ouvrir l'école aux parents et de les inclure aux événements.
        - Projets pédagogiques à valoriser.
        """)

        st.subheader("Points négatifs")
        st.markdown("""
        - Deux collègues en souffrance à cause de plusieurs obstacles matériels (toilettes non adaptées, chaleur dans les classes).
        - Mauvaise configuration des tableaux interactifs pour les enfants.
        - Restrictions pédagogiques (limitation des photocopies, impossibilité d'afficher les productions).
        - Déséquilibres dans la répartition des classes (11 PS / 4 GS).
        """)

        st.subheader("Actions possibles")
        st.markdown("""
        - Aménager les espaces pour réduire la chaleur (par exemple, échange des classes avec le dortoir).
        - Installer des tableaux blancs pour réduire l'exposition aux écrans.
        - Mettre en place des barrettes de liège pour l’affichage afin de ne pas endommager les murs.
        - Revoir la répartition des classes.
        """)


        # Catégorie : Usage du numérique
        st.markdown("### Usage du numérique")
        st.markdown("""
        - **Fréquence** : 2.3
        - **Impact** : 2.3
        """)
        st.write("Résumé :")
        st.caption("""
        Les résultats du questionnaire indiquent que les tablettes sont perçues comme des outils facilement manipulables et particulièrement adaptés aux enfants en maternelle.
        Leur utilisation semble donc être une méthode efficace et appropriée pour l'enseignement à cet âge.
        """)

        # Catégorie : Évaluation formative
        st.markdown("### Évaluation formative")
        st.markdown("""
        - **Utilisation** : Oui (60%)
        """)
        st.write("Résumé :")
        st.caption("""
        Les réponses au questionnaire indiquent que l'outil est utilisé pour identifier les points forts et les points faibles des élèves.
        Cette identification aide ensuite à proposer des ateliers différenciés, conçus pour répondre aux besoins spécifiques de chaque élève.
        De plus, ce processus permet également d'évaluer les besoins d'apprentissage des élèves afin de mieux cerner leurs lacunes et d'y apporter des solutions appropriées.
        """)

        # Catégorie : Collaboration
        st.markdown("### Collaboration")
        st.markdown("""
        - **Niveau de collaboration** : 4.3
        """)
        st.write("Résumé :")
        st.caption("""
        Non spécifié dans les réponses fournies.
        """)

        # Catégorie : Communication
        st.markdown("### Communication")
        st.markdown("""
        - **Satisfaction vie scolaire** : 3
        """)
        st.write("Résumé :")
        st.caption("""
        Non spécifié dans les réponses fournies.
        """)

        # Catégorie : Bien-être
        st.markdown("### Bien-être")
        st.markdown("""
        - **Impact du déménagement** : 3
        """)
        st.write("Résumé :")
        st.caption("""
        Les participants ont souligné la nécessité d'une meilleure gestion des priorités, notamment en termes de maintenance. Ils ont cité l'exemple de poignées de porte cassées
        qui ont entravé leur travail quotidien, et ont exprimé une certaine frustration face à la lenteur des interventions. Par ailleurs, un sentiment d'impuissance a été ressenti
        face à des problèmes persistants qui auraient pu être résolus rapidement. Néanmoins, certains participants ont appelé à la patience, rappelant que c'est la première année
        dans un nouvel environnement et qu'ils espèrent une transition plus facile l'année prochaine.
        """)

    with st.expander("Cycle 2"):

        fig_cycle_2 = plot_radar_equipe('cycle 2', df_scores_equipes)
        st.plotly_chart(fig_cycle_2, use_container_width=True)

        st.subheader("Informations générales")
        st.markdown("""
        - **Nombre de personnes dans l'équipe** : 6
        - **Ancienneté moyenne** : 6,2 ans
        """)

        st.subheader("Points positifs")
        st.markdown("""
        - Équipe stable depuis plusieurs années.
        - Travail par niveau bien organisé.
        """)

        st.subheader("Points négatifs")
        st.markdown("""
        - Souffrance liée à la gestion des classes à double niveau et aux effectifs chargés (32-33 élèves).
        - Présence de nombreux EBEP.
        - Difficultés matérielles (photocopies, mobilier, écrans).
        - Manque de consultation pour les méthodes pédagogiques et le mobilier.
        """)

        st.subheader("Actions possibles")
        st.markdown("""
        - Revoir l’organisation des classes à double niveau.
        - Allouer des heures d'APC supplémentaires pour les EBEP.
        - Mettre à disposition des outils pédagogiques adaptés (écrans à la bonne hauteur, mobilier ajusté).
        - Créer un cadre de concertation pour les choix pédagogiques.
        """)


        # Catégorie : Usage du numérique
        st.markdown("### Usage du numérique")
        st.markdown("""
        - **Fréquence** : 3,7
        - **Impact** : 3,2
        """)
        st.write("Résumé :")
        st.caption("""
        Les répondants ont souligné l'utilité des technologies numériques dans l'enseignement, notamment le Tableau Blanc Interactif (TBI) qui permet aux élèves, en particulier en CP,
        de mieux se repérer dans l'espace. La projection de manuels et de vidéos numériques via le TBI facilite également la compréhension des élèves et l'utilisation de leurs supports
        de travail pendant les consignes et les corrections. L'accès rapide à internet via le TBI est également apprécié pour diversifier les supports pédagogiques.
        Les plateformes telles que Classroom, Magic School, Chat GPT, Slide, Docs, Quizinière sont fréquemment utilisées.
        """)

        # Catégorie : Évaluation formative
        st.markdown("### Évaluation formative")
        st.markdown("""
        - **Utilisation** : Oui (100%)
        """)
        st.write("Résumé :")
        st.caption("""
        L'évaluation joue un rôle crucial dans l'enseignement, car elle permet d'identifier les compétences que les élèves sont en train d'acquérir ou n'ont pas encore acquises.
        Cela offre la possibilité de créer des groupes de besoins spécifiques pour une remédiation ciblée, soit lors de sessions spéciales en classe, soit dans le cadre d'activités pédagogiques
        complémentaires. L'évaluation formative est un outil précieux pour l'enseignant, car elle permet d'adapter et de varier les supports pédagogiques pour aider l'élève à acquérir
        les compétences visées.
        """)

        # Catégorie : Collaboration
        st.markdown("### Collaboration")
        st.markdown("""
        - **Niveau de collaboration** : 4,3
        """)
        st.write("Résumé :")
        st.caption("""
        Les répondants du questionnaire souhaitent disposer de plus de temps pour se rencontrer dans des contextes informels, afin de renforcer la cohésion de l'équipe.
        Ils souhaitent également que des espaces communs soient mis à disposition pour réaliser des activités sportives ou autres, qui favoriseraient le mélange entre les professeurs de tous
        les niveaux et le personnel administratif. Ces activités permettraient à tous de mieux se connaître et de partager des expériences. Ils proposent également l'organisation de
        cafés pédagogiques au sein de l'établissement, ainsi qu'une ou deux sorties amicales entre les professeurs.
        """)

        # Catégorie : Communication
        st.markdown("### Communication")
        st.markdown("""
        - **Satisfaction vie scolaire** : 3
        """)
        st.write("Résumé :")
        st.caption("""
        Le répondant a exprimé une insatisfaction générale envers le questionnaire, le jugeant inadapté à son contexte spécifique qui est l'éducation primaire.
        Il souligne également un manque de relation avec la vie scolaire, indiquant que les questions posées n'ont pas de pertinence pour lui.
        """)

        # Catégorie : Bien-être
        st.markdown("### Bien-être")
        st.markdown("""
        - **Impact du déménagement** : 3
        """)
        st.write("Résumé :")
        st.caption("""
        Les réponses au questionnaire soulignent une série de problèmes et de suggestions concernant notre nouvel environnement de travail.
        Il y a une préoccupation majeure concernant la différenciation entre les problèmes qui nécessitent une intervention rapide et ceux qui peuvent attendre.
        Par exemple, la question des poignées de porte cassées a été minimisée, mais cela a conduit à des situations embarrassantes où le personnel se retrouvait enfermé dans des salles ou
        des couloirs. La maintenance a été informée, mais n'a pas pu intervenir rapidement, ce qui a exacerbé le sentiment d'impuissance. Cependant, il y a une reconnaissance que nous devons
        être patients, car ce n'est que la première année dans ce nouvel environnement.
        """)

    with st.expander("Cycle 3"):

        fig_cycle_3 = plot_radar_equipe('cycle 3', df_scores_equipes)
        st.plotly_chart(fig_cycle_3, use_container_width=True)


        st.subheader("Informations générales")
        st.markdown("""
        - **Nombre de personnes dans l'équipe** : 4
        - **Ancienneté moyenne** : 6,5 ans
        """)

        st.subheader("Points positifs")
        st.markdown("""
        - Équipe stable et dynamique avec un leader.
        """)

        st.subheader("Points négatifs")
        st.markdown("""
        - Un membre en souffrance psychologique.
        - Classes chargées.
        - Restrictions matérielles perçues comme un retour en arrière (espace, photocopies).
        """)

        st.subheader("Actions possibles")
        st.markdown("""
        - Organiser des soutiens psychologiques pour les membres en souffrance.
        - Fournir des manuels adaptés pour alléger la charge de travail.
        - Réviser les règles de photocopies et améliorer les équipements matériels.
        """)

        # Catégorie : Usage du numérique
        st.markdown("### Usage du numérique")
        st.markdown("""
        - **Fréquence** : 4,5
        - **Impact** : 4
        """)
        st.write("Résumé :")
        st.caption("""
        Les réponses au questionnaire soulignent l'importance et l'efficacité de divers outils numériques dans l'éducation.
        L'outil Book Creator est apprécié pour son potentiel créatif, permettant aux élèves de créer leurs propres livres numériques avec du texte, des images et des dessins.
        Google Classroom est mentionné pour sa facilité d'utilisation et sa capacité à améliorer la communication en classe, ainsi que la gestion des travaux et devoirs.
        Les outils interactifs comme le TBI et Slide sont valorisés pour leur capacité à améliorer l'engagement des élèves et rendre l'apprentissage plus dynamique.
        """)

        # Catégorie : Évaluation formative
        st.markdown("### Évaluation formative")
        st.markdown("""
        - **Utilisation** : Oui (100%)
        """)
        st.write("Résumé :")
        st.caption("""
        L'évaluation formative est considérée comme le pilier de la remédiation et de la différenciation, permettant d'ajuster les pratiques pédagogiques en fonction des besoins immédiats des élèves.
        Elle favorise l'identification des points forts des élèves et les notions à renforcer, améliorant ainsi leurs résultats en les impliquant activement dans leur progression.
        L'évaluation formative offre un feedback continu, adapte l'enseignement aux besoins des élèves, les motive et améliore leurs performances.
        Elle est jugée indispensable car elle permet à l'élève de vérifier son niveau d'avancement dans l'acquisition des compétences.
        """)

        # Catégorie : Collaboration
        st.markdown("### Collaboration")
        st.markdown("""
        - **Niveau de collaboration** : 4,3
        """)
        st.write("Résumé :")
        st.caption("""
        L'équipe de CM2, composée d'enseignants de français, arabe et anglais, a mis l'accent sur la collaboration et l'amélioration continue dans un environnement bienveillant et jovial.
        Elle travaille à harmoniser les pratiques pour uniformiser le niveau des élèves à l'approche de leurs années collège, en se concentrant sur des projets de niveau en trois langues.
        Pourtant, malgré des temps de concertation hebdomadaires, l'équipe rencontre des difficultés pour maîtriser les séances de co-enseignement et de co-intervention,
        probablement dues à un manque de temps, de pratique et d'expertise.
        """)

        # Catégorie : Communication
        st.markdown("### Communication")
        st.markdown("""
        - **Satisfaction vie scolaire** : 3
        """)
        st.write("Résumé :")
        st.caption("""
        Les réponses au questionnaire révèlent deux problématiques principales dans l'environnement scolaire primaire.
        D'une part, il y a une déconnexion entre la vie scolaire et la direction, exacerbée par des circonstances exceptionnelles telles que le changement de direction et de site.
        Cela crée une situation où les décisions sont prises sans consultation préalable, ce qui conduit à des changements imprévus et perturbe le bon déroulement des activités.
        D'autre part, malgré le manque de ressources humaines, il y a une volonté manifeste de mettre en place des processus pour remédier aux dysfonctionnements.
        """)

        # Catégorie : Bien-être
        st.markdown("### Bien-être")
        st.markdown("""
        - **Impact du déménagement** : 3
        """)
        st.write("Résumé :")
        st.caption("""
        Les réponses au questionnaire indiquent une satisfaction générale concernant le nouveau site, notamment en raison de son emplacement central, de ses équipements modernes et d'une direction dynamique et réactive.
        Cependant, des problèmes ont été soulignés concernant l'adaptation des infrastructures aux besoins des élèves, notamment des toilettes inaccessibles depuis la cour de récréation primaire et des classes mal adaptées.
        Il a été noté un manque d'anticipation et de considération pour ces besoins, ce qui a entraîné des désagréments et une impression de retour en arrière.
        """)

    with st.expander("EPS"):

        fig_eps = plot_radar_equipe('Éducation physique et sportive', df_scores_equipes)
        st.plotly_chart(fig_eps, use_container_width=True)

        st.subheader("Informations générales")
        st.markdown("""
        - **Nombre de personnes dans l'équipe** : 4
        - **Ancienneté moyenne** : 2,8 ans
        """)

        st.subheader("Points positifs")
        st.markdown("""
        - Équipe soudée et solidaire.
        - Bonne répartition des tâches.
        - Association sportive en développement avec 100 inscrits.
        """)

        st.subheader("Points négatifs")
        st.markdown("""
        - Problème de programmation des classes à cause de l'absence de barrette.
        - Problème de sécurité : passage des élèves sur la piste de course et carrelage glissant dans les vestiaires.
        - Besoin de formation pour le mur d’escalade.
        """)

        st.subheader("Actions possibles")
        st.markdown("""
        - Revoir l’organisation des créneaux horaires pour éviter les chevauchements d’activités.
        - Améliorer la sécurité des installations (piste de course, vestiaires).
        - Organiser une formation pour l’utilisation du mur d’escalade.
        """)


        # Catégorie : Usage du numérique
        st.markdown("### Usage du numérique")
        st.markdown("""
        - **Fréquence** : 2,5
        - **Impact** : 3,5
        """)
        st.write("Résumé :")
        st.caption("""
        Les réponses au questionnaire indiquent que les outils tels que Pronote, H5P et Classroom sont largement utilisés dans l'enseignement.
        Pronote est apprécié pour sa fonctionnalité d'observation qui permet de fournir un feedback aux élèves et aux parents.
        L'intégration d'outils interactifs comme H5P dans des plateformes comme Classroom ou Pronote est souhaitée, en particulier si cela peut être complété
        par l'intelligence artificielle pour optimiser le temps. Par ailleurs, l'outil vidéo est particulièrement utile en EPS pour aider les élèves à améliorer leur pratique.
        """)

        # Catégorie : Évaluation formative
        st.markdown("### Évaluation formative")
        st.markdown("""
        - **Utilisation** : Oui (100%)
        """)
        st.write("Résumé :")
        st.caption("""
        L'évaluation formative est un outil essentiel qui permet aux élèves de se situer à chaque cours, en leur fournissant un retour sur leur pratique.
        Cela les incite à être plus attentifs et actifs en cours, tout en permettant d'adapter les méthodes d'enseignement en fonction de leurs besoins spécifiques.
        Cette approche favorise leur progression et renforce leur confiance, conduisant à de meilleurs résultats tant sur le plan sportif que personnel.
        """)

        # Catégorie : Collaboration
        st.markdown("### Collaboration")
        st.markdown("""
        - **Niveau de collaboration** : 4,3
        """)
        st.write("Résumé :")
        st.caption("""
        Les répondants du questionnaire soulignent l'importance d'accorder une rémunération aux enseignants impliqués dans la partie administrative de l'association sportive d'EPS.
        Ils insistent également sur la nécessité de mettre en place une planification rigoureuse pour l'association, comprenant des objectifs clairs, des étapes nécessaires pour les atteindre,
        et une gestion efficace des tâches principales.
        """)

        # Catégorie : Communication
        st.markdown("### Communication")
        st.markdown("""
        - **Satisfaction vie scolaire** : 3
        """)
        st.write("Résumé :")
        st.caption("""
        Les répondants au questionnaire ont exprimé le besoin de créer un guide qui récapitule les pratiques communes pour faciliter la vie scolaire.
        Ils ont souligné l'importance de la collaboration et de la dynamique au sein des membres de la communauté scolaire pour mettre en œuvre efficacement ce guide.
        """)

        # Catégorie : Bien-être
        st.markdown("### Bien-être")
        st.markdown("""
        - **Impact du déménagement** : 3
        """)
        st.write("Résumé :")
        st.caption("""
        Les réponses au questionnaire indiquent une grande satisfaction envers la direction, qui est perçue comme réactive, dynamique et à l'écoute.
        Cependant, une suggestion a été proposée pour améliorer la communication et l'efficacité : la réalisation d'un sondage pour comprendre les préoccupations et les besoins en matériels des enseignants.
        Cette approche pourrait permettre de cibler plus précisément les besoins et d'y répondre de manière plus adaptée.
        """)

    with st.expander("Espagnol"):

        fig_esp = plot_radar_equipe('Espagnol', df_scores_equipes)
        st.plotly_chart(fig_esp, use_container_width=True)

        st.subheader("Informations générales")
        st.markdown("""
        - **Nombre de personnes dans l'équipe** : 3
        - **Ancienneté moyenne** : 2,3 ans
        """)

        st.subheader("Points positifs")
        st.markdown("""
        - Équipe communiquant régulièrement.
        - Projets de voyages avec l'équipe d'arabe et volonté de réaliser des devoirs communs au lycée.
        """)

        st.subheader("Points négatifs")
        st.markdown("""
        - Difficulté à pratiquer l'expression orale avec des classes de 30 élèves.
        - Manque de mobilier nécessitant des déplacements entre les salles.
        """)

        st.subheader("Actions possibles")
        st.markdown("""
        - Réduire le nombre d'élèves pour faciliter la pratique orale.
        - Acheter du mobilier supplémentaire pour éviter les déplacements de matériel.
        """)


        # Catégorie : Usage du numérique
        st.markdown("### Usage du numérique")
        st.markdown("""
        - **Fréquence** : 5
        - **Impact** : 3,7
        """)
        st.write("Résumé :")
        st.caption("""
        Les participants du questionnaire ont indiqué une préférence pour des outils simples qui ne nécessitent pas d'apprentissage spécifique pour les élèves.
        Des outils tels que Canoprof, Quizinière et ceux fournis par ladigitale.dev ont été mentionnés. Padlet, Quizzalise et Office ont également été cités comme des ressources utiles.
        En ce qui concerne l'enseignement des langues, les applications ou sites web d'audio et de vidéo sont privilégiés car ils facilitent le travail sur la partie orale.
        """)

        # Catégorie : Évaluation formative
        st.markdown("### Évaluation formative")
        st.markdown("""
        - **Utilisation** : Oui (100%)
        """)
        st.write("Résumé :")
        st.caption("""
        L'évaluation formative est perçue comme une plus-value significative, surtout pour les élèves déjà motivés et équipés d'outils de travail adéquats.
        Elle offre une compréhension concrète des attentes de la séquence d'apprentissage.
        De plus, son influence positive est ressentie dans la révision du contenu étudié en cours, servant également à familiariser les élèves avec des activités similaires à celles de l'évaluation,
        améliorant ainsi leur préparation et leur performance.
        """)

        # Catégorie : Collaboration
        st.markdown("### Collaboration")
        st.markdown("""
        - **Niveau de collaboration** : 4,2
        """)
        st.write("Résumé :")
        st.caption("""
        Les réponses au questionnaire indiquent que l'efficacité des projets est améliorée en augmentant leur visibilité, en les présentant de manière appropriée et en recrutant des membres d'équipe avec des compétences spécifiques adaptées à chaque projet.
        Cela souligne l'importance d'une bonne gestion de projet et d'un recrutement stratégique.
        Par ailleurs, il est à noter que la dynamique de collaboration actuelle est perçue comme positive, ce qui est un point fort à maintenir et à développer davantage.
        """)

        # Catégorie : Communication
        st.markdown("### Communication")
        st.markdown("""
        - **Satisfaction vie scolaire** : 3
        """)
        st.write("Résumé :")
        st.caption("""
        Les réponses du questionnaire mettent en avant l'importance de la création de documents précis et leur diffusion à tous, en particulier au service de la vie scolaire, afin d'harmoniser les informations.
        Bien que le service de la vie scolaire soit jugé efficace, l'idée d'y intégrer davantage d'assistants est suggérée afin d'optimiser la présence du personnel dans les couloirs et la cour, rendant ainsi le service plus accessible.
        """)

        # Catégorie : Bien-être
        st.markdown("### Bien-être")
        st.markdown("""
        - **Impact du déménagement** : 3
        """)
        st.write("Résumé :")
        st.caption("""
        Les réponses au questionnaire indiquent un intérêt pour la création d'un pôle d'écoute et d'information qui serait mis en place de manière ponctuelle.
        Ce pôle aurait pour objectif de répondre aux besoins et aux interrogations des personnes concernées.
        """)

    with st.expander("Français"):

        fig_fr = plot_radar_equipe('Français', df_scores_equipes)
        st.plotly_chart(fig_fr, use_container_width=True)


        st.subheader("Informations générales")
        st.markdown("""
        - **Nombre de personnes dans l'équipe** : 5
        - **Ancienneté moyenne** : 3,8 ans
        """)

        st.subheader("Points positifs")
        st.markdown("""
        - Équipe dynamique et communicative.
        - Volonté de poursuivre les pratiques autour de la culture et du théâtre.
        """)

        st.subheader("Points négatifs")
        st.markdown("""
        - Absence de travail collaboratif autour des œuvres étudiées.
        - Manque de partage des supports et des contenus pédagogiques.
        """)

        st.subheader("Actions possibles")
        st.markdown("""
        - Créer un drive partagé pour faciliter l’échange de supports pédagogiques.
        - Mettre en place des réunions régulières pour harmoniser les pratiques autour des œuvres étudiées.
        """)

        # Catégorie : Usage du numérique
        st.markdown("### Usage du numérique")
        st.markdown("""
        - **Fréquence** : 3,6
        - **Impact** : 3,2
        """)
        st.write("Résumé :")
        st.caption("""
        Les outils numériques comme le TBI et des plateformes collaboratives telles que Classroom ou Google Drive sont utilisés pour enrichir les cours et permettre le partage de ressources pédagogiques.
        Cependant, leur usage reste encore limité pour certains enseignants, qui expriment un besoin de formation pour en tirer pleinement parti, notamment pour la création de supports interactifs.
        """)

        # Catégorie : Évaluation formative
        st.markdown("### Évaluation formative")
        st.markdown("""
        - **Utilisation** : Oui (90%)
        """)
        st.write("Résumé :")
        st.caption("""
        L'évaluation formative est couramment utilisée pour accompagner les élèves dans leur progression, notamment via des exercices de rédaction et des discussions autour des textes étudiés.
        Cette approche permet de suivre les progrès des élèves et de corriger leurs erreurs tout au long de l'apprentissage, favorisant ainsi une compréhension plus approfondie des œuvres étudiées.
        """)

        # Catégorie : Collaboration
        st.markdown("### Collaboration")
        st.markdown("""
        - **Niveau de collaboration** : 3,5
        """)
        st.write("Résumé :")
        st.caption("""
        Les membres de l'équipe de français collaborent occasionnellement pour partager des idées et des ressources, mais l'absence d'un espace centralisé pour l'échange limite l'efficacité de ces collaborations.
        Ils expriment le souhait de mettre en place des pratiques collaboratives plus régulières, telles que des ateliers d'échange et des projets interdisciplinaires.
        """)

        # Catégorie : Communication
        st.markdown("### Communication")
        st.markdown("""
        - **Satisfaction vie scolaire** : 3,7
        """)
        st.write("Résumé :")
        st.caption("""
        Les enseignants soulignent un bon niveau de communication avec la vie scolaire, mais identifient des lacunes dans le partage d'informations sur les projets pédagogiques transversaux.
        Une meilleure coordination pourrait permettre de développer davantage de synergies entre les enseignants et la vie scolaire.
        """)

        # Catégorie : Bien-être
        st.markdown("### Bien-être")
        st.markdown("""
        - **Impact du déménagement** : 3,5
        """)
        st.write("Résumé :")
        st.caption("""
        Les réponses au questionnaire révèlent une satisfaction générale vis-à-vis des nouveaux espaces, mais certains enseignants notent un manque de confort dans certaines salles, comme l'absence de supports d'affichage adaptés.
        Une meilleure adaptation des infrastructures aux besoins pédagogiques est suggérée pour améliorer l'expérience enseignante.
        """)

    with st.expander("Histoire-géographie"):

        fig_hg = plot_radar_equipe('Histoire-géographie', df_scores_equipes)
        st.plotly_chart(fig_hg, use_container_width=True)

        st.subheader("Informations générales")
        st.markdown("""
        - **Nombre de personnes dans l'équipe** : 5
        - **Ancienneté moyenne** : 2,6 ans
        """)

        st.subheader("Points positifs")
        st.markdown("""
        - Équipe dynamique et travaillant efficacement.
        """)

        st.subheader("Points négatifs")
        st.markdown("""
        - Difficulté à gérer les nombreux EBEP regroupés avec les élèves non arabophones.
        - Lourdeur du programme de 3e avec l'ajout du programme marocain.
        """)

        st.subheader("Actions possibles")
        st.markdown("""
        - Mettre en place des formations spécifiques sur la gestion des EBEP en présence du référent EBEP de l’établissement.
        - Réfléchir à des ajustements du programme de 3e pour alléger la charge.
        """)


        # Catégorie : Usage du numérique
        st.markdown("### Usage du numérique")
        st.markdown("""
        - **Fréquence** : 3,8
        - **Impact** : 3,2
        """)
        st.write("Résumé :")
        st.caption("""
        Les réponses recueillies indiquent une préférence pour l'utilisation de supports numériques variés dans le cadre de l'éducation.
        Les participants mentionnent l'usage des documents vidéo pour diversifier le contenu, ainsi que l'emploi de tableaux interactifs pour favoriser l'interaction avec les documents et les connaissances.
        L'utilisation de l'ordinateur et du vidéoprojecteur est également soulignée, ces outils permettant de travailler sur des sources variées et de concentrer l'attention des apprenants en un seul endroit.
        """)

        # Catégorie : Évaluation formative
        st.markdown("### Évaluation formative")
        st.markdown("""
        - **Utilisation** : Oui (100%)
        """)
        st.write("Résumé :")
        st.caption("""
        L'évaluation formative est principalement réalisée à l'oral, au début et à la fin de chaque heure, ainsi que dans les activités autonomes ou de groupe.
        Cette méthode est une partie intégrante du cœur du cours car elle permet d'expliquer et d'expliciter les démarches.
        Elle offre aux élèves l'opportunité de travailler certaines compétences et attentes, tout en bénéficiant d'un retour de leur enseignant.
        """)

        # Catégorie : Collaboration
        st.markdown("### Collaboration")
        st.markdown("""
        - **Niveau de collaboration** : 4,3
        """)
        st.write("Résumé :")
        st.caption("""
        En synthèse, les réponses au questionnaire indiquent un besoin de temps supplémentaire pour la concertation et l'échange de pratiques, comme les visites de classe ou la coanimation.
        Les participants apprécient la solidarité de l'équipe et les discussions constantes sur les différentes méthodes de travail.
        Ils expriment le souhait d'un dialogue accru sur les attentes et les exigences, en particulier au niveau du lycée.
        """)

        # Catégorie : Communication
        st.markdown("### Communication")
        st.markdown("""
        - **Satisfaction vie scolaire** : 3
        """)
        st.write("Résumé :")
        st.caption("""
        Les réponses au questionnaire indiquent une difficulté dans le suivi des élèves et des procédures initiées, notamment en ce qui concerne les retards et les absences qui ne sont pas toujours suivis de sanctions ou d'entretiens.
        Les enseignants se sentent souvent comme les interlocuteurs principaux des parents et des élèves, même lorsque certaines questions ne relèvent pas directement de leur responsabilité.
        Il y a un besoin exprimé pour des procédures claires, un cadre commun et une collaboration plus étroite entre la vie scolaire et les enseignants.
        """)

        # Catégorie : Bien-être
        st.markdown("### Bien-être")
        st.markdown("""
        - **Impact du déménagement** : 3
        """)
        st.write("Résumé :")
        st.caption("""
        Les réponses au questionnaire soulignent l'importance d'une bonne communication dans le cadre pédagogique.
        Elles mettent en lumière des problématiques spécifiques liées aux changements fréquents de salle d'enseignement.
        Ces changements peuvent réduire le temps de cours, compliquer la gestion de classe avec un plan de classe difficile à mettre en œuvre et empêcher l'utilisation des murs à des fins pédagogiques.
        """)

    with st.expander("Mathématiques"):

        fig_maths = plot_radar_equipe('Mathématiques', df_scores_equipes)
        st.plotly_chart(fig_maths, use_container_width=True)

        st.subheader("Informations générales")
        st.markdown("""
        - **Nombre de personnes dans l'équipe** : 6
        - **Ancienneté moyenne** : 3,4 ans
        """)

        st.subheader("Points positifs")
        st.markdown("""
        - Équipe soudée avec des compétences complémentaires (référent numérique, nouvelles technologies).
        - Forte envie de participer à des projets de réseau.
        """)

        st.subheader("Points négatifs")
        st.markdown("""
        - Difficulté initiale à utiliser les nouveaux tableaux interactifs (en amélioration).
        """)

        st.subheader("Actions possibles")
        st.markdown("""
        - Organiser des formations internes pour maîtriser l'utilisation des tableaux interactifs.
        - Favoriser l’échange de bonnes pratiques pédagogiques entre établissements OSUI.
        """)


        # Catégorie : Usage du numérique
        st.markdown("### Usage du numérique")
        st.markdown("""
        - **Fréquence** : 4,1
        - **Impact** : 3,8
        """)
        st.write("Résumé :")
        st.caption("""
        Les tableaux interactifs sont encore en phase d'appropriation par les enseignants, mais ils sont perçus comme des outils prometteurs pour améliorer l'interactivité des cours.
        Les plateformes numériques comme GeoGebra et Quizinière sont largement utilisées pour renforcer les compétences en résolution de problèmes et en géométrie.
        Cependant, certains enseignants expriment le besoin de davantage de formations pour maximiser l'impact pédagogique de ces outils.
        """)

        # Catégorie : Évaluation formative
        st.markdown("### Évaluation formative")
        st.markdown("""
        - **Utilisation** : Oui (100%)
        """)
        st.write("Résumé :")
        st.caption("""
        L'évaluation formative est systématiquement intégrée aux cours de mathématiques pour suivre les progrès des élèves et identifier leurs difficultés spécifiques.
        Elle est utilisée pour adapter les supports et les approches pédagogiques en fonction des besoins de chaque élève.
        Des outils numériques tels que Kahoot et Plickers permettent également de rendre l'évaluation plus interactive et engageante pour les élèves.
        """)

        # Catégorie : Collaboration
        st.markdown("### Collaboration")
        st.markdown("""
        - **Niveau de collaboration** : 4,2
        """)
        st.write("Résumé :")
        st.caption("""
        L'équipe de mathématiques collabore régulièrement pour harmoniser les pratiques pédagogiques et partager les ressources.
        Des projets transversaux avec d'autres disciplines, comme la physique-chimie et l'informatique, sont en cours de développement pour renforcer l'interdisciplinarité.
        Une meilleure coordination est souhaitée pour formaliser ces initiatives et partager plus efficacement les bonnes pratiques.
        """)

        # Catégorie : Communication
        st.markdown("### Communication")
        st.markdown("""
        - **Satisfaction vie scolaire** : 3,5
        """)
        st.write("Résumé :")
        st.caption("""
        Les enseignants soulignent un besoin de communication renforcée avec la vie scolaire, notamment pour le suivi des élèves en difficulté.
        Un système centralisé pour signaler les problèmes rencontrés en classe, comme les absences répétées ou les comportements perturbateurs, serait apprécié pour faciliter la collaboration.
        """)

        # Catégorie : Bien-être
        st.markdown("### Bien-être")
        st.markdown("""
        - **Impact du déménagement** : 3,2
        """)
        st.write("Résumé :")
        st.caption("""
        Le déménagement dans de nouvelles salles a été bien accueilli pour leurs équipements modernes, mais des problèmes logistiques subsistent, notamment concernant l'installation et l'organisation des espaces de travail.
        Les enseignants aimeraient disposer de plus de temps et de soutien pour aménager leurs salles selon leurs besoins pédagogiques.
        """)

    with st.expander("Physique-chimie"):

        fig_spc = plot_radar_equipe('Physique-chimie', df_scores_equipes)
        st.plotly_chart(fig_spc, use_container_width=True)

        st.subheader("Informations générales")
        st.markdown("""
        - **Nombre de personnes dans l'équipe** : 3
        - **Ancienneté moyenne** : 2,3 ans
        """)

        st.subheader("Points positifs")
        st.markdown("""
        - Progression dans la structuration des informations et des procédures.
        - Amélioration nette malgré les difficultés matérielles.
        """)

        st.subheader("Points négatifs")
        st.markdown("""
        - Problèmes de visibilité dans les salles de sciences (écrans interactifs trop petits compte tenu de la profondeur des salles de labo).
        - Manque de sécurité dans le laboratoire (armoires non fonctionnelles, évacuations non raccordées).
        - Salles dispersées, compliquant la gestion du matériel.
        - Effectifs trop élevés limitant les manipulations.
        """)

        st.subheader("Actions possibles")
        st.markdown("""
        - Mettre à jour le laboratoire pour respecter les normes de sécurité.
        - Réduire les effectifs pour permettre plus de manipulations.
        """)


        # Catégorie : Usage du numérique
        st.markdown("### Usage du numérique")
        st.markdown("""
        - **Fréquence** : 4,7
        - **Impact** : 4
        """)
        st.write("Résumé :")
        st.caption("""
        Les participants utilisent divers outils numériques, notamment des tableurs-grapheurs, des logiciels d'analyse de données et de création graphique.
        Les simulateurs et Pronote sont également exploités, ce dernier permettant de déposer cours et activités.
        L'utilisation du tableau interactif est saluée pour l'amélioration de l'interaction avec les élèves.
        """)

        # Catégorie : Évaluation formative
        st.markdown("### Évaluation formative")
        st.markdown("""
        - **Utilisation** : Oui (100%)
        """)
        st.write("Résumé :")
        st.caption("""
        Plusieurs stratégies pédagogiques sont mises en avant, telles que l'implication d'élèves performants pour aider leurs camarades, le travail régulier des élèves pour garantir l'assimilation des notions,
        et l'utilisation d'évaluations formatives pour ajuster les pratiques d'enseignement.
        """)

        # Catégorie : Collaboration
        st.markdown("### Collaboration")
        st.markdown("""
        - **Niveau de collaboration** : 4,3
        """)
        st.write("Résumé :")
        st.caption("""
        La diversité des personnalités dans l'équipe est perçue comme un atout.
        Cette diversité est valorisée à travers des réunions d'équipe et des projets communs, renforçant la cohésion et l'efficacité de l'équipe.
        """)

        # Catégorie : Communication
        st.markdown("### Communication")
        st.markdown("""
        - **Satisfaction vie scolaire** : 2
        """)
        st.write("Résumé :")
        st.caption("""
        Les répondants expriment un besoin de réactivité et de rigueur dans le partage des informations concernant les élèves à besoins particuliers.
        Un manque de procédures formelles pour la gestion des retards est également relevé, ainsi qu'une nécessité d'améliorer la communication avec la vie scolaire.
        """)

        # Catégorie : Bien-être
        st.markdown("### Bien-être")
        st.markdown("""
        - **Impact du déménagement** : 3
        """)
        st.write("Résumé :")
        st.caption("""
        Les participants ont signalé des problèmes tels que le manque de réactivité des services de maintenance (exemple : panne d'électricité non résolue)
        et un manque de clarté dans la mise en place des équipements.
        Ils souhaitent une meilleure communication concernant l'installation des postes informatiques et la disponibilité des prises électriques dans les salles de sciences.
        """)

    with st.expander("SVT"):

        fig_svt = plot_radar_equipe('Sciences de la vie et de la Terre', df_scores_equipes)
        st.plotly_chart(fig_svt, use_container_width=True)

        st.subheader("Informations générales")
        st.markdown("""
        - **Nombre de personnes dans l'équipe** : 2
        - **Ancienneté moyenne** : 2 ans
        """)

        st.subheader("Points positifs")
        st.markdown("""
        - Bon esprit d'équipe et volonté de partager les ressources.
        - Ambiance positive malgré les difficultés matérielles.
        """)

        st.subheader("Points négatifs")
        st.markdown("""
        - Salles dispersées, compliquant la gestion du matériel.
        - Problèmes de sécurité dans le laboratoire (ventilation insuffisante).
        - Effectifs trop élevés limitant les manipulations.
        """)

        st.subheader("Actions possibles")
        st.markdown("""
        - Revoir les protocoles de sécurité et conformité du laboratoire (ventilation, stockage, etc.).
        - Regrouper les salles pour faciliter la gestion des ressources.
        - Réduire les effectifs pour permettre plus de manipulations.
        - Faire un état des lieux du matériel disponible.
        """)


        # Catégorie : Usage du numérique
        st.markdown("### Usage du numérique")
        st.markdown("""
        - **Fréquence** : 4,5
        - **Impact** : 3,5
        """)
        st.write("Résumé :")
        st.caption("""
        Les enseignants utilisent principalement des logiciels spécialisés dans les Sciences de la Vie et de la Terre, ainsi qu'Excel et Internet dans leur travail quotidien.
        Les ordinateurs sont également des outils technologiques principaux.
        """)

        # Catégorie : Évaluation formative
        st.markdown("### Évaluation formative")
        st.markdown("""
        - **Utilisation** : Oui (100%)
        """)
        st.write("Résumé :")
        st.caption("""
        L'évaluation formative en travaux pratiques joue un rôle clé dans le développement de l'autonomie des élèves.
        Elle permet aussi d'évaluer l'efficacité des méthodes d'enseignement, offrant des opportunités d'adaptation et d'amélioration.
        """)

        # Catégorie : Collaboration
        st.markdown("### Collaboration")
        st.markdown("""
        - **Niveau de collaboration** : 4,9
        """)
        st.write("Résumé :")
        st.caption("""
        Des réunions régulières et divers outils de communication assurent une interaction constante et efficace.
        Cependant, des améliorations pourraient renforcer la cohésion et l'efficacité de l'équipe.
        """)

        # Catégorie : Communication
        st.markdown("### Communication")
        st.markdown("""
        - **Satisfaction vie scolaire** : 3
        """)
        st.write("Résumé :")
        st.caption("""
        Il existe un besoin de clarification et d'application uniforme des consignes.
        Organiser des ateliers d'information pourrait améliorer la compréhension des processus et renforcer la cohésion d'équipe.
        """)

        # Catégorie : Bien-être
        st.markdown("### Bien-être")
        st.markdown("""
        - **Impact du déménagement** : 3
        """)
        st.write("Résumé :")
        st.caption("""
        Un rapprochement avec les enseignants est souhaité pour mieux comprendre leurs besoins et répondre efficacement aux défis de leur travail quotidien.
        """)

    with st.expander("Résultats des matières individuelles"):
        st.subheader("Informations générales")
        st.markdown("""
        Les résultats suivants sont basés sur des enquêtes menées auprès d'enseignants individuels dans plusieurs matières.
        Ces matières ont un seul enseignant, et les données reflètent leur expérience personnelle et leurs pratiques pédagogiques.
        """)

        matieres = [
            {
                "nom": "Arts plastiques",
                "personnes": 1,
                "anciennete": 4,
                "categories": [
                    {
                        "nom": "Usage du numérique",
                        "Fréquence": 5,
                        "Impact": 3,
                        "Résumé": "Utilisation de l'ordinateur et du vidéoprojecteur pour présenter des informations de manière visuelle..."
                    },
                    {
                        "nom": "Évaluation formative",
                        "Utilisation": "oui 100%",
                        "Résumé": "L'évaluation formative améliore la compréhension des sujets abordés et accélère le processus d'apprentissage."
                    },
                    {
                        "nom": "Collaboration",
                        "Niveau de collaboration": 4.3,
                        "Résumé": "Insistance sur le partage d'expériences et la cohésion de l'équipe pédagogique."
                    },
                    {
                        "nom": "Communication",
                        "Satisfaction vie scolaire": 4,
                        "Résumé": "Évaluation utilisée pour cibler les objectifs pédagogiques en fonction des besoins des élèves."
                    },
                    {
                        "nom": "Bien-être",
                        "Impact du déménagement": 3,
                        "Résumé": "Besoin d'outils pédagogiques adaptés pour optimiser l'efficacité des formations."
                    }
                ]
            },
            {
                "nom": "Éducation musicale",
                "personnes": 1,
                "anciennete": 5,
                "categories": [
                    {
                        "nom": "Usage du numérique",
                        "Fréquence": 3,
                        "Impact": 3,
                        "Résumé": "Utilisation de vidéos, applications vocales et séquenceurs pour les activités musicales."
                    },
                    {
                        "nom": "Évaluation formative",
                        "Utilisation": "oui 100%",
                        "Résumé": "L'évaluation formative permet d'adapter l'enseignement aux besoins spécifiques de chaque élève."
                    },
                    {
                        "nom": "Collaboration",
                        "Niveau de collaboration": 4.3,
                        "Résumé": "Projet de formations internes axées sur les nouvelles pédagogies et collaborations interdisciplinaires."
                    }
                ]
            },
            {
                "nom": "Philosophie",
                "personnes": 1,
                "anciennete": 1,
                "categories": [
                    {
                        "nom": "Usage du numérique",
                        "Fréquence": 3,
                        "Impact": 3,
                        "Résumé": "Création d'exercices en ligne pour un apprentissage flexible et adapté."
                    },
                    {
                        "nom": "Évaluation formative",
                        "Utilisation": "oui 100%",
                        "Résumé": "Application des pratiques enseignées avec espoir de résultats positifs à terme."
                    }
                ]
            }
            # Ajoutez d'autres matières ici de manière similaire
        ]

        for matiere in matieres:
            st.subheader(matiere["nom"])
            st.markdown(f"- **Nombre de personnes** : {matiere['personnes']}")
            st.markdown(f"- **Ancienneté moyenne** : {matiere['anciennete']} ans")

            for category in matiere["categories"]:
                st.markdown(f"#### {category['nom']}")
                if "Fréquence" in category:
                    st.markdown(f"- **Fréquence** : {category['Fréquence']}")
                if "Impact" in category:
                    st.markdown(f"- **Impact** : {category['Impact']}")
                st.write("Résumé :")
                st.caption(category["Résumé"])
