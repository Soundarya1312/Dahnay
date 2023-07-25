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
            style={'margin-top': '40px'},
            children=[
                html.H2('Enter HouseBill Number:', style={'color': '#20B2AA'}),
                dcc.Input(id='housebill-input', type='text'),
                html.Button('Submit', id='submit-button', n_clicks=0),
            ],
        ),
        html.H2(
            'HouseBill Details:',
            style={
                'color': '#FFE4B5',
                'margin-top': '30px',
                'background-color': 'gray',
                'padding': '10px'
            }
        ),
        html.Div(
            id='housebill-details',
            style={
                'margin-top': '10px',
                'background-color': 'white',
                'padding': '10px'
            }
        ),
    ]
)


# Callback function to handle button click and retrieve housebill details
@callback(
    Output('housebill-details', 'children'),
    Input('submit-button', 'n_clicks'),
    Input('housebill-input', 'value')
)
def retrieve_housebill_details(n_clicks, housebill_number):
    if n_clicks > 0:
        # Query the housebill details based on the given HouseBill Number
        housebill_details_df = query_housebill_details(housebill_number)

        if not housebill_details_df.empty:
            return html.Div(
                style={'overflow': 'auto'},
                children=[create_housebill_table(housebill_details_df)]
            )
        else:
            return html.Div('No housebill details found for the given HouseBill Number.', style={'color': 'red'})
    return ''


# Function to query housebill details based on the HouseBill Number
def query_housebill_details(housebill_number):
    # Connect to the SQL Server
    conn = pyodbc.connect(
        'Driver={ODBC Driver 17 for SQL Server};'
        'Server=20.207.202.225;'
        'Database=Analysis Dashboard;'
        'UID=Hanumant;'
        'PWD=GIGtel@20152;'
    )

    # SQL query to retrieve housebill details based on the given HouseBill Number
    housebill_details_query = f"""
        SELECT *
        FROM CONSOLEROUTING
        WHERE HouseBill = '{housebill_number}'
    """

    # Execute the query and fetch the data into a DataFrame
    housebill_details_df = pd.read_sql(housebill_details_query, conn)

    # Close the database connection
    conn.close()

    return housebill_details_df


# Function to create a table for housebill details
def create_housebill_table(df):
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


if __name__ == '__main__':
    app = dash.Dash(__name__)
    app.layout = layout
    app.run_server(debug=True)
