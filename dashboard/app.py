import pandas as pd
from pathlib import Path
from dash import Dash, html, dcc, dash_table, Input, Output
import plotly.express as px

BASE = Path(__file__).resolve().parent
df_metrics = pd.read_csv(BASE / "data" / "metrics.csv")
df_preds   = pd.read_csv(BASE / "data" / "predicciones.csv")

app = Dash(__name__, title="Modelo – Etapa de Transferencia")
app.layout = html.Div([
    html.H2("Tablero del Modelo – Transferencia"),
    html.P("Explora desempeño, distribuciones y segmentos para decisiones accionables."),

    html.Div([
        html.Div([
            html.Label("Métrica"),
            dcc.Dropdown(
                id="metric-dd",
                options=[{"label": m, "value": m} for m in df_metrics["metric"].unique()],
                value=df_metrics["metric"].unique()[0],
                clearable=False
            )
        ], style={"width":"25%","display":"inline-block","padding":"0 10px"}),

        html.Div([
            html.Label("Modelo"),
            dcc.Dropdown(
                id="model-dd",
                options=[{"label": m, "value": m} for m in df_metrics["model"].unique()],
                value=df_metrics["model"].unique()[0],
                clearable=False
            )
        ], style={"width":"25%","display":"inline-block","padding":"0 10px"}),

        html.Div([
            html.Label("Segmento (opcional)"),
            dcc.Dropdown(
                id="seg-dd",
                options=[{"label": s, "value": s} for s in ["ALL"] + sorted(df_preds["segmento"].dropna().unique().tolist())],
                value="ALL", clearable=False
            )
        ], style={"width":"25%","display":"inline-block","padding":"0 10px"}),
    ]),

    dcc.Graph(id="metric-trend"),
    dcc.Graph(id="error-dist"),

    html.H4("Muestras y errores por observación"),
    dash_table.DataTable(
        id="tbl",
        page_size=10,
        sort_action="native",
        filter_action="native",
        style_table={"overflowX":"auto"},
    ),

    html.Hr(),
    html.P("Use este tablero junto al informe para interpretar supuestos, límites y próximos pasos.")
])

@app.callback(
    Output("metric-trend", "figure"),
    Output("error-dist", "figure"),
    Output("tbl", "data"),
    Output("tbl", "columns"),
    Input("metric-dd", "value"),
    Input("model-dd", "value"),
    Input("seg-dd", "value"),
)
def update(metric, model, segmento):
    dm = df_metrics.query("metric == @metric and model == @model").sort_values("timestamp")
    fig1 = px.line(dm, x="timestamp", y="value", markers=True, title=f"Evolución de {metric} – {model}")

    df = df_preds.copy()
    if segmento != "ALL":
        df = df.query("segmento == @segmento")

    df = df.assign(error=(df["y_pred"] - df["y_true"]).abs())
    fig2 = px.histogram(df, x="error", nbins=30, title="Distribución de error absoluto")

    cols = [{"name": c, "id": c} for c in df.columns]
    return fig1, fig2, df.to_dict("records"), cols

if __name__ == "__main__":
    app.run_server(debug=True)
