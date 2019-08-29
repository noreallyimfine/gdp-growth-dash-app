import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from joblib import load
pipeline = load('assets/pipeline.joblib')

import pandas as pd
X = load('assets/X.joblib')

states = X['State'].unique().tolist()
industry = X['Sub-industry'].unique().tolist()

header = dcc.Markdown('# Predictions', className='mb-5', style={'textAlign':'center', 'textDecoration':'underline'}),
column1 = dbc.Col(
    [
        
           
            dcc.Markdown('### State'),
            dcc.Dropdown(
                id='state',
                placeholder=states[0],
                options = [
                    {'label':val, 'value': val} for val in states
                ],
                value=states[0],
                style={'color':'#2b3e50'}   
            ),

            html.Br(),

            dcc.Markdown('### Past Year Growth Rate'),
            dcc.Slider(
                id='growth_rate',
                marks={
                    -5: '-5%',
                    -2.5: '-2.5%',
                    0: '0%',
                    2.5: '2.5%',
                    5: '5%'
                },
                value=0,
                step=0.01,
                min=-5,
                max=5,
            ),

            html.Br(),

            dcc.Markdown('### 2 Years Ago Payroll Increase'),
            dcc.Slider(
                id='pay_inc',
                min=-1,
                max=1.5,
                marks={
                    -1:'-100%',
                    -0.75: '-75%',
                    -0.5: '-50%',
                    -0.25: '-25%',
                    0: '0%',
                    .25: '25%',
                    .5: '50%',
                    .75: '75%',
                    1: '100%',
                    1.25: '125%',
                    1.5: '150%'
                },
                step=0.01,
                value=.25,
            ),

            html.Br(),

            dcc.Markdown('### Current Percent of 10 Years Ago Payroll'),
            dcc.Slider(
                id='ten_yr_pay',
                min=0,
                max=2,
                marks = {
                    0: '0%',
                    .25: '25%',
                    .50: '50%',
                    .75: '75%',
                    1: '100%',
                    1.25: '125%',
                    1.5: '150%',
                    1.75: '175%',
                    2: '200%',
                },
                value=1,
                step=0.01,
            ),

    ],
    md=6,
)

column2 = dbc.Col(
    [
        dcc.Markdown('### Industry'),
        dcc.Dropdown(
                id='industry',
                placeholder=industry[0],
                options = [
                    {'label':val, 'value': val} for val in industry
                ],
                value=industry[0],
                style={'color':'#2b3e50'},
        ),

        html.Br(),
        html.Br(),

        html.Div(
            [
                html.Div(
                    [
                        dcc.Markdown('### Past Year Total GDP (in millions of USD)'),
                        dcc.Input(
                            id='gdp',
                            type='number',
                            value=1000,
                            min=1,
                            style={'color':'#2b3e50'},
                        ),
                    ],
                    style={'textAlign':'center'}
                ),
            html.Br(), # space out dropdown bars
            html.Div(
                [
                    dcc.Markdown('### Past Year Payroll (in thousands of USD)'),
                    dcc.Input(
                        id='payroll',
                        type='number',
                        value=10000,
                        min=1,
                        style={'color':'#2b3e50'},
                    ),
                ],
                style={'textAlign':'center'}
            ),
            ]
        ),
        html.Br(),
    ],
    md=6,
)

subhead = dbc.Container(
    [

        html.Br(),
        html.Br(),
        html.Br(),
        dcc.Markdown(
            '# Growth Prediction:',
            className='mb-5',
            style={
                'textDecoration':'underline',
                'textAlign':'center'
                }
        ),
    ],
    style={'align':'center'},
)
pred_out = dbc.Col(
    [
        html.Div(
            id='prediction-content',
            className='lead mb-5', 
            style={
                'color': 'black', 
                'background-color':'white',
                'margin':'auto',
                'padding': '6px', 
                'border': '1px inset',
                'fontFamily':'Verdana',
                'textAlign':'center'
                }
        ),
        html.Div(
            id='prediction-image',
            style={
                'paddingBottom':5,
                'textAlign':'center'
                }
        )
    ], 
)

layout = dbc.Container(header), dbc.Row([column1, column2]), subhead, pred_out

@app.callback(
    [Output('prediction-content', 'children'),
    Output('prediction-image', 'children')],
    [Input('state', 'value'),
    Input('growth_rate', 'value'),
    Input('payroll', 'value'),
    Input('gdp', 'value'),
    Input('pay_inc', 'value'),
    Input('industry', 'value'),
    Input('ten_yr_pay', 'value')],
)

def predict(state, growth_rate, payroll, gdp, pay_inc, industry, ten_yr_pay):
    df = pd.DataFrame(
        columns=['State', 'Sub-industry', 'Last Year Payroll', 'Last Year Total GDP',
                'Last Year Growth Rate', '2 Year Ago Payroll Increase', 'Ten Year Payroll Change'],
        data=[[state, industry, payroll, gdp, growth_rate,  pay_inc, ten_yr_pay]]
    )
    
    y_pred = pipeline.predict(df)[0]
    
    if y_pred:
        grow_pred = 'GROW'
        output2 = html.Img(src='/assets/green_up_arrow_plot.png', className='img-fluid')
    else:
        grow_pred = 'NOT GROW'
        output2 = html.Img(src='/assets/red_down_arrow_plot.png', className='img-fluid')
    output1 = f'{industry} in {state} will {grow_pred} this year.'

    return output1, output2