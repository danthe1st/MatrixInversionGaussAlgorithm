from enum import Enum


class VisualizationType(Enum):
    REF = 0
    RREF = 1
    INVERSE = 2


operation = VisualizationType.INVERSE
inverse_matrix = [[4, 1, 2, -3],
            [-3, 3, -1, 4],
            [-1, 2, 5, 1],
            [5, 4, 3, -1]]
ref_matrix = [[4, 1, 2, -3, -16],
            [-3, 3, -1, 4, 20],
            [-1, 2, 5, 1, -4],
            [5, 4, 3, -1, -10]]
