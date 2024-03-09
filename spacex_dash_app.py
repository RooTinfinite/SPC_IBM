# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                options=[
                                    {"label": "All Sites","value": "allofthem"},
                                    {"label": spacex_df["Launch Site"].unique()[0],"value": spacex_df["Launch Site"].unique()[0]},
                                    {"label": spacex_df["Launch Site"].unique()[1],"value": spacex_df["Launch Site"].unique()[1]},
                                    {"label": spacex_df["Launch Site"].unique()[2],"value": spacex_df["Launch Site"].unique()[2]},
                                    {"label": spacex_df["Launch Site"].unique()[3],"value": spacex_df["Launch Site"].unique()[3]}
                                ],
                                value="ALL",
                                placeholder="Choose launch site ",
                                searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                # Function decorator to specify function input and output
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',min=0,max=10000,step=1000,
                                marks={
                                0:"0",
                                2500:"2500",
                                5000:"5000",
                                7500:"7500"                               
                                },
                                value=[0,10000]
                                ),

                                # TASK 
                                #4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(site):
    if site == "allofthem":
        fig = px.pie(spacex_df, values='class', names='Launch Site',title="total succes lauch by site")
    else:
        site_df=spacex_df[spacex_df["Launch Site"]== site]
        fig = px.pie(site_df, names='class',title="Succes and failure rate in %")
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), 
              Input(component_id="payload-slider", component_property="value")])

def get_scatter(site,payload):
    print(payload)
    spacex_df.sort_values(by="Payload Mass (kg)", ascending=False,inplace=True)
    lower=payload[0]
    higher=payload[1]
    if site == "allofthem":
        payload_df= spacex_df[(spacex_df["Payload Mass (kg)"] < higher)  & (spacex_df["Payload Mass (kg)"] > lower)]
        scatter = px.scatter(payload_df,x="Payload Mass (kg)",y="class",color="Booster Version",hover_data=['Launch Site'])
    else:
        site_df=spacex_df[spacex_df["Launch Site"]== site]
        payload_df= site_df[(site_df["Payload Mass (kg)"] < higher)  & (site_df["Payload Mass (kg)"] > lower)]
        scatter = px.scatter(payload_df,x="Payload Mass (kg)",y="class",color="Booster Version",hover_data=['Launch Site'])


    return scatter



# Run the app
if __name__ == '__main__':
    app.run_server()