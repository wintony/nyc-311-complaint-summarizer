import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--borough", required=True)
    return parser.parse_args()

def main():
    args = parse_args()
    borough = args.borough

    print(borough)
    
if __name__ == "__main__":
    main()
