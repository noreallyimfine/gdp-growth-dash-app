import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app

header = dbc.Row(
    dcc.Markdown(
        """  
        # Insights


        While machine learning models have a reputation of being **black boxes**,
        for some models it is possible to peek inside and see how the conclusion was
        reached. 

        In the first section, we look at what factors were most important to the model.
        Then we'll dive into a few particularly interesting decisions and analyze how 
        the model did. As an aside, **this analysis is done on a more complex version of
        the model than seen in the predictions page**. For information on the process of
        building this model, check out the [Process](/process) page.

            
       """
    ),
)

column1 = dbc.Col(
    [
        html.Br(),
        dcc.Markdown(
            '''
            The Partial Dependence Plot Interaction on the right shows the cross-section of GDP and Payroll.
            The lighter the color, the more confident the model is that the industry will grow. When GDP and
            Payroll are the highest, in the top right part of the graph, the model is most confident that the
            industry will grow.  

            One interesting thing to note is how Payroll is having a larger effect than GDP. All the puple is
            on the bottom, where Payroll is at its' lowest. In contrast even where GDP is very low, with just
            average Payroll, the model is significantly more confident in the growth of the industry.
            ''',
            style={'margin':50}
        ),
    ],
    md=6,
    style={'textAlign':'center'},
)

column2 = dbc.Col(
    [
        html.Br(),
        html.Img(
            src='assets/gdp_payroll_interact.png', 
            className='img-fluid', 
            style={'margin':20}
        )
    ],
    md=6,
    style={'textAlign':'center'},
)

insight1 = dbc.Row(
    [
        html.Br(),
        dcc.Markdown(
            '''
            In the plot below we zoom in on an individual prediction the model made. This is
            **Management of Companies and Enterprises in West Virginia**. This plot shows how
            much each factor pushed the model, in what direction, and the final prediction
            the model made. The red bars represent movement in the direction of predicting growth,
            the blue bars represent movement against. The first tick on the right of where the bars
            meet is where it starts off. On average, more industries grew than not, and the model takes
            that into account.

            For this industry, the biggest factor moving the model towards predicting no growth was
            a Surplus Increase of 0 from the previous year. Other significant factors include having
            a Quant Index score below the Base Index of 100, and the Payroll Size having shrunk in the
            past 5 years. On the other side, the specific Industry that it is, Management of Companies 
            and Enterprises, was the 1st and 3rd largest factors pushing the model towards predicting
            growth. Sandwiched between that was a Payroll to Tax ratio of 30:1.

            Ultimately, in a very close call, the model predicted this industry would grow, and it was correct!
            '''
        ),
        html.Br(),
        html.Img(
            src='assets/shaply_wv_man_of_comp_just_right.png',
            className='img-fluid'
        ),
    ]
)

insight2 = dbc.Row(
    [
        html.Br(),
        dcc.Markdown(
            '''
            Here, we look at a prediction that was also very close but this one the model got **wrong**.  

            Once again we have a low Quant Index and a Surplus Increase of 0, along with a few Tax related
            factors. Just like in the first instance, however, these did not outweigh the Industry, current
            GDP to Tax ratio, and Payroll Size.  

            This one was even closer for the model, but it did again predict that **Manufacturing in Kentucky**
            would grow. This time it was **wrong**.

            '''
        ),
        html.Br(),
        html.Img(
            src='assets/shaply_kentucky_manufa_just_wrong.png', 
            className='img-fluid'
        ),
    ]
)
layout = header, dbc.Row([column1, column2]), insight1, insight2