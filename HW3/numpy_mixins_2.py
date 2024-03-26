from numpy.lib.mixins import NDArrayOperatorsMixin
import numpy as np


class DescriptorsMixin:
    @property
    def matrix(self):
        return self._matrix

    @matrix.setter
    def matrix(self, value):
        self._matrix = value


class OutputMixin:
    def __str__(self):
        return "\n".join([" ".join(map(str, row)) for row in self.matrix])


class SaveMixin:
    def to_file(self, filename):
        with open(filename, "w") as f:
            for row in self.matrix:
                f.write(" ".join(map(str, row)) + "\n")


class MatrixOperations(DescriptorsMixin,
                       OutputMixin,
                       SaveMixin,
                       NDArrayOperatorsMixin):
    def __init__(self, data: list[list]):
        self._matrix = data

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        if method == "__call__":
            return self._operate(ufunc, *inputs, **kwargs)
        else:
            return NotImplemented

    def _operate(self, ufunc, *inputs, **kwargs):
        inputs = [x.matrix if isinstance(x, MatrixOperations)
                  else x for x in inputs]
        result_matrix = getattr(ufunc, "__call__")(*inputs, **kwargs)
        return MatrixOperations(result_matrix)


if __name__ == "__main__":
    np.random.seed(0)

    matrix1 = MatrixOperations(np.random.randint(0, 10, (10, 10)))
    matrix2 = MatrixOperations(np.random.randint(0, 10, (10, 10)))

    # Сложение матриц и запись в файл
    result_addition = matrix1 + matrix2
    result_addition.to_file("artifacts/3.2/matrix+.txt")
    print("Сумма:")
    print(str(result_addition), end="\n\n")

    # Поэлементное умножение матриц и запись в файл
    result_componentwise_multiplication = matrix1 * matrix2
    result_componentwise_multiplication.to_file("artifacts/3.2/matrix_mult.txt")
    print("Поэлементное умножение:")
    print(str(result_componentwise_multiplication),
          end="\n\n")

    # Умножение матриц и запись в файл
    result_matrix_multiplication = matrix1 @ matrix2
    result_matrix_multiplication.to_file("artifacts/3.2/matrix@.txt")
    print("Скалярное умножение:")
    print(str(result_matrix_multiplication))
