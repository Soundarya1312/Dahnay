import dash
from dash import Dash, html, dcc
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import base64

app = Dash(
    __name__, 
    external_stylesheets=[
        'https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css',
        'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'
    ],
    use_pages=True  # Using use_pages=True to enable page routing
)
server= app.server
with open("C:/Users/DLPLCORPLAP-0187/Desktop/assets/dahnay_new_logo-removebg-preview (1).png", "rb") as image_file:
    base64_logo = base64.b64encode(image_file.read()).decode("utf-8")

app.layout = html.Div([
    dmc.Header(
        height=70, 
        fixed=True,
        pl=0,
        pr=0,
        pt=0,
        style={
            'background-image': 'linear-gradient(to right, #ffcc99 0%, #6666ff 100%)', 
            'color': 'whitesmoke'
        },
        children=[
            dmc.Container(
                fluid=True,
                children=[
                    html.Img(src=f"data:image/png;base64,{base64_logo}", style={'width': '150px', 'position': 'absolute', 'top': '10px', 'left': '10px'}),
                    html.H1(
                        'SHIPMENT PROFILE REPORT', 
                        style={
                            'text-align': 'center',
                            'padding': '10px', 
                        }
                    ),
                ]
            ),
        ]
    ),

    dmc.Navbar(
        fixed=True,
        width={"base": 200},
        pl='xs',
        pb=0,
        pr='xs',
        pt=0,
        hidden=True,
        hiddenBreakpoint='sm',
        children=[
            dmc.ScrollArea(
                offsetScrollbars=True,
                type="scroll",
                children=[
                    dmc.Group(
                        style={
                            'margin-top': '15px',
                            'gap': '5px',
                        },
                        children=[
                            # Automatically include NavLink for each page registered with use_pages=True
                            dmc.NavLink(
                                label=page['name'],
                                href=page["relative_path"],
                                rightSection=DashIconify(icon="tabler-chevron-right"),
                                variant="filled",
                                active=True,
                            ) for page in dash.page_registry.values()
                        ]
                    )
                ],
            )
        ],
    ),

    html.Div(
        id='content',
        style={'margin-top': '70px', 'margin-left': '200px'},
        children=[dash.page_container]
    )
])

if __name__ == '__main__':
    app.run(debug=True)
