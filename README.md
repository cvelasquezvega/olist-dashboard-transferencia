# Proyecto final – Etapa de Transferencia

Este repositorio contiene el código y los artefactos del dashboard (Dash/Plotly) y el informe del proyecto.
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/cvelasquezvega/olist-dashboard-transferencia/HEAD)


## Estructura
```
proyecto-transferencia/
├─ data/
│  ├─ raw/                  # datos originales (solo lectura)
│  └─ processed/            # datasets limpios para modelar/exportar al dashboard
├─ dashboard/
│  ├─ app.py                # aplicación Dash
│  ├─ assets/               # estilos y logos
│  └─ data/                 # métricas y predicciones para visualización
├─ reports/
│  ├─ informe_final.md      # plantilla del informe
│  └─ figs/                 # figuras exportadas
├─ notebooks/               # EDA, modelado y export de activos
├─ src/                     # utilidades/funciones
├─ requirements.txt
└─ LINKS.txt
```

## Cómo ejecutar
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate
pip install -r requirements.txt

cd dashboard
python app.py
```

## Datos esperados por el dashboard
- `dashboard/data/metrics.csv` columnas: `run,metric,value,model,timestamp`
- `dashboard/data/predicciones.csv` columnas: `id,y_true,y_pred,split,segmento`

> Reemplaza los CSV de ejemplo por tus salidas reales desde `notebooks/`.
