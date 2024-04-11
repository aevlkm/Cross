# CROSS STREAMLIT PROJECT

# --- LIBRAIRIES ---

import streamlit as st
import pandas as pd

# --- Plotly
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
# pio.renderers.default = 'firefox'

# --- Machine Learning
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import roc_auc_score




# --- PAGE CONFIG ---
st.set_page_config(page_title='Cross Project', page_icon=':boat:', layout='wide')

# --- DATA IMPORT ---
@st.cache_data
def get_data():
  encoding_norm = "UTF-8"
  separator = ","
  file_name = "../02_Data_output/cross.csv"
  df_cross = pd.read_csv(file_name, sep=separator, low_memory=False, encoding=encoding_norm)
  return df_cross

df_cross = get_data()


# --- MACHINE LEARNING ---
@st.cache_resource
def train_model(df):

    # --- Features ---
    X = df[['evenement', 
                'nombre_personnes_impliquees', 
                'sous_categorie_flotteurs', 
                'distance_cote_milles_nautiques', 
                'vent_direction_categorie', 
                'vent_force', 
                'mer_force', 
                'maree_coefficient', 
                'saison', 
                'phase_journee']]

    # --- Target ---
    y = df['bilan_humain_encode2']

    # --- Numeric Preprocessing
    numeric_features = ['nombre_personnes_impliquees', 
                        'distance_cote_milles_nautiques']

    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='mean')),
        ('scaler', StandardScaler())
    ])

    # --- Categorical Preprocessing
    categorical_features = ['evenement', 
                            'sous_categorie_flotteurs', 
                            'vent_direction_categorie', 
                            'saison', 
                            'phase_journee']
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent', fill_value='Non Renseigné')),
        ('onehot', OneHotEncoder())
    ])

    # --- Encoding
    encoder = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])

    # --- Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # --- Training
    pipeline = Pipeline(steps=[('encoder', encoder),
                               ('classifier', RandomForestClassifier(n_estimators=100, max_depth=18, random_state=42))])
    pipeline.fit(X_train, y_train)

    y_score = pipeline.predict_proba(X_test)
    roc = roc_auc_score(y_test, y_score, multi_class='ovr', average='micro')

    # --- Return
    return pipeline, roc

# --- TRAIN MODEL ---
model, roc = train_model(df_cross)





# --- STREAMLIT ---
header = st.container(border=False)
header.header("C.R.O.S.S. 🛟  -  _Centres Régionaux Opérationnels de Surveillance et de Sauvetage_")
header.write("""<div class='fixed-header'/>""", unsafe_allow_html=True)



with header:
    st.divider()
    largeur = 150
    col1, col2, col3, col4, col5, col6 = st.columns(6, gap='medium')

    with col1:
        st.image('../99_Pictures/Logos_Streamlit/cross_grisnez.jpg', width=largeur)
    with col2:
        st.image('../99_Pictures/Logos_Streamlit/cross_jobourg.jpg', width=largeur)
    with col3:
        st.image('../99_Pictures/Logos_Streamlit/cross_corsen.jpg', width=largeur)
    with col4:
        st.image('../99_Pictures/Logos_Streamlit/cross_etel.jpg', width=largeur)
    with col5:
        st.image('../99_Pictures/Logos_Streamlit/cross_lagarde.jpg', width=largeur)
    with col6:
        st.image('../99_Pictures/Logos_Streamlit/cross_corse.jpg', width=largeur)

    st.divider()
### Custom CSS for the sticky header
st.markdown(
    """
    <style>
        div[data-testid="stVerticalBlock"] div:has(div.fixed-header) {
            position: sticky;
            top: 0rem;
            background-color: rgba(14, 17, 23, 100);
            z-index: 1200;
        }
    </style>
    """,
    unsafe_allow_html=True
)




# --- SIDEBAR ---

# --- Période
st.sidebar.header('PÉRIODE')

toggle = st.sidebar.toggle("SAISON")
if toggle == True:
    saison = 'Haute saison'
else:
    saison = 'Basse saison'

phase_journee = st.sidebar.selectbox("MOMENT DE L'ÉVÈNEMENT", options = sorted(df_cross['phase_journee'].unique()), index = 2)

# --- Position
st.sidebar.divider()
st.sidebar.header('POSITION')
distance_cote_milles_nautiques = st.sidebar.number_input("EN MILLES NAUTIQUES", step=0.1)
latitude = st.sidebar.number_input("LATITUDE", step=0.1)
longitude = st.sidebar.number_input("LONGITUDE", step=0.1)

# --- Mer
st.sidebar.divider()
st.sidebar.header('MER')
maree_coefficient = st.sidebar.selectbox('COEFFICIENT DE MARÉE', options = sorted(df_cross['maree_coefficient'].unique()), index = 1)
mer_force = st.sidebar.selectbox('ÉCHELLE DE DOUGLAS', options = sorted(df_cross['mer_force'].unique()), index = 1)

# --- Vent
st.sidebar.divider()
st.sidebar.header('VENT')
vent_direction_categorie = st.sidebar.selectbox('DIRECTION', options = df_cross['vent_direction_categorie'].unique(), index = 1)
vent_force = st.sidebar.selectbox("ÉCHELLE DE BEAUFORT", options = sorted(df_cross['vent_force'].unique()), index = 1)



# --- LOWER MAIN PAGE ---
col1, col2 = st.columns(2)

with col1 :

    # st.subheader('CARTE')

    # --- Map Dataframe Creation
    lati = latitude
    longi = longitude
    # colors_list_1 = ['#B3B3B3', '#B3B3B3', '#B3B3B3', '#B3B3B3', '#B3B3B3', '#B3B3B3', 'rgba(255,0,0,0)']
    # colors_list_2 = ['#B3B3B3', '#B3B3B3', '#B3B3B3', '#B3B3B3', '#B3B3B3', '#B3B3B3', '#D10000']
    colors_list_1 = ['black', 'black', 'black', 'black', 'black', 'black', 'rgba(255,0,0,0)']
    colors_list_2 = ['black', 'black', 'black', 'black', 'black', 'black', 'red']

    if lati == 0 and lati == 0:
        df_map = pd.DataFrame(dict({
            'nom' : ['CROSS Étel', 'CROSS La Garde', 'CROSS Corsen', 'CROSS Gris-Nez', 'CROSS Jobourg', 'CROSS Corse', 'Position'],
            'latitude' : [47.6618308, 43.1228, 48.4176632, 50.868101, 49.690402, 41.9272, 46.6424],
            'longitude' : [-3.2020183, 6.0075, -4.7867433, 1.584522, -1.934722, 8.7346, 0.7542],
            'colors' : colors_list_1
        }))
    else:
        df_map = pd.DataFrame(dict({
            'nom' : ['CROSS Étel', 'CROSS La Garde', 'CROSS Corsen', 'CROSS Gris-Nez', 'CROSS Jobourg', 'CROSS Corse', 'Position'],
            'latitude' : [47.6618308, 43.1228, 48.4176632, 50.868101, 49.690402, 41.9272, lati],
            'longitude' : [-3.2020183, 6.0075, -4.7867433, 1.584522, -1.934722, 8.7346, longi],
            'colors' : colors_list_2
        }))


    # --- Map Calculation
    fig = px.scatter_mapbox(df_map, 
                            lat = 'latitude',
                            lon = 'longitude',
                            hover_name= 'nom',
                            zoom = 4.6,
                            mapbox_style = "carto-positron")


    fig.update_layout(height=570, width=850)
    fig.update_traces(marker=dict(size=12, color=df_map['colors']))
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    # fig.update_layout(mapbox_style="carto-darkmatter")


    st.plotly_chart(fig)

with col2 :

    st.subheader('SITUATION')
    evenement = st.selectbox('ÉVÈNEMENT', options = sorted(df_cross['evenement'].unique()))

    sous_categorie_flotteurs = st.selectbox('FLOTTEURS', options = sorted(df_cross['sous_categorie_flotteurs'].unique()))


    nombre_personnes_impliquees = st.text_input('PERSONNES IMPLIQUÉES', 1)

    # --- Entries Table Creation
    donnees = {'evenement' : [evenement],
                'nombre_personnes_impliquees' : [nombre_personnes_impliquees],
                'sous_categorie_flotteurs' : [sous_categorie_flotteurs],
                'distance_cote_milles_nautiques' : [distance_cote_milles_nautiques],
                'vent_direction_categorie' : [vent_direction_categorie],
                'vent_force' : [vent_force],
                'mer_force' : [mer_force],
                'maree_coefficient' : [maree_coefficient],
                'saison' : [saison],
                'phase_journee' : [phase_journee]
                }

    entries_table = pd.DataFrame(data=donnees)



    # --- Criticité Table Creation
    df_criticite = pd.DataFrame(dict({
                'prediction' : [0, 1, 2, 3, 4, 5, 6, 7],
                # 'assistance' : [0, 0, 0, 0, 1, 1, 1, 1],
                # 'secours' : [0, 0, 1, 1, 0, 0, 1, 1],
                # 'deces' : [0, 1, 0, 1, 0, 1, 0, 1],
                'colors' : ['green', 'red', 'orange', 'red', 'green', 'red', 'orange', 'red'],
                'Criticité' : ['Très faible', 'Maximale', 'Elevée', 'Maximale', 'Faible', 'Maximale', 'Elevée', 'Maximale'],
                'signification' : ["Opération ne nécessitant pas d'engagement de moyens particuliers.", 
                                "Opération nécessitant le déclenchement rapide d'une force nautique et/ou terrestre et/ou aérienne.", 
                                "Opération nécessitant le déclenchement d'une force nautique et/ou terrestre et/ou aérienne.",
                                "Opération nécessitant le déclenchement rapide d'une force nautique et/ou terrestre et/ou aérienne.",
                                "Opération nécessitant uniquement une assistance à distance.",
                                "Opération nécessitant le déclenchement rapide d'une force nautique et/ou terrestre et/ou aérienne.",
                                "Opération nécessitant le déclenchement d'une force nautique et/ou terrestre et/ou aérienne.",
                                "Opération nécessitant le déclenchement rapide d'une force nautique et/ou terrestre et/ou aérienne."
                                ]
            }))

    st.divider()

    # --- Prediction
    prediction = model.predict(entries_table)

    if df_criticite.iloc[int(prediction), 2] == 'Très faible':
         st.subheader('CRITICITÉ ⬜')
    if df_criticite.iloc[int(prediction), 2] == 'Faible':
         st.subheader('CRITICITÉ 🟩')
    if df_criticite.iloc[int(prediction), 2] == 'Elevée':
         st.subheader('CRITICITÉ 🟨')
    if df_criticite.iloc[int(prediction), 2] == 'Maximale':
         st.subheader('CRITICITÉ 🟥')


    st.text_area('', f'{df_criticite.iloc[int(prediction), 2]} : \n  \n {df_criticite.iloc[int(prediction), 3]}')

    # st.text_area('roc', roc)















# --- HIDE PAGE ELEMENTS ---------------------------------------------------------------------
hide_st_style = """
                <style>
                footer {visibility : hidden;}
                header {visibility : hidden;}
                """
#MainMenu {visibility : hidden;}
st.markdown(hide_st_style, unsafe_allow_html=True)