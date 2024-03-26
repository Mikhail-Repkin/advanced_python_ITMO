import numpy as np


class Matrix:
    def __init__(self, data: list[list]):
        self.matrix = data  # подаем матрицы

    def __add__(self, other):
        if len(self.matrix) != len(other.matrix):
            raise ValueError("Размеры матрицы не подходят для сложения")
        result = [
            [self.matrix[i][j] + other.matrix[i][j]
             for j in range(len(self.matrix[0]))]
            for i in range(len(self.matrix))
        ]
        return Matrix(result)

    def __mul__(self, other):
        if len(self.matrix[0]) != len(other.matrix):
            raise ValueError(
                "Размеры матриц не совпадают для умножения")
        result = [
            [self.matrix[i][j] * other.matrix[i][j]
             for j in range(len(self.matrix[0]))]
            for i in range(len(self.matrix))
        ]

        return Matrix(result)

    def __matmul__(self, other):
        if len(self.matrix[0]) != len(other.matrix):
            raise ValueError(
                "Размеры матриц не совпадают для умножения"
            )
        result = [
            [
                sum(
                    self.matrix[i][k] * other.matrix[k][j]
                    for k in range(len(other.matrix)))
                for j in range(len(other.matrix[0]))
            ]
            for i in range(len(self.matrix))
        ]
        return Matrix(result)

    def to_file(self, filename):
        with open(filename, "w") as f:
            for row in self.matrix:
                f.write(" ".join(map(str, row)) + "\n")


if __name__ == "__main__":
    np.random.seed(0)

    # Создание двух матриц
    matrix1 = Matrix(np.random.randint(0, 10, (10, 10)))
    matrix2 = Matrix(np.random.randint(0, 10, (10, 10)))

    # Сложение матриц и запись в файл
    result_addition = matrix1 + matrix2
    result_addition.to_file("artifacts/3.1/matrix+.txt")

    # Умножение матриц и запись в файл
    result_matrix_multiplication = matrix1 @ matrix2
    result_matrix_multiplication.to_file("artifacts/3.1/matrix@.txt")

    # Поэлементное умножение матриц и запись в файл
    result_componentwise_multiplication = matrix1 * matrix2
    result_componentwise_multiplication.to_file("artifacts/3.1/matrix_mult.txt")
