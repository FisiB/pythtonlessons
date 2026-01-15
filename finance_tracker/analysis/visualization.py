import pandas as pd
import matplotlib.pyplot as plt
from typing import Optional

def monthly_expenses_figure(df: pd.DataFrame, title: str = "Monthly Expenses") -> Optional[plt.Figure]:
    if df is None or df.empty:
        return None
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'])
    monthly = df[df['type'] == 'expense'].groupby(df['date'].dt.to_period('M'))['amount'].sum()
    fig, ax = plt.subplots()
    monthly.index = monthly.index.to_timestamp()
    monthly.plot(kind='bar', ax=ax, title=title)
    ax.set_ylabel('Amount')
    fig.tight_layout()
    return fig

def category_pie_figure(df: pd.DataFrame, title: str = "Expenses by Category") -> Optional[plt.Figure]:
    if df is None or df.empty:
        return None
    df = df.copy()
    category_sum = df[df['type'] == 'expense'].groupby('category')['amount'].sum()
    if category_sum.empty:
        return None
    fig, ax = plt.subplots()
    category_sum.plot(kind='pie', autopct='%1.1f%%', ax=ax, title=title)
    ax.set_ylabel('')
    fig.tight_layout()
    return fig
