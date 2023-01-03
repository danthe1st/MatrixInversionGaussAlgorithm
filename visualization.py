from Matrix import SimpleMatrix
from tkinter import Tk, ttk
import time
import threading


class VisualizationMatrix(SimpleMatrix):

    def __init__(self, root: Tk, row_count: int, col_count: int, sleep_time: int = 2):
        super(VisualizationMatrix, self).__init__(row_count, col_count)
        self.root = root
        self.labels: list[list[ttk.Label]] = []
        self.detail_labels: list[ttk.Label] = []
        for i in range(col_count):
            root.columnconfigure(i, minsize=75)
            label = ttk.Label(root, text="", font=("Helvetica"))
            label.grid(row=row_count+2, column=i)
            self.detail_labels.append(label)
        for i in range(row_count):
            row = []
            root.rowconfigure(i, weight=1)
            for j in range(col_count):
                label = ttk.Label(root, text=SimpleMatrix.get_element(self, i, j), font=("Helvetica", 18))
                label.grid(row=i, column=j)
                row.append(label)
            self.labels.append(row)
        root.rowconfigure(row_count, weight=1)
        self.info_label=ttk.Label(root, text="", font=("Helvetica"))
        self.info_label.grid(row=row_count, columnspan=col_count)
        self.sleep_time=sleep_time

    def swap_rows(self, row1:int, row2:int):
        self.write_info(f"Swap rows {row1} and {row2}")
        self.bold_row(row1)
        self.bold_row(row2)
        self.draw()
        time.sleep(self.sleep_time)
        SimpleMatrix.swap_rows(self, row1, row2)
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
        SimpleMatrix.multiply_row(self, row_num, scalar)
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
            self.detail_labels[i].config(text=f"{float(SimpleMatrix.get_element(self, origin_row_num, i)*scalar):.3}")
        self.draw()
        time.sleep(3*self.sleep_time)
        SimpleMatrix.multiply_and_add(self, origin_row_num, target_row_num, scalar)
        self.draw()
        time.sleep(2*self.sleep_time)
        for i in range(self.column_count()):
            self.detail_labels[i].config(text="")
        self.reset_row(origin_row_num)
        self.reset_row(target_row_num)
        self.reset_info()
        self.draw()

    def get_pivot_column(self, row_num:int)->int:
        column = SimpleMatrix.get_pivot_column(self, row_num)
        if column!=-1:
            for i in range(column):
                self.make_italic(self.labels[row_num][i])
            self.make_bold(self.labels[row_num][column])
            self.write_info(f"Pivot of row {row_num} is {SimpleMatrix.get_element(self,row_num, column)} (column {column})")
            self.draw()
            time.sleep(self.sleep_time)
            self.reset_row(row_num)
            self.reset_info()
        return column

    def set_element(self, row:int, column:int, element:float)->float:
        if(self.sleep_time!=0):
            self.make_bold(self.labels[row][column])
            self.write_info(f"Set element of row {row}/column {column} to {float(element):.4}")
            self.draw()
        SimpleMatrix.set_element(self, row, column, element)
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
        ret = SimpleMatrix.get_element(self, row, column)
        self.draw()
        time.sleep(self.sleep_time/3)
        self.reset_label(self.labels[row][column])
        return ret

    def fill(self, data:list[list[float]]):
        self.write_info(f"reset/overwrite matrix")
        self.draw()
        time.sleep(self.sleep_time)
        old_time=self.sleep_time
        self.sleep_time=0
        SimpleMatrix.fill(self, data)
        self.reset_info()
        self.sleep_time=old_time
        time.sleep(self.sleep_time)

    def draw(self):
        for i in range(self.row_count()):
            for j in range(self.column_count()):
                self.labels[i][j].config(text=f"{float(SimpleMatrix.get_element(self, i, j)):.3}")
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
    def __init__(self, matrix: VisualizationMatrix):
        threading.Thread.__init__(self)
        self.matrix=matrix

    def run(self):
        # START calculation
        # TODO run calculation
        #e.g.
        from RowEchelon import to_row_echelon_form
        to_row_echelon_form(self.matrix, True)
        #self.matrix.get_pivot_value(1)
        #self.matrix.swap_rows(0, 1)
        #self.matrix.get_pivot_value(2)
        #self.matrix.multiply_and_add(1, 2, 0.5)
        # END calculation
        time.sleep(10)
        self.matrix.root.destroy()


def visualization_main():
    root = Tk()
    root.title("Matrix inversion, Gauss algorithm")
    #matrix = VisualizationMatrix(root, 5, 5)
    #matrix.set_element(0, 3, 1337)
    #matrix.swap_rows(1, 2)
    matrix = VisualizationMatrix(root, 4,5)
    matrix.fill([
        [4,1,2,-3,-16],
        [-3,3,-1,4,20],
        [-1,2,5,1,-4],
        [5,4,3,-1,-10]
    ])
    worker=Worker(matrix)
    worker.start()
    root.mainloop()


if __name__ == '__main__':
    visualization_main()
