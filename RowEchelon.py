from Matrix import SimpleMatrix


def to_row_echelon_form(matrix: SimpleMatrix, reduced=False):
    # check if there even is a matrix
    if matrix is None:
        return

    column_index = 0
    row_count = matrix.row_count()
    column_count = matrix.column_count()

    # iterate row by row
    for row_index in range(row_count):

        # check if index does not exceed the number of columns of the matrix
        if column_index >= column_count:
            return  # return if the index exceeds the number of columns

        # start at current row
        row_iterator = row_index

        # check for zero-entries
        while matrix.get_element(row_iterator, column_index) == 0:

            row_iterator += 1
            if row_iterator == row_count:
                row_iterator = row_index
                column_index += 1
                if column_count == column_index:
                    return

        # row iterator might be equals row index -> no swap required
        if row_iterator != row_index:
            matrix.swap_rows(row_iterator, row_index)

        # get element at current position
        elem = matrix.get_element(row_index, column_index)

        # divide each element of the current row by the elem
        matrix.multiply_row(row_index, 1/float(elem))

        # do this for all rows but the current one
        for i_row in range(row_count):
            if i_row > row_index or (reduced and i_row != row_index):

                # get value
                elem = matrix.get_element(i_row, column_index)

                # subtract one column from another - the current one is skipped and used for the subtraction

                matrix.multiply_and_add(row_index, i_row, -elem)

        column_index += 1  # go to next column


if __name__ == '__main__':

    # values = [[1, 2, -1, -4], [2, 3, -1, -11], [-2, 0, -3, 22]]
    values = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

    mx = SimpleMatrix(len(values), len(values.__getitem__(0)))

    mx.fill(values)

    to_row_echelon_form(mx)

    for i in range(mx.row_count()):
        print([int(value) for value in mx.data.__getitem__(i)])
