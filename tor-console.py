import colorama
import stem.interpreter

__doc__ = "Interactive interpreter for interacting with Tor directly."


colorama.init(autoreset=True)
if __name__ == "__main__":
    stem.interpreter.main()
