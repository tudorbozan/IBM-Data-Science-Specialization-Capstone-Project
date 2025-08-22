# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
site_names = spacex_df.loc[:,'Launch Site'].unique()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',options=[{'label':'All Sites',
                                                                        'value':'All'},
                                                                        {'label':site_names[0],
                                                                        'value':site_names[0]},
                                                                        {'label':site_names[1],
                                                                        'value':site_names[1]},
                                                                        {'label':site_names[2],
                                                                        'value':site_names[2]},
                                                                        {'label':site_names[3],
                                                                        'value':site_names[3]}],
                                            placeholder='Select a Launch Site',
                                            searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000,
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
            Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    pie_df = spacex_df
    if entered_site == "All":
        fig = px.pie(pie_df, values='class',names='Launch Site',title='Success count per site')
    else:
        fig = px.pie(pie_df[pie_df.loc[:,'Launch Site']==entered_site].loc[:,'class'].value_counts().reset_index(),
                    values='count',names='class',title=f'Success count for {entered_site}', color='class',
                    color_discrete_map={1:'lightgreen',
                                        0:'darkorange'})
    return fig
    
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
            Input(component_id='site-dropdown', component_property='value'),
            Input(component_id='payload-slider', component_property='value'))
def get_scatter_payload(entered_site,payload):
    scatter_df = spacex_df[(spacex_df.loc[:,'Payload Mass (kg)']>=payload[0])&
                            (spacex_df.loc[:,'Payload Mass (kg)']<=payload[1])]
    if entered_site == 'All':
        fig = px.scatter(scatter_df,'Payload Mass (kg)','class',color='Booster Version Category')
        return fig
    else:
        fig = px.scatter(scatter_df[scatter_df.loc[:,'Launch Site']==entered_site],'Payload Mass (kg)','class',color='Booster Version Category')
        return fig
# Run the app
if __name__ == '__main__':
    app.run()
