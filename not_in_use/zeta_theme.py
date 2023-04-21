import altair as alt

def zeta_theme():
    markColor = "#0905AF"
    backgroundColor = "#FFFFFF"
    # Typography
    font = "Avenir Next"
    # At Urban it's the same font for all text but it's good to keep them separate in case you want to change one later.
    labelFont = "Avenir Next" 
    sourceFont = "Avenir Next"
    # Axes
    axisColor = "#000000"
    gridColor = "#DEDDDD"
    # Colors
    main_palette = ["#FFF047", 
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
                    "#0FAEFF"
                   ]
    sequential_palette = ["#449BFB", 
                          "#007BD7", 
                          "#005CB3", 
                          "#003F91", 
                          "#002570", 
                          "#00175D", 
                         ]
    return {
        # width and height are configured outside the config dict because they are Chart configurations/properties not chart-elements' configurations/properties.
        # not in the guide
        "config": {
            "title": {
                "fontSize": 18,
                "font": font,
                "anchor": "middle", # equivalent of left-aligned.
                "fontColor": "#0905AF"
            },
            "range": {
                "category": main_palette,
                "diverging": sequential_palette,
            },
            "legend": {
                "labelFont": labelFont,
                "labelFontSize": 12,
                "symbolType": "square", # just 'cause
                "symbolSize": 100, # default
                "titleFont": font,
                "titleFontSize": 12,
                "title": "", # set it to no-title by default
                #"orient": "top-right", # so it's right next to the y-axis
                "offset": 0, # literally right next to the y-axis.
            },
            "view": {
                "stroke": "transparent", # altair uses gridlines to box the area where the data is visualized. This takes that off.
            },
            "background": {
                "color": "white", # white rather than transparent
            },
            ### MARKS CONFIGURATIONS ###
            "area": {
               "fill": markColor,
            },
            "line": {
               "color": markColor,
               "stroke": markColor,
               "strokeWidth": 5,
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
}
    }



alt.themes.register("my_zeta_theme", zeta_theme)
alt.themes.enable("my_zeta_theme")