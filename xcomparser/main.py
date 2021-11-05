import core
import config

def main():
    core.Parser(file=config.FILE,pause=config.PAUSE,threads=config.THREADS)

if __name__ == '__main__':
    main()