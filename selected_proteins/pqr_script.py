
from collections.abc import Sequence
from os import PathLike

# requirements:
# pip install pdb2pqr openmm pdb2pqr
# git clone https://github.com/openmm/pdbfixer.git
# cd pdbfixer
# python setup.py install


from pdb2pqr.main import build_main_parser, main_driver

from pdbfixer import PDBFixer
from openmm.app import PDBFile

def run_pdb2pqr(args: Sequence[str | PathLike]):
    """Run PDB2PQR with a list of arguments.

    Logger is not set up so that it can be called multiple times.

    :param args:  list of command-line arguments
    :type args:  list
    :return:  results of PDB2PQR run
    :rtype:  tuple
    """
    args_strlist = [str(arg) for arg in args]
    parser = build_main_parser()
    args_parsed = parser.parse_args(args_strlist)
    return main_driver(args_parsed)



def run_pdbfixer(pdbid):
    directory = f"./{pdbid}"
    filename = f"{directory}/{pdbid}_protein.pdb"
    fixer = PDBFixer(filename=filename)
    fixer.findMissingResidues()
    fixer.findNonstandardResidues()
    # fixer.replaceNonstandardResidues()
    # fixer.removeHeterogens(False)
    fixer.findMissingAtoms()
    fixer.addMissingAtoms()
    # fixer.addMissingHydrogens(7.0)
    # fixer.addSolvent(fixer.topology.getUnitCellDimensions())

    # note: this will output a file in the current directory
    PDBFile.writeFile(fixer.topology, fixer.positions, open(f'{directory}/{pdbid}.pdb', 'w'))


import os
def pipeline(pdbid):

    # set up filenames
    directory = f"./{pdbid}"
    ligand_file = f"{directory}/{pdbid}_ligand.mol2"
    protein_file = f"{directory}/{pdbid}_protein.pdb"
    fixed_file = f"{directory}/{pdbid}.pdb" # pdbfixer requires file to be {pdbid}.pdb for accessing RCSB PDB online
    output_file = f"{directory}/{pdbid}_charged.pqr"
    logfile = f"{directory}/{pdbid}_charged.log"
    
    # remove old log file if it exists
    if os.path.exists(logfile):
        os.remove(logfile)
    success = True

    # try existing pdb file
    try:
        # add "--log-level=CRITICAL" after output_file to reduce amount of output
        pdb2pqr_args = ["--ff=AMBER", protein_file, output_file,"--nodebump","--noopt"]
        missed_res, pka_df, biomolecule = run_pdb2pqr(args=pdb2pqr_args)
    except RuntimeError as e:
        print(f"Error running pdb2pqr for protein {pdbid}",flush=True)
        
        # if it failed, try to fix file and run again
        try:
            run_pdbfixer(pdbid)
            pdb2pqr_args = ["--ff=AMBER", fixed_file, output_file,"--log-level=CRITICAL","--nodebump","--noopt"]
            missed_res, pka_df, biomolecule = run_pdb2pqr(args=pdb2pqr_args)
        
        except RuntimeError as e:
            # still fails, return status false
            print(f"Error running pdb2pqr for fixed protein {pdbid}",flush=True)
            success = False
    return success

if __name__ == "__main__":
    problematic_pdbids = ['1a0q', '2hdr', '1cet', '1ux7']
    failed_pdbids = []

    for pdbid in problematic_pdbids:
        print("Run pipeline on ", pdbid)
        success = pipeline(pdbid)
        if not success:
            failed_pdbids.append(pdbid)

    print("Failed pdbids: ", failed_pdbids)
    print("Len(failed_pdbids): ", len(failed_pdbids))