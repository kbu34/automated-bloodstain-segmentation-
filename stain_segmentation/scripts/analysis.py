from argparse import ArgumentParser
from os import path

from analysis import stain_segmentation

def parse_args():
    parser = ArgumentParser(description='Segment bloodstains in an spatter pattern')
    parser.add_argument("filename", help="", metavar="FILE")

    parser.add_argument("-s", "--scale", dest="scale", type=float,
                        help="scale in pixels per mm", metavar="SCALE", default=7)
    
    parser.add_argument("-o", "--output", dest="output", help="folder for output (default is <file path>/output)", metavar="OUTPUT")
    parser.add_argument("--show", default=False, action="store_true", help="show stain detection")

    parser.add_argument("--no-linearity", dest="no_linearity",  default=False, action="store_true", help="disable linearity computation")
    parser.add_argument("--no-distribution", dest="no_distribution", default=False, action="store_true", help="disable distribution computation")
    parser.add_argument("--no-convergence", dest="no_convergence", default=False, action="store_true", help="disable convergence computation")
    
    parser.add_argument("--overwrite", default=False, action="store_true", help="overwrite output folder")
    return parser.parse_args()
    
def main():
    args = parse_args()
    pattern_metrics = dict(
        convergence = not args.no_convergence,
        linearity = not args.no_linearity,
        distribution = not args.no_distribution,
    )
    
    if args.scale < 1:
        print("Warning scale is less than 1")

    if path.isfile(args.filename):
        base, filename = path.split(args.filename)

        output_path = args.output or path.join(base, "output", filename)
        print(f"Processing {args.filename}, output path: {output_path}")

        stain_segmentation.process_image(args.filename, output_path, args.scale, args.show,  pattern_metrics=pattern_metrics)
    elif path.isdir(args.filename):
        stain_segmentation.batch_process(args.filename, args.output, args.scale, args.show, args.overwrite, pattern_metrics=pattern_metrics)
    else:
        assert False, f"{args.filename} does not exist"


if __name__ == '__main__':
    main()    