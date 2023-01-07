from Matrix import Matrix, SimpleMatrix
from RowEchelon import to_row_echelon_form


def get_submatrix_r_c(matrix: SimpleMatrix, row: float,
                      col: float) -> SimpleMatrix:
    """
    Submatrix of a matrix is obtained by deleting the rth row and cth column.
    """
    submatrix_list = [r[:col] + r[col + 1:] for r in
                      matrix.data[:row] + matrix.data[row + 1:]]
    submatrix = SimpleMatrix(len(submatrix_list), len(submatrix_list))
    submatrix.fill(submatrix_list)
    return submatrix


def get_determinant(matrix: SimpleMatrix) -> float:
    """
    Recursive function which uses "Laplace expansion" (or "cofactor expansion")
    to find the determinant of the matrix.
    Matrix minor - is the determinant of the submatrix.
    """
    dim = matrix.row_count()  # dimensions
    if dim == 1:
        return matrix.get_element(0, 0)
    det = 0  # the determinant of the matrix
    for j in range(dim):
        minor = get_determinant(get_submatrix_r_c(matrix, 0, j))
        det += ((-1) ** (0 + j)) * matrix.get_element(0, j) * minor
    return det


def get_augmented(matrix_a: SimpleMatrix,
                  matrix_b: SimpleMatrix) -> SimpleMatrix:
    """
    Returns an augmented matrix - matrix_a | matrix_b
    """
    if matrix_a is None or matrix_b is None:
        return None
    list_a = matrix_a.data
    list_b = matrix_b.data
    list_c = []
    augmented = SimpleMatrix(len(list_a), len(list_a) + len(list_b))
    for i in range(len(list_a)):
        list_c.append(list_a[i] + list_b[i])
    augmented.fill(list_c)
    return augmented


def get_identity_matrix(dim: int) -> SimpleMatrix:
    """
    Computes the identity matrix of dimensions dim x dim
    """
    identity = SimpleMatrix(dim, dim)
    for row in range(dim):
        identity.set_element(row, row, 1)
    return identity


def find_augmented_matrix(matrix: SimpleMatrix) -> SimpleMatrix:
    """
    Finds the augmented matrix consisting of the matrix and the corresponding identity matrix if it is invertable.
    It is invertable if it is square and non-singular.
    A matrix is non-singular if and only if its determinant is non-zero.
    Returns None if the matrix is not invertable
    """
    if matrix.row_count() != matrix.column_count():
        return None
    if get_determinant(matrix) == 0:
        return None
    identity_matrix = get_identity_matrix(matrix.row_count())
    return get_augmented(matrix, identity_matrix)


def get_inverse_from_augmented_matrix(augmented_matrix: Matrix):
    """
    Compute the inverse of matrix by computing the RREF of an augmented matrix M | I.
    """
    if augmented_matrix is None:
        return None
    dim = augmented_matrix.row_count()
    # Compute the RREF of the augmented matrix
    to_row_echelon_form(augmented_matrix, True)
    # Extract the right hand side of the matrix that was previously an identity
    inverse = SimpleMatrix(dim, dim)
    for i in range(dim):
        for j in range(dim):
            inverse.set_element(i, j, augmented_matrix.get_element(i, j+dim))

    return inverse

def get_inverse(matrix: SimpleMatrix) -> SimpleMatrix:
    """
    Firstly check whether the matrix is square, and then check that it
    is non-singular.
    A matrix is non-singular if and only if its determinant is non-zero.
    Afterwards, if the matrix is non-singular, compute the inverse of matrix by
    computing the ref of an augmented matrix M | I.
    """
    augmented_matrix = find_augmented_matrix(matrix)
    return get_inverse_from_augmented_matrix(augmented_matrix)


if __name__ == '__main__':
    vals = [[1, 1, 1, -1], [1, 1, -1, 1], [1, -1, 1, 1], [-1, 1, 1, 1]]

    mtrx = SimpleMatrix(4, 4)
    mtrx.fill(vals)
    inverse_matrix = get_inverse(mtrx)

    for line in inverse_matrix.data:
        print(line)
