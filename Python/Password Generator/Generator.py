import string
import timeit

# Record start time
start_time = timeit.default_timer()

workString = ''
checkList = list(string.printable[:-6:])
pwd = 'Adity@561~>"%!rhn'
ascend = 0

for c1 in checkList:
    if workString == pwd:
        break
    if c1 != pwd[ascend:ascend + 1]:
        continue
    else:
        ascend += 1
        for c2 in checkList:
            if workString == pwd:
                break
            if c2 != pwd[ascend:ascend + 1]:
                continue
            else:
                ascend += 1
                for c3 in checkList:
                    if workString == pwd:
                        break
                    if c3 != pwd[ascend:ascend + 1]:
                        continue
                    else:
                        ascend += 1
                        for c4 in checkList:
                            if workString == pwd:
                                break
                            if c4 != pwd[ascend:ascend + 1]:
                                continue
                            else:
                                ascend += 1
                                for c5 in checkList:
                                    if workString == pwd:
                                        break
                                    if c5 != pwd[ascend:ascend + 1]:
                                        continue
                                    else:
                                        ascend += 1
                                        for c6 in checkList:
                                            if workString == pwd:
                                                break
                                            if c6 != pwd[ascend:ascend + 1]:
                                                continue
                                            else:
                                                ascend += 1
                                                for c7 in checkList:
                                                    if workString == pwd:
                                                        break
                                                    if c7 != pwd[ascend:ascend + 1]:
                                                        continue
                                                    else:
                                                        ascend += 1
                                                        for c8 in checkList:
                                                            if workString == pwd:
                                                                break
                                                            if c8 != pwd[ascend:ascend + 1]:
                                                                continue
                                                            else:
                                                                ascend += 1
                                                                for c9 in checkList:
                                                                    if workString == pwd:
                                                                        break
                                                                    if c9 != pwd[ascend:ascend + 1]:
                                                                        continue
                                                                    else:
                                                                        ascend += 1
                                                                        for c10 in checkList:
                                                                            if workString == pwd:
                                                                                break
                                                                            if c10 != pwd[ascend:ascend + 1]:
                                                                                continue
                                                                            else:
                                                                                ascend += 1
                                                                                for c11 in checkList:
                                                                                    if workString == pwd:
                                                                                        break
                                                                                    if c11 != pwd[ascend:ascend + 1]:
                                                                                        continue
                                                                                    else:
                                                                                        ascend += 1
                                                                                        for c12 in checkList:
                                                                                            if workString == pwd:
                                                                                                break
                                                                                            if c12 != pwd[
                                                                                                      ascend:ascend + 1]:
                                                                                                continue
                                                                                            else:
                                                                                                ascend += 1
                                                                                                for c13 in checkList:
                                                                                                    if workString == pwd:
                                                                                                        break
                                                                                                    if c13 != pwd[
                                                                                                              ascend:ascend + 1]:
                                                                                                        continue
                                                                                                    else:
                                                                                                        ascend += 1
                                                                                                        for c14 in checkList:
                                                                                                            if workString == pwd:
                                                                                                                break
                                                                                                            if c14 != pwd[
                                                                                                                      ascend:ascend + 1]:
                                                                                                                continue
                                                                                                            else:
                                                                                                                ascend += 1
                                                                                                                for c15 in checkList:
                                                                                                                    if workString == pwd:
                                                                                                                        break
                                                                                                                    if c15 != pwd[
                                                                                                                              ascend:ascend + 1]:
                                                                                                                        continue
                                                                                                                    else:
                                                                                                                        ascend += 1
                                                                                                                        for c16 in checkList:
                                                                                                                            if workString == pwd:
                                                                                                                                break
                                                                                                                            if c16 != pwd[
                                                                                                                                      ascend:ascend + 1]:
                                                                                                                                continue
                                                                                                                            else:
                                                                                                                                for c17 in checkList:
                                                                                                                                    workString = c1 + c2 + c3 + c4 + c5 + c6 + c7 + c8 + c9 + c10 + c11 + c12 + c13 + c14 + c15 + c16 + c17
                                                                                                                                    if workString == pwd:
                                                                                                                                        print(
                                                                                                                                            "\033[1;32;1m\t\t\n\nMatch Found\n\033[0m")
                                                                                                                                        break
                                                                                                                                    else:
                                                                                                                                        print(
                                                                                                                                            f"\033[1;31;1m\t\t{workString}\033[0m")

# Record end time
end_time = timeit.default_timer()

# Calculate elapsed time
elapsed_time = end_time - start_time

print(f"Time taken: {elapsed_time} seconds")