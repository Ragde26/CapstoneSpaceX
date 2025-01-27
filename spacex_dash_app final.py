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
################################################################################################################################                                              
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site_dropdown', 
                                    options=[{'label': 'All Sites', 'value': 'ALL'},
                                             {'label': 'CCAFS LC-40','value': 'CCAFS LC-40'},
                                             {'label': 'VAFB SLC-4E','value': 'VAFB SLC-4E'},
                                             {'label': 'KSC LC-39A','value': 'KSC LC-39A'},
                                             {'label': 'CCAFS SLC-40','value': 'CCAFS SLC-40'}],
                                               value='ALL',
                                               placeholder="Select a launch site",
                                               searchable=True,
                                               ),
                                html.Div(id='container-1'),
 ###############################################################################################################################                               
                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.P("Succes Pie Chart"),
                                dcc.Graph(id='success_pie_chart'),
                                html.Br(),             
                                                    
################################################################################################################################
                                # TASK 3: Add a slider to select payload range
                                html.P("Payload range (Kg):"),
                                dcc.RangeSlider(id='payload_slider', min=0, max=10000, step=1000, marks={0: '0',2500: '2500',5000:'5000',7500:'7500',10000:'10000'},value=[min_payload,max_payload]),
                                html.Div(id='output-container-range-slider', style={'display': 'flex'}),
################################################################################################################################
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.P("Success vs Payload"),
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                html.Br(), 
                   ]) 

################################################################################################################################
                                # TASK 2:
                                # Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
                                
@app.callback (
                Output(component_id='success_pie_chart', component_property='figure'),
                Input(component_id='site_dropdown', component_property='value')
              )
                                # Function decorator to specify function input and output
def get_pie_chart(site_dropdown):
    
    if site_dropdown == 'ALL':
       figure = px.pie(spacex_df, values='class', names='Launch Site',title='Total Success Launches by Site')
       return figure
    else:
       filtered_df = spacex_df[spacex_df['Launch Site']== site_dropdown]
       filtered_df2 = filtered_df.groupby(['class'])['Flight Number'].count().reset_index(name='count') 
       figure = px.pie(filtered_df2, values='count', names='class',title=('Total Success Launches for Site' + '  ' + site_dropdown ))
       return figure  

html.Br(),

@app.callback(
            Output('container-1', 'children'),
            Input('site_dropdown', 'value')
             )
def update_output(value):
   return f'You have selected {value}'

@app.callback(
            Output('output-container-range-slider', 'children'),
            Input('payload_slider', 'value'))
def update_output(value):
    return 'You have selected "{}"'.format(value)
           
################################################################################################################################      
# TASK 4:
# Add a callback function for `site-dropdown` and `payload_slider` as inputs, `success-payload-scatter-chart` as output
@app.callback (
            Output(component_id='success-payload-scatter-chart', component_property='figure'),
            [Input(component_id='site_dropdown', component_property='value'), Input(component_id="payload_slider", component_property="value")]
             )

                                # Function decorator to specify function input and output
def get_scatter_chart(site_dropdown,payload_slider):
    
    if site_dropdown == 'ALL':
        start = payload_slider[0]
        end = payload_slider[1]
        filtered_scatter = spacex_df[(spacex_df['Payload Mass (kg)']>=start) & (spacex_df['Payload Mass (kg)']<=end)]
        #filtered_scatter1 = filtered_scatter[filtered_scatter['Payload Mass (kg)'] <= end]
        figure = px.scatter(filtered_scatter, x='Payload Mass (kg)', y='class', color='Booster Version Category')
        return figure
    else:
       filtered_df = spacex_df[spacex_df['Launch Site']== site_dropdown]
       figure = px.scatter(filtered_df, x="Payload Mass (kg)", y="class", color="Booster Version Category")
       return figure  


html.Br(),

      

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8060)