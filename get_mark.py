import os
import glob


def get_name():
    try:
        return glob.glob('fall_*.txt')[0].split('_')[-1].split('.')[0]

    except Exception as e:
        return '0000'


if __name__ == "__main__":
    print(get_name())