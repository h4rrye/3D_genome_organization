#!/usr/bin/env nextflow

nextflow.enable.dsl=2

/*
 * Pipeline parameters
 */
params.input_pdb = "chr1.pdb"
params.outdir = "results"

/*
 * Process: Run network analysis
 */
process NETWORK_ANALYSIS {
    publishDir "${params.outdir}/network", mode: 'copy'
    
    input:
    path pdb_file
    
    output:
    path "network_output.*"
    
    script:
    """
    python network_analysis.py ${pdb_file}
    """
}

/*
 * Process: Run SASA analysis
 */
process SASA_ANALYSIS {
    publishDir "${params.outdir}/sasa", mode: 'copy'
    
    input:
    path pdb_file
    
    output:
    path "sasa_output.*"
    
    script:
    """
    python sasa.py ${pdb_file}
    """
}

/*
 * Process: Run biological functions analysis
 */
process BIOLOGICAL_FUNCTIONS {
    publishDir "${params.outdir}/biological", mode: 'copy'
    
    input:
    path pdb_file
    
    output:
    path "biological_output.*"
    
    script:
    """
    python biological_functions.py ${pdb_file}
    """
}

/*
 * Process: Create dashboard
 */
process CREATE_DASHBOARD {
    publishDir "${params.outdir}/dashboard", mode: 'copy'
    
    input:
    path network_results
    path sasa_results
    path biological_results
    
    output:
    path "dashboard.*"
    
    script:
    """
    python dashboard_1.py ${network_results} ${sasa_results} ${biological_results}
    """
}

/*
 * Main workflow
 */
workflow {
    // Create input channel
    pdb_ch = Channel.fromPath(params.input_pdb)
    
    // Run analyses in parallel
    network_out = NETWORK_ANALYSIS(pdb_ch)
    sasa_out = SASA_ANALYSIS(pdb_ch)
    biological_out = BIOLOGICAL_FUNCTIONS(pdb_ch)
    
    // Combine results and create dashboard
    CREATE_DASHBOARD(
        network_out,
        sasa_out,
        biological_out
    )
}
