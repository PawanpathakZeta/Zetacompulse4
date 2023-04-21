def urban_theme():
    markColor = "#0905AF"
    axisColor = "#000000"
    backgroundColor = "transparent"
    font = "Avenir Next"
    labelFont = "Avenir Next"
    sourceFont = "Avenir Next"
    gridColor = "#DEDDDD"
    main_palette = ["#6B85EF", 
                    "#FFC233", 
                    "#FF913F", 
                    "#FF5E57", 
                    "#F72C71", 
                    "#E62D90", 
                    "#BA0090", 
                    "#CB3CAB", 
                    "#A54DC0", 
                    "#8B6BDC", 
                    "#6B85EF", 
                    "#449BFB",
                    "#0FAEFF",
                   ]
    sequential_palette = ["#0905AF",   
                          "#7714AF", 
                          "#AA36B0", 
                          "#D15CB5", 
                          "#F084BE", 
                          "#F0A4CD", 
                         ]
    return {
        "width": 685,
        "height": 380,   
#        "autosize": "fit",
        "config": {
            "title": {
                "anchor": "middle",
                "align": "center",
                "fontSize": 18,
                "font": font,
                "color": "#0905AF"
            },
            "axisX": {
               "domain": True,
               "domainColor": axisColor,
               "domainWidth": 1,
               "grid": False,
               "labelFontSize": 12,
               "labelFont": labelFont,
               "labelColor": markColor,
               "labelAngle": 0,
               "tickColor": axisColor,
               "tickSize": 5,
               "titleFontSize": 12,
               "titlePadding": 10,
               "titleFont": font,
               "title": "",
           },
           "axisY": {
               "domain": False,
               "grid": True,
               "gridColor": gridColor,
               "gridWidth": 1,
               "labelFontSize": 12,
               "labelFont": labelFont,
               "labelColor": markColor,
               "labelPadding": 8,
               "ticks": False,
               "titleFontSize": 12,
               "titlePadding": 10,
               "titleFont": font,
               "titleAngle": 0,
               "titleY": -10,
               "titleX": 18,
           },
           # "background": backgroundColor,
           # "legend": {
           #     "labelFontSize": 12,
           #     "labelFont": labelFont,
           #     "symbolSize": 100,
           #     #"symbolType": "square",
           #     "titleFontSize": 12,
           #     "titlePadding": 10,
           #     "titleFont": font,
           #     "title": "",
           #     #"orient": "top-left",
           #     "offset": 0,
           # },
           "view": {
               "stroke": "transparent",
           },
           "range": {
               "category": main_palette,
               "diverging": sequential_palette,
           },
           "area": {
               "fill": markColor,
           },
           "line": {
               "color": markColor,
               "stroke": markColor,
               "strokewidth": 5,
           },
           "trail": {
               "color": markColor,
               "stroke": markColor,
               "strokeWidth": 0,
               "size": 1,
           },
           "path": {
               "stroke": markColor,
               "strokeWidth": 0.5,
           },
           "point": {
               "filled": True,
           },
           "text": {
               "font": sourceFont,
               "color": markColor,
               "fontSize": 11,
               "align": "right",
               "fontWeight": 400,
               "size": 11,
           }, 
           "bar": {
                "size": 40,
                "binSpacing": 1,
                "continuousBandSize": 30,
                "discreteBandSize": 30,
                "fill": markColor,
                "stroke": False,
            }, 
       },
    }
    
    
import altair as alt
alt.themes.register("my_custom_theme", urban_theme)
alt.themes.enable("my_custom_theme")