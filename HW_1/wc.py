import click
import sys


def count_lines_words_bytes(file_path):
    """
    Подсчитывает количество строк, слов и байтов в переданном файле.
    """
    lines = 0
    words = 0
    bytes_count = 0

    if isinstance(file_path, int):  # stdin file descriptor
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                lines += 1
                words += len(line.split())
                bytes_count += len(line.encode())
    elif isinstance(file_path, str):  # file name
        with open(file_path, "rb") as f:
            for line in f:
                lines += 1
                words += len(line.split())
                bytes_count += len(line)

    return lines, words, bytes_count


@click.command()
@click.argument("files", nargs=-1, type=click.Path(exists=True))
def wc(files):
    """
    Утилита подсчитывает количество строк, слов и байтов в файлах. \n
    Если файлы не переданы, то утилита считывает вход с `stdin`.
    """
    if not files:
        lines, words, bytes_count = count_lines_words_bytes(sys.stdin.fileno())
        click.echo(f"\t{lines}\t{words}\t{bytes_count}")
        return

    total_lines = 0
    total_words = 0
    total_bytes = 0

    output_list = []

    for file_path in files:
        lines, words, bytes_count = count_lines_words_bytes(file_path)

        output_list.append([lines, words, bytes_count, file_path])

        total_lines += lines
        total_words += words
        total_bytes += bytes_count

    if len(files) > 1:
        sym_count_lines = len(f"{total_lines}")
        sym_count_words = len(f"{total_words}")
        sym_count_bytes_count = len(f"{total_bytes}")

        for item in output_list:
            click.echo(
                f" {item[0]:>{sym_count_lines}}  "
                f"{item[1]:>{sym_count_words}} "
                f"{item[2]:>{sym_count_bytes_count}} {item[3]}"
            )
        click.echo(f" {total_lines}  {total_words} {total_bytes} total")
    else:
        click.echo(
            f" {output_list[0][0]}  {output_list[0][1]} {output_list[0][2]} "
            f"{output_list[0][3]}"
        )


if __name__ == "__main__":
    wc()
