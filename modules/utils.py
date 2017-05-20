import sys
try:
    import colorama, termcolor
    colorama.init(autoreset=True)
except Exception as e:
    termcolor = colorama = None

__all__ = ["colored"]



def colored(text, color="green", dark=False):
    try:
        if not termcolor: raise Exception("")
        return termcolor.colored(text, color, attrs=["dark"] if dark else [])
    except Exception as e:
        return text
