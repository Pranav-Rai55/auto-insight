# visualization.py

import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from matplotlib_venn import venn2, venn3
import pandas as pd

# --------------------------
# Bar Chart
# --------------------------
def bar_chart(df, x_col, y_col, title="Bar Chart"):
    fig = px.bar(df, x=x_col, y=y_col, title=title)
    fig.show()

# --------------------------
# Column Chart (Vertical Bar)
# --------------------------
def column_chart(df, x_col, y_col, title="Column Chart"):
    fig = px.bar(df, x=x_col, y=y_col, orientation='v', title=title)
    fig.show()

# --------------------------
# Stacked Bar/Column Chart
# --------------------------
def stacked_bar_chart(df, x_col, y_cols, title="Stacked Bar Chart"):
    fig = go.Figure()
    for col in y_cols:
        fig.add_trace(go.Bar(name=col, x=df[x_col], y=df[col]))
    fig.update_layout(barmode='stack', title=title)
    fig.show()

# --------------------------
# Pie Chart
# --------------------------
def pie_chart(df, names_col, values_col, title="Pie Chart"):
    fig = px.pie(df, names=names_col, values=values_col, title=title)
    fig.show()

# --------------------------
# Donut Chart
# --------------------------
def donut_chart(df, names_col, values_col, title="Donut Chart"):
    fig = px.pie(df, names=names_col, values=values_col, hole=0.4, title=title)
    fig.show()

# --------------------------
# Area Chart
# --------------------------
def area_chart(df, x_col, y_cols, title="Area Chart"):
    fig = go.Figure()
    for col in y_cols:
        fig.add_trace(go.Scatter(x=df[x_col], y=df[col], fill='tonexty', mode='lines', name=col))
    fig.update_layout(title=title)
    fig.show()

# --------------------------
# Venn Diagram (2 or 3 sets)
# --------------------------
def venn_diagram(sets, labels):
    if len(sets) == 2:
        venn2(sets, set_labels=labels)
    elif len(sets) == 3:
        venn3(sets, set_labels=labels)
    else:
        raise ValueError("Venn diagram supports only 2 or 3 sets")
    plt.show()

# --------------------------
# Histogram
# --------------------------
def histogram(df, col, bins=10, title="Histogram"):
    fig = px.histogram(df, x=col, nbins=bins, title=title)
    fig.show()

# --------------------------
# Geographical Heatmap
# --------------------------
def geo_heatmap(df, lat_col, lon_col, value_col, title="Geographical Heatmap"):
    fig = px.density_mapbox(df, lat=lat_col, lon=lon_col, z=value_col, radius=10,
                            center=dict(lat=df[lat_col].mean(), lon=df[lon_col].mean()),
                            zoom=3, mapbox_style="open-street-map", title=title)
    fig.show()
