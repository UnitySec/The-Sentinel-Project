try:
    import colorama
    import stem.interpreter
except ImportError:
    import os, sys
    os.system(sys.executable + " -m pip install stem colorama")

colorama.init(autoreset=True)

class TorConsole:
    def __init__(self):
        pass
    
    def run(self):
        stem.interpreter.main()

if __name__ == "__main__":
    tor = TorConsole()
    tor.run()
