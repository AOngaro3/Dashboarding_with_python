import types
import pandas as pd
import dateutil.parser
import numpy as np
import ast 
import matplotlib.pyplot as plt
import panel as pn
import panel.widgets as pnw
import matplotlib.gridspec as gridspec
import param
from labellines import labelLine, labelLines
from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.models import HoverTool
from bokeh.palettes import Category20

class Dataset():
    def __init__(self, filename):
        self.df = pd.read_csv(filename)

class Dashboard(param.Parameterized):
    
    df = Dataset("./Data/vgsales.csv").df
    #data_path = "../Data/"

    #df = pd.read_csv(data_path+"vgsales.csv")
    
    piattaforma = param.ObjectSelector(default="Wii", objects=df["Platform"].unique().tolist())
    
    valore = param.ObjectSelector(default="Year", objects=["Year","Genre","Publisher"])
    
    

    def __init__(self, **params):
        
        super().__init__(**params)

        self.panel()
    
    
    
    @param.depends('piattaforma')
    def data(self):
        return self.df[self.df["Platform"] == self.piattaforma]
    
    
    @param.depends('data',"valore")
    def plot_1(self):
        group = self.valore
        try:
            #output_file("bar_sorted.html")
            a = self.data().groupby(group).sum()["Global_Sales"].div(self.data().groupby(group).size())
            
            fruits = a.index.astype("str").tolist()
            counts = a.tolist()


            # sorting the bars means sorting the range factors
            #sorted_fruits = sorted(fruits, key=lambda x: counts[fruits.index(x)])

            #ciao = 
            p = figure(x_range=fruits, plot_height=350, title="Global sales per game grouped by"+group,
                       toolbar_location=None,tools="")

            p.vbar(x=fruits, top=counts, width=0.9)


            p.add_tools(HoverTool(tooltips=[(group, "@x"),("Value","@top")]))

            p.xgrid.grid_line_color = None
            p.y_range.start = 0
            
            if group == "Publisher":
                p.xaxis.major_label_orientation = 45
                p.xaxis.axis_label_text_font_size = "2pt"
            
            return pn.pane.Bokeh(p)
        except Exception as e: 
            #print(e)
            return pn.pane.Str(str(e),sizing_mode="stretch_width")
    
    @param.depends('data',"valore")
    def plot_2(self):
        group = self.valore
        
        temp = self.data().groupby(group).sum()[["NA_Sales","EU_Sales","JP_Sales","Other_Sales"]]
        temp = temp.div(temp.sum(axis=1),axis = 0)
        temp = temp.reset_index()
        temp[group] = temp[group].astype("str")
        
        fruits = temp[group].tolist()
        years = ["NA_Sales","EU_Sales","JP_Sales","Other_Sales"]

        p = figure(x_range=fruits, plot_height=350,title="Sales percentage for each area of the world grouped by " + str(group),
                   toolbar_location=None, tools="")

        p.vbar_stack(years, x=group, width=0.9, source=temp,
                     legend_label=years,color = Category20[11][2:6])


        hover = HoverTool()
        hover.tooltips = [("Zone", "$name"),("Value","@$name")]
        hover.formatters = {'Value': 'printf'}
        p.add_tools(hover)
        

        p.y_range.start = 0
        p.x_range.range_padding = 0.1
        p.xgrid.grid_line_color = None
        p.axis.minor_tick_line_color = None
        p.outline_line_color = None
        p.legend.location = "top_left"
        p.legend.orientation = "vertical"
        p.add_layout(p.legend[0], 'right')
        
        if group == "Publisher":
            p.xaxis.major_label_orientation = 45
            p.xaxis.axis_label_text_font_size = "2pt"
        return pn.pane.Bokeh(p)

    @param.depends('piattaforma')  
    def Html_ret(self):
        plat = self.piattaforma
        return pn.pane.HTML('<span>'+plat+'</span>', style = {
          "position": "absolute",
          "top": "50%",
          "left": "50%",
          "transform": "translate(-50%, -50%)",
          "font-size":"120px",
            "letter-spacing":"0.1em",
          "-webkit-text-fill-color": "transparent",
            "-webkit-text-stroke-width": "3px",
          "-webkit-text-stroke-color": "white",
            "text-shadow": "8px 8px #d52e3f,20px 20px #000000"
})
    
    @param.depends('data')  
    def Html_ret_2(self):
        dat = self.data()
        return pn.pane.HTML('<span> Number of games produced: '+str(dat.shape[0])+'</span>', style = {
          "position": "relative",
          "top": "50%",
          "left": "70%",
          "transform": "translate(-50%, -50%)",
          "font-size":"40px",
            "letter-spacing":"0.1em",
          "-webkit-text-fill-color": "transparent",
            "-webkit-text-stroke-width": "2px",
          "-webkit-text-stroke-color": "white",
            "text-shadow": "6px 6px #d52e3f,10px 10px #000000"
})

    def panel(self):
        appbar = pn.Row(
            pn.pane.HTML('''<div>Videogames sales dashboard</div>''',style = {
              "font-size": "4rem",
            "text-align": "left",
              "height":"10vh",
      "line-height": "10vh",
	    "color": "#fcedd8",
	    "background": "#d52e3f",
	   	"font-family": "Niconne, cursive",
	    "font-weight": "200",
      "text-shadow": "2px 2px 0px #eb452b, 4px 4px 0px #efa032, 6px 6px 0px #46b59b, 8px 8px 0px #017e7f, 10px 10px 0px #052939, 12px 12px 0px #c11a2b, 14px 14px 0px #c11a2b, 16px 16px 0px #c11a2b, 18px 18px 0px #c11a2b"
},width = 1000
            ),
            pn.layout.HSpacer(height=0),
            pn.pane.PNG(
                "./scripts/cont.png",
                width=200,
                align="center",
                sizing_mode="fixed",
                margin=(10, 50, 10, 5),
            ),
            sizing_mode="stretch_width",
            css_classes=["app-bar"],
        )
        gspec = pn.GridSpec(sizing_mode='stretch_both',background = "#f2f2f2")
        gspec[0, :3] = pn.Column(appbar,pn.layout.HSpacer(height=10))
        gspec[1, 0] = pn.Column(pn.Param(self.param,
                               parameters=["piattaforma", "valore"],
                widgets={
                    "piattaforma": {
                        "type": pn.widgets.Select,
                        "inline": True,
                        "align": "end",
                        "color": "#fcba03"
                    }
                }),css_classes=['app-container'])

        gspec[1,1] = pn.Row(pn.layout.VSpacer(width=10),pn.Column(self.plot_1,css_classes=["app-container"]))
        gspec[1,2] = pn.Row(pn.layout.VSpacer(width=10),pn.Column(self.plot_2,css_classes=["app-container"],sizing_mode= "stretch_width"))
        gspec[2,0] = pn.Row(pn.layout.VSpacer(width=10),self.Html_ret)
        gspec[2,1] = pn.Row(self.Html_ret_2,width =100)

        return gspec

