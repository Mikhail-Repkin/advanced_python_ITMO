import os
import pandas as pd
from latex_generator_mr import LatexGenerator
from pdflatex import PDFLaTeX


def generate_latex(file_path,
                   caption_tab,
                   label_tab,
                   image_filename,
                   caption_fig,
                   label_fig):

    latex_gen = LatexGenerator()

    # Чтение данных таблицы из файла
    df = pd.read_excel(file_path, header=None)
    table_data = df.values.tolist()

    # LaTeX-код для таблицы
    table_latex = latex_gen.generate_latex_table(table_data,
                                                 caption=caption_tab,
                                                 label=label_tab)

    # LaTeX-код для изображения
    figure_latex = latex_gen.generate_latex_figure(image_filename,
                                                   caption=caption_fig,
                                                   label=label_fig)

    document_start = r"""\documentclass{article}
    \usepackage{graphicx}
    \begin{document}""" + "\n\n"

    document_end = "\\end{document}"

    # Соединяем код таблицы, картинки и документа
    full_latex_code = document_start + \
        table_latex + "\n\n" + \
        figure_latex + "\n\n" + \
        document_end

    # Сохраняем LaTeX в файл
    with open("artifacts/latex_code.tex", "w") as file:
        file.write(full_latex_code)

    print("Latex таблицы и картинки сохранены в файле 'latex_code.tex'")


def create_pdf(texfile_path):
    pdfl = PDFLaTeX.from_texfile(texfile_path)
    pdf, log, completed_process = pdfl.create_pdf(keep_pdf_file=True,
                                                  keep_log_file=True)

    with open("artifacts/pdf_file.pdf", "wb") as f:
        f.write(pdf)

    print("PDF сгенерирован")


def main():
    generate_latex(os.environ.get("TAB"),  # Путь к файлу Excel
                   os.environ.get("CAP_TAB"),  # Заголовок таблицы
                   os.environ.get("LAB_TAB"),  # Метка ссылки таблицы
                   os.environ.get("IMG"),  # Название изображения
                   os.environ.get("CAP_IMG"),  # Заголовок изображения
                   os.environ.get("LAB_IMG"),  # Метка ссылки изображения
                   )
    create_pdf("artifacts/latex_code.tex")


if __name__ == "__main__":
    main()
