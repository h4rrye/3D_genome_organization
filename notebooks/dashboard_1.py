# ==========================================================
#                       LIBRARIES
# ==========================================================

import pandas as pd
import numpy as np

from plotly import graph_objects as go
from plotly.subplots import make_subplots

from dash import Dash, dcc, html    # web app baes on flask
import dash_ag_grid as dag

# ==========================================================

from dash import Dash, html

app = Dash()

# Requires Dash 2.17.0 or later
app.layout = [html.Div(children='Hello World')]

if __name__ == '__main__':
    app.run(debug=True)

'''
local link to the app
ttp://127.0.0.1:8050/
'''

