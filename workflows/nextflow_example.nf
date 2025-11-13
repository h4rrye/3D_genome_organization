#!/usr/bin/env nextflow

/*
 * Nextflow Example Workflow
 * Demonstrates: processes, channels, combine/join, and publishDir best practices
 */

// ============================================================================
// PARAMETERS
// ============================================================================

params {
    input_dir = "data/input_data"
    reference = "data/reference.fa"
    outdir = "results"
    publish_mode = "copy"
}

// ============================================================================
// INPUT CHANNELS
// ============================================================================

// Channel 1: Sample files
Channel.fromPath("${params.input_dir}/*.fastq")
    .map { file -> 
        [file.baseName, file]  // [sample_id, file_path]
    }
    .set { samples_ch }

// Channel 2: Reference files (multiple references for combine example)
Channel.fromPath("${params.reference}")
    .set { refs_ch }

// Channel 3: Sample metadata (for join example)
Channel.from([
    ["sample1", "condition_A"],
    ["sample2", "condition_B"],
    ["sample3", "condition_A"]
])
.set { metadata_ch }

// ============================================================================
// PROCESS 1: Basic Process with Input/Output Channels
// ============================================================================

process basicProcess {
    publishDir "${params.outdir}/basic", 
        pattern: "*.txt",
        mode: params.publish_mode
    
    input:
    tuple val(sample_id), path(input_file) from samples_ch
    
    output:
    path "output_${sample_id}.txt" into basic_output_ch
    val sample_id into sample_ids_ch
    
    script:
    """
    echo "Processing sample: ${sample_id}" > output_${sample_id}.txt
    echo "Input file: ${input_file}" >> output_${sample_id}.txt
    echo "Timestamp: \$(date)" >> output_${sample_id}.txt
    """
}

// ============================================================================
// PROCESS 2: Demonstrating .combine() - Cartesian Product
// ============================================================================

// Create all combinations of samples and references
samples_ch
    .combine(refs_ch)
    .set { combined_ch }

process combineExample {
    publishDir "${params.outdir}/combine", 
        pattern: "*.bam",
        mode: params.publish_mode
    
    input:
    tuple val(sample_id), path(sample_file), path(reference) from combined_ch
    
    output:
    path "${sample_id}_vs_${reference.baseName}.bam" into combine_output_ch
    
    script:
    """
    # Simulate alignment: sample vs reference
    echo "Aligning ${sample_id} against ${reference.baseName}" > ${sample_id}_vs_${reference.baseName}.bam
    echo "Sample: ${sample_file}" >> ${sample_id}_vs_${reference.baseName}.bam
    echo "Reference: ${reference}" >> ${sample_id}_vs_${reference.baseName}.bam
    """
}

// ============================================================================
// PROCESS 3: Demonstrating .join() - One-to-One Matching
// ============================================================================

// Join samples with metadata by sample_id (first element)
samples_ch
    .join(metadata_ch, by: 0)  // Match on index 0 (sample_id)
    .set { joined_ch }

process joinExample {
    publishDir "${params.outdir}/join", 
        pattern: "*.txt",
        mode: params.publish_mode
    
    input:
    tuple val(sample_id), path(sample_file), val(condition) from joined_ch
    
    output:
    path "${sample_id}_${condition}.txt" into join_output_ch
    
    script:
    """
    echo "Sample: ${sample_id}" > ${sample_id}_${condition}.txt
    echo "Condition: ${condition}" >> ${sample_id}_${condition}.txt
    echo "File: ${sample_file}" >> ${sample_id}_${condition}.txt
    """
}

// ============================================================================
// PROCESS 4: Debugging Example - Common Channel Mismatch Fixes
// ============================================================================

// Example: Converting file channel to value channel
samples_ch
    .map { sample_id, file -> sample_id }  // Extract just the sample_id
    .set { sample_ids_only_ch }

process debugExample {
    publishDir "${params.outdir}/debug", 
        pattern: "*.log",
        mode: params.publish_mode
    
    input:
    val sample_id from sample_ids_only_ch  // Now it's a value channel
    
    output:
    path "${sample_id}.log" into debug_output_ch
    
    script:
    """
    echo "Processing sample: ${sample_id}" > ${sample_id}.log
    echo "This demonstrates correct channel type usage" >> ${sample_id}.log
    """
}

// ============================================================================
// PROCESS 5: Advanced publishDir Usage
// ============================================================================

process advancedPublishDir {
    // Multiple publishDir directives for different output types
    publishDir "${params.outdir}/advanced/results", 
        pattern: "*.result",
        mode: params.publish_mode,
        saveAs: { filename -> "final_${filename}" }
    
    publishDir "${params.outdir}/advanced/logs",
        pattern: "*.log",
        mode: params.publish_mode
    
    publishDir "${params.outdir}/advanced/intermediate",
        pattern: "*.tmp",
        mode: params.publish_mode,
        enabled: params.publish_mode != "copy"  // Conditional publishing
    
    input:
    path input_file from basic_output_ch
    
    output:
    path "*.result" into advanced_results_ch
    path "*.log" into advanced_logs_ch
    path "*.tmp" into advanced_tmp_ch
    
    script:
    """
    # Create different output types
    cp ${input_file} output.result
    echo "Processing log" > output.log
    echo "Temporary data" > output.tmp
    """
}

// ============================================================================
// WORKFLOW
// ============================================================================

workflow {
    // All processes are automatically included when defined above
    
    // You can also add channel inspection for debugging
    if (params.debug) {
        samples_ch.view { sample_id, file -> "Sample: ${sample_id}, File: ${file}" }
        combined_ch.view { "Combined: ${it}" }
        joined_ch.view { "Joined: ${it}" }
    }
    
    // Print summary
    basic_output_ch
        .count()
        .view { "Basic process completed: ${it} files" }
}

// ============================================================================
// NOTES FOR DEBUGGING
// ============================================================================

/*
 * Common Channel Mismatch Errors and Solutions:
 * 
 * 1. "Channel mismatch: expecting a value channel"
 *    Solution: Use .map() to extract values from file channels
 *    Example: file_ch.map { file -> file.baseName }
 * 
 * 2. "Channel mismatch: expecting a file channel"
 *    Solution: Use 'val' qualifier for values, 'path' for files
 *    Example: val sample_id from value_ch
 *             path file from file_ch
 * 
 * 3. "Tuple structure mismatch"
 *    Solution: Ensure consistent tuple sizes or use .map() to normalize
 *    Example: ch.map { a, b -> [a, b, "default"] }
 * 
 * Debugging Tips:
 * - Add .view() to channels to inspect contents
 * - Use .dump() in workflow block for detailed inspection
 * - Check Nextflow documentation for channel operators
 * - Run with -dump-channels flag: nextflow run script.nf -dump-channels
 */

