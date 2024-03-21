import plotly.graph_objects as go


class PlotlyFigureBuilder:
    def __init__(self):
        self.standard_graph_height = 350
        self.standard_margin = dict(l=100, r=0, t=80, b=0)
        self.standard_background = "white"
        self.standard_color_palette = ["rgb(255, 32, 78)", "rgb(67,67,67)"]
        self.standard_tick_font = dict(
            family="Arial",
            size=12,
            color="rgb(82, 82, 82)",
        )
        self.standard_tick_spec = (
            dict(
                family="Arial",
                size=12,
                color="rgb(82, 82, 82)",
            ),
        )
        self.standard_grid_color = "rgb(204, 204, 204)"

    def plot_comparative_line_graph(self, x_data, y_matrix, title, labels, colors=None):
        if colors is None:
            colors = self.standard_color_palette

        fig = go.Figure()
        for i in range(len(y_matrix)):
            fig.add_trace(
                go.Scatter(
                    x=x_data,
                    y=y_matrix[i],
                    mode="lines",
                    name=labels[i],
                    line=dict(color=colors[i], width=2),
                    connectgaps=True,
                )
            )

            # endpoints
            fig.add_trace(
                go.Scatter(
                    x=[x_data[0], x_data[-1]],
                    y=[y_matrix[i][0], y_matrix[i][-1]],
                    mode="markers",
                    marker=dict(color=colors[i], size=8),
                )
            )
        annotations = []

        for y_trace, label, colors in zip(y_matrix, labels, colors):
            annotations.append(
                dict(
                    xref="paper",
                    x=0.05,
                    y=y_trace[0],
                    xanchor="right",
                    yanchor="middle",
                    text=label + " {}".format(y_trace[0]),
                    font=dict(family="Arial", size=12),
                    showarrow=False,
                )
            )
            # labeling the right_side of the plot
            annotations.append(
                dict(
                    xref="paper",
                    x=0.95,
                    y=y_trace[-1],
                    xanchor="left",
                    yanchor="middle",
                    text="{}".format(y_trace[-1]),
                    font=dict(family="Arial", size=12),
                    showarrow=False,
                )
            )

        fig.update_yaxes(title_text="Employment (Thousands)")

        fig.update_layout(annotations=annotations)
        fig.update_layout(
            xaxis=dict(
                showline=True,
                showgrid=True,
                showticklabels=True,
                linecolor=self.standard_grid_color,
                linewidth=2,
                ticks="outside",
                tickfont=self.standard_tick_font,
            ),
            yaxis=dict(
                showgrid=True,
                zeroline=False,
                showline=False,
                showticklabels=False,
            ),
            autosize=False,
            margin=self.standard_margin,
            height=self.standard_graph_height,
            showlegend=False,
            # plot_bgcolor='white'
        )
        fig.update_layout(title_text=title)

        return fig

    def plot_percentage_comparison_graph_over_time(self, x_data, y_data, title, top_labels, colors=None):
        if colors is None:
            colors = self.standard_color_palette

        fig = go.Figure()
        for i in range(0, len(x_data[0])):
            for xd, yd in zip(x_data, y_data):
                fig.add_trace(
                    go.Bar(
                        x=[xd[i]],
                        y=[yd],
                        orientation="h",
                        marker=dict(color=colors[i], line=dict(color="rgb(248, 248, 249)", width=1)),
                    )
                )

        fig.update_layout(
            xaxis=dict(showgrid=False, showline=False, showticklabels=False, zeroline=False, domain=[0.15, 1]),
            yaxis=dict(
                showgrid=False,
                showline=False,
                showticklabels=False,
                zeroline=False,
            ),
            barmode="stack",
            margin=self.standard_margin,
            height=self.standard_graph_height,
            showlegend=False,
        )

        annotations = []

        for yd, xd in zip(y_data, x_data):
            # labeling the y-axis
            annotations.append(
                dict(
                    xref="paper",
                    yref="y",
                    x=0.14,
                    y=yd,
                    xanchor="right",
                    text=str(yd),
                    font=dict(family="Arial", size=14, color="rgb(67, 67, 67)"),
                    showarrow=False,
                    align="right",
                )
            )
            # labeling the first percentage of each bar (x_axis)
            annotations.append(
                dict(
                    xref="x",
                    yref="y",
                    x=xd[0] / 2,
                    y=yd,
                    text=str(round(xd[0] * 100, 2)) + "%",
                    font=dict(family="Arial", size=14, color="rgb(248, 248, 255)"),
                    showarrow=False,
                )
            )
            # labeling the first Likert scale (on the top)
            if yd == y_data[-1]:
                annotations.append(
                    dict(
                        xref="x",
                        yref="paper",
                        x=xd[0] / 2,
                        y=1.05,
                        text=top_labels[0],
                        font=dict(family="Arial", size=14, color="rgb(67, 67, 67)"),
                        showarrow=False,
                    )
                )
            space = xd[0]
            for i in range(1, len(xd)):
                # labeling the rest of percentages for each bar (x_axis)
                annotations.append(
                    dict(
                        xref="x",
                        yref="y",
                        x=space + (xd[i] / 2),
                        y=yd,
                        text=str(round(xd[i] * 100, 2)) + "%",
                        font=dict(family="Arial", size=14, color="rgb(248, 248, 255)"),
                        showarrow=False,
                    )
                )
                # labeling the Likert scale
                if yd == y_data[-1]:
                    annotations.append(
                        dict(
                            xref="x",
                            yref="paper",
                            x=space + (xd[i] / 2),
                            y=1.05,
                            text=top_labels[i],
                            font=dict(family="Arial", size=14, color="rgb(67, 67, 67)"),
                            showarrow=False,
                        )
                    )
                space += xd[i]

        fig.update_layout(annotations=annotations)
        fig.update_layout(title_text=title)
        return fig

    def plot_pie_chart(self, data, title, labels, colors):
        if colors is None:
            colors = self.standard_color_palette

        fig = go.Figure(data=[go.Pie(labels=labels, marker_colors=colors, values=data)])
        fig.update_layout(title_text=title)

        return fig
