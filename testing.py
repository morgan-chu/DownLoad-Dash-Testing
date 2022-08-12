from dash import Dash, html, dcc, Input, Output, dash_table
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output


#TODO: Running total of total volume, chart of time and urine amount, Time of last urination, cumulative plot(maybe)
#TODO: Big right sidebar with numerical values

app = Dash(__name__)
df = pd.read_csv("data/SAMPLE_PATIENT_NAMES.csv")
print(df)
app.layout = html.Div([
    html.H1(children='Project DownLoad Data Interface'),

    

    html.Div(id='Room_Number', children=[
        html.H2(children = 'Room Number', style={'text-align': 'left', 'margin-left' : '15px', 'margin-bottom' : '0px'}),
        dcc.Dropdown(df.get('Rm_Num'), id='Rm-Number', clearable = False, value = 1100, style ={'margin-left' : '7.5px'}),
    ], style={'flex': 1, 'display': 'inline-block', 'width': '20%', "verticalAlign": "top"}),

    html.Div(id='Patient_Name_Group', children = [
        html.H3(id = "Patient_Name"),
    ], style={'margin-bottom': "15px", 'flex': 1, 'display': 'inline-block', 'width': '25%', 'text-align': 'center', "verticalAlign": "bottom", 'margin-left' : '135px'}),

    html.Div(id='Current_Vol_Group', children = [
        html.H3(id = "tot_Vol"),
    ], style={'margin-bottom': "15px", 'flex': 1, 'display': 'inline-block', 'width': '25%', 'text-align': 'center', "verticalAlign": "bottom", 'margin-left' : '-114px'}),

    html.Div(id = 'Graph_Group', children = [
        dcc.Graph(id='indicator-graphic'),
        dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0
        )
    ], style={'padding': '15px', 'display': 'inline-block', 'width':'45%'}),

    html.Div(id='vol_table_group', children = [
        html.Label(children = "Table of Urine Volumes", style={'margin-bottom': '10px'}),
        html.Table(id = 'urine-vol-table'),
    ], style={'padding': '15px', 'display': 'inline-block', 'width':'40%', 'vertical-align': 'top'}),
])

@app.callback(
    Output('Patient_Name', 'children'),
    Input('Rm-Number', 'value'),
    Input('interval-component', 'n_intervals')
)
def update_output(value, intervals):
    return f'Patient Name: {df.at[value-1100, "Patient_Name"]}'

@app.callback(
    Output('tot_Vol', 'children'),
    Input('Rm-Number', 'value'),    
    Input('interval-component', 'n_intervals')
)
def update_output(rm_number, intervals):
    df = pd.read_csv("data/" + str(rm_number) + ".csv")
    dff = df['Volume(mL)']
    sum = 0
    for val in dff:
        sum += val
    return f'Total Urine Volume: {str(sum)} mL'

@app.callback(
    Output('indicator-graphic', 'figure'),
    Input('Rm-Number', 'value'), 
    Input('interval-component', 'n_intervals')
)
def update_graph(rm_number, intervals):
    df = pd.read_csv("data/" + str(rm_number) + ".csv")
    fig = px.line(df, x= "Time", y = "Volume(mL)", markers = True)
    fig.update_layout(title_text='Urine Volume Over Time', title_x=0.5)

    return fig

@app.callback(
    Output('urine-vol-table', 'children'),
    Input('Rm-Number', 'value'), 
    Input('interval-component', 'n_intervals')
)
def generate_table(rm_number, intervals, max_rows=10):
    dataframe = pd.read_csv("data/" + str(rm_number) + ".csv")
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
            )
        ,
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])


if __name__ == '__main__':
    app.run_server(debug=True)