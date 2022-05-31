import dash
import numpy as np
from dash import dcc, html, dash_table
import pandas as pd
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn import linear_model, tree
import plotly.graph_objects as go

app = dash.Dash()

df = pd.read_csv('DATA/cw11/winequelity.csv')
df_top_5 = df.head(5)


def get_drop_down_items(values: list) -> list:
    dropdown_items = []
    for i in df_top_5.columns:
        if i not in values:
            dropdown_items.append(i)
    return dropdown_items


fnameDict = {
    'Regression': get_drop_down_items(['Unnamed: 0', 'pH']),
    'Classification': get_drop_down_items(['Unnamed: 0'])
}

models = {'Regression': linear_model.LinearRegression,
          'Decision Tree': tree.DecisionTreeRegressor}

names = list(fnameDict.keys())
nestedOptions = fnameDict[names[0]]

app.layout = html.Div(
    [
        html.Div([
            html.P('Select chart type', style={}),
            dcc.Dropdown(
                id='name-dropdown',
                options=[{'label': name, 'value': name} for name in names],
                value=list(fnameDict.keys())[1]
            ),
        ], style={'width': '50%', 'display': 'inline-block'}),
        html.Div([
            html.P('Select values', style={}),
            dcc.Dropdown(
                id='opt-dropdown'
            ),
        ], style={'width': '50%', 'display': 'inline-block'}
        ),
        html.Hr(),
        dash_table.DataTable(
            df_top_5.to_dict('records'),
            [{"name": i, "id": i} for i in df_top_5.columns],
        ),
        dcc.Graph(id="graph"),
    ]
)


@app.callback(
    [dash.dependencies.Output('opt-dropdown', 'options'),
     dash.dependencies.Output('opt-dropdown', 'value')],  # setting default value for second dropdown
    [dash.dependencies.Input('name-dropdown', 'value')]
)
def update_dropdown(name):
    return [{'label': i, 'value': i} for i in fnameDict[name]], fnameDict[name][0]


@app.callback(
    dash.dependencies.Output("graph", "figure"),
    [dash.dependencies.Input('name-dropdown', "value"),  # get input values from both dropdowns
     dash.dependencies.Input('opt-dropdown', "value")]
)
def train_and_display(name, options):
    if name == 'Regression':
        X = df.pH.values[:, None]
        X_train, X_test, y_train, y_test = train_test_split(X, df[options], random_state=10000)

        model = models[name]()
        model.fit(X_train, y_train)

        x_range = np.linspace(X.min(), X.max(), 100)
        y_range = model.predict(x_range.reshape(-1, 1))

        fig = go.Figure([
            go.Scatter(x=X_train.squeeze(), y=y_train,
                       name='train', mode='markers'),
            go.Scatter(x=X_test.squeeze(), y=y_test,
                       name='test', mode='markers'),
            go.Scatter(x=x_range, y=y_range,
                       name='prediction')
        ])
        return fig
    return px.pie(df[['target', options]], values=options, names='target')


if __name__ == '__main__':
    app.run_server(debug=True)
