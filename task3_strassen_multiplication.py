#!/usr/bin/env python3

import math


class Int9:
    """
    An integer over Z9 (module 9) field
    """
    def __init__(self, n: int):
        self.n = n % 9

    def __add__(self, other):
        return Int9(self.n + other.n)

    def __sub__(self, other):
        return Int9(self.n - other.n)

    def __mul__(self, other):
        return Int9(self.n * other.n)

    def __int__(self):
        return self.n

    def __str__(self):
        return str(self.n)

    def __repr__(self):
        return 'Int9({})'.format(self.n)


class Mat9:
    """
    A matrix over Z9 (module 9) field.
    Several limitations apply to the matrix structure:
    * Matrix must be a square matrix
    * Matrix size must be a power of two
    """
    def __init__(self, m: list):
        if type(m[0][0]) != Int9:
            raise Exception("Mat9 constructor must be provided with a 2-dimensional list of Int9")
        if len(m) != len(m[0]):
            raise Exception("Non-square matrixes are not supported. Provided matrix: {}".format(m))

        self.m = m
        self.L = len(m)

    def __add__(self, other):
        if self.L != other.L:
            raise Exception(
                "__add__ is called on matrixes of different size. Arguments: {}; {}".format(self.m, other.m)
            )

        return Mat9([[self.m[i1][i2] + other.m[i1][i2] for i2 in range(self.L)] for i1 in range(self.L)])

    def __sub__(self, other):
        if self.L != other.L:
            raise Exception(
                "__sub__ is called on matrixes of different size. Arguments: {}; {}".format(self.m, other.m)
            )

        return Mat9([[self.m[i1][i2] - other.m[i1][i2] for i2 in range(self.L)] for i1 in range(self.L)])

    @staticmethod
    def _mul2(a, b):
        """
        Calculate __mul__ for matrixes of size 2
        :return: A Mat9 - product of a and b
        """
        a11 = a.m[0][0]
        a12 = a.m[0][1]
        a21 = a.m[1][0]
        a22 = a.m[1][1]

        b11 = b.m[0][0]
        b12 = b.m[0][1]
        b21 = b.m[1][0]
        b22 = b.m[1][1]

        m1 = (a11 + a22) * (b11 + b22)
        m2 = (a21 + a22) * b11
        m3 = a11 * (b12 - b22)
        m4 = a22 * (b21 - b11)
        m5 = (a11 + a12) * b22
        m6 = (a21 - a11) * (b11 + b12)
        m7 = (a12 - a22) * (b21 + b22)

        c11 = m1 + m4 - m5 + m7
        c12 = m3 + m5
        c21 = m2 + m4
        c22 = m1 - m2 + m3 + m6

        return Mat9([[c11, c12], [c21, c22]])

    @staticmethod
    def _mul(a, b):
        """
        Calculate __mul__ using Strassen algorithm
        :return: A Mat9 - product of a and b
        """
        l_div = a.L // 2

        a11 = Mat9([a.m[i][:l_div] for i in range(0, l_div)])
        a12 = Mat9([a.m[i][l_div:] for i in range(0, l_div)])
        a21 = Mat9([a.m[i][:l_div] for i in range(l_div, a.L)])
        a22 = Mat9([a.m[i][l_div:] for i in range(l_div, a.L)])

        b11 = Mat9([b.m[i][:l_div] for i in range(0, l_div)])
        b12 = Mat9([b.m[i][l_div:] for i in range(0, l_div)])
        b21 = Mat9([b.m[i][:l_div] for i in range(l_div, b.L)])
        b22 = Mat9([b.m[i][l_div:] for i in range(l_div, b.L)])

        m1 = (a11 + a22) * (b11 + b22)
        m2 = (a21 + a22) * b11
        m3 = a11 * (b12 - b22)
        m4 = a22 * (b21 - b11)
        m5 = (a11 + a12) * b22
        m6 = (a21 - a11) * (b11 + b12)
        m7 = (a12 - a22) * (b21 + b22)

        c11 = m1 + m4 - m5 + m7
        c12 = m3 + m5
        c21 = m2 + m4
        c22 = m1 - m2 + m3 + m6

        for i in range(l_div):
            c11.m[i].extend(c12.m[i])
            c21.m[i].extend(c22.m[i])
        c11.m.extend(c21.m)
        c11.L = c11.L * 2

        return c11

    def __mul__(self, other):
        if self.L != other.L:
            raise Exception(
                "__mul__ is called on matrixes of different size. Arguments: {}; {}".format(self.m, other.m)
            )

        if self.L == 1:
            return Mat9([[self.m[0][0] * other.m[0][0]]])

        if self.L == 2:
            return Mat9._mul2(self, other)

        return Mat9._mul(self, other)

    def __pow__(self, power, modulo=None):
        if power == 0:
            return Mat9([[Int9(1) if i == j else Int9(0) for i in range(self.L)] for j in range(self.L)])

        if power == 1:
            return self

        if power % 2 != 0:
            return (self ** (power - 1)) * self

        self_halfpow = self ** (power / 2)
        return self_halfpow * self_halfpow


def main():
    m = [list(map(lambda n: Int9(n), list(map(int, input().split()))))]
    for i in range(len(m[0]) - 1):
        m.append(list(map(lambda n: Int9(n), list(map(int, input().split())))))

    m_size = len(m)
    m_size_pow_2 = 2 ** int(math.ceil(math.log2(len(m))))
    if m_size_pow_2 != m_size:
        for i in range(m_size):
            m[i].extend([Int9(0) for _ in range(m_size_pow_2 - m_size)])
        m.extend([[Int9(0) for _ in range(m_size_pow_2)] for _ in range(m_size_pow_2 - m_size)])

    m9 = Mat9(m)
    result_noncut = m9 ** m_size

    result_printable = '\n'.join(
        [' '.join([
            str(result_noncut.m[i][j]) for j in range(m_size)
        ]) for i in range(m_size)]
    )

    print(result_printable)


if __name__ == '__main__':
    main()
