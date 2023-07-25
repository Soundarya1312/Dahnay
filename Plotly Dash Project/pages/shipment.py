import dash

from dash import html, dcc, callback, Input, Output

import dash_mantine_components as dmc

import pyodbc

import pandas as pd

from datetime import datetime




dash.register_page(__name__)


layout = html.Div(

    style={'backgroundColor': 'white', 'padding': '20px'},

    children=[

        dmc.Group(

            position="center",

            align="center",

            spacing="xs",

            style={

                'margin-top': '40px'

            },

            children=[

                html.H2('Enter Shipment ID:', style={'color': '#20B2AA'}),

                dcc.Input(id='shipment-input', type='text'),

                html.Button('Submit', id='submit-button', n_clicks=0),

            ],

        ),

        html.H2(

            'Shipment Details:',

            style={

                'color': '#FFE4B5',

                'margin-top': '30px',

                'background-color': 'gray',

                'padding': '10px'

            }

        ),

        html.Div(

            id='shipment-details',

            style={

                'margin-top': '10px',

                'background-color': 'white',

                'padding': '10px'

            }

        ),

        html.H2(

            'Select ETD Month Range:',

            style={

                'color': '#20B2AA',

                'margin-top': '30px'

            }

        ),

        dcc.DatePickerRange(

            id='etd-range',

            start_date_placeholder_text='Start Date',

            end_date_placeholder_text='End Date',

            display_format='YYYY-MM',

            min_date_allowed=datetime(2000, 1, 1).date(),

            max_date_allowed=datetime.now().date(),

            initial_visible_month=datetime.now().date(),

        ),

        html.Button('Submit ETD Range', id='submit-etd-button', n_clicks=0),

        html.H2(

            'Shipment Details for the Selected ETD Range:',

            style={

                'color': '#FFE4B5',

                'margin-top': '30px',

                'background-color': 'gray',

                'padding': '10px'

            }

        ),

        html.Div(

            id='shipment-details-range',

            style={

                'margin-top': '10px',

                'background-color': 'white',

                'padding': '10px'

            }

        ),

    ]

)




# Callback function to handle button click and retrieve shipment details

@callback(

    Output('shipment-details', 'children'),

    Input('submit-button', 'n_clicks'),

    Input('shipment-input', 'value')

)

def retrieve_shipment_details(n_clicks, shipment_id):

    if n_clicks > 0:

        # Query the shipment details based on the given Shipment ID

        shipment_details_df = query_shipment_details(shipment_id)

       

        if not shipment_details_df.empty:

            return html.Div(

                style={

                    'overflow': 'auto'

                },

                children=[

                    create_shipment_table(shipment_details_df)

                ]

            )

        else:

            return html.Div('No shipment details found for the given Shipment ID.', style={'color': 'red'})

    return ''




# Callback function to handle button click and retrieve shipment details for ETD range

@callback(

    Output('shipment-details-range', 'children'),

    Input('submit-etd-button', 'n_clicks'),

    Input('etd-range', 'start_date'),

    Input('etd-range', 'end_date')

)

def retrieve_shipment_details_range(n_clicks, start_date, end_date):

    if n_clicks > 0:

        # Query the shipment details based on the ETD range

        shipment_details_df = query_shipment_details_range(start_date, end_date)

       

        if not shipment_details_df.empty:

            return html.Div(

                style={

                    'overflow': 'auto'

                },

                children=create_monthly_shipment_tables(shipment_details_df)

            )

        else:

            return html.Div('No shipment details found for the selected ETD range.', style={'color': 'red'})

    return ''




# Function to query shipment details based on the Shipment ID

def query_shipment_details(shipment_id):

    # Connect to the SQL Server

    conn = pyodbc.connect(

        'Driver={ODBC Driver 17 for SQL Server};'

        'Server=20.207.202.225;'

        'Database=Analysis Dashboard;'

        'UID=Hanumant;'

        'PWD=GIGtel@20152;'

    )




    # SQL query to retrieve shipment details based on the given Shipment ID

    shipment_details_query = f"""

        SELECT *

        FROM ShipmentProfile

        WHERE ShipmentID = '{shipment_id}'

    """




    # Execute the query and fetch the data into a DataFrame

    shipment_details_df = pd.read_sql(shipment_details_query, conn)




    # Close the database connection

    conn.close()




    return shipment_details_df




# Function to query shipment details based on the ETD range

def query_shipment_details_range(start_date, end_date):

    # Convert start_date and end_date to datetime objects

    start_datetime = datetime.strptime(start_date, '%Y-%m-%d')

    end_datetime = datetime.strptime(end_date, '%Y-%m-%d')




    # Connect to the SQL Server

    conn = pyodbc.connect(

        'Driver={ODBC Driver 17 for SQL Server};'

        'Server=20.207.202.225;'

        'Database=Analysis Dashboard;'

        'UID=Hanumant;'

        'PWD=GIGtel@20152;'

    )




    # Format start_date and end_date as strings in 'YYYY-MM-DD' format

    start_date_str = start_datetime.strftime('%Y-%m-%d')

    end_date_str = end_datetime.strftime('%Y-%m-%d')




    # SQL query to retrieve shipment details based on the ETD range

    shipment_details_query = f"""

        SELECT *

        FROM ShipmentProfile

        WHERE CAST(ETDLoad AS DATE) >= '{start_date_str}' AND CAST(ETDLoad AS DATE) <= '{end_date_str}'

    """




    # Execute the query and fetch the data into a DataFrame

    shipment_details_df = pd.read_sql(shipment_details_query, conn)




    # Close the database connection

    conn.close()




    return shipment_details_df




# Function to create a table for shipment details

def create_shipment_table(df):

    return dmc.Table(

        striped=True,

        highlightOnHover=True,

        withBorder=True,

        withColumnBorders=True,

        children=[

            html.Thead(

                html.Tr(

                    [html.Th(col) for col in df.columns]

                )

            )

        ] + [

            html.Tbody([

                html.Tr(

                    [html.Td(data) for data in row]

                ) for row in df.values

            ])

        ]

    )




# Function to create tables for monthly shipment details

def create_monthly_shipment_tables(df):

    # Convert ETDLoad column to datetime

    df['ETDLoad'] = pd.to_datetime(df['ETDLoad'])




    monthly_tables = []

    month_groups = df.groupby(pd.Grouper(key='ETDLoad', freq='M'))

    for month, month_group in month_groups:

        monthly_tables.append(html.Div([

            html.H3(f'Shipment Details - {month.strftime("%B %Y")}'),

            create_shipment_table(month_group)

        ]))

    return monthly_tables




if __name__ == '__main__':

    app = dash.Dash(__name__)

    app.layout = layout

    app.run_server(debug=True)