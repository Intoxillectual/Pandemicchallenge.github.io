import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import plotly.io as pio

df = pd.read_csv("/home/stuti/covid-xprize/pred1.csv")
dff = pd.read_csv("/home/stuti/covid-xprize/pres1.csv")
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

available_indicators = df['CountryName'].unique()

app.layout = html.Div([
    dcc.Graph(id='indicator-graphic'),
    dcc.Graph(id='prescriptor-graphic'),
    dcc.Dropdown(
        id='Country-slider',
        #min=df['year'].min(),
        #max=df['year'].max(),
        value='Aruba',
        options=[{'label': i, 'value': i} for i in available_indicators],
        #step=None
    )
    
],
style={'width': '48%', 'display': 'inline-block'}

)


@app.callback(
    Output('indicator-graphic', 'figure'),
    Output('prescriptor-graphic', 'figure'),
    Input('Country-slider', 'value'))
def update_figure(selected_year):
    filtered_df = df[df.CountryName == selected_year]
    filters = dff[dff.CountryName == selected_year]

    fig = px.scatter(filtered_df, x="PredictedDailyNewCases", y="Date")

    fig.update_layout(title = 'AIs Predicted New Cases Per Day',transition_duration=500)
    #figure = px.bar(filters, x="Date", y=[trace1, trace2])
    #figure = px.bar(filters, x="Date", y="C1_School closing")#','C2_Workplace closing','C3_Cancel public events'])
    figure = px.bar(filters, x="Date", y=["C1_School closing","C2_Workplace closing", "C3_Cancel public events","C4_Restrictions on gatherings","C5_Close public transport","C6_Stay at home requirements","C7_Restrictions on internal movement","C8_International travel controls","H1_Public information campaigns","H2_Testing policy","H3_Contact tracing","H6_Facial Coverings"])
    #figure = px.bar(filters, x="Date", y="C2_Workplace closing")#,'C3_Cancel public events'])
    figure.update_layout(title = 'AIs Suggested NPI Timeline Series',transition_duration=500)
    pio.write_html(fig, file='index.html', auto_open=True)
    return fig, figure


if __name__ == '__main__':
    app.run_server(debug=True)
