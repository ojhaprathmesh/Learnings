# def function():
#     print("Hello World")
#
#
# func = function  # This Creates A New Copy
# del function  # So Deleting Original Function Does Not Affect The New Function
# func()


def funcReturn(num):
    if num == 0:
        return sum

    if num == 1:
        return print


a = funcReturn(0)
print(a)

a = funcReturn(1)
print(a)


def executor(func):
    func("This")


executor(print)


def decorate(func):
    def nowExec():
        print("Executing Now")
        func()
        print("Executed")

    return nowExec


@decorate
def whoAreYou():
    print("Harry Is A Good Boy")


# whoAreYou = decorate(whoAreYou)
whoAreYou()
