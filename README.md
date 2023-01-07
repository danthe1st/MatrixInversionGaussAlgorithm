# Matrix Inversion/Gauss algorithm

This repository contains an implementation of Row-Echelon form and Matrix inversion using the Gauss algorithm and corresponding visualizations.

The file `Matrix.py` contains a base class for matrices allowing row operations named `Matrix` and a class `SimpleMatrix` which implements these operations based on arrays.

## Row-Echelon
The file `RowEchelon.py` is responsible for converting a `Matrix` to Row-Echelon form using a function `to_row_echelon_form()` using row transformations.

A matrix is in Row-Echelon form if
- The first element of the first row is `1`.
- All other rows start with zeros followed by a "leading" `1` followed by arbitrary numbers.
- The leading `1` of any row is to the right of the leading `1` of the previous row.

If a parameter `reduced` is set to `True`, the Matrix is instead converted to Reduced Row-Echelon form.

A matrix is in Reduced Row-Echelon form if
- It is in Row-Echelon form.
- In every column that contains a leading `1`, all other numbers are `0`.

## Inversion
The file `FindInverse.py` is responsible for calculating the inverse of a matrix using the function `get_inverse()`.

The inverse of a matrix is the matrix that, multiplied with the original matrix, yields the identity matrix.

## Visualization
The file `visualization.py` provides a visualization of the algorithms using TKinter.
For this, it uses a custom `Matrix` implementation named `VisualizationMatrix` which wraps another matrix implementation and can display the matrix and provide visual indicators for changes applied to it.
This custom `Matrix` implementation is also able to slow down the calulation so that it can be watched by humans.