from Matrix import Matrix, SimpleMatrix
import visualization_config as config
from tkinter import Tk, ttk
import threading
import numbers



class VisualizationMatrix(Matrix):

    def __init__(self, root: Tk, actual: Matrix, sleep_time: int=2):
        self.root = root
        self.actual = actual
        self.element_labels: list[list[ttk.Label]] = []
        self.detail_labels: list[ttk.Label] = []
        for i in range(actual.column_count()):
            root.columnconfigure(i, minsize=75)
            label = ttk.Label(root, text="", font=("Helvetica"))
            label.grid(row=actual.row_count() + 2, column=i)
            self.detail_labels.append(label)
        for i in range(actual.row_count()):
            row = []
            root.rowconfigure(i, weight=1)
            for j in range(actual.column_count()):
                label = ttk.Label(root, text=self.actual.get_element(i, j), font=("Helvetica", 18))
                label.grid(row=i, column=j)
                row.append(label)
            self.element_labels.append(row)
        root.rowconfigure(actual.row_count(), weight=1)

        ttk.Button(text="Auto", command=self.play_btn).grid(row=0, column=self.column_count())
        ttk.Button(text="Next", command=self.next_btn).grid(row=1, column=self.column_count())

        self.info_label = ttk.Label(root, text="", font=("Helvetica"))
        self.info_label.grid(row=actual.row_count(), columnspan=actual.column_count())
        self.sleep_time = sleep_time
        self.sleep_condition = threading.Condition()
        self.autorun = False

    def play_btn(self):
        self.autorun = not self.autorun
        if self.autorun:
            self.next_btn()

    def next_btn(self):
        self.sleep_condition.acquire()
        self.sleep_condition.notify()
        self.sleep_condition.release()

    def swap_rows(self, row1:int, row2:int):
        self.write_info(f"Swap rows {row1} and {row2}")
        self.bold_row(row1)
        self.bold_row(row2)
        self.draw()
        self.wait()
        self.actual.swap_rows(row1, row2)
        self.draw()
        self.wait()
        self.reset_info()
        self.reset_row(row1)
        self.reset_row(row2)
        self.draw()

    def multiply_row(self, row_num:int, scalar:float):
        self.write_info(f"multiply row {row_num} with {float(scalar):.4}")
        self.bold_row(row_num)
        self.draw()
        self.wait()
        self.actual.multiply_row(row_num, scalar)
        self.draw()
        self.wait()
        self.reset_info()
        self.reset_row(row_num)
        self.draw()

    def multiply_and_add(self, origin_row_num:int, target_row_num:int, scalar:float):
        self.write_info(f"row {target_row_num} = row {target_row_num} + {float(scalar):.4} * row {origin_row_num}")
        self.italic_row(origin_row_num)
        self.bold_row(target_row_num)
        for i in range(self.column_count()):
            self.detail_labels[i].config(text=f"{float(self.actual.get_element(origin_row_num, i)*scalar):.3}")
        self.draw()
        self.wait(3)
        self.actual.multiply_and_add(origin_row_num, target_row_num, scalar)
        self.draw()
        self.wait(2)
        for i in range(self.column_count()):
            self.detail_labels[i].config(text="")
        self.reset_row(origin_row_num)
        self.reset_row(target_row_num)
        self.reset_info()
        self.draw()

    def get_pivot_column(self, row_num:int) -> int:
        column = self.actual.get_pivot_column(row_num)
        if column != -1:
            for i in range(column):
                self.make_italic(self.element_labels[row_num][i])
            self.make_bold(self.element_labels[row_num][column])
            self.write_info(f"Pivot of row {row_num} is {self.actual.get_element(row_num, column)} (column {column})")
            self.draw()
            self.wait()
            self.reset_row(row_num)
            self.reset_info()
            self.draw()
        return column

    def set_element(self, row:int, column:int, element:float) -> float:
        if(self.sleep_time != 0):
            self.make_bold(self.element_labels[row][column])
            self.write_info(f"Set element of row {row}/column {column} to {float(element):.4}")
            self.draw()
        self.actual.set_element(row, column, element)
        if self.sleep_time != 0:
            self.wait()
            self.draw()
            self.wait()
            self.reset_label(self.element_labels[row][column])
            self.reset_info()
        self.draw()

    def get_element(self, row:int, column:int) -> float:
        self.make_italic(self.element_labels[row][column])
        self.write_info(f"read element at row {row}, column {column}")
        ret = self.actual.get_element(row, column)
        self.draw()
        self.wait(1 / 3)
        self.reset_label(self.element_labels[row][column])
        self.reset_info()
        self.draw()
        return ret

    def fill(self, data:list[list[float]]):
        self.write_info(f"reset/overwrite matrix")
        self.draw()
        self.wait()
        old_time = self.sleep_time
        self.sleep_time = 0
        self.actual.fill(data)
        self.reset_info()
        self.sleep_time = old_time
        self.wait()

    def copy(self) -> Matrix:
        return VisualizationMatrix(self.root, self.actual.copy(), self.sleep_time)

    def row_count(self) -> int:
        return self.actual.row_count()

    def column_count(self) -> int:
        return self.actual.column_count()

    def draw(self):
        for i in range(self.row_count()):
            for j in range(self.column_count()):
                self.element_labels[i][j].config(text=f"{float(self.actual.get_element(i, j)):.3}")
        self.root.update()

    def bold_row(self, row_num):
        row = self.element_labels[row_num]
        for label in row:
            self.make_bold(label)

    def italic_row(self, row_num):
        row = self.element_labels[row_num]
        for label in row:
            self.make_italic(label)

    def make_bold(self, label):
        label.config(font=("Helvetica", 18, "bold"))

    def make_italic(self, label):
        label.config(font=("Helvetica", 18, "italic"))

    def reset_label(self, label):
        label.config(font=("Helvetica", 18))

    def reset_row(self, row_num):
        row = self.element_labels[row_num]
        for label in row:
            self.reset_label(label)

    def write_info(self, info_text: str):
        self.info_label.config(text=info_text)

    def reset_info(self):
        self.info_label.config(text="")

    def wait(self, factor:float=1):
        self.sleep_condition.acquire()
        if self.autorun:
            self.sleep_condition.wait(factor * self.sleep_time)
        else:
            self.sleep_condition.wait()
        self.sleep_condition.release()


class Worker(threading.Thread):

    def __init__(self, fn):
        threading.Thread.__init__(self)
        self.fn = fn

    def run(self):
        self.fn()

class Fraction:
    def __init__(self, numerator: numbers.Number, denominator: numbers.Number):
        if isinstance(numerator, Fraction):
            denominator=denominator*numerator.denominator
            numerator=numerator.numerator
        if isinstance(denominator, Fraction):
            numerator=numerator*denominator.denominator
            denominator=denominator.numerator
        i=2
        while i<=min(abs(numerator), abs(denominator)):
            if numerator%i==0 and denominator%i==0:
                numerator=numerator/i
                denominator=denominator/i
            else:
                i=i+1
        self.numerator=numerator
        self.denominator=denominator

    def __mul__(self, other):
        if isinstance(other, Fraction):
            return Fraction(self.numerator*other.numerator, self.denominator*other.denominator)
        if isinstance(other, numbers.Number):
            return Fraction(self.numerator*other, self.denominator)

    def __float__(self):
        if self.numerator==0:
            return 0.0
        return float(self.numerator)/float(self.denominator)

    def __neg__(self):
        return Fraction(-self.numerator,self.denominator)

    def __pow__(self, val):
        if val != -1:
            return NotImplemented
        return Fraction(self.denominator, self.numerator)

    def __eq__(self, other):
        if isinstance(other, numbers.Number):
            return float(self)==float(other)

    def __add__(self, other):
        if isinstance(other, Fraction):
            return Fraction(self.numerator*other.denominator+other.numerator*self.denominator, self.denominator*other.denominator)
        return NotImplemented

    def __repr__(self):
        return f"{self.numerator}/{self.denominator}"


def prepare_inverse(root):
    # matrix = SimpleMatrix(4, 4)
    # matrix.fill([[1, 1, 1, -1], [1, 1, -1, 1], [1, -1, 1, 1], [-1, 1, 1, 1]])
    matrix = SimpleMatrix(4, 4)
    matrix.fill(convert_arr_to_fractions(config.inverse_matrix))
    from FindInverse import find_augmented_matrix, get_inverse_from_augmented_matrix
    augmented = find_augmented_matrix(matrix)
    augmented_data=convert_arr_to_fractions(augmented.data)
    augmented=SimpleMatrix(augmented.row_count(), augmented.column_count())
    augmented.fill(augmented_data)
    if augmented is None:
        ttk.Label(root, text="Matrix is not invertible").grid(row=0, column=0)
        return Worker(lambda: None)
    vis_matrix = VisualizationMatrix(root, augmented)
    for i in range(vis_matrix.row_count()):
        vis_matrix.element_labels[i][vis_matrix.row_count()].grid(padx=(50, 0))
    return Worker(lambda: print(get_inverse_from_augmented_matrix(vis_matrix)))


def prepare_row_echelon(root):
    original = SimpleMatrix(len(config.ref_matrix), len(config.ref_matrix[0]))
    matrix = VisualizationMatrix(root, original)
    original.fill(convert_arr_to_fractions(config.ref_matrix))
    from RowEchelon import to_row_echelon_form
    return Worker(lambda: to_row_echelon_form(matrix, config.operation==config.VisualizationType.RREF))

def convert_arr_to_fractions(arr: list[list[numbers.Number]]):
    ret=[]
    for row in arr:
        sublist=[]
        for elem in row:
            sublist.append(Fraction(elem, 1))
        ret.append(sublist)
    return ret

def visualization_main():
    root = Tk()
    root.title("Matrix inversion, Gauss algorithm")
    # matrix = VisualizationMatrix(root, 5, 5)
    # matrix.set_element(0, 3, 1337)
    # matrix.swap_rows(1, 2)
    if config.operation.value<2:
        worker = prepare_row_echelon(root)
    else:
        worker = prepare_inverse(root)
    worker.start()
    root.mainloop()


if __name__ == '__main__':
    visualization_main()
