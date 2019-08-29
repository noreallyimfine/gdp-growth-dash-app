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

header = dcc.Markdown('# Predictions', className='mb-5', style={'textAlign':'center'}),
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

                

            
            
    ],
    md=4,
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
        ),

        html.Br(),

        html.Div([
            html.Div([
            dcc.Markdown('### Past Year Total GDP (in millions of USD)'),
            dcc.Input(
                id='gdp',
                type='number',
                placeholder=2800,
                value=2800,
                min=0,
                max=10000,
            ),
            ]),
            html.Div([
            dcc.Markdown('### Past Year Payroll (in thousands of USD)'),
            dcc.Input(
                id='payroll',
                type='number',
                placeholder=1300000,
                value=1300000,
                min=0,
                max=1000000000
            ),
            ]),
        ]),

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
    
)

pred_out = dbc.Row(
    [
        html.H2('Growth Prediction:', className='mb-5', style={'position':'relative'}),
        html.Br(),
        html.Br(),
        html.Div(id='prediction-content',
                className='lead', 
                style={'position':'fixed', 'right':50, 'border': '1px solid #2b3e50'}),
    ]
)

@app.callback(
    Output('prediction-content', 'children'),
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
    else:
        grow_pred = 'NOT GROW'

    return f'{industry} in {state} will {grow_pred} this year.'

layout = dbc.Container(header), dbc.Row([column1, column2]), pred_out