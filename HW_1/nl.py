import click
import sys


@click.command()
@click.argument("filename", type=click.File("r"), default="-")
@click.option(
    "--encoding",
    default="utf-8",
    help="Specify the encoding of the input file."
)
def nl(filename, encoding):
    """Утилита пронумеровывает все строки из файла или стандартного ввода."""
    if filename.name == '<stdin>' or filename.name == '-':
        file = sys.stdin
    else:
        file = open(filename.name, mode="r", encoding=encoding)

    line_number = 1
    try:
        for line in file:
            click.echo(f"\t{line_number}  {line}", nl=False)
            line_number += 1
    except KeyboardInterrupt:
        pass

    if file != sys.stdin:
        file.close()


if __name__ == "__main__":
    nl()
