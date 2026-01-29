

from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State

app = Dash(__name__)

app.layout = html.Div([
    html.Button('Submit', id='submit-btn'),
    dcc.Input(placeholder="Enter Number", id='data-input', type='number'),
    html.H1(id='results')
])

@app.callback(
    Output('results', 'children'),
    Input('submit-btn', 'n_clicks'),
    State('data-input', 'value')
)
def update_output(n_clicks, data):
    if n_clicks and data is not None:
        return f"You entered: {data}"
    return "Enter a number and click Submit"

if __name__ == '__main__':
    app.run(debug=True)