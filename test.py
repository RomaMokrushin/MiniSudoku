from sys import stdin as st


def sudoku_area(rows):
    return f"{''.join(map(lambda x: str(x), rows[0][-1][-1]))}  \n" \
           f"{''.join(map(lambda x: str(x), rows[1][-1][-1]))}  \n" \
           f"{''.join(map(lambda x: str(x), rows[2][-1][-1]))}  \n" \
           f"{''.join(map(lambda x: str(x), rows[3][-1][-1]))}"


def analyze(best_row, cols, squares):
    nums = list(best_row[1][2])
    able = able_row(nums, [1, 2, 3, 4])
    for i in range(4):
        if not nums[i]:
            able_num = able[:]
            for j in sorted(list(set(cols[i][1][2])))[1:]:
                if j in able_num:
                    able_num.remove(j)
            if best_row[0] < 2:
                if i < 2:
                    square = squares[0]
                else:
                    square = squares[1]
            else:
                if i < 2:
                    square = squares[2]
                else:
                    square = squares[3]
            for j in sorted(list(set(square[1][2])))[1:]:
                if j in able_num:
                    able_num.remove(j)
            nums[i] = able_num
    return nums


def solve_sudoku(matrix):
    rows, cols, squares = transformations(matrix)
    best_row = best_row_of_rows(rows, squares)
    if best_row == 'True':
        return sudoku_area(rows)
    able_numbers = analyze(best_row, cols, squares)
    rows.sort()
    rows[best_row[0]][-1][-1] = choose(able_numbers)
    return solve_sudoku(sudoku_area(rows))


def best_for_able(row):
    best_able = 0, 0, 0

    ables = list(filter(lambda x: isinstance(x[1], list), enumerate(row)))
    for i in range(len(ables)):
        c = 0
        for j in range(len(row)):
            if not isinstance(row[j], list):
                if row[j] in ables[i][1]:
                    c += 1
        if c > best_able[1]:
            best_able = ables[i], c
    return best_able[0]


def able_row(nums, able):
    for i in sorted(list(set(nums)))[1:]:
        if i in able:
            able.remove(i)
    return able


def transformations(matrix):
    squares = list()
    rows = list(map(lambda x: (int(x[0]), int(x[1]), int(x[2]), int(x[3])), matrix.split()))
    cols = list(zip(*rows))
    for i in range(0, 3, 2):
        squares.append((rows[i][0], rows[i][1], rows[i + 1][0], rows[i + 1][1]))
        squares.append((rows[i][2], rows[i][3], rows[i + 1][2], rows[i + 1][3]))
    rows = list(
        sorted(list(enumerate(map(lambda x: [all(x), 4 - x.count(0), [x[0], x[1], x[2], x[3]]], rows))),
               key=lambda x: (x[1][0], -x[1][1])))
    cols = list(enumerate(map(lambda x: [all(x), 4 - x.count(0), [x[0], x[1], x[2], x[3]]], cols)))
    squares = list(enumerate(map(lambda x: [all(x), 4 - x.count(0), [x[0], x[1], x[2], x[3]]], squares)))
    return rows, cols, squares


def best_row_of_rows(rows, squares):
    best_row = 'True', 0
    for i in rows:
        if not i[1][0]:
            if i[0] < 2:
                square = squares[:2]
            else:
                square = squares[2:]
            square = sum([i[1][1] for i in square])
            if square > best_row[1]:
                best_row = i, square
    return best_row[0]


def choose(able_numbers):
    indexes = list()
    numbers = able_numbers[:]
    for i in range(len(numbers)):
        if isinstance(numbers[i], list):
            if len(numbers[i]) == 1:
                numbers[i] = numbers[i][0]
            else:
                indexes.append(i)
    if all(map(lambda x: not isinstance(x, list), numbers)):
        return numbers
    id, best_able = best_for_able(numbers)
    for i in range(len(indexes)):
        indexes[i] = indexes[i], numbers[indexes[i]]
        numbers[indexes[i][0]] = 0
    indexes.remove((id, best_able))
    numbers[id] = able_row(numbers, able=best_able)
    for i in indexes:
        numbers[i[0]] = i[1]
    return choose(numbers)


print(solve_sudoku(''.join(list(st.readlines()))))
