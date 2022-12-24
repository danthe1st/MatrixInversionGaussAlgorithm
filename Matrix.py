import Matrix
# Please extend this interface for custom implementations and write your functions against this interface
class Matrix:
  def swap_rows(self, row1: int, row2: int):
    raise NotImplementedError
  def multiply_row(self, row_num: int, scalar: float):
    raise NotImplementedError
  def swap_and_multiply(self, row1: int, row_to_multiply: int, scalar: float):
    raise NotImplementedError
  def column_count(self) -> int:
    raise NotImplementedError
  def row_count(self) -> int:
    raise NotImplementedError
  def get_element(self, row: int, column: int) -> float:
    raise NotImplementedError
  def get_pivot_column(self, row: int) -> int:
    raise NotImplementedError
  def get_pivot_value(self, row: int) -> float:
    return self.get_element(row, self.get_pivot_column(row))
  def copy(self) -> Matrix:
    raise NotImplementedError
