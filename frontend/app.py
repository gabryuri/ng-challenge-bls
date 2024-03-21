import numpy as np
import streamlit as st
import plotly.graph_objects as go

from plotly_figure_builder import PlotlyFigureBuilder
from utils import fetch_data

figbuilder = PlotlyFigureBuilder()
st.set_page_config(layout="wide")
col = st.columns((4, 3), gap="medium")

base_url = "http://postgrest_server:3000"

## Women employment - Monthly
we_suffix = "women_employment"
we_data = fetch_data(base_url, we_suffix)

we_x_values = [item["date"] for item in we_data]
we_y_values = np.array(
    [[item["women_employment_thousands"] for item in we_data], [item["total_employment_thousands"] for item in we_data]]
)

women_employment_fig = figbuilder.plot_comparative_line_graph(
    x_data=we_x_values,
    y_matrix=we_y_values,
    title="Women Employment in Government over time",
    labels=["Women", "Total"],
)

## Women employment - Decades
we_dec_suffix = "women_employment_decades"
we_dec_data = fetch_data(base_url, we_dec_suffix)

we_dec_y_values = [item["decade"] for item in we_dec_data]
we_dec_x_values = [[item["percentage_of_women"], 1 - item["percentage_of_women"]] for item in we_dec_data]

we_dec_fig = figbuilder.plot_percentage_comparison_graph_over_time(
    x_data=we_dec_x_values,
    y_data=we_dec_y_values,
    title="Percentage of Women in the US Government - Decade average",
    top_labels=["Women", "Men"],
)

## Supervisory vs Production employees
# Bar chart
empl_suffix = "supervisory_vs_production"
empl_data = fetch_data(base_url, empl_suffix)

empl_x_values = [item["decade"] for item in empl_data]
empl_y_values = np.array(
    [
        [item["total_private_production_employees"] for item in empl_data],
        [item["total_supervisory_employees"] for item in empl_data],
    ]
)

employee_labels = ["Production", "Supervisory"]
employee_colors = ["rgb(73, 105, 137)", "rgb(88, 163, 153)"]

fig_employees = figbuilder.plot_comparative_line_graph(
    x_data=empl_x_values,
    y_matrix=empl_y_values,
    title="Employee count - Supervisory vs production roles",
    labels=employee_labels,
    colors=employee_colors,
)

## Pie chart
empl_pie_data = [item[-1] for item in empl_y_values]  # Last decade data

empl_pie_chart = figbuilder.plot_pie_chart(
    data=empl_pie_data,
    title="Supervisory vs production roles in the last decade",
    labels=employee_labels,
    colors=employee_colors,
)

with col[0]:
    st.plotly_chart(women_employment_fig, use_container_width=True)
    st.plotly_chart(fig_employees, use_container_width=True)

with col[1]:
    st.plotly_chart(we_dec_fig, use_container_width=True)
    st.plotly_chart(empl_pie_chart, use_container_width=True)
