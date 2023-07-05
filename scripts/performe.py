from __future__ import annotations

import importlib
import pathlib
import sys

import click


def procedures():
    procedures = []
    p = pathlib.Path(__file__).parent.parent / "performance"
    for item in p.iterdir():  # Raises FileNotFoundError
        if item.is_file():
            name = item.name
            if name.endswith(".py") and not name.startswith("_"):
                procedure = name.rstrip(".py")
                procedures.append(procedure)
    return procedures


@click.command()
@click.option("--name", prompt="Procedure name")
def performe(name):
    try:
        module = importlib.import_module(f"performance.{name}")
    except ModuleNotFoundError:
        click.secho(f"\nERROR: procedure '{name}' does not exist", fg="red", bold=True)
        print("Available procedures:")
        for procedure in procedures():
            click.secho(f" * {procedure}", fg="green")
        sys.exit(1)
    cli = getattr(module, "cli")
    procedure = cli()
    procedure()


if __name__ == "__main__":
    performe()