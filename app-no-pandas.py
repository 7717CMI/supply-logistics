import dash
from dash import dcc, html, Input, Output, dash_table
import plotly.graph_objects as go
import json
from collections import Counter
import dash_bootstrap_components as dbc

# Load data from JSON file
with open('nextload.json', 'r') as f:
    data = json.load(f)

# Get first 50 entries
loads = data['load_postings'][:50]

# Convert timestamps to readable format
for load in loads:
    if load['postedTimestamp']:
        load['postedDate'] = load['postedTimestamp'] / 1000  # Convert to seconds
    if load['pickupTimestamp']:
        load['pickupDate'] = load['pickupTimestamp'] / 1000

# Create the Dash app with modern Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])

# Custom CSS for modern light theme
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 50%, #cbd5e1 100%);
                color: #1e293b;
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                margin: 0;
                padding: 0;
            }
            
            .main-container {
                background: rgba(255, 255, 255, 0.9);
                backdrop-filter: blur(20px);
                border-radius: 20px;
                margin: 20px;
                padding: 30px;
                border: 1px solid rgba(255, 255, 255, 0.8);
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            }
            
            .metric-card {
                background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 250, 252, 0.9) 100%);
                border-radius: 16px;
                padding: 25px;
                margin: 10px;
                border: 1px solid rgba(226, 232, 240, 0.8);
                backdrop-filter: blur(10px);
                transition: all 0.3s ease;
                position: relative;
                overflow: hidden;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            }
            
            .metric-card::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 3px;
                background: linear-gradient(90deg, #3b82f6, #1d4ed8, #1e40af);
            }
            
            .metric-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 15px 30px rgba(59, 130, 246, 0.15);
            }
            
            .metric-value {
                font-size: 2.5rem;
                font-weight: 700;
                margin-bottom: 8px;
                background: linear-gradient(135deg, #3b82f6, #1d4ed8);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
            
            .metric-label {
                font-size: 0.9rem;
                color: #64748b;
                text-transform: uppercase;
                letter-spacing: 1px;
                font-weight: 500;
            }
            
            .chart-container {
                background: rgba(255, 255, 255, 0.9);
                border-radius: 16px;
                padding: 25px;
                margin: 15px 0;
                border: 1px solid rgba(226, 232, 240, 0.8);
                backdrop-filter: blur(10px);
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            }
            
            .title {
                font-size: 2.5rem;
                font-weight: 800;
                text-align: center;
                margin-bottom: 40px;
                background: linear-gradient(135deg, #3b82f6, #1d4ed8, #1e40af);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                text-shadow: 0 0 30px rgba(59, 130, 246, 0.2);
            }
            
            .subtitle {
                font-size: 1.1rem;
                text-align: center;
                color: #64748b;
                margin-bottom: 30px;
                font-weight: 300;
            }
            
            .data-table {
                background: rgba(255, 255, 255, 0.9);
                border-radius: 16px;
                padding: 25px;
                margin: 20px 0;
                border: 1px solid rgba(226, 232, 240, 0.8);
                backdrop-filter: blur(10px);
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            }
            
            .table-title {
                font-size: 1.5rem;
                font-weight: 600;
                margin-bottom: 20px;
                color: #1e293b;
                text-align: center;
            }
            
            @keyframes fadeInUp {
                from {
                    opacity: 0;
                    transform: translateY(30px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            .fade-in {
                animation: fadeInUp 0.6s ease-out;
            }
            
            .pulse {
                animation: pulse 2s infinite;
            }
            
            @keyframes pulse {
                0% { transform: scale(1); }
                50% { transform: scale(1.05); }
                100% { transform: scale(1); }
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Define the layout
app.layout = html.Div([
    html.Div([
        html.H1("NextLoad Analytics Dashboard", className="title fade-in"),
        html.P("Real-time freight logistics insights powered by advanced analytics", className="subtitle fade-in"),
        
        # Summary cards with modern design
        html.Div([
            html.Div([
                html.Div(f"{len(loads)}", className="metric-value pulse"),
                html.Div("Total Loads", className="metric-label")
            ], className="metric-card fade-in"),
            
            html.Div([
                html.Div(f"${sum(load['rateCents'] for load in loads if load['rateCents']) / len([l for l in loads if l['rateCents']]) / 100:.0f}", className="metric-value pulse"),
                html.Div("Average Rate", className="metric-label")
            ], className="metric-card fade-in"),
            
            html.Div([
                html.Div(f"{sum(load['distanceMiles'] for load in loads) / len(loads):.0f}", className="metric-value pulse"),
                html.Div("Avg Distance (mi)", className="metric-label")
            ], className="metric-card fade-in"),
            
            html.Div([
                html.Div(f"{len(set(load['equipmentType'] for load in loads if load['equipmentType']))}", className="metric-value pulse"),
                html.Div("Equipment Types", className="metric-label")
            ], className="metric-card fade-in")
        ], style={'display': 'flex', 'justifyContent': 'space-around', 'flexWrap': 'wrap', 'marginBottom': '40px'}),
        
        # Modern charts row
        html.Div([
            html.Div([
                dcc.Graph(id='equipment-pie', config={'displayModeBar': False})
            ], className="chart-container fade-in", style={'width': '48%', 'display': 'inline-block'}),
            
            html.Div([
                dcc.Graph(id='rate-histogram', config={'displayModeBar': False})
            ], className="chart-container fade-in", style={'width': '48%', 'display': 'inline-block', 'marginLeft': '4%'})
        ], style={'marginBottom': '30px'}),
        
        # Advanced visualizations
        html.Div([
            html.Div([
                dcc.Graph(id='origin-states', config={'displayModeBar': False})
            ], className="chart-container fade-in", style={'width': '48%', 'display': 'inline-block'}),
            
            html.Div([
                dcc.Graph(id='distance-rate-scatter', config={'displayModeBar': False})
            ], className="chart-container fade-in", style={'width': '48%', 'display': 'inline-block', 'marginLeft': '4%'})
        ], style={'marginBottom': '30px'}),
        
        # Modern data table
        html.Div([
            html.H3("Load Details", className="table-title"),
            dash_table.DataTable(
                id='loads-table',
                columns=[
                    {'name': 'Reference', 'id': 'referenceNumber', 'type': 'text'},
                    {'name': 'Origin', 'id': 'originCity', 'type': 'text'},
                    {'name': 'Destination', 'id': 'destinationCity', 'type': 'text'},
                    {'name': 'Distance (mi)', 'id': 'distanceMiles', 'type': 'numeric', 'format': {'specifier': '.0f'}},
                    {'name': 'Rate ($)', 'id': 'rateCents', 'type': 'numeric', 'format': {'specifier': '.2f'}},
                    {'name': 'Equipment', 'id': 'equipmentType', 'type': 'text'},
                    {'name': 'Company', 'id': 'companyName', 'type': 'text'}
                ],
                data=loads,
                page_size=10,
                style_cell={
                    'textAlign': 'left',
                    'padding': '15px',
                    'fontFamily': 'Inter, sans-serif',
                    'backgroundColor': 'rgba(255, 255, 255, 0.8)',
                    'color': '#1e293b',
                    'border': '1px solid rgba(0, 0, 0, 0.1)'
                },
                style_header={
                    'backgroundColor': 'rgba(59, 130, 246, 0.1)',
                    'color': '#3b82f6',
                    'fontWeight': '600',
                    'textTransform': 'uppercase',
                    'letterSpacing': '1px',
                    'border': '1px solid rgba(59, 130, 246, 0.2)'
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgba(248, 250, 252, 0.8)'
                    },
                    {
                        'if': {'row_index': 'even'},
                        'backgroundColor': 'rgba(255, 255, 255, 0.9)'
                    }
                ],
                style_table={'overflowX': 'auto', 'borderRadius': '12px', 'overflow': 'hidden'}
            )
        ], className="data-table fade-in")
    ], className="main-container")
])

# Callbacks for interactive charts with modern styling
@app.callback(
    Output('equipment-pie', 'figure'),
    Input('equipment-pie', 'id')
)
def update_equipment_pie(_):
    equipment_counts = Counter(load['equipmentType'] for load in loads if load['equipmentType'])
    
    fig = go.Figure(data=[go.Pie(
        labels=list(equipment_counts.keys()),
        values=list(equipment_counts.values()),
        hole=0.4,
        marker_colors=['#3b82f6', '#1d4ed8', '#1e40af', '#ef4444', '#10b981', '#f59e0b'],
        textinfo='label+percent',
        textfont_size=14,
        textfont_color='#1e293b',
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        title={
            'text': "Equipment Distribution",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': '#3b82f6', 'family': 'Inter'}
        },
        font={'color': '#1e293b', 'family': 'Inter'},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.1,
            font=dict(color='#1e293b', size=12)
        )
    )
    
    return fig

@app.callback(
    Output('rate-histogram', 'figure'),
    Input('rate-histogram', 'id')
)
def update_rate_histogram(_):
    rates_dollars = [load['rateCents'] / 100 for load in loads if load['rateCents'] and load['rateCents'] > 0]
    
    fig = go.Figure(data=[go.Histogram(
        x=rates_dollars,
        nbinsx=15,
        marker_color='#3b82f6',
        marker_line_color='#1d4ed8',
        marker_line_width=1,
        opacity=0.8
    )])
    
    fig.update_layout(
        title={
            'text': "Rate Distribution",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': '#3b82f6', 'family': 'Inter'}
        },
        xaxis_title="Rate ($)",
        yaxis_title="Frequency",
        font={'color': '#1e293b', 'family': 'Inter'},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(gridcolor='rgba(0,0,0,0.1)', color='#1e293b'),
        yaxis=dict(gridcolor='rgba(0,0,0,0.1)', color='#1e293b')
    )
    
    return fig

@app.callback(
    Output('origin-states', 'figure'),
    Input('origin-states', 'id')
)
def update_origin_states(_):
    origin_counts = Counter(load['originState'] for load in loads if load['originState'])
    
    fig = go.Figure(data=[go.Bar(
        x=list(origin_counts.keys()),
        y=list(origin_counts.values()),
        marker_color='#10b981',
        marker_line_color='#059669',
        marker_line_width=1,
        opacity=0.8
    )])
    
    fig.update_layout(
        title={
            'text': "Load Origins by State",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': '#3b82f6', 'family': 'Inter'}
        },
        xaxis_title="State",
        yaxis_title="Number of Loads",
        font={'color': '#1e293b', 'family': 'Inter'},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(gridcolor='rgba(0,0,0,0.1)', color='#1e293b'),
        yaxis=dict(gridcolor='rgba(0,0,0,0.1)', color='#1e293b')
    )
    
    return fig

@app.callback(
    Output('distance-rate-scatter', 'figure'),
    Input('distance-rate-scatter', 'id')
)
def update_distance_rate_scatter(_):
    scatter_data = []
    for load in loads:
        if load['rateCents'] and load['rateCents'] > 0:
            scatter_data.append({
                'distance': load['distanceMiles'],
                'rate': load['rateCents'] / 100,
                'equipment': load['equipmentType'] or 'Unknown',
                'origin': load['originCity'],
                'destination': load['destinationCity'],
                'company': load['companyName']
            })
    
    equipment_groups = {}
    for item in scatter_data:
        equipment = item['equipment']
        if equipment not in equipment_groups:
            equipment_groups[equipment] = {'x': [], 'y': [], 'text': []}
        equipment_groups[equipment]['x'].append(item['distance'])
        equipment_groups[equipment]['y'].append(item['rate'])
        equipment_groups[equipment]['text'].append(f"{item['origin']} → {item['destination']}<br>{item['company']}")
    
    fig = go.Figure()
    
    colors = ['#3b82f6', '#ef4444', '#10b981', '#f59e0b', '#8b5cf6', '#06b6d4']
    
    for i, (equipment, data) in enumerate(equipment_groups.items()):
        fig.add_trace(go.Scatter(
            x=data['x'],
            y=data['y'],
            mode='markers',
            name=equipment,
            text=data['text'],
            hovertemplate='<b>%{text}</b><br>Distance: %{x} miles<br>Rate: $%{y}<extra></extra>',
            marker=dict(
                color=colors[i % len(colors)],
                size=12,
                line=dict(width=1, color='white'),
                opacity=0.8
            )
        ))
    
    fig.update_layout(
        title={
            'text': "Distance vs Rate Analysis",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': '#3b82f6', 'family': 'Inter'}
        },
        xaxis_title="Distance (miles)",
        yaxis_title="Rate ($)",
        font={'color': '#1e293b', 'family': 'Inter'},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(gridcolor='rgba(0,0,0,0.1)', color='#1e293b'),
        yaxis=dict(gridcolor='rgba(0,0,0,0.1)', color='#1e293b'),
        hovermode='closest',
        legend=dict(
            font=dict(color='#1e293b', size=12),
            bgcolor='rgba(255,255,255,0.9)',
            bordercolor='rgba(0,0,0,0.1)',
            borderwidth=1
        )
    )
    
    return fig

if __name__ == '__main__':
    print("Starting NextLoad Modern Dashboard...")
    print(f"Loaded {len(loads)} load entries")
    print("Dashboard will be available at: http://localhost:8050")
    app.run(debug=True, host='0.0.0.0', port=8050)
