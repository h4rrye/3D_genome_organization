# ==========================================================
#                       LIBRARIES
# ==========================================================

import pandas as pd
import numpy as np

from plotly import graph_objects as go
from plotly.subplots import make_subplots

from dash import Dash, dcc, html
import dash_ag_grid as dag

# import plot functions
from plot_functions import create_chromosome_3d_plot

# ==========================================================

# load data
gc = pd.read_csv('x_y_z_bin_gc.csv').iloc[:, 1:]
com = pd.DataFrame(
    np.load('x_y_z_dist_com_dist_rm.npy'), 
    columns=['x', 'y', 'z', 'dist_com', 'dist_rm']
)
sasa = pd.DataFrame(
    np.load('x_y_z_dist_surf.npy'), 
    columns=['x', 'y', 'z', 'dist_surf']
)
surface_coords_scaled = pd.DataFrame(
    np.load('surface_coords_scaled.npy'), 
    columns=['x', 'y', 'z']
)

# combine data
data_combined = pd.concat(
    [gc, com[['dist_com', 'dist_rm']], sasa['dist_surf']], 
    axis=1
)

def standard_scaler(col):
    return (col - col.mean()) / col.std()

# Columns to scale
cols_to_scale = ['gc_content_percentage', 'dist_com', 'dist_rm', 'dist_surf']

# Apply scaler only to selected columns
data_combined[cols_to_scale] = data_combined[cols_to_scale].apply(standard_scaler)

# Feature columns for plotting
feature_cols = ['gc_content_percentage', 'dist_com', 'dist_rm', 'dist_surf']

# Create the 3D chromosome plot
fig = create_chromosome_3d_plot(data_combined, surface_coords_scaled, feature_cols)

# Update figure to be responsive (remove fixed width/height)
fig.update_layout(
    autosize=True,
    width=None,
    height=None
)

# ==========================================================
#                       DASHBOARD
# ==========================================================

app = Dash(__name__)

title = html.H1('3D Chromosome Plot', style={
    'color': 'white',
    'text-align': 'center',
    'margin': '10px 0',
    'padding': '10px'
})

plot_box_style = {
    'display': 'flex',
    'justify-content': 'center',
    'align-items': 'center',
    'width': '100%',
    'height': 'calc(100vh - 100px)'
}

plot_box = html.Div([
    dcc.Graph(figure=fig, id='chromosome-plot', style={
        'width': '95vw',
        'height': '90vh',
        'margin': 'auto'
    })
], style=plot_box_style)

style_dict = {
    'min-height': '100vh',
    'width': '100%',
    'display': 'flex',
    'flex-direction': 'column',
    'justify-content': 'center',
    'align-items': 'center'
}

app.layout = html.Div([title, plot_box], style=style_dict)

# For production deployment (WSGI compatibility)
server = app.server

if __name__ == '__main__':
    # For local development
    app.run(debug=True, port=8050, host='127.0.0.1')
    
    # For production (uncomment when deploying):
    # app.run(debug=False, port=8050, host='0.0.0.0')