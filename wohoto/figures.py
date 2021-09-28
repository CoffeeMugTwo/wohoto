"""
This module contains functions to produce graphics.
"""

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

import pandas as pd

from wohoto.wohoto import get_time_difference


def add_overall_pie_chart(ax: plt.axes,
                          hours_df: pd.DataFrame,
                          column_name: str) -> None:
    """
    Returns a figure object containing a pie chart showing the distribution of worked ours in groups defined by
    *column_name*

    Parameters
    ----------


    hours_df : pd.DataFrame
        Sorted data frame containing all rows in the provided files

    column_name : str
        Name of the column in *hours_df* that should be used for the grouping

    Returns
    -------
    pie_chart_figure : plt.Figure
        Figure containing the axis with the pie chart
    """

    agg_df = hours_df.loc[:, ["date", "start", "end", "project", "comment","type"]]

    agg_df["duration"] = agg_df.apply(
        lambda row: get_time_difference(row["date"], row["start"], row["date"], row["end"]),
        axis=1
    )

    grouped_df = agg_df.groupby(column_name).sum(numeric_only=False)

    ax.pie(grouped_df["duration"],
           labels=grouped_df.index,
           autopct="%1.1f%%")

    ax.set_title(f"Distribution in {column_name}")

    return


def make_plot(working_hours_df: pd.DataFrame) -> matplotlib.figure.Figure:
    """
    Creates a figure containing all plots.

    Parameters
    ----------
    working_hours_df : pd.DataFrame
        Data frame containing raw data

    Returns
    -------
    fig : matplotlib.figure.Figure
        Figure containing all plots
    """
    fig = plt.figure(tight_layout=True, figsize=(12, 12))
    gs = gridspec.GridSpec(2, 2)

    # add type pie chart
    pie_type_ax = fig.add_subplot(gs[0, 0])
    add_overall_pie_chart(pie_type_ax,
                          working_hours_df,
                          "type")

    # add project pie chart
    project_type_ax = fig.add_subplot(gs[0, 1])
    add_overall_pie_chart(project_type_ax,
                          working_hours_df,
                          "project")

    fig.suptitle(f"Analysis of working hours form {working_hours_df['date'].min()} to {working_hours_df['date'].max()}")

    return fig

