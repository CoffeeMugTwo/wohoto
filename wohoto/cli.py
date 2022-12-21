"""Console script for wohoto."""


import argparse
import sys


from wohoto.wohoto import read_input_files
from wohoto.wohoto import aggregate_by_project
from wohoto.wohoto import aggregate_by_day
from wohoto.wohoto import aggregate_by_sub_project

from wohoto.figures import make_plot


def main():
    """Console script for wohoto."""
    parser = argparse.ArgumentParser(
        description="A simple tool to process working hours data.")
    parser.add_argument("-i",
                        "--working-hours-files",
                        help="File(s) with working hours data",
                        required=True,
                        nargs="*")
    parser.add_argument("-o",
                        "--output-folder",
                        help="Folder for output files (overwrites existing results!)",
                        required=True)
    args = parser.parse_args()

    print(f"Reading files: {args.working_hours_files}")
    working_hours_df = read_input_files(args.working_hours_files)

    day_project_hours_df = aggregate_by_project(working_hours_df)
    day_hours_df = aggregate_by_day(working_hours_df)
    sub_project_hours_df = aggregate_by_sub_project(working_hours_df)

    print(f"Writing output to: {args.output_folder}")
    day_project_hours_df.to_html(f"{args.output_folder}/day_project_hours.html")
    day_hours_df.to_html(f"{args.output_folder}/day_hours.html")
    sub_project_hours_df.to_html(f"{args.output_folder}/sub_project_hours.html")

    print(f"Storing plots in: {args.output_folder}")
    fig = make_plot(working_hours_df)
    fig.savefig(f"{args.output_folder}/figures.pdf")

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
