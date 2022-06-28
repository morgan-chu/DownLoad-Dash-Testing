from dash import Dash, html, dcc, Input, Output, State, callback_context
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

app = Dash(__name__)
df = pd.read_csv("data/SAMPLE_PATIENT_NAMES.csv")
print(df)
app.layout = html.Div([
    html.H1(children='Project DownLoad Data Interface'),

    html.H2(children = 'Room Number', style={}),

    html.Div(id='Room_Number', children=[
        dcc.Dropdown(df.get('Rm_Num'), id='pandas-dropdown-1', clearable = False, value = 1100),
    ], style={'padding': 25,'flex': 1, 'display': 'inline-block', 'width': '20%'}),

    html.Div(id='Patient_Name', style={'padding': 0, 'flex': 1, 'display': 'inline-block', 'width': '40%', 'text-align': 'center'}),
])

@app.callback(
    Output('Patient_Name', 'children'),
    Input('pandas-dropdown-1', 'value')
)
def update_output(value):
    return f'Patient Name: {df.at[value-1100, "Patient_Name"]}'

if __name__ == '__main__':
    app.run_server(debug=True)