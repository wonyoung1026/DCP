import argparse
import subprocess
import time

# ================================================
# Delete given file after N seconds
# ================================================

parser = argparse.ArgumentParser(description='delete file after N minutes')
parser.add_argument('filename', type=str)
parser.add_argument('-s', '--seconds', required=True)

args = parser.parse_args()
time.sleep(int(args.seconds))

subprocess.run(["rm", "-f", "./temp/"+args.filename])
subprocess.run(["rm", "-f", "./temp/"+args.filename+".pub"])

