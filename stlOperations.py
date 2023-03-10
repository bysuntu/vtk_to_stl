from fileinput import filename
from logging import raiseExceptions
import os
from argparse import ArgumentParser
import numpy as np

def readSTL(fileName, outName, scale):

    if not os.path.isfile(fileName):
        raiseExceptions("File Doesn't exist")
        return

    with open(fileName, 'r') as f:
        with open(outName, 'w') as out:
            lines = f.readlines()
            for line in lines:
                if line.find('vertex') >= 0:
                    _, *values = line[:-1].split(' ')
                    scaledValues = ' '.join([str(float(v) * scale) for v in values])
                    out.write('vertex {}\n'.format(scaledValues))
                else:
                    out.write(line)

    return

if __name__ == '__main__':
    
    parser = ArgumentParser()
    parser.add_argument('--stl', type=str, required=True)
    parser.add_argument('--outputName', type=str, required=True)
    parser.add_argument('--scale', type=float, default=1.)
    args = parser.parse_args()
    scaled = readSTL(args.stl, args.outputName, args.scale)



