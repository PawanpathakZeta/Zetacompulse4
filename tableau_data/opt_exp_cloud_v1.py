# Import libraries
import streamlit as st
import pandas as pd
import numpy as np   
from matplotlib import pyplot as plt
import snowflake.connector as sf
from snowflake.connector.pandas_tools import write_pandas
import altair as alt
from PIL import Image
from vega_datasets import data
import calendar as cal


st.set_page_config(layout="wide", page_title='ZMP-Opportunity Explorer Streamlit app')
base="light"
primaryColor="#BF2A7C" #PINK
backgroundColor="#FFFFFF" #MAIN WINDOW BACKGROUND COLOR (white)
secondaryBackgroundColor="#EBF3FC" #SIDEBAR COLOR (light blue)
textColor="#31333F"
secondaryColor="#F0F2F6" #dark_blue
tertiaryColor ="#0810A6"
light_pink = "#CDC9FA"
plot_blue_colour="#0810A6" #vibrant blue for plots


#to put everything into one page, to avoide scrolling:
padding = 0
st.markdown(f""" <style>
    .reportview-container .main .block-container{{
        padding-top: {padding}rem;
        padding-right: {padding}rem;
        padding-left: {padding}rem;
        padding-bottom: {padding}rem;
    }} </style> """, unsafe_allow_html=True)

# 1- Layout settings

##Main Page
# Creating columns 1 and 2    -> This is for the main "page" not the side bar. 
col1, col2 = st.columns([13, 2])

## Header
col1.title('Zeta Oportunity Explorer: Demo')
"""This app is a demo project for ZMP's Oportunity Explorer dashboard"""

## Zeta Logo
#zeta_logo = Image.open('ZETA_BIG-99e027c9.webp') #white logo 
zeta_logo = Image.open('ZETA_BIG-99e027c92.png') #blue logo 
col2.image(zeta_logo)


#Radial Graph  -> omnichannel reach

#omni_channel_reach = pd.read_csv('tableau_data/Omni-Channel Reach.csv', encoding='utf_16', sep = "\t" )
#omni_channel_reach = omni_channel_reach.transpose()
#omni_channel_reach.reset_index()
#new_header = omni_channel_reach.iloc[0] #grab the first row for the header
#omni_channel_reach = omni_channel_reach[1:] #take the data less the header row
#omni_channel_reach.columns = new_header #set the header row as the df header#
#base = alt.Chart(omni_channel_reach).encode(
#    theta=alt.Theta("values:Q", stack=True),
#   radius=alt.Radius("values", scale=alt.Scale(type="sqrt", zero=True, rangeMin=20)),
#    color="index:N",
#)
#c1 = base.mark_arc(innerRadius=20, stroke="#fff")
#c2 = base.mark_text(radiusOffset=10).encode(text="values:Q")
#c1 + c2


# 1. Pie chart
match_rate = pd.DataFrame({"Field": ['Match Rate', 'Match Rate']
                                ,"Field metric": ['Matched to Data Cloud', 'Not Matched to Data Cloud']
                                ,"Percent" :[0.65, 0.35]
                                ,"Value": [65, 35]})

pie1 = alt.Chart(match_rate).encode(
    theta=alt.Theta("Value:Q", stack=True),
    color=alt.Color("Field metric:N",  scale=alt.Scale(scheme='accent')),
)
pie = pie1.mark_arc(outerRadius=120)
text = pie1.mark_text(radius=140, size=20, color='white').encode(
    text=alt.Text("Percent:Q", format='.0%',  )
) 

graph1= (pie+text)

# 2. Simple Bar chart
data_signal_matches = pd.DataFrame({"Field": ['Data Signal Matches', 'Data Signal Matches', 'Data Signal Matches', 'Data Signal Matches', 'Data Signal Matches']
                                ,"Field metric": ['Transactional', 'Location', 'Behavioral', 'Professional', 'Credit Bureau']
                                ,"Percent" :[0.93, 0.87, 0.84, 0.96, 0.75  ]
                                ,"Value": [70, 65, 63, 72, 56]})

bars2 = alt.Chart(data_signal_matches).transform_joinaggregate(
    TotalValue='sum(Value)',
).transform_calculate(
    PercentOfTotal="datum.Value / datum.TotalValue"
).mark_bar(size = 70).encode(
alt.X('Field metric:N', axis=alt.Axis(labelAngle=0)),
alt.Y('PercentOfTotal:Q', axis=alt.Axis(format='.0%', title='Match Count')),
alt.Color("Field metric:N",  scale=alt.Scale(scheme='accent'))
).properties(
width=800 # controls width of bar.
    #, height=500  # height of the table
)
text2 = bars2.mark_text(
    align='center',
    baseline='middle',
    dx=0,dy=-10, # Nudges text to right so it doesn't appear on top of the bar
    size =20
).encode(
    alt.Text('PercentOfTotal:Q',
    format ='.0%')
)

graph2 = (bars2+text2)

# 3. Stacked Bar Chart with Text Overlay
source1=data.barley()
source1.loc[source1["site"] == "Crookston", "site"] = "Male"
source1.loc[source1["site"] == "Duluth", "site"] = "Male"
source1.loc[source1["site"] == "Grand Rapids", "site"] = "Male"
source1.loc[source1["site"] == "Morris", "site"] = "Female"
source1.loc[source1["site"] == "University Farm", "site"] = "Female"
source1.loc[source1["site"] == "Waseca", "site"] = "Female"
source1 = source1[(source1.variety.isin(['Svansota','Velvet', 'Glabron', 'Peatland']))]
source1.loc[source1["variety"] == "Svansota", "variety"] = "Customer site visitors"
source1.loc[source1["variety"] == "Velvet", "variety"] = "Customer non-site visitors"
source1.loc[source1["variety"] == "Glabron", "variety"] = "Zeta per. site visitors"
source1.loc[source1["variety"] == "Peatland", "variety"] = "Zeta non-per. site visitors"

bars3 = alt.Chart(source1).mark_bar().encode(
    x=alt.X('sum(yield):Q', stack='zero'),
    y=alt.Y('variety:N'),
    color=alt.Color('site', scale=alt.Scale(scheme='accent'))
)

text3 = alt.Chart(source1).mark_text(dx=-15, dy=3, color='white').encode(
    x=alt.X('sum(yield):Q', stack='zero'),
    y=alt.Y('variety:N'),
    detail='site:N',
    text=alt.Text('sum(yield):Q', format='.0f')
)

graph3 = (bars3 + text3).properties(
width=800 # controls width of bar.
,height=375  # height of the table
)



# 4. Bar Chart with Rounded Edges
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

bars4 = alt.Chart(source).mark_bar(
    cornerRadiusTopLeft=3,
    cornerRadiusTopRight=3
).encode(
    x='date:N',
    y='count():Q',
    color=alt.Color('weather:N',  scale=alt.Scale(scheme='accent'))
).properties(
width=800 # controls width of bar.
    #, height=500  # height of the table
)

graph4 = bars4

# 5. Streamgraph with Interactive Legend
source = data.unemployment_across_industries.url

#selection = alt.selection_point(fields=['series'], bind='legend')

stream5 = alt.Chart(source).mark_area().encode(
    alt.X('yearmonth(date):T', axis=alt.Axis(domain=False, format='%Y', tickSize=0)),
    alt.Y('sum(count):Q', stack='center', axis=None),
    alt.Color('series:N', scale=alt.Scale(scheme='accent')),
    #opacity=alt.condition(selection, alt.value(1), alt.value(0.2))
).properties(
width=800 # controls width of bar.
    #, height=500  # height of the table
)
#.add_params(
#    selection
#)

graph5 = stream5

# 6. 2D Histogram Scatter Plot
source = data.movies.url

hist6 =alt.Chart(source).mark_circle(color="#7fc97f" ).encode(
    alt.X('IMDB_Rating:Q', bin=True),
    alt.Y('Rotten_Tomatoes_Rating:Q', bin=True),
    size='count()'
).properties(
width=800 # controls width of bar.
    #, height=500  # height of the table
)

graph6 =hist6 

# 7. Radial chart
source = pd.DataFrame({"values": [12, 23, 47, 6, 52, 19]})

base = alt.Chart(source).encode(
    theta=alt.Theta("values:Q", stack=True),
    radius=alt.Radius("values", scale=alt.Scale(type="sqrt", zero=True, rangeMin=20)),
    color=alt.Color("values:N", scale=alt.Scale(scheme='accent')),
)

c1 = base.mark_arc(innerRadius=20, stroke="#fff")

c2 = base.mark_text(radiusOffset=10).encode(text="values:Q")

graph7= (c1 + c2)

omni_channel_reach = pd.DataFrame({"Field": ['omni-chnnel','omni-chnnel', 'omni-chnnel' , 'omni-chnnel']
                                   ,"Field metric": ['Email', 'Programmatic', 'Social', 'Direct Mail']
                                   , "Value": [40, 50, 30, 20] 
                                   , 'Percent' :[0.4,0.5,0.3,0.2]})

base2 = alt.Chart(omni_channel_reach).encode(
    theta=alt.Theta("Value:Q", stack=True),
    radius=alt.Radius("Value", scale=alt.Scale(type="sqrt", zero=True, rangeMin=20)),
    color= alt.Color("Field metric:N", scale=alt.Scale(scheme='accent'))
)

c3 = base2.mark_arc(innerRadius=20, stroke="#fff")

c4 = base2.mark_text(radiusOffset=50, size=25).encode(alt.Text ("Percent:Q", format ='.0%'))

graph7a =(c3+c4)

# 8. Simple Bar chart
match_breakdown = pd.DataFrame({"Field": ['Match Breakdown', 'Match Breakdown', 'Match Breakdown']
                                ,"Field metric": ["Email","Full Name + Full Postal", "Phone"]
                                ,"Percent" :[0.6, 0.5, 0.4]
                                ,"Value": [60, 50, 40]})
bars8 = alt.Chart(match_breakdown).mark_bar(size=70).encode(
        x= alt.X('Field metric:N',axis=alt.Axis(labelAngle=0)),
        y=alt.Y('Value:Q', axis=alt.Axis(title='Match Count')),
        color= alt.Color("Field metric:N",  scale=alt.Scale(scheme='accent'))
        ).properties(
    width=900 # size controls width of bar. and width allocates for each bar in the chart the width
    #, height=500  # height of the table
)
text8 = bars8.mark_text(
    align='center',
    baseline='middle',
    dx=0,dy=-10, # Nudges text to right so it doesn't appear on top of the bar
    size = 20
).encode(
    text=alt.Text('Percent:Q', format='.0%')
)

graph8 = (bars8 +text8)

# 9. Hexbin chart
size =40
xFeaturesCount = 12
yFeaturesCount = 7
xField = 'date'
yField = 'date'

# the shape of a hexagon
hexagon = "M0,-2.3094010768L2,-1.1547005384 2,1.1547005384 0,2.3094010768 -2,1.1547005384 -2,-1.1547005384Z"

las_click_date =  pd.read_csv('tableau_data/las_click_date.csv')#, encoding='utf_16', sep = "\t" 

las_click_day =  pd.read_csv('tableau_data/las_click_day.csv')#, encoding='utf_16', sep = "\t" 

click_count =  pd.read_csv('tableau_data/click_count.csv')#, encoding='utf_16', sep = "\t" 

source = result = pd.concat([las_click_date, las_click_day,click_count ], axis=1)
source = source[['LAST_CLICK_DATE', 'LAST_CLICK_DAY', 'CLICK_COUNT']]
source["month_name"] = source["LAST_CLICK_DATE"].apply(lambda x: cal.month_name[x] )

##, labelExpr = ( " datum.LAST_CLICK_DATE == 1 ? 'Jan' : datum.LAST_CLICK_DATE == 2 ? 'Feb'     : datum.LAST_CLICK_DATE == 3 ? 'Mar'    : datum.LAST_CLICK_DATE == 4 ? 'Apr'    : datum.LAST_CLICK_DATE == 5 ? 'May'     : datum.LAST_CLICK_DATE == 6 ? 'Jun'     : datum.LAST_CLICK_DATE == 7 ? 'Jul' : datum.LAST_CLICK_DATE == 8 ? 'Aug'     : datum.LAST_CLICK_DATE == 9 ? 'Sep'     : datum.LAST_CLICK_DATE == 10 ? 'Oct'     : datum.LAST_CLICK_DATE == 11 ? 'Nov' :  'Dec' ")

hexbin= alt.Chart(source).mark_point(size=size*(size/2), shape=hexagon).encode(
    x=alt.X('xFeaturePos:N', axis=alt.Axis(title='Month', grid=False, tickOpacity=10, domainOpacity=10 
                                           
                                           , values=(1, 2,3,4,5,6,7,8,9,10,11,12)
                                           ,labelAngle= 0)),
    y=alt.Y('LAST_CLICK_DAY:O', axis=alt.Axis(title='Day of the week', labelPadding=20, tickOpacity=0, domainOpacity=0)),
    stroke=alt.value('black'),
    strokeWidth=alt.value(0.2),
    fill=alt.Color('mean(CLICK_COUNT):Q', scale=alt.Scale(scheme='accent')),
    tooltip=['month_name:O', 'LAST_CLICK_DAY:O', 'mean(CLICK_COUNT):Q']
).transform_calculate(
    # This field is required for the hexagonal X-Offset
    xFeaturePos='( datum.LAST_CLICK_DAY % 2) / 2 + datum.LAST_CLICK_DATE'
    
).properties(
    # Exact scaling factors to make the hexbins fit
    width=size * xFeaturesCount * 2,
    height=size * yFeaturesCount * 1.7320508076,  # 1.7320508076 is approx. sin(60°)*2
).configure_view(
    strokeWidth=0
)

graph9 = hexbin


#Stacked BARS -> category of Consumptions

# 10. Layered Area chart - Transactional categories from tableua  change the colomns "series" from eg data to the categories from transactional 
layer_df =pd.read_csv('tableau_data/Layered_graph.csv')

layered10 =alt.Chart(layer_df).mark_area().encode(
    x="MONTH:O",
    y=alt.Y("sum(count):Q"),
    color=alt.Color("action:N", scale=alt.Scale(scheme='accent'), sort=['OPENS','CLICKS'])
).properties(
    height=500 
    ,width= 1000
)

graph10 = layered10

# 11. Predictions graph 










#######################
#Visualization#


#graph1 | graph2
#graph3 | graph4
#graph5 | graph6
#graph7 | graph8
#graph9 | graph10
#graph11 | graph12

#graph1
#graph2
#graph3 
#graph4
#graph5 
#graph6
#graph7 
#graph8
#graph9 
#graph10

col1, col2 = st.columns(2)

with col1:
    st.altair_chart(graph1, use_container_width=True)  
    graph3
    graph5
    st.altair_chart(graph7, use_container_width=True)
    graph9


with col2:
    graph2
    graph4
    graph6
    graph8
    graph10