from Matrix import SimpleMatrix
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


def get_inverse(matrix: SimpleMatrix) -> SimpleMatrix:
    """
    Firstly check whether the matrix is square, and then check that it
    is non-singular.
    A matrix is non-singular if and only if its determinant is non-zero.
    Afterwards, if the matrix is non-singular, compute the inverse of matrix by
    computing the ref of an augmented matrix M | I.
    Find the inverse of the matrix by computing the RREF of the
    """

    if not matrix.row_count() == matrix.column_count():
        return None
    if get_determinant(matrix) == 0:
        return None
    dim = matrix.row_count()
    inverse = SimpleMatrix(dim, dim)
    identity_matrix = get_identity_matrix(dim)
    augmented_matrix = get_augmented(matrix, identity_matrix)
    # Compute the RREF of the augmented matrix
    to_row_echelon_form(augmented_matrix, True)
    # Extract the right hand side of the matrix that was previously an identity
    temp_data = augmented_matrix.data
    temp_data = [row[dim:] for row in temp_data]
    inverse.fill(temp_data)
    return inverse


if __name__ == '__main__':
    vals = [[1, 1, 1, -1], [1, 1, -1, 1], [1, -1, 1, 1], [-1, 1, 1, 1]]

    mtrx = SimpleMatrix(4, 4)
    mtrx.fill(vals)
    inverse_matrix = get_inverse(mtrx)

    for line in inverse_matrix.data:
        print(line)
