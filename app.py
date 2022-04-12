# necessary libraries
import dash
from dash import dcc, html, dash_table
import pandas as pd
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import datetime as dt
import dash_bootstrap_components as dbc

# dataframes
# dataframe with the information of each crag
df_climb = pd.read_csv('sports_climb.csv')
# coordenates of each crag
df_locations = pd.read_csv('crags_coord.csv')

# fixing datatypes
df_locations['lat'] = df_locations['lat'].astype('float')
df_locations['lon'] = df_locations['lon'].astype('float')

# fixing dates
df_climb['date'] = df_climb['date'].apply(lambda x: dt.datetime.fromtimestamp(x))
df_climb['month'] = df_climb['date'].dt.month
df_climb['birth'] = df_climb['birth'].astype('datetime64[ns]')
df_climb['age'] = 2017 - df_climb.birth.dt.year

# fixing sex
df_climb['sex'] = df_climb.sex.apply(lambda x: 'Male' if x == 0 else 'Female')

# fixing columns
df_locations.rename(columns={'lat': 'lon', 'lon': 'lat'}, inplace=True)

# map figure possible styles
map_styles = {'1': 'open-street-map', '2': 'stamen-terrain', '3': 'carto-positron'}

# creates map figure
fig_map = go.Figure()

# adds details
fig_map.add_traces([go.Scattermapbox(lat=df_locations.lat,
                                     lon=df_locations.lon,
                                     text=df_locations.crag,
                                     marker=go.scattermapbox.Marker(color='#EA6A47', size=15),
                                     customdata=df_locations.crag)])
# style
fig_map.update_layout(mapbox_style=map_styles['2'],
                      mapbox=dict(center=dict(lat=df_locations['lat'].iloc[0], lon=df_locations['lon'].iloc[0]),
                                  zoom=8.5),
                      margin={"r": 0, "t": 0, "l": 0, "b": 0})

# text used to construct the information hub
text_head = html.P('Before using the rest of the visualization take a little time exploring about different concepts and '
                   'functionalities that we have implemented.',style={'text-align': 'justify'} )

text_intro =html.Div([html.P(['Welcome! This dashboard was created for the course Data Visualization, of the Maters in'
                             ' Data Science and Advanced Analytics at NOVA IMS.'], style={'text-align': 'justify'}),
                      html.P([' It offers a short insight of the portuguese rock climbing crags, in particular the main'
                             ' crags around Lisbon area.'], style={'text-align': 'justify'}),
                      html.P(['Use the map to select a specific crag. By doing that, you can check how many routes there'
                             ' is by their respective grade and the best seasons for that crag. Below you can find the'
                             ' list of routes of the selected crag, the grade, the sector and the average rate '
                             'given by the climbers. On the right find more details about the ascent type and the'
                             ' proportion of ascents between male and female climbers.'], style={'text-align': 'justify'}),
                      html.P(['Feel free to inspect the details for a specific year using the dropdown menu.'],
                             style={'text-align': 'justify'}),
                      html.P(['Thanks Cohen for making the data available. Thank you for using the dashboard!'],
                             style={'text-align': 'justify'}),
                      html.P(['The authors: Tomás Jordão and Miguel Lince'], style={'text-align': 'justify'})])

text_concepts = html.Div([html.H6('Crag'),
                          html.P('A crag is a climbing cliff belonging to a climbing area. Is usually composed by sectors.',
                                 style={'text-align': 'justify'}),
                          html.H6('Sector'),
                          html.P('A specific part of the cliff, composed by routes.',
                                 style={'text-align': 'justify'}),
                          html.H6('Route'),
                          html.P('A specific defined path on the rock.',
                                 style={'text-align': 'justify'}),
                          html.H6('Method'),
                          html.P('Method which the climber ascented the route. Redpoint: ascent with more than 1 try; Flash: Ascent with one try but with previous knowlegde of the route; Onsigth: As flash but with no previous knowledge. Top-rope: climber climbs with the rope passing on the anchor of the route.',
                                 style={'text-align': 'justify'})
                          ])

text_visualzation =html.Div([html.P('The visualization shown on the right is divided into nine parts:',
                                    style={'text-align': 'justify'}),
                             html.H6('Dropdown - Overall and Map Option'),
                             html.P('This component allows the user to select between seeing all of the information or '
                                    'the information relative to a specific crag. The crag selection is made on the map.',
                                    style={'text-align': 'justify'}),
                             html.H6('Dropdown - Year selection'),
                             html.P('Using this component you can filter the information shown in the graphics and the '
                                    'table by year.',
                                    style={'text-align': 'justify'}),
                             html.H6('Summary'),
                             html.P('In here you can find the name of the crag you selected on the map, average rating '
                                    'and number of ascents on the selected year.',
                                    style={'text-align': 'justify'}),
                             html.H6('Map'),
                             html.P('In this part you can select the crag you want to see by hovering through'
                                    ' the points shown in the map.',
                                    style={'text-align': 'justify'}),
                             html.H6('Grades'),
                             html.P('In this part you can see the number of ascents by ascent method.',
                                    style={'text-align': 'justify'}),
                             html.H6('Season'),
                             html.P('Using this graphic you can see the number of ascents in each of the months.',
                                    style={'text-align': 'justify'}),
                             html.H6('Table'),
                             html.P('This part shows the differents routes a specific crag has, their dificulty and the '
                                    'grade given by previous ascensionists.'
                                    'You can select a route and filter the two graphs placed on the'
                                    'right side of the table. The Rate of the route its given by the user in a scale of 1 to 5.',
                                    style={'text-align': 'justify'}),
                             html.H6('Method'),
                             html.P('In this graphic you can see how many ascents of a specific method exists '
                                    'for all the routes or for a specific one by selecting the route in the table.',
                                    style={'text-align': 'justify'}),
                             html.H6('Gender Distribution'),
                             html.P('In this part you can see the proportion of males and female ascents.',
                                    style={'text-align': 'justify'}),
                            ])

authors = html.Div([html.H6('Developers'),
                    html.P('Tomás Jordão and Miguel Lince')])

#Accordion
accordion = dbc.Accordion(children =
        [
            dbc.AccordionItem([text_intro], #text for the introduction
                              title="Introduction",
                              style={'backgroundColor':'#F1F1F1'},
                              class_name='primary'),
            dbc.AccordionItem([text_concepts], #text explaining rockclimbing concepts
                              title="Concepts",
                              style={'backgroundColor':'#F1F1F1'}),
            dbc.AccordionItem([text_visualzation], #text explaining the visualization
                              title='Visualization',
                              style={'backgroundColor':'#F1F1F1'}),

        ],
    start_collapsed=True,

)

#links - Dataset + GitHub
links = html.Div([html.H6('Data'),
                  html.A("https://www.kaggle.com/datasets/dcohen21/8anu-climbing-logbook",
                        href='https://www.kaggle.com/datasets/dcohen21/8anu-climbing-logbook',
                        target="_blank"),
                  html.Br(),
                  html.H6('Code'),
                  html.A("https://github.com/miguelince/8anu-climbing-logbook",
                        href='https://github.com/miguelince/8anu-climbing-logbook',
                        target="_blank"),
                  ])
# saving the last year selected
list_year = [2017] #next year selected

# app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = html.Div(style={'backgroundColor': 'white'},
                      children=[
                          # This component alerts the user if the information he is selecting doesn't exist on the dataframe
                          dbc.Alert(id='Alert',
                                    children=[
                                        'The information relative to the selected crag is not available for this year!'
                                        ' Please try another year! Thank you!'],
                                    dismissable=True,
                                    is_open=False),  # linked to the alert callback

                          # 1st row - Button + Title
                          dbc.Row(children=[
                              # Information Hub
                              dbc.Col(children=[
                                  dbc.Button("Read Me!",
                                             id='Information-Button',
                                             size='lg'),
                                  dbc.Offcanvas(children=[text_head,
                                                          html.Br(),
                                                          accordion, # constructed above
                                                          html.Br(),
                                                          links, #constructed above
                                                          html.Br(),
                                                          authors, #constructed above
                                                          html.H6('Developed using'),
                                                          dbc.CardImg(src='plotly_logo_v2.png')],
                                               id="Information-Display",
                                               title="Some Helpful Information",
                                               is_open=False,
                                  ),
                              ], width=2),
                              # title
                              dbc.Col(html.H1(style={'textAlign': 'center', 'color': '#1C4E80'},
                                              children="Sportclimbing Interactive Dashboard")
                                      , width=10)
                          ]),
                          html.Br(),
                          #2nd Row - Dropdown menus
                          dbc.Row(children=[
                              #allows the user to view the overall information of a certain year
                              dbc.Col(dcc.Dropdown(id='Total',
                                                   options=['Overall', 'Map - Crag'],
                                                   value='Overall',
                                                   clearable=False,
                                                   style={'backgroundColor': '#F1F1F1'})),
                              #allows the user to change the year
                              dbc.Col(dcc.Dropdown(id='year',
                                                   options=[{'label': str(i), 'value': i} for i in
                                                            df_climb.query("year != 0").sort_values(
                                                                'year', ascending= False).year.unique()],
                                                   value=2017,
                                                   multi=False,  # disables the option of selecting multiple options
                                                   clearable=False,
                                                   style={'backgroundColor': '#F1F1F1'}
                                                   ))
                          ]),

                          html.Br(),

                          # 2nd Row - Header(summary of crag)
                          dbc.Row(children=[
                              # Header(summary of crag)
                              dbc.Col(
                                  html.H2(style={'textAlign': 'left', 'color': '#1C4E80', 'backgroundColor': '#F1F1F1'},
                                          id='summary',
                                          children=[],  # linked to 2nd callback
                                          className="border rounded-end"
                                          ))

                          ], className= "gx-1"),

                          html.Br(),

                          # 3rd Row - Map Figure + Bar Chart + Line Plot
                          dbc.Row(children=[
                              # Map Figure
                              dbc.Col(dcc.Graph(id='map_chart',
                                                figure=fig_map,  # map figure defined above
                                                hoverData=None,
                                                config={
                                                    'doubleClick': 'reset',
                                                    'scrollZoom': False},
                                                className="border rounded-3")
                                      , width=4),
                              # Bar Chart
                              dbc.Col(dcc.Graph(id='bar_chart_seasons',
                                                figure={},  # linked to 2nd Callback
                                                config={
                                                    'doubleClick': 'reset'
                                                },
                                                className="border rounded-3")

                                      , width=4),
                              # Line Plot
                              dbc.Col(dcc.Graph(id='line_util',
                                                figure={},  # linked to 2nd Callback
                                                config={
                                                    'doubleClick': 'reset'
                                                },
                                                className="border rounded-3")
                                      , width=4)
                          ]),

                          html.Br(),

                          # 4th Row - Table + Bar Chart + Pie Chart
                          dbc.Row(children=[
                              # Table
                              dbc.Col(dash_table.DataTable(id='data_table',
                                                           columns=[],  # linked to 3rd Callback
                                                           data=[],  # linked to 3rd Callback
                                                           row_selectable='single',
                                                           selected_rows=[],  # linked to 4th Callback
                                                           # page_size=12,
                                                           page_action='none',
                                                           # changing the alignment of the first two columns
                                                           style_cell_conditional=[{'if': {'column_id': c},
                                                                                    'textAlign': 'left',
                                                                                    } for c in ['Route', 'Sector']],
                                                           style_data={'whiteSpace': 'normal',
                                                                       'height': 'auto',
                                                                       'backgroundColor':'#F1F1F1'},
                                                           # style_data_conditional=[{'if':{'row_index':'odd'},
                                                           #                         'backgroundColor': '#DADADA'}],
                                                           # styling the name of the columns
                                                           style_header={'backgroundColor': '#1C4E80',
                                                                         'fontWeight': 'bold',
                                                                         'textAlign': 'center',
                                                                         'color': 'white'},
                                                           # to be scroll
                                                           style_table={'height': '450px', 'overflowY': 'auto'})
                                      , width=4),
                              # Bar Chart
                              dbc.Col(dcc.Graph(id='method_dist',
                                                figure={},  # linked to the 3rd callback
                                                className="border rounded-3")
                                      , width=4),
                              # Pie Chart
                              dbc.Col(dcc.Graph(id='sex_dist',
                                                figure={},  # linked to the 3rd callback
                                                className="border rounded-3")
                                      , width=4)
                          ])
                      ])


# Alert Callback
@app.callback(
    Output(component_id='Alert', component_property='is_open'),
    Input(component_id='year', component_property='value'),  # year selected on the dropdown
    Input(component_id='map_chart', component_property='hoverData'),  # point(crag) selected on the map
    Input(component_id='Total', component_property='value'),  # option selected between map and total of year
    State(component_id='Alert', component_property='is_open')  # default value: is_open = False
)
def alert_creator(selected_year, hoverdata,total_value, is_open):
    alert_state = is_open  # default == False

    # this alert is only activated when a point in the map figure is selected
    if hoverdata is not None and total_value != 'Overall':
        crag = hoverdata['points'][0]['customdata']  # extrating the name of the crag selected
        dff = df_climb[(df_climb.year == selected_year)]
        if crag not in dff.crag.unique():  # checks if the crag exists in the selected year
            alert_state = True  # turns the alert on
        else:
            alert_state = False  # turns the alert off

    return alert_state


# 1st Callback - Defining if the text appears or not in the introduction button
@app.callback(
    Output(component_id='Information-Display', component_property='is_open'),  # default value: is_open = False
    Input(component_id='Information-Button', component_property='n_clicks'),
    State(component_id='Information-Display', component_property='is_open')
)
def toggle_popover(n_clicks, is_open):
    """" This function changes the state to open """
    if n_clicks:  # if the button is clicked
        return not is_open  # is_open == True
    return is_open


# 2nd Callback - Header(summary of crag) + Bar Chart + Line Plot: gets this from the map
@app.callback(
    Output(component_id='bar_chart_seasons', component_property='figure'),  # Bar chart
    Output(component_id='line_util', component_property='figure'),  # Line Plot
    Output(component_id='summary', component_property='children'),  # Header(summary of crag)
    Input(component_id='year', component_property='value'),  # year selected on the dropdown
    Input(component_id='map_chart', component_property='hoverData'),  # point(crag) selected on the map
    Input(component_id='Total', component_property='value'), # option selected between map and total of year
)
def bar_chart_seasons(selected_year, hoverdata, total_value):
    # the months are presented as integers in the dataframe
    # this dict will be used to transform those values into strings
    months = {1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Ago', 9: 'Sep', 10: 'Oct',
              11: 'Nov', 12: 'Dec'}

    if hoverdata is None or total_value == 'Overall':  # when no point is selected on the map (no crag selected)
        # filtering by the year selected
        # sorting by month so that the months appear in order on the line plot
        dff = df_climb[df_climb.year == selected_year].sort_values('month')

        # transforming the integers into strings
        dff['month'] = dff.month.apply(lambda x: months[x])

        # Creating the Bar Chart
        fig_bar = go.Figure()
        fig_bar.add_traces([go.Bar(x=sorted(dff['fra_routes'].unique()),  # sorting by grade
                                   y=dff.fra_routes.value_counts().sort_index()
                                   )])
        fig_bar.layout.plot_bgcolor = '#F1F1F1'  # changing the plot background color
        fig_bar.layout.paper_bgcolor = '#F1F1F1'  # changing the figure background color
        fig_bar.update_traces(marker_color='#1C4E80')  # dark blue
        fig_bar.update_xaxes(type='category')
        fig_bar.update_layout(margin={"r": 10, "t": 10, "l": 10, "b": 10},
                              xaxis=dict(showgrid=False, title='Grade'),
                              yaxis=dict(showgrid=False, title='Number of Ascents'))

        # Line Plot
        fig_util = go.Figure()
        fig_util.add_traces([go.Scatter(x=dff['month'].unique(),
                                        y=dff.month.value_counts().sort_index()
                                        )])
        fig_util.layout.plot_bgcolor = '#F1F1F1'  # changing the plot background color
        fig_util.layout.paper_bgcolor = '#F1F1F1'  # changing the figure background color
        fig_util.update_traces(marker_color='#1C4E80')  # ligth blue
        fig_util.update_xaxes(type='category')
        fig_util.update_layout(margin={"r": 10, "t": 10, "l": 10, "b": 10},
                               xaxis=dict(showgrid=False, title='Months'),
                               yaxis=dict(showgrid=False, title='Number of Ascents'))

        # Header(summary of crag)
        header = "Overall // " + "Average Rating: {} // ".format(
            round(dff.query("rating != 0").rating.mean(), 1)) + " Ascents: {}".format(dff.month.value_counts().sum())

        return fig_bar, fig_util, header

    elif hoverdata is not None and total_value != 'Overall':  # when a point is selected on the map (no crag selected)
        crag = hoverdata['points'][0]['customdata']  # extrating the name of the crag selected

        # creating a dataframe with the input from dropdown and crag selected
        dff = df_climb[(df_climb.crag == crag) & (df_climb.year == selected_year)].sort_values('month')
        dff['month'] = dff.month.apply(lambda x: months[x])

        fig_bar = go.Figure()
        fig_bar.add_traces([go.Bar(x=sorted(dff['fra_routes'].unique()), y=dff.fra_routes.value_counts().sort_index()
                                   )])
        fig_bar.layout.plot_bgcolor = '#F1F1F1'
        fig_bar.layout.paper_bgcolor = '#F1F1F1'
        fig_bar.update_traces(marker_color='#1C4E80')
        fig_bar.update_xaxes(type='category')
        fig_bar.update_layout(margin={"r": 10, "t": 10, "l": 10, "b": 10},
                              xaxis=dict(showgrid=False, title='Grade'),
                              yaxis=dict(showgrid=False, title='Number of Ascents'))

        fig_util = go.Figure()
        fig_util.add_traces([go.Scatter(x=dff['month'].unique(), y=dff.month.value_counts().sort_index()
                                        )])
        fig_util.layout.plot_bgcolor = '#F1F1F1'
        fig_util.layout.paper_bgcolor = '#F1F1F1'
        fig_util.update_traces(marker_color='#1C4E80')
        fig_util.update_xaxes(type='category')
        fig_util.update_layout(margin={"r": 10, "t": 10, "l": 10, "b": 10},
                               xaxis=dict(showgrid=False, title='Months'),
                               yaxis=dict(showgrid=False, title='Number of Ascents'))

        header = " {} //".format(crag) + " Average Rating: {} // ".format(
            round(dff.query("rating != 0").rating.mean(), 1)) + " Ascents: {}".format(dff.month.value_counts().sum())

        return fig_bar, fig_util, header


# 3rd Callback - Table
@app.callback(
    Output(component_id='data_table', component_property='columns'),  # columns names
    Output(component_id='data_table', component_property='data'),  # column data
    Input(component_id='year', component_property='value'),  # year selected on the dropdown
    Input(component_id='map_chart', component_property='hoverData'),  # point(crag) selected on the map
    Input(component_id='Total', component_property='value'),  # option selected between map and total of year
)
def data_table(selected_year, hoverdata, total_value):
    if hoverdata is None or total_value == 'Overall':  # when no point is selected on the map (no crag selected)
        # filtering by the year selected
        df_table = df_climb[df_climb.year == selected_year]

        # removing the vias with rating  == 0
        df_table = df_table.query("rating != 0").groupby(['name', 'sector', 'fra_routes']).rating.mean().round(
            1).reset_index()
        df_table.sort_values('rating', ascending=False, inplace=True)
        df_table.rename(columns={'name': 'Route', 'sector': 'Sector', 'fra_routes': 'Grade', 'rating': 'Rating'},
                        inplace=True)

        columns = [{'name': i, 'id': i} for i in df_table.columns]  # name of the columns in the table
        table_data = df_table.to_dict('records')  # data of the table

        return columns, table_data

    elif hoverdata is not None and total_value != 'Overall':  # when a point is selected on the map (no crag selected)
        crag = hoverdata['points'][0]['customdata']  # extrating the name of the crag selected
        # creating a dataframe with the input from dropdown and crag selected
        df_table = df_climb[(df_climb.crag == crag) & (df_climb.year == selected_year)]
        df_table = df_table.query("rating != 0").groupby(['name', 'sector', 'fra_routes']).rating.mean().round(
            1).reset_index()

        df_table.sort_values('rating', ascending=False, inplace=True)
        df_table.rename(columns={'name': 'Route', 'sector': 'Sector', 'fra_routes': 'Grade', 'rating': 'Rating'},
                        inplace=True)

        columns = [{'name': i, 'id': i} for i in df_table.columns]
        table_data = df_table.to_dict('records')

        return columns, table_data


# 4th Callback - Bar chart + Pie Chart
@app.callback(
    Output(component_id='method_dist', component_property='figure'),  # Bar Chart
    Output(component_id='sex_dist', component_property='figure'),  # Pie Chart
    Input(component_id='year', component_property='value'),  # year selected on the dropdown
    Input(component_id='data_table', component_property='derived_virtual_data'),  # data from the table creeated
    Input(component_id='data_table', component_property='derived_virtual_selected_rows'),  # indices of selected rows
    Input(component_id='map_chart', component_property='hoverData'),  # point(crag) selected on the map
    Input(component_id='Total', component_property='value'),  # option selected between map and total of year
)
def style_pie_charts(selected_year, all_rows_data, slctd_rows_indices, hoverdata, total_value):
    dff_table = pd.DataFrame(all_rows_data)  # tranforming the data into a dataframe

    # if no point on the map was selected or no row was selected on the table
    if (hoverdata is None or total_value == 'Overall') and (slctd_rows_indices is None or len(slctd_rows_indices) == 0) :
        # filtering by the selected year
        dff = df_climb[df_climb.year == selected_year]

        # Bar Chart
        fig_method = go.Figure()
        # fig_method.add_traces([go.Bar(x=sorted(dff.method_id.unique()), #sorting by method
        fig_method.add_traces([go.Bar(x=['Redpoint', 'Flash', 'Onsight', 'Top rope', 'Onsight'],  # sorted by method
                                      y=dff.method_id.value_counts()
                                      )])
        fig_method.layout.plot_bgcolor = '#F1F1F1'  # changing the plot background color
        fig_method.layout.paper_bgcolor = '#F1F1F1'  # changing the figure background color
        fig_method.update_traces(marker_color='#EA6A47')
        fig_method.update_xaxes(type='category')
        fig_method.update_layout(margin={"r": 10, "t": 10, "l": 10, "b": 10},
                                 xaxis=dict(showgrid=False, title='Method'),
                                 yaxis=dict(showgrid=False, title='Number of Ascents'))

        # Pie Chart
        fig_sex = go.Figure()
        fig_sex.add_traces([go.Pie(labels=dff.sex.unique(),
                                   values=dff.sex.value_counts()
                                   )])
        fig_sex.layout.plot_bgcolor = '#F1F1F1'  # changing the plot background color
        fig_sex.layout.paper_bgcolor = '#F1F1F1'  # changing the figure background color
        fig_sex.update_traces(marker=dict(colors=['#1C4E80', '#EA6A47']))
        fig_sex.update_layout(margin={"r": 35, "t": 35, "l": 35, "b": 35}, title='Sex')

        return fig_method, fig_sex

    # if a point on the map was selected but no row was selected on the table
    elif hoverdata is not None and total_value != 'Overall' and (slctd_rows_indices is None or len(slctd_rows_indices) == 0):
        crag = hoverdata['points'][0]['customdata']  # extrating the name of the crag selected

        # filtering by the selected year and selected point on the map
        dff = df_climb[(df_climb.crag == crag) & (df_climb.year == selected_year)]

        # Bar Chart
        fig_method = go.Figure()
        # fig_method.add_traces([go.Bar(x=sorted(dff.method_id.unique()),  # sorting by method
        fig_method.add_traces([go.Bar(x=['Redpoint', 'Flash', 'Onsight', 'Top rope', 'Onsight'],  # sorted by method
                                      y=dff.method_id.value_counts()
                                      )])
        fig_method.layout.plot_bgcolor = '#F1F1F1'  # changing the plot background color
        fig_method.layout.paper_bgcolor = '#F1F1F1'  # changing the figure background color
        fig_method.update_traces(marker_color='#EA6A47')
        fig_method.update_xaxes(type='category')
        fig_method.update_layout(margin={"r": 10, "t": 10, "l": 10, "b": 10},
                                 xaxis=dict(showgrid=False, title='Method'),
                                 yaxis=dict(showgrid=False, title='Number of Ascents'))

        # Pie Chart
        fig_sex = go.Figure()
        fig_sex.add_traces([go.Pie(labels=dff.sex.unique(),
                                   values=dff.sex.value_counts()
                                   )])
        fig_sex.layout.plot_bgcolor = '#F1F1F1'  # changing the plot background color
        fig_sex.layout.paper_bgcolor = '#F1F1F1'  # changing the figure background color
        fig_sex.update_traces(marker=dict(colors=['#1C4E80', '#EA6A47']))
        fig_sex.update_layout(margin={"r": 35, "t": 35, "l": 35, "b": 35}, title='Sex')

        return fig_method, fig_sex

    # if a point on the map was selected or not and a  row was selected on the table
    elif (slctd_rows_indices is not None and total_value != 'Overall') or (slctd_rows_indices is not None and total_value == 'Overall') :
        selected_via = dff_table.iloc[slctd_rows_indices[0], 0]  # via selection

        # filtering by the selected year and selected via
        dff = df_climb[(df_climb.name == selected_via) & (df_climb.year == selected_year)]

        # Bar Chart
        fig_method = go.Figure()
        # fig_method.add_traces([go.Bar(x=sorted(dff.method_id.unique()),
        fig_method.add_traces([go.Bar(x=['Redpoint', 'Flash', 'Onsight', 'Top rope', 'Onsight'],
                                      y=dff.method_id.value_counts()
                                      )])
        fig_method.layout.plot_bgcolor = '#F1F1F1'  # changing the plot background color
        fig_method.layout.paper_bgcolor = '#F1F1F1'  # changing the figure background color
        fig_method.update_traces(marker_color='#EA6A47')
        fig_method.update_xaxes(type='category')
        fig_method.update_layout(margin={"r": 10, "t": 10, "l": 10, "b": 10},
                                 xaxis=dict(showgrid=False, title='Method'),
                                 yaxis=dict(showgrid=False, title='Number of Ascents'))

        # Pie Graph
        fig_sex = go.Figure()
        fig_sex.add_traces([go.Pie(labels=dff.sex.unique(),
                                   values=dff.sex.value_counts()
                                   )])
        fig_sex.layout.plot_bgcolor = '#F1F1F1'  # changing the plot background color
        fig_sex.layout.paper_bgcolor = '#F1F1F1'  # changing the figure background color
        fig_sex.update_traces(marker=dict(colors=['#1C4E80', '#EA6A47']))
        fig_sex.update_layout(margin={"r": 35, "t": 35, "l": 35, "b": 35}, title='Sex')

        return fig_method, fig_sex


if __name__ == '__main__':
    app.run_server(debug=True)