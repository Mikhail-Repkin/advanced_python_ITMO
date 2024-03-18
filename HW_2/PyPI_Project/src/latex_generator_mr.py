class LatexGenerator:
    """
    Класс для генерации LaTeX кода таблиц и изображений.
    """
    def generate_latex_table(self, data, caption="", label=""):
        """
        Утилита генерирует код LaTeX для таблицы\n
        из заданного двумерного списка данных.

        Аргументы:
            data (list of lists): Входные данные для таблицы.
                Каждый внутренний список представляет собой строку таблицы.
            caption (str, optional): Подпись к таблице.
            label (str, optional): Метка для ссылки на таблицу.

        Возвращает:
            str: Строка, содержащая код LaTeX для сгенерированной таблицы
        """

        rows = ["\t\t" + " & ".join(str(cell) for cell in row) +
                " \\\ \hline\n" for row in data]
        table_content = "".join(rows)

        latex_code = (
            "\\begin{table}\n"
            "\t\\centering\n"
            "\t\\begin{tabular}{|" + "|".join(
                "c" * len(data[0])
                ) + "|} \\hline\n"
            + table_content
            + "\t\\end{tabular}\n"
            + (
                (f"\t\\caption{{{caption}}}\n")
                if caption else "\t\\caption{Caption}\n"
               )
            + (
                (f"\t\\label{{{label}}}\n")
                if label else "\t\\label{tab:my_label}\n"
               )
            + "\\end{table}"
            )

        return latex_code

    def generate_latex_figure(self, filename, caption="", label=""):
        """
        Утилита генерирует код LaTeX для вставки картинки.\n
        Аргументы:
            filename (str): Имя файла изображения.\n
            caption (str): Подпись к изображению.\n
            label (str): Метка для ссылки на изображение.

        Возвращает:
            str: Строка, содержащая код LaTeX для вставки картинки
        """

        latex_code = (
            "\\begin{figure}\n"
            "\t\\centering\n"
            f"\t\\includegraphics[width=0.5\linewidth]{{{filename}}}\n"
            + (
                (f"\t\\caption{{{caption}}}\n")
                if caption else "\t\\caption{Caption}\n"
               )
            + (
                (f"\t\\label{{{label}}}\n")
                if label else "\t\\label{fig:enter-label}\n"
               )
            + "\\end{figure}"
            )

        return latex_code
