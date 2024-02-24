import click
import sys


def tail_file(file_path, n=10):
    """Функция выводит последние N строк из файла."""
    with open(file_path, "r", encoding="utf-8") as file:
        lines_list = file.readlines()
        last_lines = lines_list[-n:]
        return last_lines


@click.command()
@click.argument("files", nargs=-1, type=click.Path(exists=True))
def tail(files):
    """Утилита для вывода последних 10 строк каждого из переданных файлов.\n
    Если не передано ни одного файла, то вывод последних 17 строк из `stdin`.
    """
    try:
        if not files:
            # Если не переданы файлы, выводим последние 17 строк из stdin
            last_lines = sys.stdin.readlines()[-17:]
            click.echo("".join(last_lines))
        elif len(files) == 1:
            # Если передан только один файл, выводим содержимое без имени файла
            last_lines = tail_file(files[0])
            click.echo("".join(last_lines))
        else:
            # Если передано более одного файла, выводим имя перед содержимым
            for i, file_path in enumerate(files):
                if i > 0:
                    click.echo()  # пустая строка перед именем файла
                click.echo(f"==> {file_path} <==")
                last_lines = tail_file(file_path)
                click.echo("".join(last_lines))
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    tail()
