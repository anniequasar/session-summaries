#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MeetUp 095 - Beginners Python and Machine Learning - 16 Feb 2021 - Introduction to charting with plotly

Colab:   https://colab.research.google.com/drive/1x-Jscp45vksby-1rBjjOjA3V7EtL8lEW
Youtube: https://youtu.be/B69sxYH70rk
Meetup:  https://www.meetup.com/Beginners-Python-Machine-Learning/events/276263628/
Github:  https://github.com/anniequasar/session-summaries/tree/master/online

Learning objectives:
- pandas DataFrames and Series
- plotly.py

Links

To install third party library requirements

    pip install numpy pandas plotly

@author D Tim Cummings
"""

# Colab only: Google colab uses an old version of plotly. We need 4.5 or later. Uncomment following line in colab
# !pip list | grep plotly

# Colab only: Uncomment following line in colab to upgrade for session
# !pip install --upgrade plotly

import numpy as np
import pandas as pd
import plotly
import plotly.graph_objects as go
import plotly.express as px

# https://plotly.com/python/creating-and-updating-figures/

# plotly.py is a library for sending JSON objects to plotly.js
# at a low level we can create a dict and send it straight to plotly.js
fig = {
    "data": [{"type": "scatter", "x": [1, 2, 3], "y": [1, 3, 2], "name":"up down"},
             {"type": "scatter", "x": [1, 2, 4], "y": [1, 2.5, 3.5], "name":"climber"}
             ],
    "layout": {"title": {"text": "Scatter chart constructed as a dict"}}
}
# The method in the next line works out we are using colab and uses a colab renderer to 
# implement plotly.js in colab and display our interactive chart (try hovering and clicking)
plotly.io.show(fig)
# If you are not using interactive python you can create an html file and open it
plotly.io.write_html(fig, "fig1.html")

# Challenge 1: Given the following lists of x and y values which represent sigmoid function
# Plot the values in a scatter chart using dict 
x = np.linspace(-10, 10, 21) 
y = 1/(1 + np.exp(-x)) 
print(f"Values for sigmoid plot {x=}")
print(f"Values for sigmoid plot {y=}")

# Solution to challenge 1
# if you are only showing one item in data list, you need to explicitly show the legend
fig = {
    "data": [{"type": "scatter", "x": x, "y": y, "name": "sigmoid", "showlegend": True}],
    "layout": {"title": {"text": "Sigmoid function constructed as a dict"}}
}
plotly.io.show(fig)

# At a higher level we can use plotly graph_objects which have a built-in validation 
fig = go.Figure(
    data=[go.Bar(x=[1, 2, 3], y=[1, 3, 2], name="blue boxes", showlegend=True,)],
    layout=go.Layout(
        title=go.layout.Title(text="Bar chart constructed using graph objects")
    )
)
# Figure has a "write_html()" method for those not using interactive python
fig.write_html("fig2.html")
# In Google colab we can call "show()" method
fig.show()

# print fig to see how graph_objects are converted to a dict
print(f"graph_objects are converted to dict. Summary (no template) {fig=}")

# use to_dict() to see the full dictionary
print(f"graph_objects are converted to dict. Full (with template) {fig.to_dict()=}")

# Challenge 2: Using x and y from Challenge 1 plot the values using graph_objects

# Solution to challenge 2
# Also demonstrates how to use lines or markers or both and how to set marker symbols
fig = go.Figure(
    data=[go.Scatter(x=x, y=y, name="sigmoid", showlegend=True, mode="lines+markers", marker_symbol="hash-dot", marker_line_width=1, marker_size=15)],
    layout=go.Layout(
        title=go.layout.Title(text="Sigmoid function constructed from graph_object")
    )
)
# see the created dict. Notice what happens with marker_line_width
print(f"Solution 2: {fig=}")
fig.show()

# How to see all markers available
# https://plotly.com/python/marker-style/
raw_symbols = plotly.validators.scatter.marker.SymbolValidator().values
print(f"Symbols available\n{raw_symbols=}")

# Challenge 3 - Assemble data into tuples 
# (int_id, str_id, name_stem, name_variant)
# name_stem = name but removing all -open and -dot
# name_variant = -open and -dot in original name
# NB plotly 4.4.1 and earlier don't include int id in raw symbols

# Solution to challenge 3
grouped_symbols = []
for i in range(0, len(raw_symbols), 3):
    int_id, str_id, name = raw_symbols[i], raw_symbols[i+1], raw_symbols[i+2]
    name_stem = name.replace("-open", "").replace("-dot", "")
    name_variant = name[len(name_stem):]
    # name_stem, name_variant = (name, "") if idx_dash == -1 else (name[:idx_dash], name[idx_dash:])
    grouped_symbols.append((int_id, str_id, name_stem, name_variant))
print("Solution 3: Grouped symbols", grouped_symbols)

# Challenge 4: Sort list of tuples by name

# Solution 4
grouped_symbols.sort(key=lambda t: t[2])
name_variants = [gs[3] for gs in grouped_symbols]
name_stems = [gs[2] for gs in grouped_symbols]
name_symbols = [gs[2] + gs[3] for gs in grouped_symbols]
num_symbols = [gs[0] for gs in grouped_symbols]
print("Solution 4")
print(f"grouped_symbols={grouped_symbols}")
print(f"name_stems={name_stems}")
print(f"name_variants={name_variants}")
print(f"name_symbols={name_symbols}")
print(f"num_symbols={num_symbols}")

# Challenge 5: Draw a scatter graph of the symbols
# mode = "markers"
# x = name_variant
# y = name_stem
# marker_symbol = symbol

# Solution 5
fig = go.Figure(go.Scatter(mode="markers", x=name_variants, y=name_stems, marker_symbol=num_symbols,
                           marker_line_color="midnightblue", marker_color="lightskyblue", 
                           marker_line_width=2, marker_size=15, 
                           hovertemplate="name: %{y}%{x}<br>number: %{marker.symbol}"))
fig.update_layout(title="Mouse over symbols for name & number!",
                  xaxis_range=[-1, 4], yaxis_range=[len(set(name_stems)), -1],  # number of unique name_stems sorted top to bottom
                  margin=dict(b=0, r=0), xaxis_side="top", height=1600, width=500)
# default margin is b=80, r=80, l=80, t=100
fig.show()

# plotly express is higher level api designed for data exploration
df1 = pd.DataFrame(data={"id": [1, 2, 3], "score": [1, 3, 2], "group": ["up-down"] * 3})
df2 = pd.DataFrame(data={"id": [1, 2, 4], "score": [1, 2, 5], "group": ["climber"] * 3})
df = pd.concat([df1, df2])
print(f"DataFrame for plotting using plotly express {df=}")
px.line(df, x="id", y="score", color="group")

# Challenge 6: Using x and y from Challenge 1 plot the values using plotly express

# Solution 6
df = pd.DataFrame(data=y, index=x, columns=["sigmoid"])
df['fn'] = 'sigmoid'
print(f"Solution 6: {df.head()=}")
# px.line and px.scatter use dataframe index on x axis by default
fig = px.line(df, y="sigmoid", title="Sigmoid function constructed from plotly express", color='fn')
fig.show()

# plotly express comes with some default datasets if you want to practise
df = px.data.gapminder().query("continent=='Oceania'")
fig = px.line(df, x="year", y="lifeExp", color='country')
fig.show()
print(f"Plotly express gapminder data {df.info()=}")

# Other chart types https://plotly.com/python/

# Sankey https://plotly.com/python/sankey-diagram/
labels = ["Average personal income tax", "Welfare", "aged", "disability", "families", "unemployed", "other welfare", "Health", "Defence", "Education", "Public services", "Interest", "Transport and communication", "Energy", "Public order", "Foreign affairs", "Industry assistance", "Housing and community", "Recreation and culture", "Immigration", "Other"]
sources = [0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
targets = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] 
values = [3951, 1604, 1049, 851, 249, 198, 1916, 898, 828, 483, 408, 193, 189, 137, 137, 137, 126, 95, 90, 412]
fig = go.Figure(go.Sankey(
    node={"label": labels, },
    link={
        "source": sources,
        "target": targets,
        "value": values},
    valueformat=".0f",))
fig.show()

# 3D Isosurface plots https://plotly.com/python/3d-isosurface-plots/
X, Y, Z = np.mgrid[-5:5:40j, -5:5:40j, -5:5:40j]

# ellipsoid
values = X * X * 0.5 + Y * Y + Z * Z * 2

fig = go.Figure(data=go.Isosurface(
    x=X.flatten(),
    y=Y.flatten(),
    z=Z.flatten(),
    value=values.flatten(),
    colorscale='BlueRed',
    isomin=10,
    isomax=50,
    surface_count=3,
    caps=dict(x_show=False, y_show=False)
    ))
fig.show()

# Notice how surface_count = 3 gets translated to surface = {'count': 3}
# This is called "Magic Underscore Notation" and is a "plotly specific" feature
# Happens almost every time there is an underscore in parameter name
print(f"Observe 'surface_count=3'\n{fig=}")

# Challenge 7: Find another example of "Magic Underscore Notation" we have used

# Solution 7: Look at Solution 2
# marker_line_width=1 is equivalent to marker={"line": {"width": 1}}
# Can also specify the layout title text
fig2 = go.Figure(
    data=[go.Scatter(x=x, y=y, name="sigmoid", showlegend=True, mode="lines+markers", marker_symbol="hash-dot", marker_line_width=1, marker_size=15)],
    layout_title_text="Title created using magic underscore notation"
)
print(f"Creating Figure using 'layout_title_text'\n{fig2=}")
fig2.show()
fig2.update_layout(title_text='My title updated using title_text')
print(f"Updating Figure using 'update_layout' and 'title_text'\n{fig2=}")
fig2.update(layout_title_text="My title updated using 'update' and 'layout_title_text'")

# Remember how we created a evenly spaced array using linspace or arange
print(f"{np.arange(-10, 10.1, 0.5)=}")
print(f"{np.linspace(-10, 10, 41)=}")

# We can do the same using one dimensional mesh grid, specifying the interval between values (like np.arange()) (end is non-inclusive)
print(f"{np.mgrid[-10:10.1:0.5]=}")

# Can also use complex numbers to specify number of values (like np.linspace()) (end is inclusive)
print(f"{np.mgrid[-10:10:41j]=}")

# Challenge 8: Create a mesh grid X1 having 3 values from 0 to 1 and Y1 having 3 values from 1 to 2
# Calculate array V1 where V1[i, j] = X1[i, j]**2 + Y1[i, j]**2
# Flatten V1 into a one dimensional array

# Solution 8:
X1, Y1 = np.mgrid[0:1:3j, 1:2:3j]
V1 = (X1**2 + Y1**2).flatten()
print(f"Solution 8: {V1=}")
