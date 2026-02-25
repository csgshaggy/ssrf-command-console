# plugins/math_tools.py

def get_modes():
    return {
        "math_double": {
            "description": "Double a number",
            "options": {}
        },
        "math_square": {
            "description": "Square a number",
            "options": {}
        }
    }


def run(mode_name, target, options):
    try:
        num = float(target)
    except:
        return "Invalid number"

    if mode_name == "math_double":
        return str(num * 2)

    if mode_name == "math_square":
        return str(num * num)

    return "Unknown math mode"
