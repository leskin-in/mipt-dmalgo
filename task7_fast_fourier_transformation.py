#!/usr/bin/env python3

import math


def main():
    coeffs = list(map(float, input().split()))
    coeffs = [complex(coeff, 0.0) for coeff in coeffs]

    result = fast_fourier_transform(coeffs)

    print(' '.join([f'{r.real},{r.imag}' for r in result]))


def fast_fourier_transform(coeffs: list) -> list:
    """
    Conduct a fast Fourier transformation on the given 'coeffs' polynomial
    :return: result of the fourier transformation
    """
    result = [complex(0.0, 0.0) for _ in range(len(coeffs))]

    if len(coeffs) == 1:
        result[0] = coeffs[0]
        return result

    coeffs_0 = fast_fourier_transform([coeffs[i * 2] for i in range(len(coeffs) // 2)])
    coeffs_1 = fast_fourier_transform([coeffs[i * 2 + 1] for i in range(len(coeffs) // 2)])

    w = complex(1.0, 0.0)
    wn = complex(math.cos((2.0 * math.pi) / len(coeffs)), math.sin((2.0 * math.pi) / len(coeffs)))

    for i in range(len(coeffs) // 2):
        result[i] = coeffs_0[i] + w * coeffs_1[i]
        result[i + (len(coeffs) // 2)] = coeffs_0[i] - w * coeffs_1[i]
        w *= wn

    return result


if __name__ == '__main__':
    main()
