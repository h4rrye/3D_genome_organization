## Creating Nextflow pipeline for the entire analysis



**Prompt**

I want to create a nextflow pipeline for the data processing and dashboard i created. Guide me through it and explain the steps so that I can learn along the way. You can start with giving me the steps and do not give me the enitre code chunk uless i explicitly ask for it.

**Input Files**

1. PDB file (which will be downloaded while running the python script)
2. FASTA file
3. 3 intermediate files that will be created using 3 python scripts and i want them to work in parallel.

**Scripts**

1. `chromosome_sasa.py`
   1. Input: PDB
   2. Output: sasa.npy
2. `chromosome_network.py`
   1. Input: PDB
   2. Output: network.npy
3. `chromosome_biological_features.py`
   1. Input: PDB & FASTA
   2. Output: biological_features.npy
4. `plot_function.py`
   1. Input: None
   2. Output: creates a plotting function to be used in the dashboard
5. `dashboard.py`
   1. Input: `sasa.npy`, `network.npy`, `biological_features.npy`, and imports the plotting function from the `plot_function.py`

**Output**

The entire set of scripts creates a web dashboard using plotly dash.



**Flow**

- scripts 1, 2 and 3 run in parallel to create the intermediate files
- then script 5 uses all the 3 intermediate files plus script 4 to create and render the dashboard

___

**NEXT STEPS**

<small> NOTE: Only start working on this once the pipeline is working properly</small>

1. containerize the entire thing with Docker
2. Deploy on AWS

