# Mapa Emocional Interactivo de Composiciones Musicales
# Proyecto Terminal - UAM Cuajimalpa 2025

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

# 1. CARGAR EXCEL

df = pd.read_excel("matriz_pivot_con_genero.xlsx")

emotion_columns = df.select_dtypes(include="number").columns


# 2. NORMALIZACIÓN + PCA
X_scaled = StandardScaler().fit_transform(df[emotion_columns])
coords = PCA(n_components=2, random_state=42).fit_transform(X_scaled)
df["x"], df["y"] = coords[:, 0], coords[:, 1]

# 3. K-MEANS
df["cluster"] = KMeans(n_clusters=3, random_state=42).fit_predict(X_scaled)

# 4. AUDIO
df["archivo_audio"] = "/assets/" + df["ID_Cancion"].astype(str) + "_clip.mp3"

# 5. CLUSTERS
cluster_names = {
    0: "Energía Positiva",
    1: "Calma Afectiva",
    2: "Intensidad Emocional"
}

cluster_letters = {0: "E", 1: "C", 2: "I"}

cluster_colors = {
    0: "#3ddc84",
    1: "#4dabf7",
    2: "#ff6b6b"
}


# 6. FUNCIÓN PARA CREAR FIGURA
def crear_figura(frame=0, activos=[0, 1, 2]):
    fig = go.Figure()

    for c in activos:
        df_c = df[df["cluster"] == c]

        # ANIMACIÓN FLOTANTE
        dx = 0.04 * np.sin(frame / 10 + c)
        dy = 0.04 * np.cos(frame / 12 + c)

        fig.add_trace(go.Scatter(
            x=df_c["x"] + dx,
            y=df_c["y"] + dy,
            mode="text",
            text=[cluster_letters[c]] * len(df_c),
            textfont=dict(
                size=18,
                family="Arial Black",
                color=cluster_colors[c]
            ),
            customdata=df_c[["archivo_audio", "ID_Cancion", "Genero"]],
            hovertemplate=
                "<b>%{customdata[1]}</b><br>"
                "Género: %{customdata[2]}<br>"
                f"{cluster_names[c]}<extra></extra>",
            name=cluster_names[c]
        ))

    fig.update_layout(
        paper_bgcolor="#020617",
        plot_bgcolor="#020617",
        showlegend=False,

        title=dict(
            text="Mapa Emocional Interactivo De Composiciones Musicales",
            x=0.5,
            font=dict(size=20, color="white")
        ),

        transition=dict(duration=80),
        margin=dict(l=40, r=40, t=70, b=40)
    )

    fig.update_xaxes(showgrid=False, visible=False)
    fig.update_yaxes(showgrid=False, visible=False)

    fig.update_traces(
        opacity=0.95,
        textposition="middle center",
        textfont_shadow="0px 0px 8px rgba(255,255,255,0.35)", 
        hoverlabel=dict(
            bgcolor="#020617",
            font_size=13,
            font_family="Arial",
            font_color="white"
        )
    )

    return fig


# 7. APP
app = dash.Dash(__name__)

app.layout = html.Div(
    style={"display": "flex", "height": "100vh", "backgroundColor": "#020617"},
    children=[

        # PANEL LATERAL
        html.Div(
            style={
                "width": "300px",
                "padding": "20px",
                "color": "white",
                "borderRight": "1px solid #1e293b"
            },
            children=[
                html.H3("Clusters emocionales"),
                dcc.Checklist(
                    id="selector-cluster",
                    options=[
                        {"label": " Energía Positiva", "value": 0},
                        {"label": " Calma Afectiva", "value": 1},
                        {"label": " Intensidad Emocional", "value": 2}
                    ],
                    value=[0, 1, 2],
                    labelStyle={"display": "block", "marginBottom": "8px"}
                ),
                html.Hr(),
                html.P("Mapa emocional animado"),
                html.P("Hover para escuchar canciones")
            ]
        ),

        # MAPA
        html.Div(
            style={"flex": 1},
            children=[
                dcc.Graph(id="mapa"),
                html.Audio(id="audio", autoPlay=True, style={"display": "none"}),
                dcc.Interval(id="intervalo", interval=80, n_intervals=0)
            ]
        )
    ]
)

# 8. CALLBACKS
@app.callback(
    Output("mapa", "figure"),
    Input("intervalo", "n_intervals"),
    Input("selector-cluster", "value")
)
def actualizar_figura(frame, activos):
    return crear_figura(frame, activos)

@app.callback(
    Output("audio", "src"),
    Input("mapa", "hoverData")
)
def reproducir_audio(hoverData):
    if hoverData is None:
        return ""
    return hoverData["points"][0]["customdata"][0]

# 9. RUN
if __name__ == "__main__":
    app.run(debug=True)
