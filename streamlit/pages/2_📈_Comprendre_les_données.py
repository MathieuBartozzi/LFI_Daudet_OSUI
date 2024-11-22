
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.subplots as sp
import plotly.graph_objects as go
import os
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


# st.logo('logo.jpg')

##### CHARGEMENT DES DONNÉES ######

# Fonction de chargement des données avec cache


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

    df_eleve = pd.read_csv(os.path.join(data_dir, "df_eleve.csv"), sep=';')
    df_notes_devoir = pd.read_csv(os.path.join(data_dir, "df_notes_devoir.csv"), sep=';')
    df_absenceseleves = pd.read_csv(os.path.join(data_dir, "df_absenceseleves.csv"), sep=';')
    df_retards = pd.read_csv(os.path.join(data_dir, "df_retards.csv"), sep=';')
    df_punition = pd.read_csv(os.path.join(data_dir, "df_punition.csv"), sep=';',na_values=[''])
    df_passagesinfirmerie = pd.read_csv(os.path.join(data_dir, "df_passagesinfirmerie.csv"), sep=';')
    df_sanction = pd.read_csv(os.path.join(data_dir, "df_sanction.csv"), sep=';')
    df_appreciationprofesseurs = pd.read_csv(os.path.join(data_dir, "df_appreciationprofesseurs.csv"), sep=';')

    return df_eleve, df_notes_devoir, df_absenceseleves, df_retards, df_punition, df_passagesinfirmerie, df_sanction, df_appreciationprofesseurs


# Appel de la fonction pour charger les données
df_eleve, df_notes_devoir, df_absenceseleves, df_retards, df_punition, df_passagesinfirmerie, df_sanction, df_appreciationprofesseurs = load_data()


#defintion des couleurs
couleurs_filles_garcons = [px.colors.qualitative.G10[2], px.colors.qualitative.G10[3]]
couleurs_college_lycee = [px.colors.qualitative.G10[8], px.colors.qualitative.G10[9]]


tab1, tab2, tab3 = st.tabs(["**VIE SCOLAIRE**", "**RESULTATS**", '**BULLETINS**'])

############################## VIE SCOLAIRE  ##############################
with tab1 :
    st.write("")
    st.subheader("Fréquences des absences, passages à l'infirmerie, punitions, retards", divider="gray")

    # Counting occurrences by date
    absences_by_date = df_absenceseleves['date'].value_counts().sort_index()
    infirmerie_by_date = df_passagesinfirmerie['date'].value_counts().sort_index()
    punition_by_date = df_punition['date'].value_counts().sort_index()
    retards_by_date = df_retards['date'].value_counts().sort_index()


    # Create subplots for each event type, displayed in two columns
    fig_freq = sp.make_subplots(
        rows=2, cols=2,
        shared_xaxes=True,
        subplot_titles=(
            "Absences",
            "Infirmerie",
            "Punitions",
            "Retards"
        )
    )

    # Absences
    fig_freq.add_trace(go.Bar(
        x=absences_by_date.index,
        y=absences_by_date.values,
        name="Absences",
        marker_color=px.colors.qualitative.G10[4]
    ), row=1, col=1)

    # Passages à l'infirmerie
    fig_freq.add_trace(go.Bar(
        x=infirmerie_by_date.index,
        y=infirmerie_by_date.values,
        name="Passages à l'infirmerie",
        marker_color=px.colors.qualitative.G10[5]
    ), row=1, col=2)

    # Punitions
    fig_freq.add_trace(go.Bar(
        x=punition_by_date.index,
        y=punition_by_date.values,
        name="Punitions",
        marker_color=px.colors.qualitative.G10[6]
    ), row=2, col=1)

    # Retards
    fig_freq.add_trace(go.Bar(
        x=retards_by_date.index,
        y=retards_by_date.values,
        name="Retards",
        marker_color=px.colors.qualitative.G10[7]
    ), row=2, col=2)

    # Update layout
    fig_freq.update_layout(
        height=600,  # Adjust height for better visibility
        showlegend=False
    )

    # Set x-axis titles
    fig_freq.update_xaxes(title_text="Date", row=2, col=1)
    fig_freq.update_xaxes(title_text="Date", row=2, col=2)

    # Adjust y-axis titles (optional)
    fig_freq.update_yaxes(title_text=None, row=1, col=1)
    fig_freq.update_yaxes(title_text=None, row=1, col=2)
    fig_freq.update_yaxes(title_text=None, row=2, col=1)
    fig_freq.update_yaxes(title_text=None, row=2, col=2)

    # Display the chart in Streamlit
    st.plotly_chart(fig_freq)


    with st.container(border=True):
        st.write("""
            1. Les absences augmentent en fin de trimestre, avec un pic notable en fin d'année.
            2. Les passages à l'infirmerie restent constants tout au long de l'année.
            3. Lors des périodes 1, 2 et 3, les punitions atteignent un pic en fin de période, indiquant probablement une fatigue des élèves et des équipes. Sur la dernière période, le pic se situe plutôt au début, coïncidant avec une forte hausse des absences sur cette même période.
        """)

    ############ CREATION DU DATAFRAME indicateurs_eleves pour la vie scolaire ############

    # Calcul de la moyenne annuelle pondérée pour chaque élève
    notes_annuelles = df_notes_devoir.groupby('eleve_id').apply(
        lambda x: x['note_sur_20'].sum() / x['coeff'].sum()
    ).reset_index(name='moyenne_annuelle')

    # Calcul des indicateurs d'absences, retards, punitions, passages à l'infirmerie
    absences_total = df_absenceseleves.groupby('eleve_id').size().reset_index(name='total_absences')
    retards_total = df_retards.groupby('eleve_id').size().reset_index(name='total_retards')
    punitions_total = df_punition.groupby('eleve_id').size().reset_index(name='total_punitions')
    infirmerie_total = df_passagesinfirmerie.groupby('eleve_id').size().reset_index(name='total_passages_infirmerie')


    # Ajout de la colonne 'niveau' de df_notes_devoir à indicateurs_eleves
    indicateurs_eleves = notes_annuelles.merge(absences_total, on='eleve_id', how='left') \
                             .merge(retards_total, on='eleve_id', how='left') \
                             .merge(punitions_total, on='eleve_id', how='left') \
                             .merge(infirmerie_total, on='eleve_id', how='left') \
                             .merge(df_eleve[['eleve_id', 'sexe']], on='eleve_id', how='left') \
                             .merge(df_notes_devoir[['eleve_id', 'niveau']].drop_duplicates(), on='eleve_id', how='left')


    # Encoder la variable `sexe` : 0 pour "F" (filles) et 1 pour "M" (garçons)
    indicateurs_eleves['sexe'] = indicateurs_eleves['sexe'].map({'F': 0, 'M': 1})

    # Remplir les valeurs manquantes par 0
    indicateurs_eleves.fillna(0, inplace=True)

    ############ PROFILAGE ############

    # Normalisation des indicateurs, incluant la variable `sexe`
    scaler = StandardScaler()
    indicateurs_normalises = scaler.fit_transform(indicateurs_eleves[['moyenne_annuelle', 'total_absences',
                                                            'total_retards', 'total_punitions',
                                                            'total_passages_infirmerie', 'sexe']])

    # Convertir en DataFrame pour ajouter la colonne 'cluster'
    indicateurs_normalises_df = pd.DataFrame(indicateurs_normalises, columns=['moyenne_annuelle', 'total_absences',
                                                                            'total_retards', 'total_punitions',
                                                                            'total_passages_infirmerie', 'sexe'])

    # Appliquer le clustering K-means avec la variable `sexe` incluse
    kmeans = KMeans(n_clusters=4, random_state=0)
    indicateurs_normalises_df['cluster'] = kmeans.fit_predict(indicateurs_normalises)

    # Ajouter les clusters au DataFrame d'origine
    indicateurs_eleves['cluster'] = indicateurs_normalises_df['cluster']

    # Calcul des pourcentages d'élèves dans chaque cluster
    profil_counts = indicateurs_eleves['cluster'].value_counts(normalize=True) * 100
    profil_counts.index = [f"Profil {i + 1}" for i in profil_counts.index]  # Renommer les index pour afficher "Profil 1", "Profil 2", etc.

    # Création du graphique en camembert avec Plotly
    fig_profil = px.pie(
        names=profil_counts.index,  # Utiliser les noms des profils pour chaque secteur
        values=profil_counts.values,  # Utiliser les pourcentages calculés pour chaque profil
        # title="Répartition des élèves par profil",
        hole=0.5,
        color_discrete_sequence=px.colors.qualitative.G10
    )
    # Mettre la légende en bas
    fig_profil.update_layout(
        width=500,              # Largeur du graphique
        height=350,
        legend=dict(
            orientation="h",    # Orientation horizontale
            yanchor="bottom",   # Alignement vertical : bas
            y=-0.2,             # Position verticale (en-dessous du graphique)
            xanchor="center",   # Alignement horizontal : centré
            x=0.5               # Position horizontale (centré)
        )
    )

    st.write("")
    st.subheader('Profilage des élèves',divider="gray")
    st.write(
        "Ce graphique illustre la répartition des élèves en différents profils, déterminés par une analyse de **clustering**. Cette analyse a été réalisée en croisant la moyenne annuelle, les absences, les retards, les punitions, les passages à l'infirmerie, ainsi que le sexe des élèves. On peut identifier **quatre groupes** d’élèves présentant des caractéristiques communes.")


    col1, col2 = st.columns([2,1])

    with col1 :

        st.plotly_chart(fig_profil)

    with col2 :



        with st.popover("Profil 1"):
            st.markdown("""
            Ce groupe se caractérise par une **moyenne annuelle de 12,01**, avec un nombre élevé d'**absences (31,95)** et de **retards (19,9)**. Les élèves de ce profil reçoivent également un nombre significatif de **punitions (10,06)** et ont un nombre modéré de passages à l'infirmerie (**4,24**). Ce profil inclut une majorité mixte avec une proportion de garçons de **53,76 %**. Ce profil pourrait correspondre à des élèves ayant des besoins en termes de suivi assiduité et comportement.
            """)
        st.write("")

        with st.popover("Profil 2"):
            st.markdown("""
            Les élèves de ce profil présentent une **moyenne annuelle élevée de 15,14** et affichent des valeurs faibles en **absences (13,43)**, **retards (5,54)**, et **punitions (1,01)**. Les passages à l'infirmerie sont également bas (**2,92**). Ce groupe est exclusivement composé de filles, suggérant un profil d'élèves académiquement performantes et disciplinées.
            """)
        st.write("")
        with st.popover("Profil 3"):
            st.markdown("""
            Les élèves de ce groupe affichent une **moyenne annuelle de 12,46**, avec un nombre modéré d'**absences (19,25)**, **retards (6,5)**, et **punitions (5,25)**. Cependant, le nombre de passages à l'infirmerie est exceptionnellement élevé (**108**). Ce groupe est composé de filles à **75 %**. Ce profil pourrait indiquer des élèves nécessitant une attention particulière en termes de santé.
            """)
        st.write("")
        with st.popover("Profil 4"):
            st.markdown("""
            Ce profil présente une **moyenne annuelle de 14,27**, un faible nombre d'**absences (13,43)**, de **retards (4,5)**, et de **punitions (2,34)**. Les passages à l'infirmerie restent limités (**2,28**). Ce groupe est exclusivement composé de garçons, ce qui pourrait correspondre à un profil d'élèves académiquement performants et disciplinés.
            """)

    with st.container(border=True):
        st.markdown("""
        **Actions possibles:**
1. Renforcer les outils de suivi pour les élèves du **Profil 1** (ex. : sensibilisation aux absences et retards).
2. Soutenir les besoins spécifiques de santé du **Profil 3**, en investiguant les causes des passages fréquents à l'infirmerie.
3. Valoriser les efforts des élèves performants (**Profils 2 et 4**).

                    """)




    ############ FACTEURS IMPACTANTS ############
    st.write("")
    st.subheader('Analyse des facteurs impactants', divider="gray")


    st.write("L'analyse des relations entre différents indicateurs scolaires (moyenne annuelle, absences, retards, punitions, genre) permet d'identifier dans quelle mesure ces variables sont corrélées entre elles. Une corrélation indique qu’une variation dans un indicateur est associée à une variation dans un autre, ce qui peut révéler des tendances sous-jacentes dans les comportements ou les performances des élèves.")

    # Création des scatter plots pour chaque relation
    fig_corr = sp.make_subplots(rows=2, cols=3, subplot_titles=(
        "Moyenne vs Absences", "Moyenne vs Retards", "Moyenne vs Punitions",
        "Absences vs Retards", "Absences vs Punitions", "Retards vs Punitions"))

    # Moyenne vs Absences
    scatter1 = px.scatter(indicateurs_eleves, x='total_absences', y='moyenne_annuelle',
                        color_discrete_sequence=[px.colors.qualitative.G10[0]],trendline="ols")
    for trace in scatter1.data:
        fig_corr.add_trace(trace, row=1, col=1)

    # Moyenne vs Retards
    scatter2 = px.scatter(indicateurs_eleves, x='total_retards', y='moyenne_annuelle',
                        color_discrete_sequence=[px.colors.qualitative.G10[1]],trendline="ols")
    for trace in scatter2.data:
        fig_corr.add_trace(trace, row=1, col=2)

    # Moyenne vs Punitions
    scatter3 = px.scatter(indicateurs_eleves, x='total_punitions', y='moyenne_annuelle',
                        color_discrete_sequence=[px.colors.qualitative.G10[2]],trendline="ols")
    for trace in scatter3.data:
        fig_corr.add_trace(trace, row=1, col=3)

    # Absences vs Retards
    scatter4 = px.scatter(indicateurs_eleves, x='total_absences', y='total_retards',
                        color_discrete_sequence=[px.colors.qualitative.G10[3]],trendline="ols")
    for trace in scatter4.data:
        fig_corr.add_trace(trace, row=2, col=1)

    # Absences vs Punitions
    scatter5 = px.scatter(indicateurs_eleves, x='total_absences', y='total_punitions',
                        color_discrete_sequence=[px.colors.qualitative.G10[4]],trendline="ols")
    for trace in scatter5.data:
        fig_corr.add_trace(trace, row=2, col=2)

    # Retards vs Punitions
    scatter6 = px.scatter(indicateurs_eleves, x='total_retards', y='total_punitions',
                        color_discrete_sequence=[px.colors.qualitative.G10[5]], trendline="ols")
    for trace in scatter6.data:
        fig_corr.add_trace(trace, row=2, col=3)

    # Modifier le layout pour tous les scatter plots dans fig_corr
    fig_corr.update_layout(height=800,width=1000, template="plotly_white")



    # Affichage dans Streamlit
    st.plotly_chart(fig_corr)



    indicators = ['total_absences', 'total_retards', 'total_punitions', 'total_passages_infirmerie']
    indicator_names = ['Absences', 'Retards', 'Punitions', 'Passages Infirmerie']

    # Mise à jour des données par sexe
    sexe_summary = indicateurs_eleves[['total_absences', 'total_retards', 'total_punitions', 'total_passages_infirmerie', 'sexe']].groupby('sexe').mean().reset_index()
    sexe_summary['sexe'] = sexe_summary['sexe'].map({0: 'Filles', 1: 'Garçons'})


    # Transformation des données
    df_melted = sexe_summary.melt(id_vars='sexe', value_vars=indicators, var_name='Indicateur', value_name='Valeur')
    df_melted['Indicateur'] = df_melted['Indicateur'].replace(dict(zip(indicators, indicator_names)))

    # Création du graphique
    fig_sex_bar = px.bar(df_melted, x='sexe', y='Valeur', color='sexe',
                facet_col='Indicateur', facet_col_wrap=5, color_discrete_sequence=couleurs_filles_garcons,
                labels={'sexe': 'Sexe', 'Valeur': 'Valeur moyenne', 'Indicateur': 'Indicateur'})

    # Mise à jour de la disposition
    fig_sex_bar.update_layout(
        showlegend=True,
        legend_title_text=None,
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5),  # Position de la légende
        height=500,  # Ajustement de la hauteur du graphique
        margin=dict(t=50, b=0, l=0, r=0)  # Marges pour un affichage optimal
    )
    fig_sex_bar.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

    # Ajustement des espacements entre les facettes
    fig_sex_bar.update_xaxes(matches=None, title=None,showticklabels=False)  # Enlève le titre "Sexe" redondant
    fig_sex_bar.update_yaxes(showgrid=True)


    # Calcul des moyennes des indicateurs par niveau
    niveau_summary = indicateurs_eleves[['total_absences', 'total_retards', 'total_punitions', 'total_passages_infirmerie', 'niveau']].groupby('niveau').mean().reset_index()

    # Transformation des données
    df_melted_niveau = niveau_summary.melt(id_vars='niveau', value_vars=indicators, var_name='Indicateur', value_name='Valeur')
    df_melted_niveau['Indicateur'] = df_melted_niveau['Indicateur'].replace(dict(zip(indicators, indicator_names)))

    # Création du graphique
    fig_niveau_bar = px.bar(df_melted_niveau, x='niveau', y='Valeur', color='niveau',
                            facet_col='Indicateur', facet_col_wrap=5, color_discrete_sequence=couleurs_college_lycee,
                            labels={'niveau': 'Niveau', 'Valeur': 'Valeur moyenne', 'Indicateur': 'Indicateur'})

    # Mise à jour de la disposition
    fig_niveau_bar.update_layout(
        showlegend=True,
        legend_title_text=None,
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5),  # Position de la légende
        height=500,  # Ajustement de la hauteur du graphique
        margin=dict(t=50, b=0, l=0, r=0)  # Marges pour un affichage optimal
    )
    fig_niveau_bar.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

    # Ajustement des espacements entre les facettes
    fig_niveau_bar.update_xaxes(matches=None, title=None, showticklabels=False)  # Enlève le titre "Niveau" redondant
    fig_niveau_bar.update_yaxes(showgrid=True)


   # Affichage côte à côte dans deux colonnes
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(fig_sex_bar, use_container_width=True)

    with col2:
        st.plotly_chart(fig_niveau_bar, use_container_width=True)

    # Explication du graphique

    with st.container(border=True):
        st.write("""

        1. **Moyenne vs Absences, Retards, Punitions** : Il y a  une tendance globale où un nombre élevé d’absences, de retards, ou de punitions est souvent associé à une baisse de la moyenne annuelle. Bien que ces relations ne soient pas strictement linéaires, on observe qu’un cumul de comportements problématiques semble affecter la moyenne.

        2. **Absences, Retards, et Punitions entre eux** : Il semble exister une corrélation modérée entre absences, retards et punitions, suggérant que les élèves en difficulté sur un de ces aspects sont souvent concernés par les autres.

        3. **Écarts entre filles et garçons** : Les garçons présentent un nombre moyen de punitions et de retards supérieur à celui des filles. À l'inverse, les filles affichent un nombre moyen d'absences plus élevé que les garçons. Les autres indicateurs, comme la moyenne annuelle et les passages à l'infirmerie, restent relativement proches entre les deux groupes. Ces écarts peuvent orienter vers des actions spécifiques selon les besoins observés pour chaque groupe.

        4. **Écarts entre collège et lycée** : Les élèves du lycée affichent un nombre moyen d'absences nettement plus élevé que ceux du collège. En revanche, les indicateurs de retards, punitions, et passages à l'infirmerie sont plus faibles pour les élèves du lycée. Les moyennes annuelles restent relativement similaires entre les deux niveaux, indiquant des performances académiques comparables malgré ces différences comportementales.

        """)





with tab2:
    st.write("")
    st.subheader('Fréquence et rythmes des évaluations', divider="gray")

    def plot_note_distribution_by_day_and_trimester(df_notes_devoir):
        """
        Affiche la répartition des notes par jour avec une couleur différente par trimestre.

        Args:
            df_notes_devoir (pd.DataFrame): DataFrame contenant les colonnes 'date', 'note', et 'trimestre'.

        Returns:
            None: Affiche le graphique directement dans Streamlit.
        """
        # Vérifiez que la colonne 'date' est bien au format datetime
        df_notes_devoir['date'] = pd.to_datetime(df_notes_devoir['date'], errors='coerce')

        # Vérifiez que la colonne 'note' est bien numérique
        df_notes_devoir['note'] = pd.to_numeric(df_notes_devoir['note'], errors='coerce')

        # Grouper par jour et trimestre, compter le nombre de notes
        note_distribution_by_day = (
            df_notes_devoir
            .groupby([df_notes_devoir['date'].dt.date, 'trimestre'])
            .size()
            .reset_index(name='Nombre de notes')
        )

        # Créer le bar chart avec couleur par trimestre
        fig = px.bar(
            note_distribution_by_day,
            x='date',
            y='Nombre de notes',
            color='trimestre',  # Utilisation de la colonne existante
            title="Répartition des notes par jour et trimestre",
            labels={'date': 'Date', 'Nombre de Notes': 'Nombre de Notes', 'trimestre': 'Trimestre'},
            height=500,
            color_discrete_sequence=[px.colors.qualitative.G10[1],px.colors.qualitative.G10[2],px.colors.qualitative.G10[3]]
        )

        # Ajuster le layout pour rendre le graphique plus lisible
        fig.update_layout(
            xaxis=dict(title="Date", tickformat="%b %d", tickangle=45),
            yaxis=dict(title="Nombre de notes"),
            showlegend=True
        )

        # Afficher dans Streamlit
        st.plotly_chart(fig, use_container_width=True)


    plot_note_distribution_by_day_and_trimester(df_notes_devoir)

    with st.container(border=True):
        st.markdown("""
                    L'analyse de la répartition des notes sur l'année révèle une concentration marquée des évaluations autour de certaines périodes, en particulier à la fin des trimestres. Cette tendance reflète une charge de travail inégale, avec des périodes de forte activité suivies de périodes plus calmes.

Pour optimiser la charge de travail des élèves et des enseignants, il pourrait être bénéfique de lisser la fréquence des évaluations tout au long de l'année.  Cela permettrait non seulement de réduire le stress lié aux périodes de forte activité, mais également d'améliorer la qualité des apprentissages en favorisant une évaluation continue et régulière.

Une meilleure collaboaration entre les équipes pédagogies pourrait constituer une étape clé dans cette démarche. Cette régulation contribuerait à un climat scolaire plus apaisé et offrirait aux élèves une meilleure gestion de leur charge de travail.
                    """)


    # Merge the two DataFrames on 'eleve_id' to bring the 'sexe' column into df_notes_devoir
    df_notes_devoir = df_notes_devoir.merge(df_eleve[['eleve_id', 'sexe']], on='eleve_id', how='left')

    # Ajouter une colonne normalisée sur 20
    # df_notes_devoir['note_sur_20'] = (df_notes_devoir['note'] / df_notes_devoir['sur']) * 20

    # Filtrer le DataFrame pour exclure les niveaux 6e, 5e, et 4e (a enlever plus tard)
    #df_notes_devoir = df_notes_devoir[~df_notes_devoir['niveau_de_classe'].isin(['6e', '5e', '4e'])]

    # Calculer la médiane des notes sur 20
    median_note = df_notes_devoir['note_sur_20'].median()

    # 1. Distribution des moyennes des élèves par genre
    fig_dist = px.histogram(
        df_notes_devoir,
        x='note_sur_20',
        color='sexe',
        nbins=20,
        title='Distribution des moyennes des élèves par genre',
        labels={'note_sur_20': 'Notes sur 20', 'sexe': 'Genre'},
        barmode='overlay',
        opacity=0.4,
        color_discrete_sequence=couleurs_filles_garcons
    )

    # 2. Élèves avec moyennes < médiane par genre
    below_median = df_notes_devoir[df_notes_devoir['note_sur_20'] < median_note].groupby('sexe').size().reset_index(name='count')
    fig_below = px.bar(
        below_median,
        x='sexe',
        y='count',
        title=f"Élèves avec moyennes < médiane (~{median_note:.2f})",
        labels={'sexe': 'Genre', 'count': 'Nombre de notes'},
        color='sexe',
        text='count',
        color_discrete_sequence=couleurs_filles_garcons
    )

    # 3. Élèves avec moyennes ≥ médiane par genre
    above_median = df_notes_devoir[df_notes_devoir['note_sur_20'] >= median_note].groupby('sexe').size().reset_index(name='count')
    fig_above = px.bar(
        above_median,
        x='sexe',
        y='count',
        title=f"Élèves avec moyennes ≥ médiane (~{median_note:.2f})",
        labels={'sexe': 'Genre', 'count': 'Nombre de notes'},
        color='sexe',
        text='count',
        color_discrete_sequence=couleurs_filles_garcons
    )

    # Mise à jour des tracés
    fig_dist.update_layout(bargap=0.1)
    fig_below.update_traces(textposition='outside')
    fig_above.update_traces(textposition='outside')

    st.write("")
    st.subheader("Distribution des notes par genre", divider="gray")
    # st.plotly_chart(fig_dist, use_container_width=True)

    # Créer trois colonnes
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_dist, use_container_width=True)

    with col2:
        col1, col2 = st.columns(2)
        with col1:
                st.plotly_chart(fig_below, use_container_width=True)

        with col2:
                st.plotly_chart(fig_above, use_container_width=True)


    # Calcul des moyennes pondérées par matière et sexe
    weighted_mean_by_gender_subject = (
        df_notes_devoir
        .groupby(['matiere', 'sexe'])
        .apply(lambda x: (x['note_sur_20'] * x['coeff']).sum() / x['coeff'].sum())
        .reset_index(name='moyenne_ponderee')
    )

    # Pivot pour faciliter la comparaison entre garçons et filles
    pivot_mean = weighted_mean_by_gender_subject.pivot(index='matiere', columns='sexe', values='moyenne_ponderee').reset_index()

    # Ajouter une colonne pour indiquer qui performe mieux
    pivot_mean['Meilleur genre'] = pivot_mean.apply(
        lambda row: 'Filles' if row['F'] > row['M'] else 'Garçons', axis=1
    )

    # Visualisation avec un bar plot
    fig = px.bar(
        pivot_mean,
        x='matiere',
        y=['F', 'M'],
        barmode='group',
        color_discrete_sequence=couleurs_filles_garcons,
        title='Comparaison des moyennes par matière et par genre'
    )
    # Mise à jour de la disposition pour supprimer l'étiquette de l'axe X
    fig.update_layout(
    xaxis_title=None,
    yaxis_title=None# Supprime le label de l'axe X
)

    # Ajouter un tableau des résultats
    pivot_mean_table = pivot_mean[['matiere', 'F', 'M', 'Meilleur genre']]


    # Trier les matières selon la différence entre filles et garçons
    pivot_mean['Différence F-M'] = pivot_mean['F'] - pivot_mean['M']

    # Top 8 des matières où les filles performent le mieux
    top_filles = pivot_mean.sort_values(by='Différence F-M', ascending=False).head(8)[['matiere', 'F', 'M']]

    # Top 8 des matières où les garçons performent le mieux
    top_garcons = pivot_mean.sort_values(by='Différence F-M', ascending=True).head(8)[['matiere', 'F', 'M']]


    # Créer un DataFrame final pour affichage côte à côte
    top_8_table = pd.DataFrame({
        'Top Filles': top_filles['matiere'].values,
        'Top Garçons': top_garcons['matiere'].values
    })

    # Afficher dans Streamlit
    col1, col2 =st.columns([1,2])
    with col1:
        st.write("")
        st.write("**Top des matières par genre**")
        st.dataframe(top_8_table)

    # Afficher les résultats dans Streamlit
    with col2:
        st.plotly_chart(fig, use_container_width=True)


    with st.container(border=True):
        st.markdown("""
        L'analyse révèle des différences significatives entre filles et garçons en termes de performances et de répartition par matière. Les filles affichent des résultats globalement plus homogènes, notamment dans les langues et les SES, tandis que les garçons ont des résultats légérements supérieur en EPS et Philosophie. Les élèves avec des moyennes inférieures à la médiane sont majoritairement des garçons, soulignant un besoin de soutien renforcé pour ce groupe.

        **Pistes d'Action :**
        - Renforcer le suivi des garçons, notamment dans les matières où ils rencontrent des difficultés.
        - Encourager les filles à consolider leurs performances dans le matières scientifique, tout en valorisant leurs forces en langues.
        - Mettre en place des approches pédagogiques différenciées pour réduire les écarts de performance et favoriser une réussite équilibrée.
        """)



    st.write("")
    st.subheader("Niveau de maîtrise selon le profil", divider="gray")



    # Fonction pour calculer la moyenne des notes par groupe et par matière
    @st.cache_data
    def calculate_average_by_group(df, threshold, condition):
        if condition == "high":
            group = df[df['note_sur_20'] >= threshold]
        elif condition == "low":
            group = df[df['note_sur_20'] < threshold]
        return group.groupby('matiere')['note_sur_20'].mean()

    # Fonction pour créer un radar chart
    def create_radar_chart(data, categories, title, group_name):
        return go.Figure(
            go.Scatterpolar(
                r=data[categories].values,
                theta=categories,
                fill='toself',
                name=group_name,
            )
        ).update_layout(
            polar=dict(radialaxis=dict(visible=True)),
            title=title,
            height=400,
            width=500,
        )

    # Calcul des moyennes pour les deux groupes
    @st.cache_data
    def get_common_categories_and_data(df):
        top_avg = calculate_average_by_group(df, threshold=15, condition="high")
        low_avg = calculate_average_by_group(df, threshold=10, condition="low")
        common_categories = top_avg.index.intersection(low_avg.index)
        return top_avg, low_avg, common_categories

    # Main logic
    def display_radar_charts(df):
        top_avg, low_avg, common_categories = get_common_categories_and_data(df)

        # Création des radar charts pour chaque groupe
        fig_top = create_radar_chart(top_avg, common_categories, "Profil d'élève à moyenne élevée", "Profil d'élève à moyenne élevée")
        fig_low = create_radar_chart(low_avg, common_categories, "Profil d'élève à moyenne faible", "Profil d'élève à moyenne faible")

        # Affichage dans deux colonnes
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig_top, use_container_width=True)
        with col2:
            st.plotly_chart(fig_low, use_container_width=True)

    # Appel de la fonction principale
    display_radar_charts(df_notes_devoir)

    with st.container(border=True):
        st.markdown("""
        Les comparaisons montrent une nette divergence entre les élèves performants et moins performants. Les élèves performants affichent une homogénéité dans leurs résultats, avec des points forts répartis sur plusieurs matières. En revanche, les élèves moins performants accusent des lacunes globales, particulièrement marquées dans les matières scientifiques. Ils semblent aller chercher des points d'appui en EPS, SNT, SVT.
        """)



    st.write("")
    st.subheader('Décrochage scolaire : fréquence, facteurs', divider="gray")

    st.write("Dans cette partie, on défini un élève comme *décrocheur* si sa moyenne générale affiche une baisse signifactive (5 points) pendant un intervalle de temps précis (2 semaines). ")

    # 1. Préparation des données
    @st.cache_data
    def prepare_data(df_notes_devoir):
        # Assurez-vous que la colonne 'date' est au format datetime
        df_notes_devoir['date'] = pd.to_datetime(df_notes_devoir['date'], errors='coerce')
        return df_notes_devoir

    # 2. Calcul de la moyenne pondérée quotidienne
    @st.cache_data
    def calculate_daily_average(df_notes_devoir):
        return (
            df_notes_devoir
            .groupby(['eleve_id', 'date'])
            .apply(lambda group: pd.Series({
                'moyenne_journalière': (group['note_sur_20'] * group['coeff']).sum() / group['coeff'].sum()
            }))
            .reset_index()
        )

    # 3. Identification des élèves décrocheurs
    @st.cache_data
    def identify_dropouts(moyenne_jour, seuil=-5, periode_jours=15):
        # Ajouter une colonne pour la date de référence (15 jours avant)
        moyenne_jour['date_15_jours_avant'] = moyenne_jour['date'] - pd.Timedelta(days=periode_jours)

        # Joindre les données pour récupérer la moyenne de 15 jours avant
        moyenne_jour = moyenne_jour.merge(
            moyenne_jour[['eleve_id', 'date', 'moyenne_journalière']],
            left_on=['eleve_id', 'date_15_jours_avant'],
            right_on=['eleve_id', 'date'],
            how='left',
            suffixes=('', '_15_jours_avant')
        )

        # Critères pour identifier les décrocheurs
        moyenne_jour['est_décrocheur'] = (
            (moyenne_jour['moyenne_journalière'] - moyenne_jour['moyenne_journalière_15_jours_avant'] <= seuil) &
            (~moyenne_jour['moyenne_journalière_15_jours_avant'].isna())
        )
        return moyenne_jour

    # 4. Calcul du taux de décrochage
    @st.cache_data
    def calculate_dropout_rate(moyenne_jour):
        taux_decrochage = (
            moyenne_jour
            .groupby('date')['est_décrocheur']
            .mean()
            .reset_index(name='taux_decrochage')
        )
        taux_decrochage['taux_decrochage'] *= 100
        return taux_decrochage

    # 5. Visualisation du taux de décrochage dans le temps
    def plot_dropout_rate(taux_decrochage):
        fig = px.line(
            taux_decrochage,
            x='date',
            y='taux_decrochage',
            title="Évolution du taux de décrochage",
            labels={'date': 'Date', 'taux_decrochage': 'Taux de Décrochage (%)'}
        )
        st.plotly_chart(fig, use_container_width=True)

    # 6. Comptabiliser les décrochages par matière
    @st.cache_data
    def compute_dropouts_by_subject(moyenne_jour, df_notes_devoir):
        moyenne_jour = moyenne_jour.merge(
            df_notes_devoir[['eleve_id', 'date', 'matiere']],
            on=['eleve_id', 'date'],
            how='left'
        )
        decrochages_par_matiere = (
            moyenne_jour[moyenne_jour['est_décrocheur']]
            .groupby(['eleve_id', 'matiere'])
            .size()
            .reset_index(name='nombre_de_décrochages')
        )
        return decrochages_par_matiere

    # 7. Ajouter des informations générales (sexe, classe)
    @st.cache_data
    def enrich_with_student_info(decrochages_par_matiere, df_notes_devoir):
        profil_eleve = df_notes_devoir[['eleve_id', 'sexe', 'classes']].drop_duplicates()
        return decrochages_par_matiere.merge(profil_eleve, on='eleve_id', how='left')

    # 8. Visualisation des décrochages par matière
    def plot_dropouts_by_subject(decrochages_par_matiere):
        fig = px.bar(
            decrochages_par_matiere.groupby('matiere')['nombre_de_décrochages'].sum().reset_index().sort_values(by='nombre_de_décrochages', ascending=False),
            x='matiere',
            y='nombre_de_décrochages',
            title="Répartition des décrochages par matière",
            labels={'nombre_de_décrochages': 'Nombre de Décrochages', 'matiere': 'Matière'}
        )
        st.plotly_chart(fig, use_container_width=True)

    # 9. Visualisation des décrochages par sexe et matière
    def plot_dropouts_by_gender_and_subject(decrochages_par_matiere):
        fig = px.bar(
            decrochages_par_matiere.groupby(['sexe', 'matiere'])['nombre_de_décrochages'].sum().reset_index().sort_values(by='nombre_de_décrochages', ascending=False),
            x='matiere',
            y='nombre_de_décrochages',
            color='sexe',
            title="Décrochages par genre et matière",
            labels={'nombre_de_décrochages': 'Nombre de Décrochages', 'matiere': 'Matière', 'sexe': 'Sexe'},
            barmode='group',
            color_discrete_sequence=couleurs_filles_garcons
        )
        st.plotly_chart(fig, use_container_width=True)

    # 10. Visualisation des décrochages par classe
    def plot_dropouts_by_class(decrochages_par_matiere):
        fig = px.bar(
            decrochages_par_matiere.groupby('classes')['nombre_de_décrochages'].sum().reset_index().sort_values(by='nombre_de_décrochages', ascending=False),
            x='classes',
            y='nombre_de_décrochages',
            title="Répartition des décrochages par classe",
            labels={'nombre_de_décrochages': 'Nombre de Décrochages', 'classes': 'Classe'}
        )
        st.plotly_chart(fig, use_container_width=True)

    # Appeler les fonctions dans un flux logique
    df_notes_devoir = prepare_data(df_notes_devoir)
    moyenne_jour = calculate_daily_average(df_notes_devoir)
    moyenne_jour = identify_dropouts(moyenne_jour, seuil=-5, periode_jours=15)
    taux_decrochage = calculate_dropout_rate(moyenne_jour)

    decrochages_par_matiere = compute_dropouts_by_subject(moyenne_jour, df_notes_devoir)
    decrochages_par_matiere = enrich_with_student_info(decrochages_par_matiere, df_notes_devoir)

    col1, col2 =st.columns(2)
    with col1 :

        plot_dropout_rate(taux_decrochage)

        plot_dropouts_by_class(decrochages_par_matiere)

    with col2:

        plot_dropouts_by_gender_and_subject(decrochages_par_matiere)

        plot_dropouts_by_subject(decrochages_par_matiere)


    with st.container(border=True):
        st.markdown("""

1. **Évolution du taux de décrochage dans le temps** :
   L'évolution montre des pics sporadiques liés à des périodes de baisse significative des notes (5 points sur 15 jours). Ces variations peuvent être influencées par des périodes d'examens, des événements pédagogiques, ou des vacances.

2. **Répartition des décrochages par matière** :
   Les matières comme **Histoire-Géo/EMC** et **Mathématiques** concentrent le plus grand nombre de décrochages.

3. **Décrochages par sexe et matière** :
   On observe une disparité notable : les garçons décrochent davantage en **Mathématiques**, tandis que les filles montrent une proportion plus équilibrée entre les matières comme **Français** et **Histoire-Géo/EMC**.

4. **Répartition des décrochages par classe** :
   Les classes de **1B/C** et **2A** enregistrent les niveaux les plus élevés de décrochages.

""")
    st.write("")
    st.subheader("Corrélations entre les Matières", divider="gray")

    st.write("Ces graphiques permettent d'analyser les corrélations entre les moyennes obtenues par les élèves dans différentes matières. Celui de droite illustre visuellement ces corrélations, allant de -1 (corrélation négative forte) à +1 (corrélation positive forte), avec des couleurs indiquant l'intensité des relations : plus le bleu est foncé, plus la corrélation est forte et positive.")

    def compute_subject_correlations(df):
        """
        Calculer les corrélations entre les matières à partir des notes des élèves.
        """
        # Pivot des données pour avoir les matières en colonnes et les élèves en lignes
        pivot_df = df.pivot_table(index='eleve_id', columns='matiere', values='note_sur_20', aggfunc='mean')

        # Calculer la matrice de corrélation
        correlation_matrix = pivot_df.corr()
        return correlation_matrix

    def plot_correlation_heatmap(correlation_matrix):
        """
        Afficher le heatmap des corrélations entre matières avec Plotly.
        """
        # Créer une heatmap avec Plotly
        fig = px.imshow(
            correlation_matrix,
            labels=dict(x="Matière 1", y="Matière 2", color="Corrélation"),
            x=correlation_matrix.columns,
            y=correlation_matrix.index,
            color_continuous_scale='RdBu',
            zmin=-1,
            zmax=1,
            title="Corrélations entre Matières"
        )

        # Ajuster le layout
        fig.update_layout(
            title_font_size=18,
            xaxis_title=None,
            yaxis_title=None,
            margin=dict(l=100, r=100, t=50, b=50)
        )

        # Afficher dans Streamlit
        st.plotly_chart(fig, use_container_width=True)


    # Calculer la matrice de corrélation
    correlation_matrix = compute_subject_correlations(df_notes_devoir)

    # Afficher les visualisations
    @st.cache_data
    def get_top_correlations(correlation_matrix, n=10):
        """
        Récupère les n paires avec les corrélations les plus élevées à partir de la matrice de corrélation.
        """
        # Réorganiser la matrice de corrélation en une liste
        corr_pairs = correlation_matrix.unstack()  # Convertir la matrice en série
        corr_pairs = corr_pairs.drop_duplicates()  # Supprimer les doublons symétriques
        corr_pairs = corr_pairs[corr_pairs.index.get_level_values(0) != corr_pairs.index.get_level_values(1)]  # Exclure les auto-corrélations

        # Ajouter des noms temporaires aux index pour éviter les conflits
        corr_pairs.index.names = ['Matière 1', 'Matière 2']

        # Trier par valeur absolue pour avoir les corrélations les plus fortes (positives ou négatives)
        sorted_corr = corr_pairs.abs().sort_values(ascending=False).head(n)

        # Résolution du conflit de colonnes lors de reset_index
        top_corr_df = sorted_corr.reset_index()  # Reset index en un DataFrame
        top_corr_df.columns = ['Matière 1', 'Matière 2', 'Corrélation']  # Renommer explicitement les colonnes

        return top_corr_df


    # Utilisation
    top_corr_df = get_top_correlations(correlation_matrix, n=10)

    def plot_top_correlations_bar(corr_df, n=10):
        """
        Affiche un bar plot horizontal des corrélations les plus élevées.

        Parameters:
            corr_df (DataFrame): Un DataFrame avec les colonnes ['Matière 1', 'Matière 2', 'Corrélation'].
            n (int): Nombre de paires à afficher.
        """
        # Trier les corrélations par ordre décroissant
        top_corr = corr_df.sort_values(by='Corrélation', ascending=True).head(n)

        # Créer une colonne combinée pour l'affichage
        top_corr['Paires de Matières'] = top_corr['Matière 1'] + " - " + top_corr['Matière 2']

        # Création du graphique
        fig = px.bar(
            top_corr,
            x='Corrélation',
            y='Paires de Matières',
            orientation='h',  # Barres horizontales
            title='Top Paires Corrélées entre Matières',
            labels={'Corrélation': 'Coefficient de Corrélation', 'Paires de Matières': 'Paires de Matières'},
            text='Corrélation'  # Affiche les valeurs sur les barres
        )

        # Ajuster les options de layout pour une meilleure lisibilité
        fig.update_layout(
            yaxis=dict(title=''),
            xaxis=dict(title='Coefficient de Corrélation'),
            margin=dict(l=100, r=20, t=40, b=40),
            height=400
        )

        # Afficher dans Streamlit
        st.plotly_chart(fig, use_container_width=True)

    # Appel de la fonction avec le DataFrame des corrélations

    col1, col2=st.columns(2)
    with col1:
        plot_top_correlations_bar(top_corr_df, n=10)
    with col2:
        plot_correlation_heatmap(correlation_matrix)

    with st.container(border=True):
        st.write("Les corrélations observées entre certaines matières, notamment entre les disciplines scientifiques et technologiques (ex. SNT et SPC), ainsi qu'entre les sciences humaines et les langues (Philosophie et SES), mettent en lumière des convergences dans les compétences mobilisées, comme l'analyse, la logique ou l'argumentation. Ces résultats suggèrent des opportunités pour développer des projets interdisciplinaires entre les matières les plus fortement corrélées.")









with tab3:
    st.write("")
    st.markdown("""

    Dans ce travail, nous avons analysé les appréciations des bulletins scolaires pour mieux comprendre les retours pédagogiques aux élèves. Voici les scores analysés :

    - **Score de sentiment** :
    Un modèle d'IA appelé [Vader Sentiment Analysis](https://github.com/cjhutto/vaderSentiment) évalue le degré de positivité d’une appréciation en attribuant un score entre 0 (très négatif) et 1 (très positif).

    Les scores suivants sont calculés à l'aide de [GPT-4o Mini](https://openai.com/index/gpt-4o-mini-advancing-cost-efficient-intelligence/), un modèle d’IA avancé :
    - **Score de travail** : Indique si l’appréciation contient une mention **positive sur le travail** de l’élève, 0 sinon.
    - **Score de comportement** : Reflète si l’appréciation souligne un **comportement positif** de l’élève, 0 sinon.
    - **Score d’engagement** : Identifie si l’appréciation mentionne un **engagement positif** en classe, 0 sinon.
    - **Score de détail** : Vérifie si l’appréciation est détaillée, apportant des informations précises (1 = oui, 0 = non).
    - **Score de conseil** : Indique si l’appréciation propose un conseil clair pour l’élève (1 = oui, 0 = non).

    Ces modèles, bien qu’utiles pour identifier des tendances générales, comportent des marges d’erreur et peuvent ne pas toujours refléter fidèlement la nuance des appréciations.

    Ces analyses sont croisées par **niveau de classe**, **genre**, et **matière**, avec une attention particulière portée à leur évolution sur les trois trimestres.
    """)

    st.write("")
    st.subheader('Scores de bulletin par genre et par niveau', divider="gray")

    # Fonction pour créer un graphique
    def create_bar_chart(data, x, y, color, title, category_orders, color_discrete_sequence):
        """
        Crée un graphique en barres avec les paramètres donnés.

        Args:
            data (DataFrame): Données à visualiser.
            x (str): Colonne pour l'axe X.
            y (str): Colonne pour l'axe Y.
            color (str): Colonne pour la couleur.
            title (str): Titre du graphique.
            category_orders (dict): Ordre des catégories pour les axes.
            color_discrete_sequence (list): Séquence des couleurs pour les catégories.

        Returns:
            Figure: Un graphique Plotly.
        """
        fig = px.bar(
            data,
            x=x,
            y=y,
            color=color,
            barmode='group',
            title=title,
            category_orders=category_orders,
            color_discrete_sequence=color_discrete_sequence
        )
        fig.update_layout(
            xaxis_title=None,  # Supprime le label de l'axe X
            yaxis_title=None   # Supprime le label de l'axe Y
        )
        return fig


    # Assurer l'ordre des niveaux
    ordre_niveaux = ['6e', '5e', '4e', 'Seconde', 'Première', 'Terminale']
    df_appreciationprofesseurs['niveau_de_classe'] = pd.Categorical(
        df_appreciationprofesseurs['niveau_de_classe'],
        categories=ordre_niveaux,
        ordered=True
    )


    # Moyennes des scores par genre et niveau
    scores_genre_niveau = df_appreciationprofesseurs.groupby(['sexe', 'niveau_de_classe'])[
        ['score_travail', 'score_comportement', 'score_engagement', 'score_de_sentiment']
    ].mean().reset_index()


    # Créer les colonnes pour les graphiques
    col1, col2 = st.columns(2)

    # Graphique : Score de travail
    with col1:
        fig_1 = create_bar_chart(
            scores_genre_niveau,
            x='niveau_de_classe',
            y='score_travail',
            color='sexe',
            title="Mention du travail : moyenne des scores",
            category_orders={"niveau_de_classe": ordre_niveaux},
            color_discrete_sequence=couleurs_filles_garcons
        )
        st.plotly_chart(fig_1, use_container_width=True)

    # Graphique : Score de comportement
    with col2:
        fig_2 = create_bar_chart(
            scores_genre_niveau,
            x='niveau_de_classe',
            y='score_comportement',
            color='sexe',
            title="Mention du comportement : moyenne des scores",
            category_orders={"niveau_de_classe": ordre_niveaux},
            color_discrete_sequence=couleurs_filles_garcons
        )
        st.plotly_chart(fig_2, use_container_width=True)

    # Ajouter une deuxième ligne pour les deux autres graphiques
    col3, col4 = st.columns(2)

    # Graphique : Score d'engagement
    with col3:
        fig_3 = create_bar_chart(
            scores_genre_niveau,
            x='niveau_de_classe',
            y='score_engagement',
            color='sexe',
            title="Mention de l'engagement : moyenne des scores",
            category_orders={"niveau_de_classe": ordre_niveaux},
            color_discrete_sequence=couleurs_filles_garcons
        )
        st.plotly_chart(fig_3, use_container_width=True)

    # Graphique : Score de sentiment
    with col4:
        fig_4 = create_bar_chart(
            scores_genre_niveau,
            x='niveau_de_classe',
            y='score_de_sentiment',
            color='sexe',
            title="Sentiment global : moyennne des scores",
            category_orders={"niveau_de_classe": ordre_niveaux},
            color_discrete_sequence=couleurs_filles_garcons
        )
        st.plotly_chart(fig_4, use_container_width=True)





    # Fonction pour afficher un graphique d'évolution
    def plot_evolution(evolution_scores, y_column, title):
        """
        Crée un graphique d'évolution basé sur les scores moyens par trimestre et niveau de classe.

        Args:
            evolution_scores (DataFrame): Données agrégées avec les moyennes.
            y_column (str): Nom de la colonne à afficher sur l'axe Y.
            title (str): Titre du graphique.

        Returns:
            Figure: Un graphique Plotly.
        """
        fig = px.line(
            evolution_scores,
            x='trimestre',
            y=y_column,
            color='niveau_de_classe',
            title=title,
            category_orders={"niveau_de_classe": ordre_niveaux}
        )
        fig.update_layout(
            xaxis_title=None,  # Supprimer les labels des axes si nécessaire
            yaxis_title=None,
            legend_title="Niveau de classe"
        )
        return fig


    # Moyennes trimestrielles des scores par niveau de classe et trimestre
    evolution_scores = df_appreciationprofesseurs.groupby(
        ['trimestre', 'niveau_de_classe']
    )[['score_travail', 'score_comportement', 'score_engagement']].mean().reset_index()

    # Titre de la page
    st.write("")
    st.subheader("Évolution des scores par trimestre et niveau de classe", divider="gray")

    # Création des colonnes pour organiser les graphiques
    col1, col2, col3 = st.columns(3)

    # Graphique : Évolution des scores de travail
    with col1:
        fig_travail = plot_evolution(evolution_scores, 'score_travail', "Scores de travail")
        st.plotly_chart(fig_travail, use_container_width=True)

    # Graphique : Évolution des scores de comportement
    with col2:
        fig_comportement = plot_evolution(evolution_scores, 'score_comportement', "Scores de comportement")
        st.plotly_chart(fig_comportement, use_container_width=True)

    # Graphique : Évolution des scores d'engagement
    with col3:
        fig_engagement = plot_evolution(evolution_scores, 'score_engagement', "Scores d'engagement")
        st.plotly_chart(fig_engagement, use_container_width=True)


    with st.container(border=True):

        st.markdown("""
        Les graphiques montrent des **variations notables** dans les mentions liées au **travail**, au **comportement** et à l’**engagement** selon le **genre** et le **niveau de classe**. Les **filles** semblent obtenir des scores légèrement supérieurs sur la mention du **travail**, tandis que les **garçons** progressent sur le **comportement** en cycle terminal. L’évolution des scores par trimestre met en lumière une **baisse générale de l’engagement** après le **deuxième trimestre**, suggérant une **perte de motivation potentielle** en cours d’année. Ces observations peuvent refléter des **différences dans les attentes des enseignants** ou des **dynamiques de classe**. Il serait utile d’**investiguer davantage** les **pratiques pédagogiques** pour mieux comprendre ces écarts et **adapter les stratégies de suivi ou d’accompagnement** selon les besoins spécifiques des élèves et des groupes.
        """)



    st.write("")
    st.subheader("Details et Conseils par matieres", divider="gray")


    # --- Fonction pour tracer la moyenne des scores par enseignant ---
    def plot_average_score(dataframe, column, title, groupby_col='prof_id'):
        """
        Crée un graphique montrant la moyenne des scores par enseignant.

        Args:
            dataframe (DataFrame): Le DataFrame contenant les données.
            column (str): Colonne contenant le score à analyser (ex. : 'score_detail').
            title (str): Titre du graphique.
            groupby_col (str): Colonne pour le regroupement (ex. : 'prof_id').

        Returns:
            Plotly Figure: Graphique des moyennes.
        """
        averages = dataframe.groupby(groupby_col)[column].mean().reset_index()
        averages.rename(columns={column: "Moyenne", groupby_col: "Enseignant"}, inplace=True)

        fig = px.bar(
            averages,
            x="Enseignant",
            y="Moyenne",
            title=title,
            labels={"Moyenne": "Moyenne du Score"},
            color_discrete_sequence=[px.colors.qualitative.G10[6]],
        )
        fig.update_layout(
            xaxis=dict(
            showticklabels=False),  # Désactiver les étiquettes de l'axe X
            xaxis_title=None,
            yaxis_title="Moyenne du Score",
            xaxis_tickangle=45,
            font=dict(size=12)
        )
        return fig

    # --- Générer les graphiques des moyennes ---
    fig_average_details = plot_average_score(
        df_appreciationprofesseurs,
        'score_detail',
        "Moyenne des scores des 'appréciations détaillées' par enseignant"
    )

    fig_average_conseils = plot_average_score(
        df_appreciationprofesseurs,
        'score_conseil',
        "Moyenne des scores des 'appréciations avec conseil' par enseignant"
    )


    # --- Fonction mise à jour pour l'histogramme uniquement ---
    def plot_distribution_histogram(dataframe, column, title, groupby_col='prof_id'):
        """
        Crée un histogramme montrant la distribution des moyennes des scores par enseignant.

        Args:
            dataframe (DataFrame): Le DataFrame contenant les données.
            column (str): Colonne contenant le score à analyser (ex. : 'score_detail').
            title (str): Titre du graphique.
            groupby_col (str): Colonne pour le regroupement (ex. : 'prof_id').

        Returns:
            Plotly Figure: Histogramme de la distribution.
        """
        # Calculer les moyennes par enseignant
        averages = dataframe.groupby(groupby_col)[column].mean().reset_index()
        averages.rename(columns={column: "Moyenne", groupby_col: "Enseignant"}, inplace=True)

        # Créer l'histogramme
        fig = px.histogram(
            averages,
            x="Moyenne",
            nbins=10,  # Nombre de bins dans l'histogramme
            title=title,
            labels={"Moyenne": "Moyenne des Scores"},
            color_discrete_sequence=[px.colors.qualitative.G10[7]]  # Couleur des barres
        )
        # Personnalisation : espacement et bordures
        fig.update_layout(
            xaxis_title="Moyenne des Scores",
            yaxis_title="Fréquence",
            font=dict(size=12),
            bargap=0.1  # Espacement entre les barres
        )
        return fig

    # --- Tracer pour les deux scores ---
    fig_hist_details = plot_distribution_histogram(
        df_appreciationprofesseurs,
        'score_detail',
        "Distribution des moyennes des scores 'appréciation détaillées'."
    )

    fig_hist_conseils = plot_distribution_histogram(
        df_appreciationprofesseurs,
        'score_conseil',
        "Distribution des moyennes des scores 'appréciation avec conseil'."
    )


    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(fig_average_details, use_container_width=True)

    with col2:
        st.plotly_chart(fig_hist_details, use_container_width=True)


    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(fig_average_conseils, use_container_width=True)

    with col2:
        st.plotly_chart(fig_hist_conseils, use_container_width=True)





    # --- Fonction pour calculer et tracer les moyennes par matière ---
    def plot_average_score_by_subject(dataframe, column, title, groupby_col='matiere'):
        """
        Crée un graphique montrant la moyenne des scores par matière.

        Args:
            dataframe (DataFrame): Le DataFrame contenant les données.
            column (str): Colonne contenant le score à analyser (ex. : 'score_detail').
            title (str): Titre du graphique.
            groupby_col (str): Colonne pour le regroupement (ex. : 'matiere').

        Returns:
            Plotly Figure: Graphique des moyennes.
        """
        averages = dataframe.groupby(groupby_col)[column].mean().reset_index()
        averages.rename(columns={column: "Moyenne", groupby_col: "Matière"}, inplace=True)
        averages = averages.sort_values(by="Moyenne", ascending=False)


        fig = px.bar(
            averages,
            x="Matière",
            y="Moyenne",
            title=title,
            labels={"Moyenne": "Moyenne du Score"},
            color_discrete_sequence=px.colors.qualitative.G10,
        )
        fig.update_layout(
            xaxis_title=None,
            yaxis_title="Moyenne du Score",
            xaxis_tickangle=45,
            font=dict(size=12)
        )
        return fig

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(
            plot_average_score_by_subject(
                df_appreciationprofesseurs,
                "score_detail",
                "Moyenne des scores 'appréciations détaillées' par matière"
            ),
            use_container_width=True
        )

    with col2:
        st.plotly_chart(
            plot_average_score_by_subject(
                df_appreciationprofesseurs,
                "score_conseil",
                "Moyenne des scores avec 'appréciations avec conseils' par matière"
            ),
            use_container_width=True
        )

    with st.container(border=True):
        st.markdown("""
                    Les graphiques révèlent une **forte variabilité** dans les proportions d’appréciations détaillées et avec conseils entre les enseignants. Certains affichent une proportion élevée de scores détaillés, témoignant d’un **engagement important dans la personnalisation des retours**, tandis que d’autres montrent des valeurs plus faibles, reflétant une **hétérogénéité des pratiques pédagogiques**. La majorité des enseignants atteignent des niveaux satisfaisants, mais des efforts pourraient être concentrés sur ceux en dessous de **50 %**. Il est recommandé de renforcer les **bonnes pratiques au sein des équipes** par des ateliers de partage, tout en identifiant les besoins de formation pour améliorer l’usage des conseils pédagogiques.
                    En ce qui concerne les disciplines, les graphiques mettent en évidence des **disparités significatives**. Les matières linguistiques, comme l’espagnol, le français et la philosophie, affichent des taux élevés d’appréciations détaillées, suggérant un effort notable de **personnalisation des retours**. En revanche, des disciplines comme l’éducation musicale ou les arts plastiques enregistrent des scores plus faibles, probablement en lien avec le **nombre d’élèves plus important à gérer**. Pour les conseils pédagogiques, la philosophie et le français se démarquent à nouveau, tandis que les matières scientifiques, comme la technologie ou l’EPS, apparaissent **moins riches en recommandations**. Ces résultats appellent à une **harmonisation des pratiques pédagogiques**, en tenant compte des spécificités disciplinaires, afin d’offrir un accompagnement équilibré et adapté aux élèves.

        """)


    st.write("")
    st.subheader("Correlation entre score des bulletins et moyennes trimestrielles par matiere", divider="gray")

    # --- Étape 1 : Préparer les données ---
    # Calcul de la moyenne des notes trimestrielles pour chaque élève par matière
    avg_notes = df_notes_devoir.groupby(["eleve_id", "matiere"])["note"].mean().reset_index()
    avg_notes.rename(columns={"note": "moyenne_notes"}, inplace=True)

    # Calcul de la moyenne des scores des appréciations pour chaque élève par matière
    avg_scores = df_appreciationprofesseurs.groupby(["eleve_id", "matiere"])[
        ["score_de_sentiment", "score_travail", "score_comportement",
        "score_engagement", "score_detail", "score_conseil"]
    ].mean().reset_index()

    # Fusionner les deux DataFrames pour obtenir une vue complète
    merged_data = pd.merge(avg_notes, avg_scores, on=["eleve_id", "matiere"], how="inner")

    # Vérification de la fusion
    if "matiere" not in merged_data.columns:
        st.error("La colonne 'matiere' est absente après la fusion. Vérifiez vos données.")
        st.stop()

    # --- Étape 2 : Calcul des corrélations ---
    @st.cache_data
    def compute_correlation_by_discipline(data):
        """
        Calcule la corrélation entre la moyenne des notes et les scores des appréciations par discipline.

        Args:
            data (DataFrame): Données fusionnées contenant les notes et les scores.

        Returns:
            DataFrame: Résultats des corrélations par discipline.
        """
        correlation_results = data.groupby("matiere").apply(
            lambda group: pd.Series({
                "correlation_sentiment": group["moyenne_notes"].corr(group["score_de_sentiment"]),
                "correlation_travail": group["moyenne_notes"].corr(group["score_travail"]),
                "correlation_comportement": group["moyenne_notes"].corr(group["score_comportement"]),
                "correlation_engagement": group["moyenne_notes"].corr(group["score_engagement"]),
                "correlation_detail": group["moyenne_notes"].corr(group["score_detail"]),
                "correlation_conseil": group["moyenne_notes"].corr(group["score_conseil"]),
            })
        ).reset_index()

        return correlation_results

    # Calculer les corrélations
    correlation_results = compute_correlation_by_discipline(merged_data)


    # Visualisation des corrélations
    cols = st.columns(3)  # Créer deux colonnes

    for i, col in enumerate(correlation_results.columns[1:]):  # Ignorer la colonne 'matiere'
        with cols[i % 3]:  # Alterner entre les deux colonnes
            st.plotly_chart(
                px.bar(
                    correlation_results,
                    x="matiere",
                    y=col,
                    title=f"Corrélation entre '{col.split('_')[1]}' et moyennes des notes",
                    labels={"matiere": "Matière", col: "Corrélation"},
                    color_discrete_sequence=["#636EFA"]
                ),
                use_container_width=True
            )


    # --- Étape 4 : Distribution des scores et moyennes ---
    st.write("### Distribution des moyennes des scores et des notes par matière")

    # Distribution des moyennes des scores
    score_distribution = merged_data.groupby("matiere")[
        ["score_de_sentiment", "score_travail", "score_comportement",
        "score_engagement", "score_detail", "score_conseil"]
    ].mean().reset_index()
    score_distribution_melted = score_distribution.melt(id_vars="matiere", var_name="Score", value_name="Moyenne")
    st.plotly_chart(
        px.bar(
            score_distribution_melted,
            x="matiere",
            y="Moyenne",
            color="Score",
            barmode="group",
            title="Moyenne des scores d'appréciation par matière",
            labels={"matiere": "Matière", "Moyenne": "Moyenne des Scores"},
            color_discrete_sequence=px.colors.qualitative.G10
        ),
        use_container_width=True
    )

    with st.container(border=True):
        st.markdown("""
Les graphiques révèlent des **corrélations variées** entre les scores d’appréciation et les moyennes des élèves, selon les matières. Des corrélations positives marquées sont observées pour les **matières linguistiques** (français, philosophie, espagnol), notamment pour les scores liés au travail, à l'engagement et au sentiment global, indiquant une cohérence entre les retours des enseignants et les performances des élèves. Cependant, certaines matières comme **les sciences** (SVT, SPC) présentent des corrélations plus faibles, voire négatives pour les scores de détail et de conseil, ce qui pourrait signaler un décalage dans l’évaluation des élèves ou une approche différente des appréciations.

En moyenne, les scores d'appréciation diffèrent également par matière. Les **disciplines littéraires** affichent des scores plus élevés pour les conseils et le détail des retours, tandis que les matières scientifiques présentent des niveaux plus homogènes mais globalement moins élevés. Cela peut refléter des **différences dans les attentes pédagogiques** ou dans la charge de travail liée à la correction et aux retours individualisés.

**Pistes d'actions :**

1. Favoriser une **harmonisation des pratiques d’évaluation**, notamment en sciences, pour aligner les retours sur les performances des élèves.
2. Échanger en conseil pédagogique sur les critères d’appréciation, particulièrement sur les conseils et les retours détaillés, afin de renforcer leur impact des appréciations de bulletins.
4. Exploiter les corrélations positives en matières linguistiques comme **modèle de bonnes pratiques** pour les autres disciplines.

                    """)
