from Matrix import Matrix, SimpleMatrix
from tkinter import *
from tkinter import ttk
import time
import threading


class VisualizationMatrix(SimpleMatrix):

    def __init__(self, root: Tk, row_count: int, col_count: int):
        super(VisualizationMatrix, self).__init__(row_count, col_count)
        self.root = root
        self.labels: list[list[Label]] = []
        for i in range(row_count):
            row = []
            for j in range(col_count):
                label = ttk.Label(root, text=self.get_element(i, j), font=("Helvetica", 18))
                label.grid(row=i, column=j)
                row.append(label)
            self.labels.append(row)

    def swap_rows(self, row1:int, row2:int):
        self.bold_row(row1)
        self.bold_row(row2)
        self.draw()
        time.sleep(1)
        SimpleMatrix.swap_rows(self, row1, row2)
        self.draw()
        time.sleep(1)
        self.reset_row(row1)
        self.reset_row(row2)
        self.draw()

    def multiply_row(self, row_num:int, scalar:float):
        self.bold_row(row_num)
        self.draw()
        time.sleep(1)
        SimpleMatrix.multiply_row(self, row_num, scalar)
        self.draw()
        time.sleep(1)
        self.reset_row(row_num)
        self.draw()

    def multiply_and_add(self, origin_row_num:int, target_row_num:int, scalar:float):
        self.bold_row(origin_row_num)
        self.bold_row(target_row_num)
        self.draw()
        time.sleep(1)
        SimpleMatrix.multiply_and_add(self, origin_row_num, target_row_num, scalar)
        self.draw()
        time.sleep(1)
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
            time.sleep(1)
            self.reset_row(row_num)

        return column


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


class Worker(threading.Thread):
    def __init__(self, matrix: VisualizationMatrix):
        threading.Thread.__init__(self)
        self.matrix=matrix

    def run(self):
        # TODO run calculation
        while True:
            self.matrix.swap_rows(0,1)
            self.matrix.set_element(0, 2, self.matrix.get_element(0, 0)+1)
            self.matrix.multiply_and_add(1,0,2)
            self.matrix.get_pivot_value(0)
        self.matrix.root.destroy()


def main():
    root = Tk()
    matrix = VisualizationMatrix(root, 5, 5)
    matrix.set_element(0, 3, 1337)
    matrix.swap_rows(1, 2)
    worker=Worker(matrix)
    worker.start()
    root.mainloop()


if __name__ == '__main__':
    main()
