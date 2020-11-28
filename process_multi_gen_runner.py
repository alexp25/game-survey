import subprocess


import subprocess

script = [
    "py -3 process_multi_gen.py --platform=1 --min-score=0",
    "py -3 process_multi_gen.py --platform=1 --min-score=80",
    "py -3 process_multi_gen.py --platform=2 --min-score=0",
    "py -3 process_multi_gen.py --platform=2 --min-score=80",
    "py -3 process_multi_gen.py --platform=3 --min-score=0",
    "py -3 process_multi_gen.py --platform=3 --min-score=4"
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
