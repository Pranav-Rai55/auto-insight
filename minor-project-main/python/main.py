# main.py — Compact Tableau-Style Dashboard with Improved Summary Statistics & Dynamic Title

import pandas as pd
import plotly.express as px
import plotly.io as pio
import webbrowser
import os
from upload import load_data_from_path
from cleaning import remove_duplicates, handle_missing
from analysis import correlation
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

app = FastAPI()


# Allow only your React app to access Python backend
origins = [
    "http://localhost:5173",  # React dev server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Python server connected with React ✔"}

@app.post("/process")
async def process_file(file: UploadFile = File(...)):
    # 1️⃣ Read uploaded CSV
    df = pd.read_csv(file.file)

    # 2️⃣ Save uploaded file so dashboard generator can use it
    temp_path = "uploaded.csv"
    df.to_csv(temp_path, index=False)

    # 3️⃣ Update global DATA_FILE_PATH
    global DATA_FILE_PATH
    DATA_FILE_PATH = temp_path

    # 4️⃣ Call your existing dashboard generator
    generate_dashboard()

    # 5️⃣ Return the URL of the generated HTML file
    return {
        "html_url": "http://localhost:8000/dashboard"
    }


@app.get("/dashboard")
def serve_dashboard():
    return FileResponse("dashboard.html")

# --------------------------
# CONFIGURATION
# --------------------------
DATA_FILE_PATH = r"C:\Users\nakul\OneDrive\Desktop\amazon_sales_dataset_500.csv"  # Change this path
OUTPUT_FILE = "dashboard.html"


# --------------------------
# Helper Functions
# --------------------------
def format_rupees(value):
    """Format number as Indian currency (e.g., ₹12.45L or ₹1.2M)."""
    if value >= 1_000_000:
        return f"₹{value/1_000_000:.2f}M"
    elif value >= 100_000:
        return f"₹{value/100_000:.2f}L"
    elif value >= 1_000:
        return f"₹{value/1_000:.2f}K"
    else:
        return f"₹{value:,.0f}"


def pick_columns(df):
    """Auto-detect numeric, categorical, datetime, and key chart columns."""
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    categorical_cols = df.select_dtypes(include='object').columns.tolist()
    datetime_cols = df.select_dtypes(include=['datetime', 'datetimetz']).columns.tolist()

    for col in categorical_cols[:]:
        try:
            df[col] = pd.to_datetime(df[col])
            datetime_cols.append(col)
            categorical_cols.remove(col)
        except Exception:
            pass

    time_col = min(datetime_cols, key=lambda c: df[c].isna().sum()) if datetime_cols else None
    pie_col, val_col, hist_col, stacked_cols = None, None, None, []

    for c in categorical_cols:
        if df[c].nunique() <= 15:
            pie_col = c
            val_col = numeric_cols[0] if numeric_cols else None
            break

    if numeric_cols:
        hist_col = df[numeric_cols].var().idxmax()

    if numeric_cols and categorical_cols:
        x_col = categorical_cols[0]
        y_col = numeric_cols[0]
        color_col = categorical_cols[1] if len(categorical_cols) > 1 else None
        stacked_cols = [x_col, y_col, color_col]

    return numeric_cols, categorical_cols, time_col, stacked_cols, pie_col, val_col, hist_col


def generate_kpis(df, numeric_cols):
    """Generate compact single-line KPI cards."""
    kpi_colors = ["#00E5FF", "#FF6B6B", "#FFD93D", "#8B5CF6"]
    kpis_html = "<div class='kpi-container'>"
    kpis_html += f"<div class='kpi' style='border-color:{kpi_colors[0]}'><h3>Total Rows</h3><p>{len(df):,}</p></div>"
    kpis_html += f"<div class='kpi' style='border-color:{kpi_colors[1]}'><h3>Total Columns</h3><p>{len(df.columns)}</p></div>"

    revenue_col = next((col for col in numeric_cols if 'revenue' in col.lower()), None)
    units_col = next((col for col in numeric_cols if 'unit' in col.lower() and 'sold' in col.lower()), None)

    if revenue_col:
        total_revenue = df[revenue_col].sum()
        kpis_html += f"""
            <div class='kpi' style='border-color:{kpi_colors[2]}'>
                <h3>Revenue</h3>
                <p>{format_rupees(total_revenue)}</p>
            </div>
        """

    if units_col:
        total_units = int(df[units_col].sum())
        kpis_html += f"""
            <div class='kpi' style='border-color:{kpi_colors[3]}'>
                <h3>Units Sold</h3>
                <p>{total_units:,}</p>
            </div>
        """

    kpis_html += "</div>"
    return kpis_html


def generate_summary(df):
    """Generate clean, formatted summary statistics for numeric columns."""
    numeric_df = df.select_dtypes(include='number')
    if numeric_df.empty:
        return "<p>No numeric data available for summary statistics.</p>"

    summary = numeric_df.describe().T.reset_index()
    summary.rename(columns={
        "index": "Column",
        "count": "Count",
        "mean": "Mean",
        "std": "Std Dev",
        "min": "Min",
        "25%": "25th %ile",
        "50%": "Median",
        "75%": "75th %ile",
        "max": "Max"
    }, inplace=True)

    # Round values and format numbers with commas
    for col in summary.columns[1:]:
        summary[col] = summary[col].apply(lambda x: f"{x:,.2f}" if pd.notna(x) else "-")

    return summary.to_html(index=False, classes="summary-table")


# --------------------------
# MAIN DASHBOARD FUNCTION
# --------------------------
def generate_dashboard():
    print("🚀 Loading data...")
    df = load_data_from_path(DATA_FILE_PATH)

    print("🧹 Cleaning data...")
    df = remove_duplicates(df)
    df = handle_missing(df, method='drop')

    print("📊 Running analysis...")
    summary_html = generate_summary(df)
    dashboard_name = os.path.splitext(os.path.basename(DATA_FILE_PATH))[0].replace("_", " ").title()

    numeric_cols, categorical_cols, time_col, stacked_cols, pie_col, val_col, hist_col = pick_columns(df)
    color_theme = px.colors.qualitative.Plotly
    kpis_html = generate_kpis(df, numeric_cols)
    chart_sections = []

    # === Section 1: Sales Trends ===
    section1 = "<h2 class='section-title'>📈 Sales & Time Trends</h2><div class='chart-container'>"
    if time_col and numeric_cols:
        for y_col in numeric_cols[:2]:
            fig_line = px.line(df, x=time_col, y=y_col, markers=True,
                               title=f"{y_col} over {time_col}",
                               color_discrete_sequence=color_theme)
            fig_line.update_traces(line=dict(width=3))
            section1 += f"<div class='chart-box'>{pio.to_html(fig_line, full_html=False, include_plotlyjs='cdn')}</div>"
    section1 += "</div>"
    chart_sections.append(section1)

    # === Section 2: Category / Region Analysis ===
    section2 = "<h2 class='section-title'>🌍 Category & Regional Analysis</h2><div class='chart-container'>"
    if stacked_cols:
        x_col, y_col, color_col = stacked_cols
        fig_stacked = px.bar(df, x=x_col, y=y_col, color=color_col,
                             title="Stacked Column Chart",
                             barmode='stack', text_auto=True,
                             color_discrete_sequence=px.colors.qualitative.Pastel)
        section2 += f"<div class='chart-box'>{pio.to_html(fig_stacked, full_html=False, include_plotlyjs=False)}</div>"

    if pie_col:
        fig_pie = px.pie(df, names=pie_col, values=val_col,
                         title=f"Distribution by {pie_col}", hole=0.35,
                         color_discrete_sequence=px.colors.qualitative.Set3)
        section2 += f"<div class='chart-box'>{pio.to_html(fig_pie, full_html=False, include_plotlyjs=False)}</div>"
    section2 += "</div>"
    chart_sections.append(section2)

    # === Section 3: Performance Metrics ===
    section3 = "<h2 class='section-title'>📊 Performance Metrics</h2><div class='chart-container'>"
    if hist_col:
        fig_hist = px.histogram(df, x=hist_col, nbins=20,
                                title=f"Distribution of {hist_col}",
                                color_discrete_sequence=["#FF6B6B"], text_auto=True)
        section3 += f"<div class='chart-box'>{pio.to_html(fig_hist, full_html=False, include_plotlyjs=False)}</div>"

    if numeric_cols:
        corr = correlation(df[numeric_cols])
        if not corr.empty:
            fig_corr = px.imshow(corr, text_auto=True, color_continuous_scale='Viridis',
                                 title="Correlation Heatmap")
            section3 += f"<div class='chart-box'>{pio.to_html(fig_corr, full_html=False, include_plotlyjs=False)}</div>"
    section3 += "</div>"
    chart_sections.append(section3)

    charts_html = "".join(chart_sections)

    # --------------------------
    # HTML Layout
    # --------------------------
    html = f"""
    <html>
    <head>
        <title>{dashboard_name} | Data Insights Dashboard</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
            body {{
                font-family: 'Poppins', sans-serif;
                background: radial-gradient(circle at top left, #0F2027, #203A43, #2C5364);
                color: #F5F5F5;
                margin: 0;
            }}
            header {{
                background: linear-gradient(90deg, #141E30, #243B55);
                color: #00E5FF;
                text-align: center;
                padding: 40px 0 30px;
                box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
            }}
            h1 {{
                font-size: 2.4em;
                margin: 0;
            }}
            .main-content {{
                padding: 40px 60px;
            }}
            .kpi-container {{
                display: flex;
                justify-content: center;
                gap: 15px;
                margin: 20px auto 40px;
                flex-wrap: nowrap;
                max-width: 95%;
            }}
            .kpi {{
                flex: 1;
                background: #1E293B;
                border: 2px solid;
                border-radius: 12px;
                text-align: center;
                padding: 12px 5px;
                color: #FFF;
                box-shadow: 0 4px 12px rgba(0,0,0,0.3);
                transition: all 0.3s ease;
                min-width: 160px;
            }}
            .kpi h3 {{
                font-size: 1em;
                margin-bottom: 6px;
                color: #FFD93D;
            }}
            .section-title {{
                text-align: left;
                color: #FFD93D;
                font-size: 1.6em;
                margin: 30px 10px 15px;
                border-left: 6px solid #00E5FF;
                padding-left: 12px;
            }}
            .chart-container {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(550px, 1fr));
                gap: 35px;
                margin-bottom: 50px;
            }}
            .chart-box {{
                background: #1E293B;
                border-radius: 18px;
                border: 2px solid rgba(0, 229, 255, 0.6);
                box-shadow: 0 0 15px rgba(0, 229, 255, 0.2);
                padding: 20px;
            }}
            .summary-section {{
                background: #1E293B;
                padding: 25px;
                border-radius: 15px;
                border: 2px solid #00E5FF;
                box-shadow: 0 0 20px rgba(0, 229, 255, 0.2);
                margin-top: 50px;
            }}
            .summary-section h2 {{
                text-align: center;
                color: #FFD93D;
                margin-bottom: 15px;
                font-size: 1.5em;
            }}
            .summary-table {{
                width: 100%;
                border-collapse: collapse;
                color: #E5E5E5;
                text-align: center;
                font-size: 0.95em;
            }}
            .summary-table th {{
                background: #00E5FF33;
                color: #FFD93D;
                padding: 10px;
                border-bottom: 2px solid #00E5FF;
            }}
            .summary-table td {{
                padding: 8px;
                border: 1px solid rgba(255,255,255,0.1);
            }}
            .summary-table tr:nth-child(even) {{ background-color: #243B55; }}
            footer {{
                background: linear-gradient(90deg, #141E30, #243B55);
                color: #00E5FF;
                text-align: center;
                padding: 20px;
                font-weight: 500;
                margin-top: 50px;
            }}
        </style>
    </head>
    <body>
        <header>
            <h1>📊 {dashboard_name} Dashboard</h1>
            <p style="color:#FFD93D;">Automated Data Insights Dashboard</p>
        </header>

        <div class="main-content">
            {kpis_html}
            {charts_html}
            <div class="summary-section">
                <h2>📘 Summary Statistics</h2>
                <p style="text-align:center; color:#A0AEC0; margin-bottom:15px;">Overview of numerical data distribution</p>
                {summary_html}
            </div>
        </div>

        <footer>
            ⚡ Auto-Generated Interactive Dashboard | Powered by Plotly & Python
        </footer>
    </body>
    </html>
    """

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    abs_path = os.path.abspath(OUTPUT_FILE)
    print(f"✅ Dashboard saved to: {abs_path}")
    webbrowser.open(f"file://{abs_path}", new=2)


if __name__ == "__main__":
    generate_dashboard()
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
