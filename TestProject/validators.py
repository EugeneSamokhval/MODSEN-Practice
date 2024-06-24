import re


def is_point(user_input: str):
    pattern = r"\[\d+,\s+\d+\]"
    return bool(re.fullmatch(pattern, user_input))


def is_pos_digital(user_input: str):
    try:
        if int(user_input) > 0:
            return True
        else:
            return False
    except:
        return False


print(is_pos_digital("-dqav"))
