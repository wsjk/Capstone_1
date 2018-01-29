#Following Python packages are necessary for data visualiations below

import matplotlib.pyplot as plt
import seaborn as sns
from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objs as go
import cufflinks as cf

init_notebook_mode(connected=True)
cf.go_offline()

def get_plotly(dfs, x, y="", dfname="", xlabel='', ylabel="", text = 'title', size="", plot_type='scatter', title="", histnorm='probability'):
    if not dfname:
        dfname = ['series {}'.format(i) for i in range(len(dfs))]
    if plot_type == 'scatter':
        data = [{'x':df[x], 
                'y':df[y], 
                'mode':'markers', 
                'text':df.reset_index()[text],
                'marker':dict(size=df[size] if size else ""),
                'name':dfname}  
                for df, dfname in zip(dfs, dfname)]

        layout = go.Layout(title=title if title else y + ' vs ' + x,
            xaxis=dict(title=xlabel if xlabel else x),
            yaxis=dict(title=ylabel if ylabel else y)
            )
        
        fig = go.Figure(data=data, layout=layout)
        iplot(fig)
    elif plot_type == 'hist':
        # distribution of Hits and Flops by budget

        data = [go.Histogram(x=df[x],
                        name=dfname,
                        histnorm = 'probability'
                        ) for df, dfname in zip(dfs,dfname)]

        layout = go.Layout(title=title if title else 'histogram of ' + x, xaxis=dict(title=xlabel if xlabel else x),
                        yaxis=dict(title=ylabel  if ylabel else y))
        fig = go.Figure(data=data, layout=layout)

        iplot(fig)