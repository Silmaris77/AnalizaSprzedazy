import pandas as pd
import plotly.graph_objects as go
from dash import html, dcc

def render_tab(df):
    layout = html.Div([
        html.H1('Kanały sprzedaży', style={'text-align': 'center'}),
        html.Div([
            dcc.DatePickerRange(id='sales-range',
                                start_date=df['tran_date'].min(),
                                end_date=df['tran_date'].max(),
                                display_format='YYYY-MM-DD')
        ], style={'width': '100%', 'text-align': 'center'}),
        html.Div([
            html.Div([dcc.Graph(id='sales-weekdays')], style={'width': '50%'}),
            html.Div([dcc.Graph(id='customer-analysis')], style={'width': '50%'})
        ], style={'display': 'flex'})
    ])
    return layout

# Funkcja renderująca wykres sprzedaży w zależności od dnia tygodnia
def sales_weekdays_fig(df, start_date, end_date):
    if not start_date or not end_date:
        return go.Figure()

    truncated = df[
        (df['tran_date'] >= start_date) &
        (df['tran_date'] <= end_date)
    ]
    truncated['weekday'] = truncated['tran_date'].dt.day_name()

    grouped = truncated.groupby(['weekday', 'Store_type'])['total_amt'].sum().unstack().fillna(0)

    traces = []
    for col in grouped.columns:
        traces.append(go.Bar(
            x=grouped.index,
            y=grouped[col],
            name=col,
            hoverinfo='text',
            hovertext=[f'{y/1e3:.2f}k' for y in grouped[col].values]
        ))

    return go.Figure(data=traces, layout=go.Layout(
        title='Sprzedaż w zależności od dnia tygodnia',
        barmode='stack',
        legend=dict(x=0, y=-0.7),
        # xaxis=dict(title='Dzień tygodnia'),
        yaxis=dict(title='Sprzedaż')
    ))

# Funkcja renderująca analizę klientów w zależności od kanału sprzedaży
def customer_analysis_fig(df, start_date, end_date):
    if not start_date or not end_date:
        return go.Figure()

    truncated = df[
        (df['tran_date'] >= start_date) &
        (df['tran_date'] <= end_date)
    ]
    
    grouped = truncated.groupby('Store_type')['cust_id'].nunique()

    return go.Figure(data=[go.Bar(
        x=grouped.index,
        y=grouped.values,
        text=grouped.values,
        hoverinfo='text',
    )], layout=go.Layout(
        title='Liczba unikalnych klientów w kanale sprzedaży',
        
        xaxis=dict(title='Kanał sprzedaży'),
        yaxis=dict(title='Liczba klientów'),  
    ))
