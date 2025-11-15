# ================================
#           libraries
# ================================

import ssl
import urllib.request

import mdtraj as md
import numpy as np
import pandas as pd
from Bio import SeqIO

url = 'https://calla.rnet.missouri.edu/genome3d/GSDB/Database/AX9716PF/GSE105544_ENCFF010WBP/VC/LorDG/chr1.pdb'
# chromosome model used: https://gsdb.mu.hekademeia.org/details.php?id=GSE105544_ENCFF010WBP
# resolution: 500Kb

# loading PDB file to check the raw file for some EDA

with open ('chr1.pdb', 'r') as f:
    file = f.read()

lines = file.split('\n')

# Create unverified context for this specific download
ssl_context = ssl._create_unverified_context()

# Download the file
with urllib.request.urlopen(url, context=ssl_context) as response:
    with open('chr1.pdb', 'wb') as out_file:
        out_file.write(response.read())

# Load from local file
chr_str = md.load_pdb('chr1.pdb')
coords = chr_str.xyz.reshape(-1, 3)


fasta_file = '../data/raw/hg38_chr1_FASTA.fasta'

sequences = []
for record in SeqIO.parse(fasta_file, 'fasta'):
    sequences.append(record)
    print('_' * 60)
    print(f'ID: {record.id}')
    # print(f'Sequence: {record.seq}')
    print(f'Description: {record.description}')
    print('_' * 60)

def gc_content_calculator(sequence, window):
    """Calculate GC content based on the window size"""

    sequence_upper = str(sequence).upper()
    seq_len = len(sequence_upper)
    num_windows = (seq_len - window) // window + 1
    bins = []
    gc_percentages = []

    gc_chars = {'G', 'C'}
    for i in range(0, seq_len - window + 1, window):
        sequence_frag = sequence_upper[i:i + window]
        gc_count = sum(1 for char in sequence_frag if char in gc_chars)
        if gc_count == 0 and 'N' in sequence_frag:
            bins.append(i)
            gc_percentages.append('telo-centro')
        elif gc_count > 0:
            gc_content_percentage = round((gc_count / window) * 100, 2)
            bins.append(i)
            gc_percentages.append(gc_content_percentage)

    return pd.DataFrame({
        'bin': bins,
        'gc_content_percentage': gc_percentages
    })

gc = gc_content_calculator(sequences[0].seq, 500000)


coords_df = pd.DataFrame(coords, columns=['x', 'y', 'z'])

merged_file = pd.concat([
    coords_df.reset_index(drop=True),
    gc[gc['gc_content_percentage'] != 'telo-centro'].reset_index(drop=True)
], axis=1).iloc[:451, :]

merged_file.to_csv('x_y_z_bin_gc.csv')

np.save('x_y_z_bin_gc.npy', merged_file)
