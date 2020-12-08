"""Console script for job_report."""
import sys
import click


@click.command()
def main(args=None):
    """Console script for job_report."""
    click.echo("Replace this message by putting your code into "
               "job_report.cli.main")
    click.echo("See click documentation at https://click.palletsprojects.com/")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
