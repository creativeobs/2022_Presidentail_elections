# --Run these codes on CMD
# -- Connect to atlas from local:
# mongosh "mongodb+srv://cluster0.6hxbu.mongodb.net/myFirstDatabase" --username Saladdin

# -- Import to atlas from local
# mongoimport --uri mongodb+srv://Saladdin:darkestdark14@cluster0.6hxbu.mongodb.net/election --collection candidates --type csv --headerline --file candidates.csv

from datetime import date
from dash.html.Center import Center
from numpy import select
from numpy.lib.nanfunctions import _nanmedian_small
import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
from dash import Dash, dcc, html, Input, Output, State  # pip install dash (version 2.0.0 or higher)
import pymongo
from pymongo import MongoClient
import dash_bootstrap_components as dbc


# ------------ Dash App
app = Dash(__name__, external_stylesheets=[dbc.themes.ZEPHYR],
                                            meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, height=device-height, initial-scale=1.0'}],
                            suppress_callback_exceptions=True)

# ------------ App layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page_content')
])

# ------------ Navigation Bar
nav = dbc.Nav(
        [   
            dbc.NavItem(dbc.NavLink("Web Application Dashboards with Dash", disabled=True, href="/")),
            dbc.NavItem(dbc.NavLink("About", href="/about", active="exact" )),
            dbc.NavItem(dbc.NavLink("Graphs", href="/graphs", active="exact")),
            dbc.NavItem(dbc.NavLink("Authors", href="/authors", active="exact")),
        ],
        className= "bg-primary, py-3",
        )
     
#--------------------About Cards
bar_card = dbc.Card(
    [
        dbc.CardImg(src="https://i2.wp.com/annkemery.com/wp-content/uploads/2017/01/EmeryAnalytics_Horizontal-Bar-Chart-1.png?resize=975%2C375", top=True),
        dbc.CardBody(html.P("Description for Bar Graph", className="card-text")),
    ],
    style={"width": "30rem", "height" : "25rem"},
)

line_card = dbc.Card(
    [
        dbc.CardImg(src="https://th.bing.com/th/id/OIP.m320nT_XR_XQ-uRGhUFT4wHaFA?pid=ImgDet&rs=1", top=True),
        dbc.CardBody(html.P("Description for Line Graph", className="card-text")),
    ],
    style={"width": "30rem", "height" : "25rem"},
)

# ------------ About layout 
about_layout =  dbc.Container([
    nav,
    dbc.Row([
        dbc.Col(html.H1("About", className="text-center mt-3"),
        ) 
    ]),
    dbc.Row([
        dbc.Col([
                html.Img(src=app.get_asset_url('./images/line_chart.png'), className='h-75 d-inline ml-3'),
                html.Div(html.P("This online dashboard is used to monitor social media mentions of the running candidates for Presidency on the incoming Election 2022", className='text-justify text-break'),
                className='w-25 d-inline-block')
                ], width={'size':14,'offset':1}
        ),    
    ]),  
    dbc.Row([
        dbc.Col([
                html.Div(html.P("This online dashboard is used to monitor social media mentions of the running candidates for Presidency on the incoming Election 2022", className='text-justify text-break'),
                className='w-25 d-inline-block'),
                html.Img(src=app.get_asset_url('./images/socialgirl.png'), className='h-75 d-inline ml-3')
                ], width={'size':14,'offset':2}
        ),    
    ]),
    dbc.Row([html.Center(html.H2("Help us to up your candidate!", className='text-center float-left float-right'))]),
    dbc.Row([
        dbc.Col([
                html.Img(src=app.get_asset_url('./images/candidate.png'), className='h-75  float-right'), 
                ],
        ),
        
        # dbc.Col([ # Will add some sort of survey
        #         html.Img(src=app.get_asset_url('./images/candidate.png'), className='h-75 float-left float-right')
        #         ],
        # ),        
    ]),
    dbc.Row(dbc.Col(html.Img(src=app.get_asset_url('./images/team_page.png'),style={"width": "45rem",}, ),width ={"offset": 3},), ),
    dbc.Row([
        dbc.Col(html.H3("Meet our Developers"), className="lead", width ={"offset": 5} ),     
        # dbc.Col(
        #     html.Img(src=app.get_asset_url('./images/team_page.png'),style={"width": "40rem"}),
        #   width = 8, lg= {"size": 8, "offset": 0, "order":"first"}), 
        # dbc.Col( width = 8, lg= {"size": 8, "offset": 2, }
        #     html.H3("Meet our Developers",  ), 
        #   width = 4, lg= {"size": 8, "offset": 0, "order":"last"}),
        
        
    ], ),     
    dbc.Row( dbc.Col(dbc.Button("Let's go!", outline=True, color="success", href="/authors",className=" my-3 mx-5", style={"width": "8rem", }), width ={"offset": 5} ),),
    
     

], fluid = True)
  
# ------------ Graphs layout 
graphs_layout = html.Div([
    html.Div(id='graphs_content'),
    nav,
    dbc.Row(dbc.Col(html.H3("Bar Graph"), class_name =" display-4 text-center, my-3 mx-0"
                     ), style={'textAlign':'center'},
                ),
    dbc.Col(dcc.Graph(id='bar', figure={}, className = "p-2 border border-secondary")),

    dbc.Row(dbc.Col(html.H3("Line Graph"), class_name =" display-4 text-center, my-3 mx-0"
                         ), style={'textAlign':'center'},
                ), 
    
    dbc.Row(dbc.Col(dcc.Dropdown(id="slct_tf",
                 options=[
                     {"label": "Daily", "value": "daily"},
                     {"label": "Weekly", "value": "weekly"},
                     {"label": "Monthly", "value": "monthly"}],
                 multi=False,
                 value="daily",
                 ),
                  width={'size': 3, 'offset': 1},
                   ),
                ),

    html.Hr(className ="my-3"),
    dbc.Row(dbc.Col(dcc.Dropdown(id="slct_cand",
                # options=[{'label': k, 'value': k} for k in list(bar_df.sort_values(by='sum', ascending=False)['Date'])],
                # value=list(bar_df['Date'])[0],
                options=[{'label': 'Marcos', 'value':'Marcos' }],
                value='Marcos'
                 ),
                  width={'size': 3, 'offset': 1},
                   ),
                ),
    html.P(
    [
        "Time Frame: ",
        dbc.Badge(
            id ="badge_t",
            color="success",
            pill=True,
            text_color="white",
            # className="float-left",
        ),
    ],
    className="position-relative mx-3", 
    ),
    
    dbc.Col(dcc.Graph(id='line', figure={}, className = "p-2 border border-secondary")),
])

#-------------Author Cards
author1 = dbc.Card(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.CardImg(
                        src=app.get_asset_url("./images/a.png"),
                        className="img-fluid rounded-start",
                    ),
                    className="col-md-4",
                ),
                dbc.Col(
                    dbc.CardBody(
                        [
                            html.H4("John Mark Acala", className="card-title"),
                            
                        ]
                    ),
                    className="col-md-8",
                    ),

                
            ],

            className="g-0 d-flex align-items-center ", 
        ),   
        
        
    ],
    className="my-5 mx-3",
    style={"maxWidth": "540px", },
)
author2 = dbc.Card(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.CardImg(
                        src=app.get_asset_url("./images/b.png"),
                        className="img-fluid rounded-start",
                    ),
                    className="col-md-4",
                ),
                dbc.Col(
                    dbc.CardBody(
                        [
                            html.H4("John Kenneth Camarador", className="card-title"),
                            
                        ]
                    ),
                    className="col-md-8",
                    ),

                
            ],

            className="g-0 d-flex align-items-center ", 
        ),   
        
        
    ],
    className="my-3 mx-3 float-right",
    style={"maxWidth": "540px" },
)
author3 = dbc.Card(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.CardImg(
                        src=app.get_asset_url("./images/c.png"),
                        className="img-fluid rounded-start",
                    ),
                    className="col-md-4",
                ),
                dbc.Col(
                    dbc.CardBody(
                        [
                            html.H4("Russel John Evangelista", className="card-title"),
                            
                        ]
                    ),
                    className="col-md-8",
                    ),

                
            ],

            className="g-0 d-flex align-items-center ", 
        ),   
        
        
    ],
    className="my-3 mx-3", 
    style={"maxWidth": "540px"},
)
author4 = dbc.Card(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.CardImg(
                        src=app.get_asset_url("./images/d.png"),
                        className="img-fluid rounded-start",
                    ),
                    className="col-md-4",
                ),
                dbc.Col(
                    dbc.CardBody(
                        [
                            html.H4("Shaina Mirandilla", className="card-title"),
                            
                        ]
                    ),
                    className="col-md-8",
                    ),

                
            ],

            className="g-0 d-flex align-items-center ", 
        ),   
        
        
    ],
    className="my-3 mx-3",
    style={"maxWidth": "540px"},
)
author5 = dbc.Card(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.CardImg(
                        src=app.get_asset_url("./images/e.png"),
                        className="img-fluid rounded-start",
                    ),
                    className="col-md-4",
                ),
                dbc.Col(
                    dbc.CardBody(
                        [
                            html.H5("Amhie Olag", className="card-title"),
                            
                        ]
                    ),
                    className="col-md-8",
                    ),

                
            ],

            className="g-0 d-flex align-items-center ", 
        ),   
        
        
    ],
    className="my-3 mx-3",
    style={"maxWidth": "540px"},
)



# ------------ Authors layout 
authors_layout = html.Div([
        html.Div(id='authors_content'),
        
        nav,
        dbc.Row(dbc.Col(html.H3("This is Our Team"), class_name =" display-4 text-center, my-3 mx-0 lead"
                        ), style={'textAlign':'center',}, 
                    ),
        dbc.Row(dbc.Col(html.Img(src=app.get_asset_url('./images/build.png'),  className='h-70 d-inline ml-3', style={"width": "55rem"}),width={"offset":2},)),  
        dbc.Row(dbc.Col(
            dbc.Spinner(size="lg", color="primary", type="grow", ),
            width={'offset': 6}), class_name ="my-10"
        ),    
        #style ={"background-color" : "#eceff1"}
        dbc.Row(dbc.Col(author1, width={'offset': 1})),
        dbc.Row(dbc.Col(author2, width={'offset': 6}), ),
        dbc.Row(dbc.Col(author3, width={'offset': 1})),
        dbc.Row(dbc.Col(author4, width={'offset': 6}),),
        dbc.Row(dbc.Col(author5, width={'offset': 1}))
])

# ------------ Navigation Callback
@app.callback(Output('page_content', 'children'),
             [Input('url', 'pathname'),
             ])
  
 

def display_page(pathname):
    if pathname == '/about':
        return about_layout
    elif pathname == '/graphs':
        return graphs_layout
    elif pathname == '/authors':
        return authors_layout
    else:
        return about_layout

   

# ------------ Graphs page Callbacks

# ------------ RUN!
if __name__ == '__main__':
    app.run_server(debug=True)

