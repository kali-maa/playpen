import os
import sys


# A modified version of the same function in Day 2.
def process_opcode(opcode_in, inbuf=None, outbuf=sys.stdout, debug=False):
    opcode_list = opcode_in.copy()
    n = len(opcode_list)
    i_list = 0

    def _get_val(mode, idx):
        if mode == 0:  # position mode
            val = opcode_list[opcode_list[idx]]
        elif mode == 1:  # immediate mode
            val = opcode_list[idx]
        else:
            raise ValueError(f'Invalid parameter mode={mode}')
        return val

    while i_list < n:
        instruction = opcode_list[i_list]
        if debug:
            print(f'instructions={instruction}')

        cur_opcode = instruction % 100  # 2 right-most digits
        pars = list(map(int, [c for c in str(int(instruction / 100))]))
        n_pars = len(pars)
        max_pars = 3
        if n_pars < max_pars:  # leading zeroes
            for i in range(max_pars - n_pars):
                pars.insert(0, 0)

        if cur_opcode == 99:
            outbuf.write('exit' + os.linesep)
            if debug:
                print('***** EXIT *****')
            break
        elif cur_opcode == 1:  # sum
            x1 = _get_val(pars[2], i_list + 1)
            x2 = _get_val(pars[1], i_list + 2)
            opcode_list[opcode_list[i_list + 3]] = x1 + x2
            i_list += 4
        elif cur_opcode == 2:  # multiply
            x1 = _get_val(pars[2], i_list + 1)
            x2 = _get_val(pars[1], i_list + 2)
            opcode_list[opcode_list[i_list + 3]] = x1 * x2
            i_list += 4
        elif cur_opcode == 3:  # input
            if inbuf is None:
                x = input('Enter input (int): ')
            else:
                x = inbuf.readline()
                if debug:
                    print(f'input={x}')
            opcode_list[opcode_list[i_list + 1]] = int(x)
            i_list += 2
        elif cur_opcode == 4:  # output
            x1 = _get_val(pars[2], i_list + 1)
            if debug:
                print(f'output={x1}')
            outbuf.write(str(x1) + os.linesep)
            i_list += 2
        elif cur_opcode == 5:  # jump if true
            x1 = _get_val(pars[2], i_list + 1)
            x2 = _get_val(pars[1], i_list + 2)
            if x1 != 0:
                i_list = x2
            else:
                i_list += 3
        elif cur_opcode == 6:  # jump if false
            x1 = _get_val(pars[2], i_list + 1)
            x2 = _get_val(pars[1], i_list + 2)
            if x1 == 0:
                i_list = x2
            else:
                i_list += 3
        elif cur_opcode == 7:  # less than
            x1 = _get_val(pars[2], i_list + 1)
            x2 = _get_val(pars[1], i_list + 2)
            if x1 < x2:
                opcode_list[opcode_list[i_list + 3]] = 1
            else:
                opcode_list[opcode_list[i_list + 3]] = 0
            i_list += 4
        elif cur_opcode == 8:  # equal
            x1 = _get_val(pars[2], i_list + 1)
            x2 = _get_val(pars[1], i_list + 2)
            if x1 == x2:
                opcode_list[opcode_list[i_list + 3]] = 1
            else:
                opcode_list[opcode_list[i_list + 3]] = 0
            i_list += 4
        else:
            raise ValueError(f'Unsupported opcode={cur_opcode}')

    return opcode_list


def main():
    # Part 1 & 2
    puzzle = [3,225,1,225,6,6,1100,1,238,225,104,0,101,71,150,224,101,-123,224,224,4,224,102,8,223,223,101,2,224,224,1,224,223,223,2,205,209,224,1001,224,-3403,224,4,224,1002,223,8,223,101,1,224,224,1,223,224,223,1101,55,24,224,1001,224,-79,224,4,224,1002,223,8,223,101,1,224,224,1,223,224,223,1,153,218,224,1001,224,-109,224,4,224,1002,223,8,223,101,5,224,224,1,224,223,223,1002,201,72,224,1001,224,-2088,224,4,224,102,8,223,223,101,3,224,224,1,223,224,223,1102,70,29,225,102,5,214,224,101,-250,224,224,4,224,1002,223,8,223,1001,224,3,224,1,223,224,223,1101,12,52,225,1101,60,71,225,1001,123,41,224,1001,224,-111,224,4,224,102,8,223,223,1001,224,2,224,1,223,224,223,1102,78,66,224,1001,224,-5148,224,4,224,1002,223,8,223,1001,224,2,224,1,223,224,223,1101,29,77,225,1102,41,67,225,1102,83,32,225,1101,93,50,225,1102,53,49,225,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,1107,677,677,224,1002,223,2,223,1005,224,329,101,1,223,223,7,677,677,224,1002,223,2,223,1005,224,344,1001,223,1,223,7,226,677,224,102,2,223,223,1006,224,359,101,1,223,223,1108,226,226,224,1002,223,2,223,1005,224,374,1001,223,1,223,8,226,677,224,1002,223,2,223,1006,224,389,1001,223,1,223,1108,226,677,224,1002,223,2,223,1006,224,404,101,1,223,223,1107,677,226,224,102,2,223,223,1006,224,419,101,1,223,223,1007,677,677,224,1002,223,2,223,1005,224,434,101,1,223,223,7,677,226,224,102,2,223,223,1006,224,449,1001,223,1,223,1008,226,677,224,1002,223,2,223,1006,224,464,101,1,223,223,8,677,677,224,1002,223,2,223,1006,224,479,101,1,223,223,108,226,226,224,102,2,223,223,1005,224,494,101,1,223,223,1107,226,677,224,1002,223,2,223,1006,224,509,101,1,223,223,107,226,226,224,1002,223,2,223,1006,224,524,1001,223,1,223,107,677,677,224,1002,223,2,223,1005,224,539,101,1,223,223,1007,226,226,224,102,2,223,223,1006,224,554,101,1,223,223,108,677,677,224,102,2,223,223,1005,224,569,101,1,223,223,107,677,226,224,102,2,223,223,1005,224,584,101,1,223,223,1008,226,226,224,102,2,223,223,1006,224,599,101,1,223,223,1108,677,226,224,1002,223,2,223,1006,224,614,101,1,223,223,8,677,226,224,102,2,223,223,1005,224,629,1001,223,1,223,1008,677,677,224,102,2,223,223,1006,224,644,101,1,223,223,1007,226,677,224,102,2,223,223,1005,224,659,101,1,223,223,108,226,677,224,102,2,223,223,1006,224,674,101,1,223,223,4,223,99,226]  # noqa
    process_opcode(puzzle)


if __name__ == '__main__':
    main()
