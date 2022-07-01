"""Main module."""

import datetime as dt
import pandas as pd


def read_input_files(list_of_files: list) -> pd.DataFrame:
    """
    Read input files and return data frame with all inputs

    Parameters
    ----------
    list_of_files : list(str)
        List of all paths to the input files

    Returns
    -------
    hours_df : pd.DataFrame
        Sorted data frame containing all rows in the provided files
    """
    column_names = ["date", "start", "end", "project", "type", "comment"]
    dummy_df = pd.DataFrame(columns=column_names)
    temp_df_list = [dummy_df]
    for input_file in list_of_files:
        temp_df = pd.read_csv(input_file,
                              sep=";",
                              index_col=False,
                              comment="#")
        temp_df_list.append(temp_df)

    hours_df = pd.concat(temp_df_list,
                         ignore_index=True)\
                 .sort_values(by=["date", "start"],
                              axis=0)

    # Convert date to datetime
    # hours_df["date"] = pd.to_datetime(hours_df["date"])



    # add year-month column
    hours_df['year_month'] = hours_df.apply(
        lambda row: f"{pd.Timestamp(row['date']).year}-{pd.Timestamp(row['date']).month}",
        axis=1
    )
    # add calendar week column
    hours_df['calendar_week'] = hours_df.apply(
        lambda row: pd.Timestamp(row['date']).week,
        axis=1
    )

    print(hours_df.info())
    print(hours_df)

    return hours_df


def get_time_difference(start_date: str,
                        start_time: str,
                        end_date: str,
                        end_time:str) -> dt.timedelta:
    """
    Return the time difference between *start_date*-*start_time* and *end_date*-*end_time* as a timedelta

    Parameters
    ----------
    start_date : str
        Start date in iso format (YYYY-MM-DD)
    start_time : str
        Start time in iso format (HH-MM)
    end_date : str
        End date in iso format (YYYY-MM-DD)
    end_time : str
        End time in iso format (HH-MM)

    Returns
    -------
    duration : dt.timedelta
    """
    start_date_time = dt.datetime.fromisoformat(f"{start_date}T{start_time}")
    end_date_time = dt.datetime.fromisoformat(f"{end_date}T{end_time}")
    duration = end_date_time - start_date_time
    return duration


def agg_sum_project(data_frame: pd.DataFrame) -> pd.DataFrame:
    """
    Sums up all timedeltas in duration columns and comments up and returns a data frame with the results in respective
    columns

    Parameters
    ----------
    data_frame : pd.DataFrame
        Data frame containing a "duration" column containing dt.timedeltas and a columns containing strings

    Returns
    -------
    agg_df : pd.DataFrame
        A Data frame containing a "duration" and a "comments" column
    """
    duration_sum = data_frame["duration"].sum()
    comments_sum = data_frame["comment"].sum()
    agg_df = pd.DataFrame({"duration": [duration_sum], "comment": [comments_sum]})
    return agg_df


def aggregate_by_project(hours_df: pd.DataFrame) -> pd.DataFrame:
    """
    Process *hours_df* to return a data frame with summed up working hours per day and project.

    Parameters
    ----------
    hours_df : pd.DataFrame
        Data frame containing the working hours and project information

    Returns
    -------
    day_project_hours_df : pd.DataFrame
        Data frame containing the summed up hours per day and project
    """
    agg_df = hours_df.loc[:, ["year_month", "date", "start", "end", "project", "comment"]]

    agg_df["duration"] = agg_df.apply(
        lambda row: get_time_difference(row["date"], row["start"], row["date"], row["end"]),
        axis=1
    )
    # ToDo: Add functionality to remove duplicates in comments when summing up
    # day_project_hours_df = agg_df.groupby(["date", "project"]).apply(agg_sum_project)
    day_project_hours_df = agg_df.groupby(["year_month", "project", "date"]).apply(agg_sum_project)
    return day_project_hours_df


def agg_sum_day(data_frame: pd.DataFrame) -> pd.DataFrame:
    """
    Sums up all timedeltas in duration and returns a data frame with the results in respective
    columns

    Parameters
    ----------
    data_frame : pd.DataFrame
        Data frame containing a "duration" column containing dt.timedeltas

    Returns
    -------
    agg_df : pd.DataFrame
        A Data frame containing a "duration" and a "comments" column
    """
    #ToDo: There is a lot of overlap with agg_sum_project function
    duration_sum = data_frame["duration"].sum()
    agg_df = pd.DataFrame({"duration": [duration_sum]})
    return agg_df


def aggregate_by_day(hours_df: pd.DataFrame) -> pd.DataFrame:
    """
    Process *hours_df* to return a data frame with the summed up working hours per day.

    Parameters
    ----------
    hours_df : pd.DataFrame
        Data frame containing hte working hours and project information

    Returns
    -------
    day_hours_df : pd.DataFrame
        Data frame containing the summed up hours per day
    """
    agg_df = hours_df.loc[:, ["date", "start", "end"]]

    agg_df["duration"] = agg_df.apply(
        lambda row: get_time_difference(row["date"], row["start"], row["date"], row["end"]),
        axis=1
    )

    day_hours_df = agg_df.groupby("date").apply(agg_sum_day)
    return day_hours_df
