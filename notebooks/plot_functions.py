import numpy as np
import pandas as pd
from plotly import graph_objects as go

def create_chromosome_3d_plot(data_combined, surface_coords_scaled, feature_cols):
    """
    Create 3D chromosome plot with interactive dropdown and toggle.
    
    Parameters:
    -----------
    data_combined : pd.DataFrame
        DataFrame with x, y, z and feature columns
    surface_coords_scaled : pd.DataFrame
        DataFrame with surface coordinates (x, y, z)
    feature_cols : list
        List of feature column names for coloring
        
    Returns:
    --------
    fig : plotly.graph_objects.Figure
        Plotly figure object
    """
    # Calculate bounds from both line and points data
    all_x = np.concatenate([data_combined['x'], surface_coords_scaled['x']])
    all_y = np.concatenate([data_combined['y'], surface_coords_scaled['y']])
    all_z = np.concatenate([data_combined['z'], surface_coords_scaled['z']])

    x_range = [all_x.min(), all_x.max()]
    y_range = [all_y.min(), all_y.max()]
    z_range = [all_z.min(), all_z.max()]

    # Your DataFrame with x, y, z and feature columns
    feature_cols = ['gc_content_percentage', 'dist_com', 'dist_rm', 'dist_surf']
    fig = go.Figure()

    # Initial trace (line plot)
    initial_col = feature_cols[0]

    fig.add_trace(go.Scatter3d(
        x=data_combined['x'],
        y=data_combined['y'],
        z=data_combined['z'],
        mode='lines',
        line=dict(
            width=9,
            color=data_combined[initial_col],
            colorscale='Turbo',
            cmin=data_combined[feature_cols].min().min(),
            cmax=data_combined[feature_cols].max().max(),
            showscale=True,  # Show colorbar
            colorbar=dict(title=''),  # Remove colorbar title
        ),
        name='Chromosome Line'
    ))

    # Add 3D points trace
    fig.add_trace(go.Scatter3d(
        x=surface_coords_scaled['x'],
        y=surface_coords_scaled['y'],
        z=surface_coords_scaled['z'],
        mode='markers',
        marker=dict(size=2, color='skyblue', opacity=0.1),
        name='Surface Points'
    ))

    # Create buttons for dropdown (color selection) - Use 'update' instead of 'restyle'
    buttons = []
    for col in feature_cols:
        buttons.append(
            dict(
                label=col.replace('_', ' ').title(),
                method='update',
                args=[
                    {
                        'line.color': [data_combined[col]],
                        'line.colorbar.title': ''  # Keep title empty when updating
                    },
                    {}  # Empty layout update to preserve camera
                ]
            )
        )

    # Add button to toggle points visibility
    toggle_points_button = dict(
        label='Toggle Surface Points',
        method='update',
        args=[
            {'visible': [True, True]},
            {}  # Empty layout to preserve camera
        ],
        args2=[
            {'visible': [True, False]},
            {}  # Empty layout to preserve camera
        ]
    )

    fig.update_layout(
        updatemenus=[
            dict(
                type='dropdown',
                buttons=buttons,
                direction='down',
                showactive=True,
                x=0.02,
                xanchor='left',
                y=1.02,
                yanchor='top',
                bgcolor='rgba(255,255,255,0.8)',
                bordercolor='gray',
                borderwidth=1
            ),
            dict(
                type='buttons',
                buttons=[toggle_points_button],
                direction='right',
                x=0.02,
                xanchor='left',
                y=0.95,
                yanchor='top',
                bgcolor='rgba(255,255,255,0.8)',
                bordercolor='gray',
                borderwidth=1
            )
        ],
        title='',
        uirevision='constant',
        showlegend=True,
        legend=dict(
            title_text='',
            visible=True
        ),
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent plot background
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent paper background
        scene=dict(
            xaxis=dict(
                visible=False,
                range=x_range,
                autorange=False
            ),
            yaxis=dict(
                visible=False,
                range=y_range,
                autorange=False
            ),
            zaxis=dict(
                visible=False,
                range=z_range,
                autorange=False
            ),
            aspectmode='data',
            bgcolor='rgba(0,0,0,0)',  # Transparent scene background
        ),
        width=1000,
        height=800,
        margin=dict(l=0, r=0, b=0, t=0, pad=0),
    )

    return fig