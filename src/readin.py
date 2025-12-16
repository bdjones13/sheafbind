import pandas as pd
def mol2_to_pqre(pdbid, suffix, base_dir="../data/v2007"):
    # base_dir = "../data/v2007"
    filename = f"{base_dir}/{pdbid}/{pdbid}_{suffix}.mol2"

    with open(filename) as file:
        lines = file.readlines()

    index_meta = lines.index("@<TRIPOS>MOLECULE\n") + 2
    meta = lines[index_meta].split()


    index_atoms_start = lines.index("@<TRIPOS>ATOM\n")
    index_atoms_end = lines.index("@<TRIPOS>BOND\n")
    filtered_lines = [line.split() for line in lines[index_atoms_start + 1:index_atoms_end]]
    if len(filtered_lines) != int(meta[0]):
        raise Exception("incorrect number of atoms")

    # turn into Pandas DataFrame, remove unnecessary columns, label columns
    df = pd.DataFrame(filtered_lines)
    df = df.iloc[:, [2, 3, 4, 5,8]]
    df.columns = ["x", "y", "z", "element","charge"]
    df["element"] = df["element"].str.split(".").str[0]
    df[["x", "y", "z","charge"]] = df[["x", "y", "z","charge"]].apply(pd.to_numeric)
    return df