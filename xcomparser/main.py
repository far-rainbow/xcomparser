''' XCOM PARSER '''
import config
import core


def main():
    ''' MAIN '''
    core.Parser(file=config.FILE,
                pause=config.PAUSE,
                threads=config.THREADS)

if __name__ == '__main__':
    main()
