def to_list(string: str) -> list[int]:
    return list(map(int, string.split()))


def intersection(list1: list[int], list2: list[int]) -> None:
    table = {}
    result = []

    for num in list1:
        table[num] = table.get(num, 0) + 1

    for num in list2:
        if num in table and table[num] > 0:
            result.append(num)
            table[num] -= 1

    print(sorted(result))


size = int(input())
arr1 = to_list(input())
arr2 = to_list(input())

intersection(arr1, arr2)
