from Matrix import Matrix, SimpleMatrix
from tkinter import Tk, ttk
import time
import threading


class VisualizationMatrix(Matrix):

    def __init__(self, root: Tk, actual: Matrix, sleep_time: int = 2):
        self.root = root
        self.actual=actual
        self.labels: list[list[ttk.Label]] = []
        self.detail_labels: list[ttk.Label] = []
        for i in range(actual.column_count()):
            root.columnconfigure(i, minsize=75)
            label = ttk.Label(root, text="", font=("Helvetica"))
            label.grid(row=actual.row_count()+2, column=i)
            self.detail_labels.append(label)
        for i in range(actual.row_count()):
            row = []
            root.rowconfigure(i, weight=1)
            for j in range(actual.column_count()):
                label = ttk.Label(root, text=self.actual.get_element(i, j), font=("Helvetica", 18))
                label.grid(row=i, column=j)
                row.append(label)
            self.labels.append(row)
        root.rowconfigure(actual.row_count(), weight=1)
        self.info_label=ttk.Label(root, text="", font=("Helvetica"))
        self.info_label.grid(row=actual.row_count(), columnspan=actual.column_count())
        self.sleep_time=sleep_time

    def swap_rows(self, row1:int, row2:int):
        self.write_info(f"Swap rows {row1} and {row2}")
        self.bold_row(row1)
        self.bold_row(row2)
        self.draw()
        time.sleep(self.sleep_time)
        self.actual.swap_rows(row1, row2)
        self.draw()
        time.sleep(self.sleep_time)
        self.reset_info()
        self.reset_row(row1)
        self.reset_row(row2)
        self.draw()

    def multiply_row(self, row_num:int, scalar:float):
        self.write_info(f"multiply row {row_num} with {float(scalar):.4}")
        self.bold_row(row_num)
        self.draw()
        time.sleep(self.sleep_time)
        self.actual.multiply_row(row_num, scalar)
        self.draw()
        time.sleep(self.sleep_time)
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
        time.sleep(3*self.sleep_time)
        self.actual.multiply_and_add(origin_row_num, target_row_num, scalar)
        self.draw()
        time.sleep(2*self.sleep_time)
        for i in range(self.column_count()):
            self.detail_labels[i].config(text="")
        self.reset_row(origin_row_num)
        self.reset_row(target_row_num)
        self.reset_info()
        self.draw()

    def get_pivot_column(self, row_num:int)->int:
        column = self.actual.get_pivot_column(row_num)
        if column!=-1:
            for i in range(column):
                self.make_italic(self.labels[row_num][i])
            self.make_bold(self.labels[row_num][column])
            self.write_info(f"Pivot of row {row_num} is {self.actual.get_element(row_num, column)} (column {column})")
            self.draw()
            time.sleep(self.sleep_time)
            self.reset_row(row_num)
            self.reset_info()
            self.draw()
        return column

    def set_element(self, row:int, column:int, element:float)->float:
        if(self.sleep_time!=0):
            self.make_bold(self.labels[row][column])
            self.write_info(f"Set element of row {row}/column {column} to {float(element):.4}")
            self.draw()
        self.actual.set_element(row, column, element)
        if self.sleep_time!=0:
            time.sleep(self.sleep_time)
            self.draw()
            time.sleep(self.sleep_time)
            self.reset_label(self.labels[row][column])
            self.reset_info()
        self.draw()

    def get_element(self, row:int, column:int)->float:
        self.make_italic(self.labels[row][column])
        self.write_info(f"read element at row {row}, column {column}")
        ret = self.actual.get_element(row, column)
        self.draw()
        time.sleep(self.sleep_time/3)
        self.reset_label(self.labels[row][column])
        self.reset_info()
        self.draw()
        return ret

    def fill(self, data:list[list[float]]):
        self.write_info(f"reset/overwrite matrix")
        self.draw()
        time.sleep(self.sleep_time)
        old_time=self.sleep_time
        self.sleep_time=0
        self.actual.fill(data)
        self.reset_info()
        self.sleep_time=old_time
        time.sleep(self.sleep_time)

    def copy(self)->Matrix:
        return VisualizationMatrix(self.root, self.actual.copy(), self.sleep_time)

    def row_count(self)->int:
        return self.actual.row_count()

    def column_count(self)->int:
        return self.actual.column_count()

    def draw(self):
        for i in range(self.row_count()):
            for j in range(self.column_count()):
                self.labels[i][j].config(text=f"{float(self.actual.get_element(i, j)):.3}")
        self.root.update()

    def bold_row(self, row_num):
        row=self.labels[row_num]
        for label in row:
            self.make_bold(label)
    def italic_row(self, row_num):
        row=self.labels[row_num]
        for label in row:
            self.make_italic(label)

    def make_bold(self, label):
        label.config(font=("Helvetica", 18, "bold"))

    def make_italic(self, label):
        label.config(font=("Helvetica", 18, "italic"))

    def reset_label(self, label):
        label.config(font=("Helvetica", 18))

    def reset_row(self, row_num):
        row=self.labels[row_num]
        for label in row:
            self.reset_label(label)

    def write_info(self, info_text: str):
        self.info_label.config(text=info_text)

    def reset_info(self):
        self.info_label.config(text="")


class Worker(threading.Thread):
    def __init__(self, fn):
        threading.Thread.__init__(self)
        self.fn=fn

    def run(self):
        self.fn()



def prepare_inverse(root):
    matrix = SimpleMatrix(4, 4)
    matrix.fill([[1, 1, 1, -1], [1, 1, -1, 1], [1, -1, 1, 1], [-1, 1, 1, 1]])
    matrix = SimpleMatrix(4, 4)
    matrix.fill([[4, 1, 2, -3],
            [-3, 3, -1, 4],
            [-1, 2, 5, 1],
            [5, 4, 3, -1]])
    from FindInverse import find_augmented_matrix, get_inverse_from_augmented_matrix
    augmented = find_augmented_matrix(matrix)
    vis_matrix = VisualizationMatrix(root, augmented)
    return Worker(lambda: get_inverse_from_augmented_matrix(vis_matrix))


def prepare_row_echelon(root):
    matrix = VisualizationMatrix(root, SimpleMatrix(4, 5))
    matrix.fill([[4, 1, 2, -3, -16],
            [-3, 3, -1, 4, 20],
            [-1, 2, 5, 1, -4],
            [5, 4, 3, -1, -10]])
    from RowEchelon import to_row_echelon_form
    return Worker(lambda: to_row_echelon_form(matrix, True))

def visualization_main():
    root = Tk()
    root.title("Matrix inversion, Gauss algorithm")
    #matrix = VisualizationMatrix(root, 5, 5)
    #matrix.set_element(0, 3, 1337)
    #matrix.swap_rows(1, 2)
    #worker = prepare_row_echelon(root)
    worker = prepare_inverse(root)
    worker.start()
    root.mainloop()


if __name__ == '__main__':
    visualization_main()
