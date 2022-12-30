from Matrix import SimpleMatrix
from tkinter import Tk, ttk
import time
import threading


class VisualizationMatrix(SimpleMatrix):

    def __init__(self, root: Tk, row_count: int, col_count: int, sleep_time: int = 1):
        super(VisualizationMatrix, self).__init__(row_count, col_count)
        self.root = root
        self.labels: list[list[ttk.Label]] = []
        for i in range(row_count):
            row = []
            for j in range(col_count):
                label = ttk.Label(root, text=self.get_element(i, j), font=("Helvetica", 18))
                label.grid(row=i, column=j)
                row.append(label)
            self.labels.append(row)
        self.sleep_time=sleep_time

    def swap_rows(self, row1:int, row2:int):
        self.bold_row(row1)
        self.bold_row(row2)
        self.draw()
        time.sleep(self.sleep_time)
        SimpleMatrix.swap_rows(self, row1, row2)
        self.draw()
        time.sleep(self.sleep_time)
        self.reset_row(row1)
        self.reset_row(row2)
        self.draw()

    def multiply_row(self, row_num:int, scalar:float):
        self.bold_row(row_num)
        self.draw()
        time.sleep(self.sleep_time)
        SimpleMatrix.multiply_row(self, row_num, scalar)
        self.draw()
        time.sleep(self.sleep_time)
        self.reset_row(row_num)
        self.draw()

    def multiply_and_add(self, origin_row_num:int, target_row_num:int, scalar:float):
        self.bold_row(origin_row_num)
        self.bold_row(target_row_num)
        self.draw()
        time.sleep(self.sleep_time)
        SimpleMatrix.multiply_and_add(self, origin_row_num, target_row_num, scalar)
        self.draw()
        time.sleep(self.sleep_time)
        self.reset_row(origin_row_num)
        self.reset_row(target_row_num)
        self.draw()

    def get_pivot_column(self, row_num:int)->int:
        column = SimpleMatrix.get_pivot_column(self, row_num)
        if column!=-1:
            for i in range(column):
                self.make_italic(self.labels[row_num][i])
            self.make_bold(self.labels[row_num][column])
            self.draw()
            time.sleep(self.sleep_time)
            self.reset_row(row_num)

        return column

    def set_element(self, row:int, column:int, element:float)->float:
        self.make_bold(self.labels[row][column])
        self.draw()
        SimpleMatrix.set_element(self, row, column, element)
        time.sleep(self.sleep_time)
        self.draw()
        time.sleep(self.sleep_time)
        self.reset_label(self.labels[row][column])
        self.draw()

    def draw(self):
        for i in range(self.row_count()):
            for j in range(self.column_count()):
                self.labels[i][j].config(text=self.get_element(i, j))
        self.root.update()

    def bold_row(self, row_num):
        row=self.labels[row_num]
        for label in row:
            self.make_bold(label)

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

    def fill(self, data:list[list[float]]):
        old_time=self.sleep_time
        self.sleep_time=0
        SimpleMatrix.fill(self, data)
        self.sleep_time=old_time


class Worker(threading.Thread):
    def __init__(self, matrix: VisualizationMatrix):
        threading.Thread.__init__(self)
        self.matrix=matrix

    def run(self):
        # START calculation
        # TODO run calculation
        #e.g.
        #from RowEchelon import to_row_echelon_form
        #to_row_echelon_form(self.matrix)
        self.matrix.get_pivot_value(1)
        self.matrix.swap_rows(0, 1)
        self.matrix.get_pivot_value(2)
        # END calculation
        time.sleep(10)
        self.matrix.root.destroy()


def visualization_main():
    root = Tk()
    #matrix = VisualizationMatrix(root, 5, 5)
    #matrix.set_element(0, 3, 1337)
    #matrix.swap_rows(1, 2)
    matrix = VisualizationMatrix(root, 3, 4)
    matrix.fill([
        [1,2,-2, -15],
        [2,1,-5, -21],
        [1,-4,1, 18]
    ])
    worker=Worker(matrix)
    worker.start()
    root.mainloop()


if __name__ == '__main__':
    visualization_main()
