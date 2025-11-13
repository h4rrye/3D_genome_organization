# Nextflow Tutorial: Processes, Channels, and Best Practices

## 1. Creating a Basic Process with Input/Output Channels

### Basic Process Structure

```nextflow
// Define input channels
Channel.fromPath("data/*.fastq")
    .set { reads_ch }

Channel.fromPath("reference/*.fa")
    .set { ref_ch }

// Basic process with inputs and outputs
process alignReads {
    // Input channels
    input:
    path reads from reads_ch
    path reference from ref_ch
    
    // Output channels
    output:
    path "*.bam" into bam_ch
    path "*.bai" into bai_ch
    
    // Script block
    script:
    """
    bwa mem -t ${task.cpus} ${reference} ${reads} | \
        samtools view -bS - > output.bam
    samtools index output.bam
    """
}
```

### Process with Multiple Inputs

```nextflow
process processData {
    input:
    val sample_id from sample_ch
    path fastq_file from fastq_ch
    path config_file from config_ch
    
    output:
    path "output_${sample_id}.txt" into results_ch
    val sample_id into sample_ids_ch
    
    script:
    """
    process_data.py \\
        --sample ${sample_id} \\
        --input ${fastq_file} \\
        --config ${config_file} \\
        --output output_${sample_id}.txt
    """
}
```

### Process with Optional Inputs

```nextflow
process optionalInput {
    input:
    path required_file from required_ch
    path optional_file from optional_ch.ifEmpty([])
    
    output:
    path "result.txt" into result_ch
    
    script:
    def opt_flag = optional_file ? "--optional ${optional_file}" : ""
    """
    tool.py --input ${required_file} ${opt_flag} > result.txt
    """
}
```

---

## 2. .combine() vs .join() Operators

### .combine() - Cartesian Product

The `.combine()` operator creates a **cartesian product** of channels, matching every item from the first channel with every item from the second channel.

```nextflow
// Example: Process all samples with all references
Channel.from("sample1", "sample2", "sample3")
    .set { samples_ch }

Channel.from("ref1", "ref2")
    .set { refs_ch }

// This creates 3 x 2 = 6 combinations:
// (sample1, ref1), (sample1, ref2), (sample2, ref1), 
// (sample2, ref2), (sample3, ref1), (sample3, ref2)
samples_ch
    .combine(refs_ch)
    .view()
```

**Use case:** When you need to test all combinations of inputs.

### .join() - One-to-One Matching

The `.join()` operator matches items from channels **by index** (first with first, second with second, etc.).

```nextflow
// Example: Match samples with their corresponding references
Channel.from("sample1", "sample2", "sample3")
    .set { samples_ch }

Channel.from("ref1", "ref2", "ref3")
    .set { refs_ch }

// This creates 3 pairs:
// (sample1, ref1), (sample2, ref2), (sample3, ref3)
samples_ch
    .join(refs_ch)
    .view()
```

**Use case:** When you have paired data that should be matched by position.

### .combine() with Key Matching

You can use `.combine()` with a closure to match on specific keys:

```nextflow
// Channels with tuples (key, value)
Channel.from([
    ["sample1", "data1"],
    ["sample2", "data2"]
])
.set { data_ch }

Channel.from([
    ["sample1", "ref1"],
    ["sample2", "ref2"]
])
.set { ref_ch }

// Match by first element (key)
data_ch
    .combine(ref_ch, by: 0)  // Match on index 0 (the key)
    .view()
// Output: [["sample1", "data1"], ["sample1", "ref1"]]
//         [["sample2", "data2"], ["sample2", "ref2"]]
```

### Practical Example: When to Use Each

```nextflow
// Scenario 1: All samples need all references (use combine)
process alignAllCombinations {
    input:
    tuple val(sample), path(fastq) from samples_ch
    path reference from refs_ch
    
    output:
    path "*.bam" into bam_ch
    
    script:
    """
    bwa mem ${reference} ${fastq} > output.bam
    """
}

samples_ch.combine(refs_ch).set { combined_ch }

// Scenario 2: Each sample has its own reference (use join)
process alignPaired {
    input:
    tuple val(sample), path(fastq) from samples_ch
    tuple val(sample), path(reference) from refs_ch
    
    output:
    path "*.bam" into bam_ch
    
    script:
    """
    bwa mem ${reference} ${fastq} > output.bam
    """
}

samples_ch.join(refs_ch, by: 0).set { paired_ch }
```

---

## 3. Debugging Channel Mismatch Errors

### Common Channel Mismatch Errors

#### Error 1: "Channel mismatch: expecting a value channel"

```nextflow
// ❌ WRONG: Process expects a value but receives a file channel
process processData {
    input:
    val sample_id from file_ch  // ERROR: file_ch emits files, not values
    
    script:
    """
    echo ${sample_id}
    """
}

// ✅ CORRECT: Extract value from file channel
process processData {
    input:
    path file from file_ch
    val sample_id = file.baseName  // Extract value from file
    
    script:
    """
    echo ${sample_id}
    """
}
```

#### Error 2: "Channel mismatch: expecting a file channel"

```nextflow
// ❌ WRONG: Process expects a file but receives a value
process processData {
    input:
    path file from value_ch  // ERROR: value_ch emits values, not files
    
    script:
    """
    cat ${file}
    """
}

// ✅ CORRECT: Convert value to file or use correct channel type
process processData {
    input:
    val file_path from value_ch
    
    script:
    """
    cat ${file_path}
    """
}
```

#### Error 3: Tuple Structure Mismatch

```nextflow
// ❌ WRONG: Tuple structure doesn't match
Channel.from(["sample1", "data1"])
    .set { ch1 }

Channel.from(["sample2", "data2", "extra"])
    .set { ch2 }

ch1.join(ch2)  // ERROR: Different tuple sizes

// ✅ CORRECT: Ensure consistent tuple structure
Channel.from([
    ["sample1", "data1", "extra1"],
    ["sample2", "data2", "extra2"]
])
.set { ch1 }

Channel.from([
    ["sample1", "ref1"],
    ["sample2", "ref2"]
])
.set { ch2 }

ch1.join(ch2, by: 0)  // Match by first element
```

### Debugging Strategies

#### 1. Use `.view()` to Inspect Channels

```nextflow
Channel.from("sample1", "sample2")
    .view()  // Print channel contents

Channel.fromPath("data/*.fastq")
    .map { file -> [file.baseName, file] }
    .view { sample, file -> "Sample: ${sample}, File: ${file}" }
```

#### 2. Check Channel Types

```nextflow
// Check what type of channel you have
def my_channel = Channel.from("value1", "value2")
// This is a value channel

def my_file_channel = Channel.fromPath("data/*.fastq")
// This is a file channel

// Convert between types if needed
my_file_channel
    .map { file -> file.baseName }  // Convert file channel to value channel
    .set { value_ch }
```

#### 3. Use `.dump()` for Detailed Inspection

```nextflow
// Add to your workflow
workflow {
    my_channel.dump(tag: "my_channel")
    process1.out.channel.dump(tag: "process1_output")
}
```

#### 4. Common Fixes

```nextflow
// Fix 1: Extract values from file channels
Channel.fromPath("data/*.fastq")
    .map { file -> [file.baseName, file] }  // Extract sample name
    .set { samples_ch }

// Fix 2: Ensure tuple consistency
Channel.from(["sample1", "data1"])
    .map { sample, data -> [sample, data, "default_value"] }  // Add missing element
    .set { fixed_ch }

// Fix 3: Use correct input qualifier
process example {
    input:
    val sample_id from value_ch      // For values
    path input_file from file_ch     // For files
    tuple val(id), path(file) from tuple_ch  // For tuples
}
```

---

## 4. Best Practices for publishDir

### Basic publishDir Usage

```nextflow
process alignReads {
    publishDir "results/alignment", mode: 'copy'
    
    input:
    path reads from reads_ch
    
    output:
    path "*.bam" into bam_ch
    
    script:
    """
    bwa mem ${reads} > output.bam
    """
}
```

### Best Practices

#### 1. Use Pattern-Based Publishing

```nextflow
process alignReads {
    publishDir "results/alignment", 
        pattern: "*.bam",           // Only publish BAM files
        mode: 'copy',
        saveAs: { filename -> "aligned_${filename}" }  // Rename files
    
    output:
    path "*.bam" into bam_ch
    path "*.bai" into bai_ch  // This won't be published (not matching pattern)
}
```

#### 2. Organize by Process or Sample

```nextflow
// Option A: Organize by process
process alignReads {
    publishDir "results/alignment", mode: 'copy'
    // ...
}

process callVariants {
    publishDir "results/variants", mode: 'copy'
    // ...
}

// Option B: Organize by sample (dynamic paths)
process alignReads {
    publishDir "results/${sample_id}/alignment", 
        mode: 'copy',
        pattern: "*.bam"
    
    input:
    val sample_id from sample_ch
    path reads from reads_ch
    
    output:
    path "*.bam" into bam_ch
}
```

#### 3. Choose the Right Mode

```nextflow
// 'copy' - Copy files (default, safest)
publishDir "results", mode: 'copy'

// 'move' - Move files (faster, but removes from work dir)
publishDir "results", mode: 'move'

// 'link' - Create symbolic links (fastest, but requires same filesystem)
publishDir "results", mode: 'link'

// 'rellink' - Create relative symbolic links
publishDir "results", mode: 'rellink'
```

#### 4. Conditional Publishing

```nextflow
process alignReads {
    publishDir params.publish_results ? "results/alignment" : null,
        mode: 'copy'
    
    // Or use a conditional pattern
    publishDir "results/alignment",
        pattern: params.keep_intermediates ? "*" : "*.bam",
        mode: 'copy'
}
```

#### 5. Publish Only Final Results

```nextflow
// Don't publish intermediate files
process intermediateStep {
    // No publishDir - files stay in work directory
    output:
    path "intermediate.txt" into intermediate_ch
}

// Only publish final results
process finalStep {
    publishDir "results/final", mode: 'copy'
    input:
    path intermediate from intermediate_ch
    
    output:
    path "final_result.txt" into final_ch
}
```

#### 6. Use publishDir in nextflow.config for Global Settings

```nextflow
// nextflow.config
process {
    publishDir = [
        path: { "${params.outdir}/${process.name}" },
        mode: 'copy',
        pattern: "*.{bam,bai,vcf}",
        enabled: true
    ]
}
```

#### 7. Handle Multiple Outputs with Different Patterns

```nextflow
process multiOutput {
    publishDir "results/alignments", 
        pattern: "*.bam",
        mode: 'copy'
    
    publishDir "results/indexes",
        pattern: "*.bai",
        mode: 'copy'
    
    publishDir "results/logs",
        pattern: "*.log",
        mode: 'copy'
    
    output:
    path "*.bam" into bam_ch
    path "*.bai" into bai_ch
    path "*.log" into log_ch
}
```

#### 8. Avoid Publishing Large Intermediate Files

```nextflow
// ❌ BAD: Publishing everything
process alignReads {
    publishDir "results", mode: 'copy'  // Publishes ALL outputs
    // ...
}

// ✅ GOOD: Selective publishing
process alignReads {
    publishDir "results/alignment",
        pattern: "*.bam",  // Only publish final BAM files
        mode: 'copy'
    // ...
}
```

### Complete Example

```nextflow
// nextflow.config
params {
    outdir = "results"
    publish_mode = "copy"
}

process {
    withName: "alignReads" {
        publishDir = [
            path: { "${params.outdir}/alignment" },
            pattern: "*.bam",
            mode: params.publish_mode,
            saveAs: { filename -> "aligned_${filename}" }
        ]
    }
    
    withName: "callVariants" {
        publishDir = [
            path: { "${params.outdir}/variants" },
            pattern: "*.vcf",
            mode: params.publish_mode
        ]
    }
}

// main.nf
process alignReads {
    input:
    tuple val(sample_id), path(reads) from samples_ch
    
    output:
    path "*.bam" into bam_ch
    path "*.bai" into bai_ch  // Not published (doesn't match pattern)
    
    script:
    """
    bwa mem ${reads} > ${sample_id}.bam
    samtools index ${sample_id}.bam
    """
}

process callVariants {
    publishDir "results/variants", pattern: "*.vcf", mode: 'copy'
    
    input:
    path bam from bam_ch
    
    output:
    path "*.vcf" into vcf_ch
    
    script:
    """
    bcftools mpileup -f reference.fa ${bam} | \
        bcftools call -mv - > variants.vcf
    """
}
```

---

## Summary

1. **Processes**: Use `input:` and `output:` blocks to define channels. Match channel types (value vs file vs tuple).

2. **combine() vs join()**: 
   - Use `.combine()` for cartesian products (all combinations)
   - Use `.join()` for one-to-one matching by index
   - Use `.combine(by: key)` for key-based matching

3. **Debugging**: Use `.view()` and `.dump()` to inspect channels. Ensure consistent tuple structures and correct input qualifiers.

4. **publishDir**: Use patterns to selectively publish, organize by process/sample, choose appropriate modes, and avoid publishing large intermediate files.

