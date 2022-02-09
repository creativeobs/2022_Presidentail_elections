# --Run these codes on CMD
# -- Connect to atlas from local:
# mongosh "mongodb+srv://cluster0.6hxbu.mongodb.net/myFirstDatabase" --username Saladdin

# -- Import to atlas from local
# mongoimport --uri mongodb+srv://Saladdin:darkestdark14@cluster0.6hxbu.mongodb.net/election --collection candidates --type csv --headerline --file candidates.csv

from datetime import date
from numpy import select
from numpy.lib.nanfunctions import _nanmedian_small
import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
from dash import Dash, dcc, html, Input, Output, State  # pip install dash (version 2.0.0 or higher)
import pymongo
import plotly.io as pio
from pymongo import MongoClient
import dash_bootstrap_components as dbc




# ------------ Setup connection to mongodb and Setup DFs
client = MongoClient("mongodb+srv://Saladdin:darkestdark14@cluster0.6hxbu.mongodb.net/election?ssl=true&ssl_cert_reqs=CERT_NONE", connect=False)
db = client["election"]
counts_daily = db.counts_daily
counts_weekly = db.weekly_daily
counts_monthly = db.monthly_daily
posts = db.posts


df_daily = pd.DataFrame(list(counts_daily.find()))
df_weekly = pd.DataFrame(list(counts_weekly.find()))
df_monthly = pd.DataFrame(list(counts_monthly.find()))

# ------------ Pre-process bar_df
bar_df = df_daily
bar_df = bar_df.reset_index(drop=True)
bar_df = bar_df.drop(columns='_id')
bar_df = bar_df.transpose()  # Swap columns into rows
bar_df = bar_df.reset_index()
bar_df.columns = bar_df.iloc[0]
bar_df = bar_df.drop(0)
bar_df[bar_df.columns[1:]] = bar_df[bar_df.columns[1:]].apply(pd.to_numeric) # Convert to numeric before total
bar_df["sum"] = bar_df.sum(axis=1) # Total count column for bar graph
bar_df = bar_df.sort_values(by='sum', ascending=True) #Sort
bar_df = bar_df.loc[bar_df['Date']!='duterte carpio sara zimmerman ', :] # Remove sara
bar_df = bar_df.loc[bar_df['sum']>0, :] # Remove Candidates with zero counts 

# ------------ Dash App

app = Dash(__name__, external_stylesheets=[dbc.themes.ZEPHYR, './my-style.css'],
                                            meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}],
                            suppress_callback_exceptions=True)

# ------------ App layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page_content')
])

# ------------ Navigation Bar
nav = dbc.Nav(
        [   
            dbc.NavItem(dbc.NavLink("Web Application Dashboards with Dash", disabled=True, href="/", 
            style ={"margin-right": "30px", "color":"#181174 !important", "border-bottom": "2px solid transparent"})),
            dbc.NavItem(dbc.NavLink("About", href="/about", )),
            dbc.NavItem(dbc.NavLink("Graphs", href="/graphs")),
            dbc.NavItem(dbc.NavLink("Authors", href="/authors")),
        ],
        className= "bg-light, py-3",
        )
       
# ------------ Graphs layout 
graphs_layout = html.Div([
    html.Div(id='graphs_content'),
    nav,
    dbc.Row(dbc.Col(html.H3("Bar Graph"), class_name =" display-4 text-center, my-3 mx-0"
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


    dbc.Col(dcc.Graph(id='bar', figure={}, className = "p-2 border border-secondary")),

    
    html.Hr(className ="my-3"),
    dbc.Row(dbc.Col(html.H3("Line Graph"), class_name =" display-4 text-center, my-3 mx-0"
                         ), style={'textAlign':'center'},
                ), 
    
    
    
    dbc.Row(dbc.Col(dcc.Dropdown(id="slct_cand",
                options=[{'label': k, 'value': k} for k in list(bar_df.sort_values(by='sum', ascending=False)['Date'])],
                value=list(bar_df['Date'])[0],
                 ),
                  width={'size': 3, 'offset': 1},
                   ),
                ),
    
    html.P(
    [
        "Candidate: ",
        dbc.Badge(
            id ="badge_c",
            color="info",
            pill=True,
            text_color="white",
            # className="float-left",
        ),
    ],
    className="position-relative mx-4", 
    ),

    dbc.Col(dcc.Graph(id='line', figure={}, className = "p-2 border border-secondary")),

])


#--------------------About Cards
bar_card = dbc.Card(
    [
        dbc.CardImg(src="https://i2.wp.com/annkemery.com/wp-content/uploads/2017/01/EmeryAnalytics_Horizontal-Bar-Chart-1.png?resize=975%2C375", top=True),
        dbc.CardBody(html.P("Description for Bar Graph", className="card-text")),
         dbc.Button("Go somewhere", color="primary"),
    ],
    style={"width": "30rem", "height" : "25rem"},
)
line_card = dbc.Card(
    [
        dbc.CardImg(src="https://th.bing.com/th/id/OIP.m320nT_XR_XQ-uRGhUFT4wHaFA?pid=ImgDet&rs=1", top=True),
        dbc.CardBody(html.P("Description for Line Graph", className="card-text")),
        dbc.Button("Go somewhere", color="primary"),
    ],
    style={"width": "30rem", "height" : "25rem"},
)


# ------------ About layout 
about_layout = html.Div([
    html.Div(id='about_content'),
    nav,
    dbc.Row(dbc.Col(html.H3("This is Our Project"), class_name =" display-4 text-center, my-3 mx-0"
                     ), style={'textAlign':'center'},
            
                ),
                
    dbc.Row( dbc.Col(html.P(
            "This website app asdfghjkl. How it works", className="lead"),
            ),  style={'textAlign':'center'},
    ),            
    dbc.Row(
    [
        dbc.Col(bar_card, width="auto"),
        dbc.Col(line_card, width="auto"),
        

    ],justify="evenly",
    ),


                
])

#-------------authorcards
author1 = dbc.Card(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.CardImg(
                        src="https://th.bing.com/th/id/OIP.1Agw8tPi1oidtC_q4U4ZdgHaHa?pid=ImgDet&w=1890&h=1890&rs=1",
                        className="img-fluid rounded-start",
                    ),
                    className="col-md-4",
                ),
                dbc.Col(
                    dbc.CardBody(
                        [
                            html.H4("Person 1", className="card-title"),
                            
                        ]
                    ),
                    className="col-md-8",
                    ),

                
            ],

            className="g-0 d-flex align-items-center ", 
        ),   
        
        
    ],
    className="my-3 mx-3",
    style={"maxWidth": "540px", },
)
author2 = dbc.Card(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.CardImg(
                        src="https://th.bing.com/th/id/OIP.1Agw8tPi1oidtC_q4U4ZdgHaHa?pid=ImgDet&w=1890&h=1890&rs=1",
                        className="img-fluid rounded-start",
                    ),
                    className="col-md-4",
                ),
                dbc.Col(
                    dbc.CardBody(
                        [
                            html.H4("Person 2", className="card-title"),
                            
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
                        src="https://th.bing.com/th/id/OIP.1Agw8tPi1oidtC_q4U4ZdgHaHa?pid=ImgDet&w=1890&h=1890&rs=1",
                        className="img-fluid rounded-start",
                    ),
                    className="col-md-4",
                ),
                dbc.Col(
                    dbc.CardBody(
                        [
                            html.H4("Person 3", className="card-title"),
                            
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
                        src="https://th.bing.com/th/id/OIP.1Agw8tPi1oidtC_q4U4ZdgHaHa?pid=ImgDet&w=1890&h=1890&rs=1",
                        className="img-fluid rounded-start",
                    ),
                    className="col-md-4",
                ),
                dbc.Col(
                    dbc.CardBody(
                        [
                            html.H4("Person 4", className="card-title"),
                            
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
                        src="https://th.bing.com/th/id/OIP.1Agw8tPi1oidtC_q4U4ZdgHaHa?pid=ImgDet&w=1890&h=1890&rs=1",
                        className="img-fluid rounded-start",
                    ),
                    className="col-md-4",
                ),
                dbc.Col(
                    dbc.CardBody(
                        [
                            html.H5("Person 5", className="card-title"),
                            
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
    dbc.Row(dbc.Col(html.H3("This is Our Team"), class_name =" display-4 text-center, my-5 mx-0"
                     ), style={'textAlign':'center'},
                ),
    dbc.Row(dbc.Col(author1, width={'offset': 1})),
    dbc.Row(dbc.Col(author2, width={'offset': 6}), style ={"background-color" : "#eceff1"}),
    dbc.Row(dbc.Col(author3, width={'offset': 1})),
    dbc.Row(dbc.Col(author4, width={'offset': 6}), style ={"background-color" : "#eceff1"}),
    dbc.Row(dbc.Col(author5, width={'offset': 1})), 
    

])


# ------------ Navigation Callback
@app.callback(Output('page_content', 'children'),
              [Input('url', 'pathname')])
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
@app.callback(
    [Output(component_id='bar', component_property='figure'),
    Output(component_id='line', component_property='figure'),
    Output(component_id='badge_t', component_property='children'),
    Output(component_id='badge_c', component_property='children'),], 
    [Input(component_id='slct_tf', component_property='value'),
    Input(component_id='slct_cand', component_property='value')]
    )
def update_graph(slct_tf, slct_cand):
    global df_daily, df_weekly, df_monthly, bar_df

    # Bar Graph - Total counts
    col_name =bar_df.columns[0]
    col_count = bar_df.columns[-1]
    bar_fig = px.bar(bar_df, x=col_count, y=col_name, orientation='h',  labels={col_count: "Count", col_name: "Name"}, 
                        color = col_name, opacity=0.8, height = 900)
    # bar_fig.update_traces(texttemplate='%{col_count:.2s}', textposition='outside',
    #                    width=[.3,.3,.3,.3,.3,.3,.3,.3,.3,.3,.3,.3,.3,.3,.3,.3,.3,.3,.3,.3,.6])
    badge_time = slct_tf 

    # Line Graph - Per timeframe and candidate
    if slct_tf == 'daily':
        line_df = df_daily
    elif slct_tf == 'weekly':
        line_df = df_weekly
    elif slct_tf == 'monthly':
        line_df = df_weekly
    
    
    line_fig = px.line(line_df, x="Date", y=slct_cand, title=f'{slct_cand} timeseries')
    badge_candidate=slct_cand

    return bar_fig, line_fig, badge_time, badge_candidate

# ------------ RUN!
if __name__ == '__main__':
    app.run_server(debug=True)

