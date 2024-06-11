def zero(func=None):
    if not func:
        return 0
    else:
        return func[0](0, func[1])


def one(func=None):
    if not func:
        return 1
    else:
        return func[0](1, func[1])


def two(func=None):
    if not func:
        return 2
    else:
        return func[0](2, func[1])


def three(func=None):
    if not func:
        return 3
    else:
        return func[0](3, func[1])


def four(func=None):
    if not func:
        return 4
    else:
        return func[0](4, func[1])


def five(func=None):
    if not func:
        return 5
    else:
        return func[0](5, func[1])


def six(func=None):
    if not func:
        return 6
    else:
        return func[0](6, func[1])


def seven(func=None):
    if not func:
        return 7
    else:
        return func[0](7, func[1])


def eight(func=None):
    if not func:
        return 8
    else:
        return func[0](8, func[1])


def nine(func=None):
    if not func:
        return 9
    else:
        return func[0](9, func[1])


def plus(a, b=None):
    if b == None:
        return plus, a
    else:
        return a+b


def minus(a, b=None):
    if b == None:
        return minus, a
    else:
        return a-b


def times(a, b=None):
    if b == None:
        return times, a
    else:
        return a*b


def divided_by(a, b=None):
    if b == None:
        return divided_by, a
    else:
        return a//b


print(nine(times(zero())))
