import argparse
import fractions
import functools
import math
import operator
import os
import shutil
import sys
import textwrap
from phidnet.matrix.matrix import cross, array


class MatrixError(Exception):
    pass



class Matrix:
    def __init__(self, rows, cols, fill=0):   # Initialize a `rows` x `cols` matrix filled with `fill`
        self.numrows = rows
        self.numcols = cols
        self.grid = [[fill for i in range(cols)] for j in range(rows)]



    def __str__(self):   # Returns a string representation of the matrix
        maxlen = max(len(str(e)) for _, _, e in self)
        string = 'matrix[ \n' + '\n'.join(
            ' '.join(str(e).rjust(maxlen) for e in row) for row in self.grid
        )
        string = string + "\n]"
        return textwrap.dedent(string)



    def __repr__(self):   # Returns a string representation of the object
        return '<%s %sx%s 0x%x>' % (
            self.__class__.__name__, self.numrows, self.numcols, id(self)
        )



    def __getitem__(self, index_string):
        type_input = str(type(index_string))
        if type_input == "<class 'str'>":
            row_index, col_index = index_string.split(",")

            if row_index == '' or row_index==":":
                row_start = 0
                row_stop = self.numrows
            elif ':' in row_index:
                row_start, _, row_stop = row_index.partition(":")
                try:
                    row_start = int(row_start)
                    row_stop = int(row_stop)
                except ValueError:
                    print("Bad Data")
            else:
                try:
                    row_start = int(row_index)
                    row_stop = int(row_index) + 1
                except ValueError:
                    print("Bad Data")

            if col_index == '' or col_index == ":":
                col_start = 0
                col_stop = self.numcols
            elif ':' in col_index:
                col_start, _, col_stop = col_index.partition(":")
                try:
                    col_start = int(col_start)
                    col_stop = int(col_stop)
                except ValueError:
                    print("Bad Data")
            else:
                try:
                    col_start = int(col_index)
                    col_stop = int(col_index) + 1
                except ValueError:
                    print("Bad Data")

            return array([self[i][col_start:col_stop] for i in range(row_start,row_stop)])

        else:
            return self.grid[index_string]




    def __contains__(self, item):   # Containment: `item in self`.
        for _, _, element in self:
            if element == item:
                return True
        return False



    def __neg__(self):   # Negative operator: `- self`. Returns a negated copy.
        return self.map(lambda element: -element)



    def __pos__(self):   # Positive operator: `+ self`. Returns a copy.
        return self.map(lambda element: element)



    def __eq__(self, other):   # Equality: `self == other`.
        return self.equals(other)



    def __ne__(self, other):   # Inequality: `self != other`.
        return not self.__eq__(other)



    def __add__(self, other):   # self + other
        if type(other) != Matrix:   # matrix + scalar
            m = Matrix(self.numrows, self.numcols)
            for row, col, element in self:
                m[row][col] = element + other
            return m
        else:   # matrix + matrix
            if not isinstance(other, Matrix):
                raise MatrixError('cannot add %s to a matrix' % type(other))
            if self.numrows != other.numrows or self.numcols != other.numcols:
                raise MatrixError('cannot add matrices of different sizes')
            m = Matrix(self.numrows, self.numcols)
            for row, col, element in self:
                m[row][col] = element + other[row][col]
            return m



    def __sub__(self, other):   # self - other
        if type(other) != Matrix:   # matrix - scalar
            m = Matrix(self.numrows, self.numcols)
            for row, col, element in self:
                m[row][col] = element - other
            return m
        else:   # matrix - matrix
            if not isinstance(other, Matrix):
                raise MatrixError('cannot subtract %s from a matrix' % type(other))
            if self.numrows != other.numrows or self.numcols != other.numcols:
                raise MatrixError('cannot subtract matrices of different sizes')
            m = Matrix(self.numrows, self.numcols)
            for row, col, element in self:
                m[row][col] = element - other[row][col]
            return m



    def __mul__(self, other):   # self * other
        if type(other) != Matrix:   # matrix * scalar
            m = Matrix(self.numrows, self.numcols)
            for row, col, element in self:
                m[row][col] = element * other
            return m
        else:   # matrix * matrix
            if not isinstance(other, Matrix):
                raise MatrixError('cannot multiply %s from a matrix' % type(other))
            if self.numrows != other.numrows or self.numcols != other.numcols:
                raise MatrixError('cannot multiply matrices of different sizes')
            m = Matrix(self.numrows, self.numcols)
            for row, col, element in self:
                m[row][col] = element * other[row][col]
            return m



    def __truediv__(self, other):   # self / other
        if type(other) != Matrix:   # matrix / scalar
            m = Matrix(self.numrows, self.numcols)
            for row, col, element in self:
                m[row][col] = element / other
            return m
        elif type(other) == Matrix:   # matrix / matrix
            if not isinstance(other, Matrix):
                raise MatrixError('cannot multiply %s from a matrix' % type(other))
            if self.numrows != other.numrows or self.numcols != other.numcols:
                raise MatrixError('cannot multiply matrices of different sizes')
            m = Matrix(self.numrows, self.numcols)
            for row, col, element in self:
                m[row][col] = element / other[row][col]
            return m



    def __pow__(self, other):   # Exponentiation: `self ** other`.
        if other >= 1:
            m = self.copy()
            for i in range(other - 1):
                m = m * self
            return m
        elif other == 0:
            m = self.copy()
            return m * 0 + 1



    def __gt__(self, other):
        if type(other) != Matrix:   # matrix  scalar
            m = Matrix(self.numrows, self.numcols)
            for row, col, element in self:
                m[row][col] = element > other
            return m
        else:   # matrix  matrix
            if not isinstance(other, Matrix):
                raise MatrixError('cannot subtract %s from a matrix' % type(other))
            if self.numrows != other.numrows or self.numcols != other.numcols:
                raise MatrixError('cannot subtract matrices of different sizes')
            m = Matrix(self.numrows, self.numcols)
            for row, col, element in self:
                m[row][col] = element > other[row][col]
            return m



    def __lt__(self, other):
        if type(other) != Matrix:   # matrix  scalar
            m = Matrix(self.numrows, self.numcols)
            for row, col, element in self:
                m[row][col] = element < other
            return m
        else:   # matrix  matrix
            if not isinstance(other, Matrix):
                raise MatrixError('cannot subtract %s from a matrix' % type(other))
            if self.numrows != other.numrows or self.numcols != other.numcols:
                raise MatrixError('cannot subtract matrices of different sizes')
            m = Matrix(self.numrows, self.numcols)
            for row, col, element in self:
                m[row][col] = element < other[row][col]
            return m



    def __le__(self, other):
        if type(other) != Matrix:   # matrix  scalar
            m = Matrix(self.numrows, self.numcols)
            for row, col, element in self:
                m[row][col] = element <= other
            return m
        else:   # matrix  matrix
            if not isinstance(other, Matrix):
                raise MatrixError('cannot subtract %s from a matrix' % type(other))
            if self.numrows != other.numrows or self.numcols != other.numcols:
                raise MatrixError('cannot subtract matrices of different sizes')
            m = Matrix(self.numrows, self.numcols)
            for row, col, element in self:
                m[row][col] = element <= other[row][col]
            return m



    def __ge__(self, other):
        if type(other) != Matrix:   # matrix  scalar
            m = Matrix(self.numrows, self.numcols)
            for row, col, element in self:
                m[row][col] = element >= other
            return m
        else:   # matrix  matrix
            if not isinstance(other, Matrix):
                raise MatrixError('cannot subtract %s from a matrix' % type(other))
            if self.numrows != other.numrows or self.numcols != other.numcols:
                raise MatrixError('cannot subtract matrices of different sizes')
            m = Matrix(self.numrows, self.numcols)
            for row, col, element in self:
                m[row][col] = element >= other[row][col]
            return m



    def __iter__(self):
        """ Iteration: `for row, col, element in self`. """
        for row in range(self.numrows):
            for col in range(self.numcols):
                yield row, col, self[row][col]



    def div_by(self, d):   # return d / self
        m = Matrix(self.numrows, self.numcols)
        for row, col, element in self:
            m[row][col] = d / element
        return m



    def to_list(self):
        li = []
        for row in range(self.numrows):
            li.append(self[row])
        return li



    def exp(self):
        if type(self) != Matrix:
            return math.exp(self)
        else:
            m = Matrix(self.numrows, self.numcols)
            for row, col, element in self:
                m[row][col] = math.exp(self[row][col])
            return m



    def argmax(self):
        max = self[0][0]
        for row in range(self.numrows):
            for col in range(self.numcols):
                if (self[row][col] > max):
                    max = self[row][col]
                    maxIdx = [row, col]
        if (row == 0):
            return maxIdx[1]
        else:
            return maxIdx



    def max(self):
        max = self[0][0]
        for row in range(self.numrows):
            for col in range(self.numcols):
                if (self[row][col] > max):
                    max = self[row][col]
        return max



    def log(self):
        if type(self) != Matrix:
            return math.log(self)
        else:
            m = Matrix(self.numrows, self.numcols)
            for row, col, element in self:
                m[row][col] = math.log(self[row][col])
            return m



    def row(self, n):   # Returns an iterator over the specified row.
        for col in range(self.numcols):
            yield self[n][col]



    def col(self, n):   # Returns an iterator over the specified column.
        for row in range(self.numrows):
            yield self[row][n]



    def rows(self):   # Returns a row iterator for each row in the matrix.
        for row in range(self.numrows):
            yield self.row(row)



    def cols(self):   # Returns a column iterator for each column in the matrix.
        for col in range(self.numcols):
            yield self.col(col)



    def rowvec(self, n):   # Returns the specified row as a new row vector.
        v = Matrix(1, self.numcols)
        for col in range(self.numcols):
            v[0][col] = self[n][col]
        return v



    def colvec(self, n):   # Returns the specified column as a new column vector.
        v = Matrix(self.numrows, 1)
        for row in range(self.numrows):
            v[row][0] = self[row][n]
        return v



    def equals(self, other, delta=None):   # Returns true if `self` and `other` are identically-sized matrices and their corresponding elements agree to within `delta`. If `delta` is omitted, we perform a simple equality check (`==`) on corresponding elements instead.
        if self.numrows != other.numrows or self.numcols != other.numcols:
            return False
        if delta:
            for row, col, element in self:
                if abs(element - other[row][col]) > delta:
                    return False
        else:
            for row, col, element in self:
                if element != other[row][col]:
                    return False
        return True



    def copy(self):   # Returns a copy of the matrix.
        return self.map(lambda element: element)



    def trans(self):   # Returns the transpose of the matrix as a new object.
        m = Matrix(self.numcols, self.numrows)
        for row, col, element in self:
            m[col][row] = element
        return m



    def det(self):   # Returns the determinant of the matrix.
        if not self.is_square():
            raise MatrixError('non-square matrix does not have determinant')
        ref, _, multiplier = get_row_echelon_form(self)
        ref_det = functools.reduce(
            operator.mul,
            (ref[i][i] for i in range(ref.numrows))
        )
        return ref_det / multiplier



    def minor(self, row, col):   # Returns the specified minor.
        return self.del_row_col(row, col).det()



    def cofactor(self, row, col):   # Returns the specified cofactor.
        return pow(-1, row + col) * self.minor(row, col)



    def cofactors(self):   # Returns the matrix of cofactors as a new object.
        m = Matrix(self.numrows, self.numcols)
        for row, col, element in self:
            m[row][col] = self.cofactor(row, col)
        return m



    def adjoint(self):   # Returns the adjoint matrix as a new object.
        return self.cofactors().trans()



    def inv(self):   # Returns the inverse matrix if it exists or raises MatrixError.
        if not self.is_square():
            raise MatrixError('non-square matrix cannot have an inverse')
        identity = Matrix.identity(self.numrows)
        rref, inverse = get_reduced_row_echelon_form(self, identity)
        if rref != identity:
            raise MatrixError('matrix is non-invertible')
        return inverse



    def del_row_col(self, row_to_delete, col_to_delete):   # Returns a new matrix with the specified row & column deleted.
        return self.del_row(row_to_delete).del_col(col_to_delete)



    def del_row(self, row_to_delete):   # Returns a new matrix with the specified row deleted.
        m = Matrix(self.numrows - 1, self.numcols)
        for row, col, element in self:
            if row < row_to_delete:
                m[row][col] = element
            elif row > row_to_delete:
                m[row - 1][col] = element
        return m



    def del_col(self, col_to_delete):   # Returns a new matrix with the specified column deleted.
        m = Matrix(self.numrows, self.numcols - 1)
        for row, col, element in self:
            if col < col_to_delete:
                m[row][col] = element
            elif col > col_to_delete:
                m[row][col - 1] = element
        return m



    def map(self, func):   # Forms a new matrix by mapping `func` to each element.
        m = Matrix(self.numrows, self.numcols)
        for row, col, element in self:
            m[row][col] = func(element)
        return m



    def rowop_multiply(self, row, m):   # In-place row operation. Multiplies the specified row by `m`.
        for col in range(self.numcols):
            self[row][col] = self[row][col] * m



    def rowop_swap(self, r1, r2):   # In-place row operation. Interchanges the two specified rows.
        for col in range(self.numcols):
            self[r1][col], self[r2][col] = self[r2][col], self[r1][col]



    def rowop_add(self, r1, m, r2):   # In-place row operation. Adds `m` times row `r2` to row `r1`.
        for col in range(self.numcols):
            self[r1][col] = self[r1][col] + m * self[r2][col]



    def ref(self):   # Returns the row echelon form of the matrix.
        return get_row_echelon_form(self)[0]



    def rref(self):   # Returns the reduced row echelon form of the matrix.
        return get_reduced_row_echelon_form(self)[0]



    def len(self):   # Vectors only. Returns the length of the vector.
        return math.sqrt(sum(e ** 2 for _, _, e in self))



    def dir(self):   # Vectors only. Returns a unit vector in the same direction.
        return (1 / self.len()) * self



    def is_square(self):   # True if the matrix is square.
        return self.numrows == self.numcols



    def is_invertible(self):   # True if the matrix is invertible.
        try:
            inverse = self.inv()
            return True
        except MatrixError:
            return False



    def rank(self):   # Returns the rank of the matrix.
        rank = 0
        for row in self.ref().rows():
            for element in row:
                if element != 0:
                    rank += 1
                    break
        return rank



    def sum(self):
        sum = 0
        for row, col, element in self:
            sum += self[row][col]
        return sum



    def cross(self, other):   # Returns the vector product: `self` x `other`.
        return cross(self, other)



    def elements(self):   # Returns an iterator over the matrix's elements.
        for row in range(self.numrows):
            for col in range(self.numcols):
                yield self[row][col]



    @staticmethod
    def from_list(l):   # Instantiates a new matrix object from a list of lists.
        m = Matrix(len(l), len(l[0]))
        for rownum, row in enumerate(l):
            for colnum, element in enumerate(row):
                m[rownum][colnum] = element
        return m



    @staticmethod
    def from_string(s, rowsep=None, colsep=None, parser=fractions.Fraction):   # Instantiates a new matrix object from a string.
        rows = s.strip().split(rowsep) if rowsep else s.strip().splitlines()
        m = Matrix(len(rows), len(rows[0].split(colsep)))
        for rownum, row in enumerate(rows):
            for colnum, element in enumerate(row.split(colsep)):
                m[rownum][colnum] = parser(element)
        return m



    @staticmethod
    def identity(n):   # Instantiates a new n x n identity matrix.
        m = Matrix(n, n)
        for i in range(n):
            m[i][i] = 1
        return m



# --------------------------------------------------------------------------
# Algorithms
# --------------------------------------------------------------------------



# We determine the row echelon form of the matrix using the forward phase of
# the Gauss-Jordan elimination algorithm. If a `mirror` matrix is supplied,
# we apply the same sequence of row operations to it. Note that neither
# matrix is altered in-place; instead copies are returned.
def get_row_echelon_form(matrix, mirror=None):
    matrix = matrix.copy()
    mirror = mirror.copy() if mirror else None
    det_multiplier = 1

    # Start with the top row and work downwards.
    for top_row in range(matrix.numrows):

        # Find the leftmost column that is not all zeros.
        # Note: this step is sensitive to small rounding errors around zero.
        found = False
        for col in range(matrix.numcols):
            for row in range(top_row, matrix.numrows):
                if matrix[row][col] != 0:
                    found = True
                    break
            if found:
                break
        if not found:
            break

        # Get a non-zero entry at the top of this column.
        if matrix[top_row][col] == 0:
            matrix.rowop_swap(top_row, row)
            det_multiplier *= -1
            if mirror:
                mirror.rowop_swap(top_row, row)

        # Make this entry '1'.
        if matrix[top_row][col] != 1:
            multiplier = 1 / matrix[top_row][col]
            matrix.rowop_multiply(top_row, multiplier)
            matrix[top_row][col] = 1 # assign directly in case of rounding errors
            det_multiplier *= multiplier
            if mirror:
                mirror.rowop_multiply(top_row, multiplier)

        # Make all entries below the leading '1' zero.
        for row in range(top_row + 1, matrix.numrows):
            if matrix[row][col] != 0:
                multiplier = -matrix[row][col]
                matrix.rowop_add(row, multiplier, top_row)
                if mirror:
                    mirror.rowop_add(row, multiplier, top_row)

    return matrix, mirror, det_multiplier



# Determine the reduced row echelon form of the matrix using the Gauss-Jordan
# elimination algorithm. If a `mirror` matrix is supplied, the same sequence
# of row operations will be applied to it. Note that neither matrix is
# altered in-place; instead copies are returned.
def get_reduced_row_echelon_form(matrix, mirror=None):

    # Forward phase: determine the row echelon form.
    matrix, mirror, ignore = get_row_echelon_form(matrix, mirror)

    # The backward phase of the algorithm. For each row, starting at the
    # bottom and working up, find the column containing the leading 1 and
    # make all the entries above it zero.
    for last_row in range(matrix.numrows - 1, 0, -1):
        for col in range(matrix.numcols):
            if matrix[last_row][col] == 1:
                for row in range(last_row):
                    if matrix[row][col] != 0:
                        multiplier = -matrix[row][col]
                        matrix.rowop_add(row, multiplier, last_row)
                        if mirror:
                            mirror.rowop_add(row, multiplier, last_row)
                break

    return matrix, mirror



# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------



# Command line helptext.
helptext = """
Usage: %s [OPTIONS] [FLAGS]
  Matrix analysis utility. Enter a matrix interactively at the terminal or
  pipe to stdin from a file, e.g.
    $ pymatrix < matrix.txt
  Elements are parsed as fractions (rational numbers) by default. An
  alternative parser can be specified using the --parser flag.
Options:
  -p, --parser <str>    One of 'int', 'float', 'complex', 'fraction'.
Flags:
  -h, --help            Print this help text and exit.
  -v, --version         Print the application's version number and exit.
""" % os.path.basename(sys.argv[0])



# Custom argparse action to override the default help text.
class HelpAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        print(helptext.strip())
        sys.exit()



# Read in a matrix interactively from the terminal.
def terminal_input():
    termcols, _ = shutil.get_terminal_size()
    print('─' * termcols)
    print("  Enter a matrix, one row per line. Enter a blank line to end.")
    print('─' * termcols + '\n')
    lines = []
    while True:
        line = input("  ").strip()
        if line:
            lines.append(line)
        else:
            break
    return '\n'.join(lines)



# Analyse a matrix and print a report.
def analyse(matrix):
    rows, cols, rank = matrix.numrows, matrix.numcols, matrix.rank()
    title = '  Rows: %s  ·  Cols: %s  ·  Rank: %s' % (rows, cols, rank)
    termcols, _ = shutil.get_terminal_size()

    if matrix.is_square():
        det = matrix.det()
        title += '  ·  Det: %s' % det

    print('─' * termcols + title + '\n' + '─' * termcols)

    print("\n• Input\n")
    print(textwrap.indent(str(matrix), '  '))

    print("\n• Row Echelon Form\n")
    print(textwrap.indent(str(matrix.ref()), '  '))

    print("\n• Reduced Row Echelon Form\n")
    print(textwrap.indent(str(matrix.rref()), '  '))

    if matrix.is_square():
        if det != 0:
            print("\n• Inverse\n")
            print(textwrap.indent(str(matrix.inv()), '  '))

        print("\n• Cofactors\n")
        print(textwrap.indent(str(matrix.cofactors()), '  '))

    print('\n' + '─' * termcols)



# Entry point for the command line interface.
def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-v', '--version',
        action="version",
        #version=__version__,
    )
    parser.add_argument('-h', '--help',
        action = HelpAction,
        nargs=0,
    )
    parser.add_argument('-p', '--parser',
        help='string parser',
        default='fraction',
    )
    args = parser.parse_args()

    if sys.stdin.isatty():
        string = terminal_input()
    else:
        string = sys.stdin.read()

    options = {
        'fraction': fractions.Fraction,
        'int': int,
        'float': float,
        'complex': complex,
    }

    if args.parser in options:
        analyse(Matrix.from_string(string, parser=options[args.parser]))
    else:
        sys.exit('Error: unknown parser argument.')



if __name__ == '__main__':
    main()