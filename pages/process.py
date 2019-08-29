import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app

header = dbc.Col(
            dcc.Markdown(
                '# Process', 
                className='mb-5', 
                style={
                    'textAlign': 'center', 
                    'textDecoration': 'underline'
                }
            )
)
column1 = dbc.Col(
    [
        dcc.Markdown(
            """  

            #### Gathering Data  

            For this project I got data from the [Bureau of Economic Analysis](https://www.bea.gov/data/economic-accounts/industry).
            The data came as 9 different datasets. Each dataset was one economic measure over time. There was data on 91 industries over the 50 states,
            plus a few aggregations of regions and the country as a whole.  
            """
        ),
        html.Img(src='assets/df_2.png',
                className='img-fluid', 
        ),
        html.Br(),
        html.Br(),
        dcc.Markdown(
            """ 
              
            ### Cleaning Data

            Cleaning the data turned out to be a bit tricky because each dataset had labeled missing values differently. I was able to find the labels 
            by noticing the numeric columns had an object datatype and trying to change them to numeric would throw an error. Looking at all the values 
            in the column, I could find the ones that weren't numbers and replace them with NaNs to be dealt with.    

            To fill the NaN values, I used the data from the previous or following year as that would represent the closest I could get to the real
            value. Using mean or median of the column, a standard practice for filling NaNs would not have worked due to the vastly different sizes
            of industries in different places. 

            #### Wrangling Data

            Each dataset had a bunch of descriptive columns. Some, such as GeoName (State) and Description (Industry) were crucial.
            Others, like GeoFIPS, Region, and IndustryId were redundant. Component Name and Unit were important but not useful in the current form.

            The actual data columns were just named with the year. Since each dataset had this same structure, I needed to rename the data columns so
            the information in them would be retained through a merge. 

            I used the component name information and tacked that on to the year in the column names so each column now had both a year and an economic
            component being measured.  
            """
        ),
        html.Div(
            html.Img(
                src='assets/merged_df_example.png',
                    className='img-fluid', 
            ),
            style={'textAlign':'center'}
        ),
        html.Br(),
        dcc.Markdown(
            """
            At this point I had my single dataset with all the important information preserved but I wasn't done yet.

            The data I have is essentially time-series data. The order of the years matters. However that won't be captured by the computer looking
            at the data. 

            To bring to life the time component of this data I created some new features that measured changes over time. One feature that proved
            particularly useful for my model was how much Payroll increased year-over-year.

            ### Modeling

            Before beginning to build and iterate on a model, I needed to decide what the target would be. Although the dataset came with a feature
            for the growth rate of an industry in a given year, I decided to alter it and aim for predicting whether or not the industry would grow
            in the coming year. I created a column that was True/False if the industry had grown, and the latest year of data I had was the target.
            (If an industry had a 0% growth rate I counted that as False)

            I split off and held out a test set, only manipulating it to engineer the same features as I did for the training set. The baseline model
            to beat was 60%, being the accuracy you would get if you just guessed every industry in every state would **grow**. If my model couldn't do
            significantly better than that, it wouldn't be very useful.
            
            I used both a 3-way split and [cross-validation](https://jakevdp.github.io/PythonDataScienceHandbook/05.03-hyperparameters-and-model-validation.html)
            to iterate on my model. The 3-way split I used for trying new model types and cross-validation I used for tuning the hyperparameters.

            Right away I saw improvements over the baseline and it was the case here that more complex models did better. For the final
            model I used all the features from the two previous years as well as the features I had engineered (which incorporated older
            information as well). The best model for this problem was sciki-learn's [GradientBoostingClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.GradientBoostingClassifier.html)
            and, with the right hyperparameters, I got an accuracy score of nearly 80%.  
            """

        ), 
        html.Div(
            html.Img(
                src='assets/final_test_accuracy.png', className='img-fluid',
                style={
                    'height': '50%',
                    'width': '50%'
                }
            ), 
            style={'textAlign': 'center'}
        ),
        html.Br(),
        dcc.Markdown(
            """
            In the bar plot below, we can see the 10 most important features in the model. To get a better sense of how different values
            for each feature affect individual predictions, head over to [Insights](/insights) to zoom in on a few interesting predictions.
            Or you can go to [Predictions](/predictions) to tune the features yourself and see what the model predicts!  
            """
        ),
        html.Div(
            html.Img(
                src='assets/feat_imps_label.png', 
                className='img-fluid'
            ),
            style={'textAlign': 'center'}
        ),
    ],
)

layout = header, dbc.Row([column1])