import subprocess


import subprocess

script = [
    "py -3 process_compare_gen.py --platform=1 --mode=1 --min-score=0 --use-limits=1",
    "py -3 process_compare_gen.py --platform=1 --mode=2 --min-score=0 --use-limits=1",
    "py -3 process_compare_gen.py --platform=2 --mode=1 --min-score=0 --use-limits=0",
    "py -3 process_compare_gen.py --platform=2 --mode=2 --min-score=0 --use-limits=1",
    "py -3 process_compare_gen.py --platform=3 --mode=1 --min-score=0 --use-limits=1",
    "py -3 process_compare_gen.py --platform=3 --mode=2 --min-score=0 --use-limits=1",

    "py -3 process_compare_gen.py --platform=1 --mode=1 --min-score=80 --use-limits=1",
    "py -3 process_compare_gen.py --platform=1 --mode=2 --min-score=80 --use-limits=1",
    "py -3 process_compare_gen.py --platform=2 --mode=1 --min-score=80 --use-limits=0",
    "py -3 process_compare_gen.py --platform=2 --mode=2 --min-score=80 --use-limits=1",
    "py -3 process_compare_gen.py --platform=3 --mode=1 --min-score=4 --use-limits=1",
    "py -3 process_compare_gen.py --platform=3 --mode=2 --min-score=4 --use-limits=1"
]

for i, s in enumerate(script):
    print("#" + str(i+1) + ": " + s + "\n")
    # subprocess.call(s, shell=True)
    p = subprocess.Popen(s, stdout=subprocess.PIPE, shell=True)
    out, err = p.communicate() 
    out = out.decode("utf-8") 
    result = out.split('\n')
    for lin in result:
        if not lin.startswith('#'):
            print(lin)
