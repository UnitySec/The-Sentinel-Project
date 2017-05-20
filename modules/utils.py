import sys
try:
    import colorama, termcolor
    colorama.init(autoreset=True)
except Exception as e:
    termcolor = colorama = None

__all__ = ["colored", "iterate"]



def colored(text, color="green", dark=False):
    try:
        if not termcolor: raise Exception("")
        return termcolor.colored(text, color, attrs=["dark"] if dark else [])
    except Exception as e:
        return text

def pprint(obj, depth=0, check = None, color="", dark=True):
    if not check:
        check = lambda x: str(x).strip()
    prefix = f"{'    ' * (depth-1)}{' -  ' if depth == 1 else '- '}"
    if isinstance(obj, dict):
        for key, value in obj.copy().items():
            key = key.replace("_", "-").title()
            if check(value):
                if isinstance(value, (dict, list, tuple)):
                    print(colored(f"{prefix}{key}:", color))
                    pprint(value, depth+1, check, color, dark)
                else:
                    print(colored(f"{prefix}{key}: ", color) + colored(f"{value}", color, dark))
    elif isinstance(obj, (tuple, list)):
        for value in obj:
            pprint(obj, depth, check, color, dark)
    else:
        if check(value):
            print(colored(f"{prefix}{obj}", color, dark))
