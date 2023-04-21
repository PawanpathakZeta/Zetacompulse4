import streamlit as st
import pandas as pd
import numpy as np   
from matplotlib import pyplot as plt
import altair as alt
from PIL import Image
from vega_datasets import data
import calendar as cal
# import urban_theme # where the color theme i
source = data.seattle_weather()
source['date'] = source['date'].dt.month
source.loc[source["date"] == 1, "date"] = "Automotive"
source.loc[source["date"] == 2, "date"] = "Business"
source.loc[source["date"] == 3, "date"] = "Education"
source.loc[source["date"] == 4, "date"] = "Entertainment"
source.loc[source["date"] == 5, "date"] = "Health"
source.loc[source["date"] == 6, "date"] = "Home"
source.loc[source["date"] == 7, "date"] = "Humanities"
source.loc[source["date"] == 8, "date"] = "Life Events"
source.loc[source["date"] == 9, "date"] = "Recreation"
source.loc[source["date"] == 10, "date"] = "Science"
source.loc[source["date"] == 11, "date"] = "Society"
source.loc[source["date"] == 12, "date"] = "Technology"
source = source[(source.weather.isin(['drizzle','fog', 'rain', 'sun']))]
source.loc[source["weather"] == "drizzle", "weather"] = "Q1"
source.loc[source["weather"] == "fog" , "weather"] = "Q2"
source.loc[source["weather"] ==  "rain" , "weather"] = "Q3"
source.loc[source["weather"] ==  "sun", "weather"] = "Q4"
bars1 = alt.Chart(source ,title= "Quarterly Categorical Comsumption -> from vega_data set but then modifiyin gvalues and col names").mark_bar(
    cornerRadiusTopLeft=3,
    cornerRadiusTopRight=3
).encode(
    x=alt.X('date:N', axis=alt.Axis(labelAngle=-48), title=None),
    y= alt.Y('count():Q', ),
    color=alt.Color('weather:N',legend=alt.Legend(title="Quarter") )
).properties(
width=850 # controls width of bar.
, height=445  # height of the table
)
# ​
source2 =pd.read_csv('bubble_chart.csv')
hist2 =alt.Chart(source2.dropna(), title='Price Sensitivity Scores .. -> from csv "bubble_chart.csv" ').mark_circle(color="#0905AF").encode(
    alt.X('Income bins:O', bin=True, axis=alt.Axis(title='Income bins(K)')),
    alt.Y('Age:O', bin=True, sort="descending",  axis=alt.Axis(title="Age bins")),
    size='Price sensitivity scores:Q'
).properties(
width=850 # controls width of bar.
, height=445 # height of the table
)
# ​
source3 = data.movies.url
# ​
hist3= alt.Chart(source3, title="from vega_data set ").mark_circle().encode(
    alt.X('IMDB_Rating:Q', bin=True),
    alt.Y('Rotten_Tomatoes_Rating:Q', bin=True),
    size='count()'
).properties(
width=850 # controls width of bar.
, height=445  # height of the table
)
# ​
# ​
# ​
source4 =pd.read_csv('bubble_chart.csv')
hist4 =alt.Chart(source4, title='Zeta-scores across Age and income Bands -> from csv "bubble_chart.csv"  same code as the avoble chart').mark_circle(color="#0905AF").encode(
    alt.X('IMDB_Rating', bin=True ),
    alt.Y('Rotten_Tomatoes_Rating',bin=True ),
    size='count()'
).properties(
width=850 # controls width of bar.
, height=445  # height of the table
)
# ​
source5 =pd.read_csv('bubble_chart.csv')
hist5 =alt.Chart(source5, title='Price Sensitivity Scores Across Age and Income Band -> from csv "bubble_chart.csv"').mark_circle(color="#0905AF").encode(
    alt.X('IMDB_Rating', bin=True, ),
    alt.Y('Rotten_Tomatoes_Rating', bin=True,),
    size='count()'
).properties(
width=850 # controls width of bar.
, height=445  # height of the table
)
# ​
# ​
#alt.vconcat(bars4, hist6)
st.set_page_config(layout="wide")
# ​
col1, col2 , col3 = st.columns([7,1,7])
# ​
with col1:
    st.header("  ")
    bars1
    st.header("  ")
    hist2
    st.header("  ")
    hist3
    st.header("  ")
    #hist4
    st.header("  ")
    hist5
    st.header("  ")