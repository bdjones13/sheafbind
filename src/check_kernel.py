import sys
cands = ['site','numpy','scipy','gudhi','petls','ipykernel']
for m in cands:
    try:
        __import__(m)
        print('ok', m)
    except Exception as e:
        print('ERROR', m, type(e).__name__, e)