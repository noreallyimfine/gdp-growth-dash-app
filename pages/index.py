import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

from app import app

"""
https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout

Layout in Bootstrap is controlled using the grid system. The Bootstrap grid has 
twelve columns.

There are three main layout components in dash-bootstrap-components: Container, 
Row, and Col.

The layout of your app should be built as a series of rows of columns.

We set md=4 indicating that on a 'medium' sized or larger screen each column 
should take up a third of the width. Since we don't specify behaviour on 
smaller size screens Bootstrap will allow the rows to wrap so as not to squash 
the content.
"""

column1 = dbc.Col(
    [
        dcc.Markdown(
            """

            ## Predict GDP Growth by Industry

            While GDP ([Gross Domestic Product](https://en.wikipedia.org/wiki/Gross_domestic_product)) is most commonly talked about on a national scale,
             a more fine-grained approach can be very informative. 

            The **Grow or Contract** app looks at the industries within each state and predicts how they will do individually.

            This approach allows you to keep your finger on the pulse of, not just the economy as a whole, but the specific industries relevant to you.

            """
        ),
        dcc.Link(dbc.Button('Find a Prediction', color='primary'), href='/predictions')
    ],
    md=4,
)

column2 = dbc.Col(
    [
        html.Img(src='assets/gdp_image.jpg', className='img-fluid max-width: 50%'),
    ]
)

layout = dbc.Row([column1, column2])