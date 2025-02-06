import os
from dotenv import load_dotenv
import dash
from dash import dcc, html, Input, Output
import argparse
from constants import RESET_PROMPT_FNAME

load_dotenv()

app = dash.Dash(__name__)


# Function to read and sort text files
def get_sorted_text_files():
    files = [f for f in os.listdir(args.folder) if f.endswith('.txt')]
    files.sort()
    return files


# Function to read the content of the text files and create a list of Divs
def read_text_files():
    divs = []
    for file in get_sorted_text_files():
        with open(os.path.join(args.folder, file), 'r') as f:
            content = f.read()
            divs.append(html.Div([
                html.H3(file),
                html.P(content, style={'whiteSpace': 'pre-wrap'})
            ]))
    return divs


# Layout of the Dash app
app.layout = html.Div([
    html.H1("Text File Viewer"),
    html.Div(id='text-content'),
    dcc.Interval(
        id='interval-component',
        interval=1*1000,  # Update every second
        n_intervals=0
    ),
    html.Button('Reset prompt', id='save-button', n_clicks=0, style={'marginTop': '20px'})
])


# Callback to update the text content
@app.callback(
    Output('text-content', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_text(n):
    return read_text_files()


@app.callback(
    Output('save-button', 'n_clicks'),
    Input('save-button', 'n_clicks'),
    prevent_initial_call=True
)
def save_file_to_reset_prompt(n_clicks):
    file_path = os.path.join(args.folder, RESET_PROMPT_FNAME)
    with open(file_path, 'w') as f:
        f.write("Reset prompt")
    return n_clicks


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder', type=str)
    args = parser.parse_args()
    app.run_server(debug=False)
