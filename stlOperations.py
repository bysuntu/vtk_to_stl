from logging import raiseExceptions
import os
from stl import mesh
from argparse import ArgumentParser

def readSTL(fileName, scale):

    if not os.path.isfile(fileName):
        raiseExceptions("File Doesn't exist")
        return

    data = mesh.Mesh.from_file(fileName)
    data.data *= scale
    return data

if __name__ == '__main__':
    
    parser = ArgumentParser()
    parser.add_argument('--stl', type=str(), required=True)
    parser.add_argument('--scale', type=float, default=1.)
    args = parser.parse_args()
    readSTL(args.stl, args.scale)


