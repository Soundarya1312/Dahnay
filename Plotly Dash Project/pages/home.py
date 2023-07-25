import dash
from dash import html, dcc
import dash_mantine_components as dmc
import plotly.graph_objs as go
import pyodbc
import pandas as pd

dash.register_page(__name__, path='/')

# Establish a connection to the SQL Server
conn = pyodbc.connect(
    'Driver={ODBC Driver 17 for SQL Server};'
    'Server=20.207.202.225;'
    'Database=Analysis Dashboard;'
    'UID=Hanumant;'
    'PWD=GIGtel@20152;'
)

# SQL queries and data retrieval

# SQL query to retrieve data for JobSalesRep-wise TEU count (top 5)
sales_rep_query = """
    SELECT TOP 5 JobSalesRep, COUNT(TEU) AS TEUCount
    FROM ShipmentProfile
    GROUP BY JobSalesRep
    ORDER BY TEUCount DESC
"""

# Execute the query and fetch the data into a DataFrame
sales_rep_df = pd.read_sql(sales_rep_query, conn)

# SQL query to retrieve data for LocalClientName-wise TEU count (top 5)
client_name_query = """
    SELECT TOP 5 LocalClientName, COUNT(TEU) AS TEUCount
    FROM ShipmentProfile
    GROUP BY LocalClientName
    ORDER BY TEUCount DESC
"""

# Execute the query and fetch the data into a DataFrame
client_name_df = pd.read_sql(client_name_query, conn)

# SQL query to retrieve data for JobBranch-wise RecognizedRevenue (top 10)
revenue_query = """
    SELECT TOP 10 JobBranch, SUM(CAST(REPLACE(RecognizedRevenue, ',', '') AS decimal(18, 2))) AS TotalRevenue
    FROM ShipmentProfile
    GROUP BY JobBranch
    ORDER BY TotalRevenue DESC
"""

# Execute the query and fetch the data into a DataFrame
revenue_df = pd.read_sql(revenue_query, conn)

# SQL query to retrieve data for CarrierName-wise TEU count (top 5)
carrier_name_query = """
    SELECT TOP 5 CarrierName, COUNT(TEU) AS TEUCount
    FROM ShipmentProfile
    GROUP BY CarrierName
    ORDER BY TEUCount DESC
"""

# Execute the query and fetch the data into a DataFrame
carrier_name_df = pd.read_sql(carrier_name_query, conn)

# Close the database connection
conn.close()

total_teu_sales_rep = sales_rep_df['TEUCount'].sum()
total_teu_client_name = client_name_df['TEUCount'].sum()
total_teu_job_branch = revenue_df['TotalRevenue'].sum()
total_teu_carrier_name = carrier_name_df['TEUCount'].sum()


sample_countries = [
    {'name': 'United States', 'lat': 37.0902, 'lon': -95.7129},
    {'name': 'China', 'lat': 35.8617, 'lon': 104.1954},
    {'name': 'Germany', 'lat': 51.1657, 'lon': 10.4515},
    {'name': 'India', 'lat': 20.5937, 'lon': 78.9629},
    {'name': 'United Kingdom', 'lat': 55.3781, 'lon': -3.4360},
]

def create_point_map(countries):
    return {
        'data': [
            go.Scattergeo(
                lon=[country['lon'] for country in countries],
                lat=[country['lat'] for country in countries],
                text=[country['name'] for country in countries],
                mode='markers',
                marker=dict(
                    size=10,
                    color='rgba(255, 0, 0, 0.8)',  # Change the color to red with transparency (alpha=0.8)
                    line=dict(width=1, color='rgba(255, 0, 0, 1)'),  # Set the marker edge color to red
                    symbol='circle',
                ),
                hoverinfo='text'
            )
        ],
        'layout': go.Layout(
            geo=dict(
                scope='world',
                projection=dict(type='natural earth'),  # Change the projection type to natural earth
                showland=True,
                landcolor='rgb(243, 243, 243)',  # Set land color to light gray
                showcountries=True,
                countrycolor='rgb(204, 204, 204)',  # Set country border color to gray
                showocean=True,
                oceancolor='rgb(158, 202, 225)',  # Set ocean color to a light blue
                showlakes=True,
                lakecolor='rgb(158, 202, 225)',  # Set lake color to the same light blue as the ocean
                showrivers=True,
                rivercolor='rgb(158, 202, 225)',  # Set river color to the same light blue as the ocean
            ),
            margin=dict(l=0, r=0, t=0, b=0),  # Adjust the margin for better display
            height=400,  # Set the map height to 400 pixels
            plot_bgcolor='white',
            paper_bgcolor='white',
            font={'color': 'black'},
        )
    }

# Custom colors for pie charts
pie_chart_colors = ['#488A99', '#20283E', '#DADADA', '#DBAE58', '#AC3E31']

job_branch_pie_chart_colors = ['#7E909A', '#1C4E80', '#EA6A47', '#1F3F49', '#6AB187']


layout = html.Div(
    style={'backgroundColor': 'white', 'padding': '20px'},
    children=[
        # First row: Gradient Color Cards with Icons
        dmc.Group(
            position="right",
            align="center",
            spacing="xs",
            grow=1,
            style={
                'display': 'flex', 
                'justify-content': 'space-around', 
                'flex-wrap': 'wrap', 
                'padding': '10px 15px', 
                'background-color': '#ccc', 
                'border-radius': '10px',
                'box-shadow': '1px 2px #ccc',
            },
            children=[
                dmc.Paper(
                    radius="md",
                    withBorder=True,
                    shadow='sm',
                    p='sm',
                    style={
                        'width': '20%', 
                        'height': '125px',
                        'margin': '5px', 
                        'background-image': 
                        'linear-gradient(to bottom right, #6495ED, #D8BFD8)', 
                        'padding': '7px',
                        'border-radius': '15px',
                    },
                    children=[
                        html.Div(
                            style={
                                'display': 'flex',
                            },
                            children=[
                                html.I(className='fa fa-truck fa-2x', style={'color': 'white'}), 
                                html.H6('Total TEUs JobSalesRep', style={
                                    'color': 'white',
                                    'display': 'flex',
                                    'align-items': 'center',
                                    'margin-left': '10px',
                                }),
                            ],
                        ),
                        html.H4(total_teu_sales_rep, style={
                            'display': 'flex',
                            'align-items': 'center',
                            'justify-content': 'center',
                            'height': '50px',
                        })
                    ]
                ),
                dmc.Paper(
                    radius="md",
                    withBorder=True,
                    shadow='sm',
                    p='sm',
                    style={
                        'width': '20%', 
                        'height': '125px',
                        'margin': '5px', 
                        'background-image': 'linear-gradient(to bottom right, #008080, #9ACD32)', 
                        'padding': '10px', 
                        'border-radius': '15px',
                    },
                    children=[
                        html.Div(
                            style={
                                'display': 'flex',
                            },
                            children=[
                                html.I(className='fa fa-users fa-2x', style={'color': 'white'}),
                                html.H6('Total TEUs ClientName', style={
                                    'color': 'white',
                                    'display': 'flex',
                                    'align-items': 'center',
                                    'margin-left': '10px',
                                }),
                            ],
                        ),
                        html.H4(total_teu_client_name, style={
                            'display': 'flex',
                            'align-items': 'center',
                            'justify-content': 'center',
                            'height': '50px',
                        })
                    ]
                ),
                dmc.Paper(
                    radius="md",
                    withBorder=True,
                    shadow='sm',
                    p='sm',
                    style={'width': '20%', 'height': '125px',  'margin': '5px', 'background-image': 'linear-gradient(to bottom right, #FF5733, #FFD700)', 'padding': '10px', 'border-radius': '15px'},
                    children=[
                        html.Div(
                            style={
                                'display': 'flex',
                            },
                            children=[
                                html.I(className='fa fa-briefcase fa-2x', style={'color': 'white'}),  # Add the briefcase icon
                                html.H6('Total TEUs JobBranch', style={
                                    'color': 'white',
                                    'display': 'flex',
                                    'align-items': 'center',
                                    'margin-left': '10px',
                                }),
                            ],
                        ),
                        html.H4(total_teu_job_branch, style={
                            'display': 'flex',
                            'align-items': 'center',
                            'justify-content': 'center',
                            'height': '50px',
                        })
                    ]
                ),
                dmc.Paper(
                    radius="md",
                    withBorder=True,
                    shadow='sm',
                    p='sm',
                    style={'width': '20%', 'height': '125px', 'margin': '5px', 'background-image': 'linear-gradient(to bottom right, #D8BFD8, #FFFF00)', 'padding': '10px', 'border-radius': '15px'},
                    children=[
                        html.Div(
                            style={
                                'display': 'flex',
                            },
                            children=[
                                html.I(className='fa fa-ship fa-2x', style={'color': 'white'}),  # Add the ship icon
                                html.H6('Total TEUs CarrierName', style={
                                    'color': 'white',
                                    'display': 'flex',
                                    'align-items': 'center',
                                    'margin-left': '10px',
                                }),
                            ],
                        ),
                        html.H4(total_teu_carrier_name, style={
                            'display': 'flex',
                            'align-items': 'center',
                            'justify-content': 'center',
                            'height': '50px',
                        })
                    ]
                ),
            ]
        ),

        # Second row: Pie Charts
        html.Div(
            style={'display': 'flex', 'justify-content': 'space-between', 'flex-wrap': 'wrap'},
            children=[
                dmc.Paper(
                    radius="md",
                    withBorder=True,
                    shadow='sm',
                    p='sm',
                    style={'width': '48%', 'margin': '5px', 'border-radius': '15px', 'border': '5px solid #cc4b4b'},
                    children=[
                        dcc.Graph(
                            id='revenue',
                            figure={
                                'data': [
                                    go.Pie(
                                        labels=revenue_df['JobBranch'],
                                        values=revenue_df['TotalRevenue'],
                                        hole=0.5,
                                        marker=dict(colors=job_branch_pie_chart_colors)
                                    )
                                ],
                                'layout': go.Layout(
                                    title='JobBranch-wise Recognized Revenue',
                                    plot_bgcolor='white',
                                    paper_bgcolor='white',
                                    font={'color': 'black'}
                                )
                            }
                        ),
                    ]
                ),
                dmc.Paper(
                    radius="md",
                    withBorder=True,
                    shadow='sm',
                    p='sm',
                    style={'width': '48%', 'margin': '5px', 'border-radius': '15px', 'border': '5px solid #cc4b4b'},
                    children=[
                        dcc.Graph(
                            id='carrier-name',
                            figure={
                                'data': [
                                    go.Pie(
                                        labels=carrier_name_df['CarrierName'],
                                        values=carrier_name_df['TEUCount'],
                                        marker=dict(colors=pie_chart_colors)
                                    )
                                ],
                                'layout': go.Layout(
                                    title='CarrierName-wise TEU Count',
                                    font={'color': 'black'},
                                    showlegend=False,
                                )
                            }
                        )
                    ]
                ),
            ]
        ),
        # Third row: Bar Charts
        html.Div(
            style={'display': 'flex', 'justify-content': 'space-between', 'flex-wrap': 'wrap'},
            children=[
                dmc.Paper(
                    radius="md",
                    withBorder=True,
                    shadow='sm',
                    p='sm',
                    style={'width': '48%', 'margin': '5px', 'border-radius': '15px', 'border': '5px solid #cc4b4b'},
                    children=[
                        dcc.Graph(
                            id='sales-rep',
                            style={'height': '320px'},
                            figure={
                                'data': [
                                    go.Bar(
                                        x=sales_rep_df['TEUCount'],
                                        y=sales_rep_df['JobSalesRep'],
                                        marker=dict(color='#1f77b4'),
                                        orientation='h'
                                    )
                                ],
                                'layout': go.Layout(
                                    title='JobSalesRep-wise TEU Count',
                                    xaxis=dict(title='TEU Count'),
                                    yaxis=dict(title='JobSalesRep'),
                                    plot_bgcolor='white',
                                    paper_bgcolor='white',
                                    font={'color': 'black'}
                                )
                            }
                        ),
                    ]
                ),
                dmc.Paper(
                    radius="md",
                    withBorder=True,
                    shadow='sm',
                    p='sm',
                    style={'width': '48%', 'margin': '5px', 'border-radius': '15px', 'border': '5px solid #cc4b4b'},
                    children=[
                        dcc.Graph(
                            id='client-name',
                            style={'height': '320px'},
                            figure={
                                'data': [
                                    go.Bar(
                                        x=client_name_df['LocalClientName'],
                                        y=client_name_df['TEUCount'],
                                        marker=dict(color='#ff7f0e')
                                    )
                                ],
                                'layout': go.Layout(
                                    title='LocalClientName-wise TEU Count',
                                    xaxis=dict(title='LocalClientName'),
                                    yaxis=dict(title='TEU Count'),
                                    plot_bgcolor='white',
                                    paper_bgcolor='white',
                                    font={'color': 'black'}
                                )
                            }
                        ),
                    ]
                ),
            ]
        ),
        # Fourth row: Sample Map
        dmc.Paper(
            radius="md",
            withBorder=True,
            shadow='sm',
            p='sm',
            style={
                'border': '10px solid #cc4b4b',
                'border-radius': '10px'
            },
            children=[
                html.H3('Sample Map', style={'color': '#F08080', 'text-align': 'center'}),
                dcc.Graph(
                    id='point-map',
                    figure=create_point_map(sample_countries)
                )
            ]
        )
    ]
)