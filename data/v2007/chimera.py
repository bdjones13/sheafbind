
import os
import sys

def get_pdbids(total_n, n):
    base_dir = os.path.join(".")

    # list all subdirectories of base_dir
    pdbids = []
    for pdbid in sorted(os.listdir(base_dir)):
        pdb_dir = os.path.join(base_dir, pdbid)
        if not os.path.isdir(pdb_dir):
            continue
        pdbids.append(pdbid)
    
    pdbids_per_runner = len(pdbids) // total_n

    print(f"pdbids_per_runner={pdbids_per_runner}",flush=True)
    pdbids_split = [pdbids[i*pdbids_per_runner:min((i+1)*pdbids_per_runner,len(pdbids))] for i in range(total_n+1)]

    subsums = [len(L) for L in pdbids_split]

    assert (sum(subsums) == len(pdbids))
    pdbids_current = pdbids_split[n]
        
    return pdbids_current



if __name__=="__main__":
    if len(sys.argv) < 3:
        print("Usage: 'python chimera.py total_n n', where total_n is the total number of runners and n is the current runner")
    pdbids = get_pdbids(int(sys.argv[1]),int(sys.argv[2]))

    for i, pdbid in enumerate(pdbids):
        print(f"({i}/{len(pdbids)})run with {pdbid}",flush=True)
        os.system(f'/opt/software-current/2023.06/x86_64/generic/software/ChimeraX/1.9-ubuntu22.04-amd64/bin/ChimeraX --nogui --offscreen --script "chimera_pdbid.cxc {pdbid}" ')