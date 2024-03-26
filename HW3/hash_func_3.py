from matrix_ops_1 import Matrix


class DescriptorsMixin:
    @property
    def matrix(self):
        return self._matrix

    @matrix.setter
    def matrix(self, value):
        self._matrix = value


class HashMixin:
    """Хэш по сумме всех элементов матрицы"""
    def sum_elements(self):
        total_sum = 0

        for row in self._matrix:
            for elem in row:
                total_sum += elem

        return total_sum

    def __hash__(self):
        return self.sum_elements()


class CachedMatrixProduct(Matrix,
                          DescriptorsMixin,
                          HashMixin):
    """Скалярное произведение матриц с кэшированием"""
    def __init__(self, data: list[list]) -> None:
        super().__init__(data)
        self._matrix = data
        self._result_cache = {}  # (хэши): результат произведения матриц

    def calc_matrix_product(self, other):
        hash_key = (hash(self), hash(other))

        if hash_key in self._result_cache:
            return CachedMatrixProduct(self._result_cache[hash_key])

        result = self.__matmul__(other)
        self._result_cache[hash_key] = result.matrix

        return CachedMatrixProduct(self._result_cache[hash_key])


if __name__ == "__main__":
    A = CachedMatrixProduct([[10, 0], [0, 10]])
    B = CachedMatrixProduct([[5, 5], [5, 5]])
    C = CachedMatrixProduct([[5, 10], [5, 0]])
    D = CachedMatrixProduct([[5, 5], [5, 5]])

    # Проверка на коллизию
    if (hash(A) == hash(C) and
        (A != C) and
        (B.matrix == D.matrix) and
        (A @ B != C @ D)
        ):

        AB = A.calc_matrix_product(B)  # результат произведения A @ B
        CD = C.calc_matrix_product(D)  # результат произведения C @ D
        CD_true = C @ D  # настоящий результат произведения C @ D (без кэша)

        hash_AB = hash(AB)
        hash_CD = hash(CD)

        # Сохранение результатов в файлы
        A.to_file("artifacts/3.3/A.txt")
        B.to_file("artifacts/3.3/B.txt")
        C.to_file("artifacts/3.3/C.txt")
        D.to_file("artifacts/3.3/D.txt")

        AB.to_file("artifacts/3.3/AB.txt")
        CD_true.to_file("artifacts/3.3/CD.txt")

        with open("artifacts/3.3/hash.txt", "w") as f:
            f.write("AB: {}\n".format(hash_AB))
            f.write("CD: {}\n".format(hash_CD))

        # Вывод информации
        print("Хэш AB:", hash_AB)
        print("Хэш CD:", hash_CD)
        print("Коллизия обнаружена:", hash_AB == hash_CD)
    else:
        print("Условия для поиска коллизии не соблюдены.")
