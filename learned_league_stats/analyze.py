
import argparse
import logging

import get_data 
import visualize


# names_to_track = ['HombergerC', 'VatterV', 'PantoneJ', 'BrignallR']
# names_to_track = ['HombergerC', 'VatterV', 'EberhartR']
# names_to_track = ['PantoneJ', 'BrignallR']

CONFIG = {
        'rundle': 'A_Cascade',
        # 'rundle': 'D_Cascade_Div_2',
        'season': '77',
        'names': ['AlbertMichael']
        # names:  = ['HombergerC', 'VatterV', 'PantoneJ', 'BrignallR'],
        # names: = ['HombergerC', 'VatterV', 'EberhartR'],
        # names: = ['PantoneJ', 'BrignallR'],
        }


def set_up_logger(level=logging.DEBUG):
    logger = logging.getLogger()
    logger.setLevel(level)
    sh = logging.StreamHandler()
    formatter = logging.Formatter(
        # '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        '%(levelname)s: %(message)s'
        )
    sh.setFormatter(formatter)
    logger.addHandler(sh)
    return logger 

logger = set_up_logger()

def get_and_save_data(fname='data.json'):
    logger.info('Downloading Data')
    data = get_all_data()
    logger.info('Saving Data')
    save_data(data, fname)
    logger.info('Done!')

def test():
    logger.debug('Debug message')
    logger.info('Info message')
    logger.warn('Warning message')

def plot():
    visualize.plot_all()


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('command', type=str,
            choices=['plot', 'update', 'test'],
            nargs="?",
            default='test',
            help="which command to run")
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    if args.command == 'plot':
        visualize.plot_all()
    elif args.command == 'update':
        get_and_save_data()
    elif args.command == 'test':
        test()


if __name__ == '__main__':
    main()
