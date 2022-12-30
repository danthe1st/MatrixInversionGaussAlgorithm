import Matrix


# Please extend this interface for custom implementations and write your functions against this interface
class Matrix:
    '''
    General interface for matrices allowing for row operations
    '''
    def swap_rows(self, row1: int, row2: int):
        '''
        Swaps two rows in the matrix.
        :param row1: the index of the first row, starting at 0
        :param row2: the index of the second row, starting at 0
        '''
        raise NotImplementedError

    def multiply_row(self, row_num: int, scalar: float):
        '''
        Multiplies a row with a scalar.
        This method changes the row.
        :param row_num: the index of the row to change
        :param scalar: the scalar to multiply with
        '''
        raise NotImplementedError

    def multiply_and_add(self, origin_row_num: int, target_row_num: int, scalar: float):
        '''
        Multiplies a row with a scalar and adds it to another row.
        This method modifies the target row but not the origin row.
        Informally: matrix[target_row_num]=matrix[target_row_num]+matrix[origin_row_num]*scalar
        :param origin_row_num: the index of the origin row, starting at 0
        :param target_row_num: the index of the target row, starting at 0
        :param scalar: the scalar to multiply the origin row with
        '''
        raise NotImplementedError

    def column_count(self) -> int:
        '''
        Gets the number of columns
        :return: the number of columns
        '''
        raise NotImplementedError

    def row_count(self) -> int:
        '''
        Gets the number of rows
        :return: the number of columns
        '''
        raise NotImplementedError

    def get_element(self, row: int, column: int) -> float:
        '''
        Gets a specific element of the matrix
        :param row: the row index, starting at 0
        :param column: the column index, starting at 0
        :return: the element at the specific row and column
        '''
        raise NotImplementedError

    def set_element(self, row: int, column: int, element: float):
        '''
        Sets a specific element of the matrix to a specific value.
        This method does not preserve equivalence on equation systems!
        :param row: the row index, starting at 0
        :param column: the column index, starting at 0
        :param element: the new element at the specific row and column
        '''
        raise NotImplementedError

    def get_pivot_column(self, row_num: int) -> int:
        '''
        Gets the pivot column of a specific row
        :param row_num: the row index, starting at 0 or -1 if no pivot exists
        :return: the index of the pivot element, starting at 0
        '''
        raise NotImplementedError

    def get_pivot_value(self, row: int) -> float:
        '''
        Gets the value of the pivot of a specific row
        :param row: the row index, starting at 0
        :return: the value of the pivot of a specific row
        '''
        return self.get_element(row, self.get_pivot_column(row))

    def copy(self) -> Matrix:
        '''
        Makes a (deep) copy of the matrix.
        :return: a new matrix with the same element.
        '''
        raise NotImplementedError

    def fill(self, data: list[list[float]]):
        assert len(data)==self.row_count()
        for i in range(self.row_count()):
            assert len(data[i])==self.column_count()
            for j in range(self.column_count()):
                self.set_element(i, j, data[i][j])


class SimpleMatrix(Matrix):
    '''
    Simple implementation of Matrix based on lists.
    '''
    def __init__(self, row_count: int, col_count: int):
        self.data: list[list[float]] = [ [0] * col_count for i in range(row_count)]

    def swap_rows(self, row1:int, row2:int):
        tmp = self.data[row1]
        self.data[row1] = self.data[row2]
        self.data[row2] = tmp

    def multiply_row(self, row_num:int, scalar:float):
        row = self.data[row_num]
        for i in range(len(row)):
            self.data[row_num][i] = self.data[row_num][i] * scalar

    def multiply_and_add(self, origin_row_num:int, target_row_num:int, scalar:float):
        for i in range(self.column_count()):
            self.data[target_row_num][i] = self.data[target_row_num][i] + self.data[origin_row_num][i] * scalar

    def column_count(self) -> int:
        return len(self.data[0])

    def row_count(self) -> int:
        return len(self.data)

    def get_element(self, row:int, column:int) -> float:
        return self.data[row][column]

    def set_element(self, row:int, column:int, element:float) -> float:
        self.data[row][column] = element

    def get_pivot_column(self, row_num:int)->int:
        row=self.data[row_num]
        for i in range(len(row)):
            if row[i] != 0:
                return i
        return -1

    def copy(self) -> Matrix:
        copy = self.data.copy()
        for i in range(len(copy)):
            copy[i] = copy[i].copy()
