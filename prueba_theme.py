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
#import zeta_theme
import urban_theme # where the color theme is 


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
col1.title('Zeta Customer Growth Intelligence')
"""Growth Intelligence & Insights Using Zeta Data"""

## Zeta Logo
#zeta_logo = Image.open('ZETA_BIG-99e027c9.webp') #white logo 
zeta_logo = Image.open('ZETA_BIG-99e027c92.png') #blue logo 
col2.image(zeta_logo)


# 1. Pie chart

match_rate = pd.DataFrame({"values": ['unknown', 'unmatch', 'match_name', 'match_phone','match_email'],"values1": [200, 469, 675, 1404,1800]})
plot_title = alt.TitleParams("Match distribution",dx=65)
pie1=alt.Chart(match_rate).mark_arc(innerRadius=15, stroke="#fff").encode(
    theta=alt.Theta("Count:Q", stack=True),
    radius=alt.Radius("Count", scale=alt.Scale(type="sqrt", zero=True,rangeMin=20)),
    order=alt.Order("Count",type="quantitative", sort= "ascending"),
    color=alt.Color("Match Category:N")
).properties(
    height=400, width=400,
    title=plot_title
)
graph1 = pie1.mark_arc(innerRadius=20, stroke="#fff")


# match_rate = pd.DataFrame({"values": ['v_match_email', 'iv_match_phone', 'iii_match_name', 'ii_unmatch','i_unknown'],"values1": [1800, 1404, 675, 469,200]})
# # match_rate = pd.DataFrame({"values": ['unknown', 'unmatch', 'match_name', 'match_phone','match_email'],"values1": [200, 469, 675, 1404,1800]})
# plot_title = alt.TitleParams("Match distribution",dx=80)
# pie1=alt.Chart(match_rate).mark_arc(innerRadius=15, stroke="#fff").encode(
#     theta=alt.Theta("values1", stack=True),
#     radius=alt.Radius("values1", scale=alt.Scale(type="sqrt", zero=True,rangeMin=20)),
#     color=alt.Color("values")
#     # tooltip=["values", "values1"] ## Displays tooltip
# ).properties(
#     height=400, width=400,
#     title=plot_title
# )
# # pie1.configure_title(
# #     fontSize=20,
# #     font='Courier',
# #     anchor='start',
# #     color='gray',
# #     # subtitlePadding=20,
# #     dx=200
# # )
# c1 = pie1.mark_arc(innerRadius=20, stroke="#fff")


# graph1= c1

#graph1= pie

st.text(" ")



# 2. Simple Bar chart
data_signal_matches = pd.DataFrame({"Field": ['Data Signal Matches', 'Data Signal Matches', 'Data Signal Matches', 'Data Signal Matches', 'Data Signal Matches']
                                ,"Field metric": ['Transactional', 'Location', 'Behavioral', 'Professional', 'Credit Bureau']
                                ,"Percent" :[0.93, 0.87, 0.84, 0.96, 0.75  ]
                                ,"Value": [70, 65, 63, 72, 56]})

plot_title = alt.TitleParams("Data Signal Matches",dx=90)
bars2 = alt.Chart(data_signal_matches, title= plot_title
).transform_joinaggregate(
    TotalValue='sum(Value)',
).transform_calculate(
    PercentOfTotal="datum.Percent"
).mark_bar(size = 70).encode(
alt.X('Field metric:N',  title=None),
alt.Y('PercentOfTotal:Q', axis=None),
alt.Color("Field metric:N", )
).properties(
width=800 # controls width of bar.
, height=400  # height of the table
)
text2 = bars2.mark_text(
    align='center',
    baseline='middle',
    dx=0,dy=-15, # Nudges text to right so it doesn't appear on top of the bar
    size =20
).encode(
    text= alt.Text('PercentOfTotal:Q', format ='.0%')
    ,color = alt.value("#0905AF")
)

graph2 = (bars2+text2)



# 3. Streamgraph with Interactive Legend
abd = pd.read_csv('data_Interactive Charts_new.csv')
abd = abd[~abd.series.isin(["Agriculture","Information","Mining and Extraction"])]
abd.loc[abd["series"] == "Government", "series"] = "Apparel & Accesories" #
abd.loc[abd["series"] == "Construction", "series"] = "Automotive" #
abd.loc[abd["series"] == "Manufacturing", "series"] = "Consumer Services" #
abd.loc[abd["series"] == "Wholesale and Retail Trade", "series"] = "Entertainment"#
abd.loc[abd["series"] == "Transportation and Utilities", "series"] = "Food & Pharmacy" #
abd.loc[abd["series"] == "Finance", "series"] = "Home" #
abd.loc[abd["series"] == "Business services", "series"] = "Mass Retailers" #
abd.loc[abd["series"] == "Education and Health", "series"] = "Office, Electronics, Games" #
abd.loc[abd["series"] == "Leisure and hospitality", "series"] = "Restaurant" #
abd.loc[abd["series"] == "Other", "series"] = "Specialty Retail" #
abd.loc[abd["series"] == "Self-employed", "series"] = "Travel" #

#selection = alt.selection_point(fields=['series'], bind='legend')
plot_title = alt.TitleParams("Transactional Category",dx=100)
stream3= alt.Chart(abd, title=plot_title).mark_area().encode(
    # alt.X('yearmonth(date2):T', axis=alt.Axis(domain=True, format='%Y', tickSize=0) , title=None),
    alt.X('date2:T'),
    alt.Y('sum(count):Q', stack='center', axis=None),
    alt.Color('series:N',scale=alt.Scale(scheme='category20b'))
    #opacity=alt.condition(selection, alt.value(1), alt.value(0.2))
).properties(
width=900 # controls width of bar.
, height=415  # height of the table
).interactive()
#.add_params(
#    selection
#)

graph3 = stream3

# 4. 2D Histogram Scatter Plot
plot_title = alt.TitleParams("Price Sensitivity Scores Across Age and Income Band",dx=80)
source =pd.read_csv('bubble_chart.csv')
hist4 =alt.Chart(source, title=plot_title).mark_circle(color="#0905AF").encode(
    alt.X('Income bins', bin=True, axis=alt.Axis(title='Income bins(K)')),
    alt.Y('Age', bin=True, axis=alt.Axis(title="Age bins")),
    size='Price sensitivity scores'
).properties(
width=850 # controls width of bar.
, height=445  # height of the table
)
graph4 =hist4 



# 5. Radial chart

source=pd.DataFrame({"values": ['i.Email', 'ii.Programatic', 'iii.Social', 'iv.Direct mail'],"values1": [30, 10, 13, 50]})
# columns=["a", "b", "c"])
plot_title = alt.TitleParams("Omni-Channel Reach",dx=70)
base = alt.Chart(source, title=plot_title).encode(
    theta=alt.Theta("values1", stack=True),
    radius=alt.Radius("values1", scale=alt.Scale(type="sqrt", zero=True, rangeMin=20)),
    # radius=alt.Radius("values", scale=alt.Scale(['a','b','c','d'])),
    # labels=["a", "b", "c"],
    color=alt.Color("values",scale=alt.Scale(scheme='rainbow'),)
)


c1 = base.mark_arc(innerRadius=20, stroke="#fff")

c2 = base.mark_text(radiusOffset=20, size=18, dx=8, dy=-5).encode(text="values1",  color = alt.value("#0905AF"))

graph5= (c1)

# 6. Hexbin chart
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
plot_title = alt.TitleParams("Click Behavior of the Day across Months",dx=30)
hexbin= alt.Chart(source, title=plot_title).mark_point(size=size*(size/2), shape=hexagon).encode(
    x=alt.X('xFeaturePos:N', axis=alt.Axis(title='Month', grid=False, tickOpacity=10, domainOpacity=10 
                                           , values=(1, 2,3,4,5,6,7,8,9,10,11,12)
                                           ,labelAngle= 0)),
    y=alt.Y('LAST_CLICK_DAY:O', axis=alt.Axis(title='Day of the week', labelPadding=20, tickOpacity=0, domainOpacity=0)),
    #stroke=alt.value('black'),
    strokeWidth=alt.value(0.2),

    fill=alt.Color('mean(CLICK_COUNT):Q',  legend=alt.Legend(title='Key')), #scale =
    # fill=alt.Color('mean(CLICK_COUNT):Q'), #scale = 
    tooltip=['LAST_CLICK_DATE:O', 'LAST_CLICK_DAY:O', 'mean(CLICK_COUNT):Q']
).transform_calculate(
    # This field is required for the hexagonal X-Offset
    xFeaturePos='( datum.LAST_CLICK_DAY % 2) / 2 + datum.LAST_CLICK_DATE'
    
).properties(
    # Exact scaling factors to make the hexbins fit
    width=size * xFeaturesCount * 2 *0.985,
    height=size * yFeaturesCount * 1.7320508076 *0.985,  # 1.7320508076 is approx. sin(60°)*2
).configure_view(
    strokeWidth=0
)

graph6 = hexbin


# 7. Predictions graph 
forecast = pd.read_csv('competitors2.csv')
forecast1 = forecast.reset_index().melt('date', var_name='Company', value_name='Conversions')
forecast1 = forecast1[~forecast1.Company.isin(['index'])]
plot_title = alt.TitleParams("Conversion Predictions",dx=60)
line_a=alt.Chart(forecast1,title=plot_title).mark_line().encode(
    x='yearmonth(date):T',
    y='mean(Conversions):Q',
    color='Company:N'
).transform_filter(
    alt.FieldOneOfPredicate(field='Company', oneOf=['Motel6', 'Motel6_pred'])
).properties(
    height=600 
    ,width= 1800
).interactive()


line_b = alt.Chart(forecast1,title=plot_title).mark_line().encode(
    x='yearmonth(date):T',
    y='mean(Conversions):Q',
    color='Company:N'
).transform_filter(
   alt.FieldOneOfPredicate(field='Company', oneOf=['Jetblue', 'Jetblue_pred'])
).properties(
    height=600 
    ,width= 1800
).interactive()

line_ab = alt.Chart(forecast1,title="Conversion Behavior").mark_line().encode(
    x='yearmonth(date):T',
    y='mean(Conversions):Q',
    color='Company:N'
).transform_filter(
   alt.FieldOneOfPredicate(field='Company', oneOf=['Motel6', 'Motel6_pred','Jetblue', 'Jetblue_pred'])
).properties(
    height=600 
    ,width= 1800
).interactive()


# df = pd.DataFrame([['Action', 5, 'F'], 
#                    ['Crime', 10, 'F'], 
#                    ['Action', 3, 'M'], 
#                    ['Crime', 9, 'M']], 
#                   columns=['Genre', 'Rating', 'Gender'])

# chart = alt.Chart(df).mark_bar().encode(
#    column=alt.Column(
#        'Genre', title=""),
#    x=alt.X('Gender', axis=alt.Axis(ticks=False, labels=False, title='')),
#    y=alt.Y('Rating', axis=alt.Axis(grid=False)),
#    color='Gender'

# ).properties(width=300, title=alt.TitleParams(
#         ['This is a footer.'],
#         baseline='bottom',
#         orient='bottom',
#         anchor='start',
#         fontWeight='normal',
#         fontSize=10,
#         dy=20, dx=300,
#         align='left'
#     ))



# title1 = alt.Chart(
#     {"values": [{"text": "The Title"}]}
# ).mark_text(size=20).encode(
#     text="text:N"
# )

# subtitle1 = alt.Chart(
#     {"values": [{"text": "Subtitle"}]}
# ).mark_text(size=14).encode(
#     text="text:N"
# )



# chart3=alt.vconcat(
#     title1,
#     subtitle1,
#     chart
# )
sentence1 ="Matched to Data Cloud: count of records matched to DC"
sentence2 ='Not Matched to Data Cloud: count of records not matched to DC'
sentence3 ='behavioral: count of records with a behavioral signal in the DC'
sentence4 ='Professional: count of records with a professional signal in the DC'
sentence5 ='Location: count of records with a location signal in the DC'
sentence6 ='Transactional: count of records with a transactional signal in the DC'
sentence7 ='Email: count of records matched to DC using email'
sentence8 ='Phone: count of records matched to DC using phone'
#######################


col1, col2 , col3 = st.columns([7,1,7])

with col1:
    st.header("  ")
    st.altair_chart(graph1, use_container_width=True)
    # st.markdown('<div style="text-align: left;">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp;Customer record match distribution</div>', unsafe_allow_html=True)  
    # st.markdown('<div style="text-align: left;">&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp;Customer record match distribution</div>', unsafe_allow_html=True)  
    st.markdown('<div style="text-align: center;">Customer record match distribution</div>', unsafe_allow_html=True)  
    # st.text(".               Customer record match distribution")
    # st.text("Customer record match distribution")
    # st.latex(r'''\hspace \int a x^2  erwfqe                          \n'''))
    # graph5
    st.header("  ")
    # graph5
    st.altair_chart(graph3, use_container_width=True)
    st.header("  ")
    # st.markdown('<div style="text-align: left;">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp;Transactional patterns over time seen in Zeta data</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align: center;">Transactional patterns over time seen in Zeta data</div>', unsafe_allow_html=True)
    # st.text(".           Transactional patterns over time seen in Zeta data")
    # st.header("  ")
    # st.header("  ")
    # st.header("_______________________________________________________________________________________________")
    # st.header("***********************************************************************************************************************************")
    st.header("  ")
    
    st.altair_chart(graph5, use_container_width=True)
    st.header("  ")
    st.header("  ")
    st.header("  ")
    # st.header("  ")
    # graph9
    #source_h
    # st.text(".               Optimal channel mix and strategy for customer base")
    # st.markdown('<div style="text-align: left;">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp;Optimal channel mix and strategy for customer base</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align: center;">Optimal channel mix and strategy for customer base</div>', unsafe_allow_html=True)
    # graph10
    st.header("  ")
    # st.header("  ")
    options = st.multiselect('Select your competitor',('Company', 'Competitor B'))

    # if 'Competitor B' in options:
    #     # st.altair_chart(line_b, use_container_width=True)
    #     line_b
    #     # st.header("  ") 
    
    # else:
    #     line_a
    #     # st.altair_chart(line_a, use_container_width=True)
    #     # st.header("  ")
    # st.markdown('<div style="text-align: right;">Conversions predictions and comparison based on different clients</div>', unsafe_allow_html=True)
    # # st.header("  ")
    # # st.text('Conversions predictions and comparison based on different clients')


with col2:
    st.header("  ")
    st.header("  ")
    st.header("  ")
    st.header("  ")
    st.header("  ")
    # st.header("_________________________")
    st.header("  ")
    st.header("  ")
    st.header("  ")
    st.header("  ")
    st.header("  ")
    st.header("  ")
    st.header("  ")


with col3:
    st.header("  ")
    # graph2
    st.altair_chart(graph2)
    st.markdown('<div style="text-align: center;">Zeta can enrich upwards of 96% of customer records</div>', unsafe_allow_html=True)  
    # st.text(".               Zeta can enrich upwards of 96% of customer records")
    st.header("  ")
    # graph4
    # st.header("  ")
    st.altair_chart(graph4, use_container_width=True)
    st.markdown('<div style="text-align: center;">Zeta Price Sensitivity score for customer records</div>', unsafe_allow_html=True)  
    # st.text(".         Zeta Price Sensitivity score for customer records")
    # graph8  
    st.header("  ")
    # st.header("  ")
    # st.header("  ")
    # st.header("_______________________________________________________________________")
    # st.altair_chart(graph9, use_container_width=True)
    st.altair_chart(graph6, use_container_width=True)
    st.markdown('<div style="text-align: center;">Engagement of customer records intra-week and across months</div>', unsafe_allow_html=True)
    # st.text(".          Engagement of customer records intra-week and across months")
    st.header("  ")
    # st.altair_chart(chart3, use_container_width=True)

# options = st.multiselect('Select your competitor',('Company', 'Competitor B'))
if ('Competitor B' in options) &('Company' in options):
    line_ab    
elif 'Competitor B' in options:
    line_b
else:
    line_a
# st.markdown('<div style="text-align: left;">&nbsp; &nbsp; &nbsp;&nbsp;&nbsp;&nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp;&nbsp;&nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp;&nbsp;&nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp;&nbsp;&nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp;Conversions predictions and comparison based on different clients</div>', unsafe_allow_html=True)
st.markdown('<div style="text-align: center;">Conversions predictions and comparison based on different clients</div>', unsafe_allow_html=True)
# st.text('.                                                                Conversions predictions and comparison based on different clients')



st.header("  ")
st.header('Glossary')
st.write(sentence1)
st.write(sentence2)
st.write(sentence3)
st.write(sentence4)
st.write(sentence5)
st.write(sentence6)
st.write(sentence7)
st.write(sentence8)


footer="""<style>

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: white;
color: black;
text-align: center;
}
</style>
<div class="footer">
<p>(c) 2023 Zeta Global, Dev Version 1, GDSA</p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)



 