from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser(description='Segment bloodstains in an spatter pattern')
    parser.add_argument("filename", help="", metavar="FILE")

    parser.add_argument("-s", "--scale", dest="scale", type=float,
                        help="scale in pixels per mm", metavar="SCALE", default=7)
    
    parser.add_argument("-o", "--output", dest="output", help="folder for output (default is <file path>/output)", metavar="OUTPUT")
    parser.add_argument("--show", default=False, help="show stain detection")

    return parser.parse_args()
    
