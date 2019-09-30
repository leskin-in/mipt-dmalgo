#!/usr/bin/env python3


def gate_AND(input1: int, input2: int, output: int) -> str:
    return 'GATE {} AND {} {}'.format(output, input1, input2)


def gate_OR(input1: int, input2: int, output: int) -> str:
    return 'GATE {} OR {} {}'.format(output, input1, input2)


def gate_NOT(input1: int, output: int) -> str:
    return 'GATE {} NOT {}'.format(output, input1)


def gate_OUTPUT(from_id: int, output_id: int) -> str:
    return 'OUTPUT {} {}'.format(output_id, from_id)


def generate_2_3_block(index: int, n: int, block_start: int) -> (str, int):
    """
    Generate a 2-3 block

    :param index: digit index in each of three input numbers
    :param n: number of digits in a number
    :param block_start: gate index of a block to start this block with

    :return: generated block and next 'block_start'
    """
    a = index
    b = index + n
    c = index + 2 * n

    nodes = []
    new_node = block_start

    # Upper bit

    nodes.append(tuple([new_node, gate_AND(a, b, new_node)]))  # 0
    new_node += 1

    nodes.append(tuple([new_node, gate_OR(a, b, new_node)]))  # 1
    new_node += 1

    nodes.append(tuple([new_node, gate_AND(nodes[1][0], c, new_node)]))  # 2
    new_node += 1

    nodes.append(tuple([new_node, gate_OR(nodes[0][0], nodes[2][0], new_node)]))  # 3
    new_node += 1

    # Lower bit

    nodes.append(tuple([new_node, gate_NOT(nodes[0][0], new_node)]))  # 4
    new_node += 1

    nodes.append(tuple([new_node, gate_AND(nodes[4][0], nodes[1][0], new_node)]))  # 5
    new_node += 1

    nodes.append(tuple([new_node, gate_AND(nodes[5][0], c, new_node)]))  # 6
    new_node += 1

    nodes.append(tuple([new_node, gate_OR(nodes[5][0], c, new_node)]))  # 7
    new_node += 1

    nodes.append(tuple([new_node, gate_NOT(nodes[6][0], new_node)]))  # 8
    new_node += 1

    nodes.append(tuple([new_node, gate_AND(nodes[8][0], nodes[7][0], new_node)]))  # 9
    new_node += 1

    # Upper bit number
    nodes.append(tuple([-1, gate_OUTPUT(nodes[3][0], index + 1)]))
    # Lower bit number
    nodes.append(tuple([-1, gate_OUTPUT(nodes[9][0], (n + 1) + index)]))

    result = '\n'.join([node[1] for node in nodes])
    return result, new_node


def generate_zero_block(n: int, block_start: int) -> (str, int):
    """
    Generate a special block for zero-padding of upper and lower bit numbers.
    An implicit assumption is made that at least one input node (with index 0)
    exists.

    :param n: number of digits in a number
    :param block_start: gate index of a block to start this block with

    :return: generated block and next 'block_start'
    """
    nodes = []
    new_node = block_start

    nodes.append(tuple([new_node, gate_NOT(0, new_node)]))  # 0
    new_node += 1

    nodes.append(tuple([new_node, gate_AND(0, nodes[0][0], new_node)]))  # 1
    new_node += 1

    # Upper bit number padding (least significant bit)
    nodes.append(tuple([-1, gate_OUTPUT(nodes[1][0], 0)]))
    # Lower bit number padding (most significant bit)
    nodes.append(tuple([-1, gate_OUTPUT(nodes[1][0], 2 * (n + 1) - 1)]))

    result = '\n'.join(node[1] for node in nodes)
    return result, new_node


def main():
    n = int(input())

    blocks = []
    block = None
    block_start = n * 3
    for i in range(n):
        block, block_start = generate_2_3_block(i, n, block_start)
        blocks.append(block)

    block, block_start = generate_zero_block(n, block_start)
    blocks.append(block)

    result = '\n'.join(blocks)
    print(result)


if __name__ == '__main__':
    main()
