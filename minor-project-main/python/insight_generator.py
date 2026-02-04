# insight_generator.py
"""
Generate textual insights about the dataset.
- Provides a rule-based summary always
- If OPENAI_API_KEY is available, will call OpenAI to produce richer insights
"""

from typing import Dict, Any, List
import os
import pandas as pd
import numpy as np

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", None)


def rule_based_insights(df: pd.DataFrame, column_types: Dict[str, str], top_n: int = 3) -> List[str]:
    """Simple deterministic insights (safe fallback)."""
    insights = []
    # dataset size
    insights.append(f"The dataset has {df.shape[0]} rows and {df.shape[1]} columns.")

    # missing values top columns
    missing = df.isna().sum().sort_values(ascending=False)
    if missing.iloc[0] > 0:
        top_miss = missing[missing > 0].head(top_n)
        for col, cnt in top_miss.items():
            insights.append(f"Column '{col}' has {int(cnt)} missing values ({cnt/df.shape[0]:.1%}).")

    # top numeric trends: highest mean
    numeric_cols = [c for c, t in column_types.items() if t == "numeric"]
    if numeric_cols:
        means = df[numeric_cols].mean().sort_values(ascending=False)
        top = means.head(top_n)
        for col, val in top.items():
            insights.append(f"Numeric column '{col}' has mean ≈ {val:.3g}.")

    # categorical top levels
    cat_cols = [c for c, t in column_types.items() if t == "categorical"]
    if cat_cols:
        for c in cat_cols[:top_n]:
            top_levels = df[c].value_counts().head(3).to_dict()
            insights.append(f"Top values for '{c}': {top_levels}.")

    return insights


def openai_insights_prompt(df_summary: Dict[str, Any]) -> str:
    """Craft a concise prompt for the LLM using the pre-computed summary."""
    # Keep prompt short to avoid sending entire dataframe
    parts = []
    ds = df_summary.get("dataset_info", {})
    parts.append(f"Dataset has {ds.get('n_rows')} rows and {ds.get('n_columns')} columns.")
    # add column summaries
    for col, info in list(df_summary.get("columns", {}).items())[:10]:  # limit to first 10 cols
        ci = df_summary["columns"][col]
        parts.append(
            f"Column '{col}': type={ci.get('inferred_type')}, missing={ci.get('n_missing')}, unique={ci.get('n_unique')}."
        )
    prompt = "You are a helpful data analyst. Given the dataset summary below, produce 3 concise, prioritized business insights (1-2 sentences each) and suggest 2 charts to visualize them.\n\n"
    prompt += "\n".join(parts)
    return prompt


def generate_insights(df: pd.DataFrame, df_summary: Dict[str, Any], max_insights: int = 5) -> Dict[str, Any]:
    """
    Return:
      {
        "rule_based": [...],
        "llm": "text or None",
        "chart_suggestions": [...]
      }
    """
    result = {}
    col_types = {col: info["inferred_type"] for col, info in df_summary["columns"].items()}
    result["rule_based"] = rule_based_insights(df, col_types, top_n=3)

    # If no API key, skip LLM and return
    if not OPENAI_API_KEY:
        result["llm"] = None
        result["chart_suggestions"] = []  # frontend can use visualizer recommendations
        return result

    # Otherwise call OpenAI (ChatCompletion)
    try:
        import openai

        openai.api_key = OPENAI_API_KEY
        prompt = openai_insights_prompt(df_summary)
        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini" if hasattr(openai, "ChatCompletion") else "gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400,
            temperature=0.2,
        )
        # Extract text (support API variations)
        if isinstance(resp, dict):
            llm_text = resp["choices"][0]["message"]["content"]
        else:
            # Some openai python versions return an object with .choices
            llm_text = resp.choices[0].message.content
        result["llm"] = llm_text
        # Try to extract chart suggestions from LLM text (simple heuristic)
        suggestions = []
        if "chart" in (llm_text or "").lower():
            # just send back the llm text for frontend to parse or show
            suggestions = [line.strip() for line in (llm_text.splitlines()[:5]) if line.strip()]
        result["chart_suggestions"] = suggestions
    except Exception as e:
        result["llm"] = None
        result["chart_suggestions"] = []
        result["llm_error"] = str(e)

    return result
