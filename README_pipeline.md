# Nextflow Pipeline for Chromatin Analysis

## Overview
This pipeline runs three analysis scripts in parallel and generates a dashboard from their combined outputs.

## Pipeline Structure
```
chr1.pdb → network_analysis.py ──┐
         → sasa.py ───────────────┼→ dashboard_1.py → Dashboard
         → biological_functions.py┘
```

## Requirements
- Nextflow (>= 21.04)
- Python 3.9+
- Required Python packages (numpy, pandas, matplotlib, etc.)

## Usage

### Basic run
```bash
nextflow run main.nf
```

### Custom input file
```bash
nextflow run main.nf --input_pdb path/to/your/file.pdb
```

### Custom output directory
```bash
nextflow run main.nf --outdir my_results
```

### With Docker
```bash
nextflow run main.nf -profile docker
```

### With Conda
```bash
nextflow run main.nf -profile conda
```

## Output Structure
```
results/
├── network/          # Network analysis outputs
├── sasa/            # SASA analysis outputs
├── biological/      # Biological functions outputs
├── dashboard/       # Final dashboard
├── pipeline_report.html
├── timeline.html
└── trace.txt
```

## Resume a failed run
```bash
nextflow run main.nf -resume
```
