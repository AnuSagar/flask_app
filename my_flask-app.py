import dash
from dash.dependencies import Input, Output,State
import dash_html_components as html
import dash_core_components as dcc
from get_user_status import *
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Textarea(
        id='textarea-example',
        value='Textarea content initialized\nwith multiple lines of text',
        style={'width': '20%', 'height': 100},
    ),
    html.Button(id='submit-button', type='submit', children='Submit'),
    html.Div(id='textarea-example-output', style={'whiteSpace': 'pre-line'}),
     
        
])

@app.callback(
    Output('textarea-example-output', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('textarea-example', 'value')],
)

def update_output(clicks, input_value):
    if clicks is not None:
        text = get_user_add_status(input_value)
        
        return(text)


if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)