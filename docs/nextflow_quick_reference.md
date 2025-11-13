# Nextflow Quick Reference Guide

## Basic Process Template

```nextflow
process processName {
    publishDir "results/processName", pattern: "*.out", mode: 'copy'
    
    input:
    val input_value from value_ch
    path input_file from file_ch
    tuple val(id), path(file) from tuple_ch
    
    output:
    path "output.txt" into output_ch
    val result_id into id_ch
    
    script:
    """
    command --input ${input_file} --id ${input_value} > output.txt
    """
}
```

## Channel Operators Cheat Sheet

| Operator | Description | Use Case |
|----------|-------------|----------|
| `.combine(ch)` | Cartesian product (all combinations) | Test all sample×reference combinations |
| `.join(ch)` | One-to-one by index | Match paired data by position |
| `.join(ch, by: key)` | Match by key/index | Match samples with metadata by ID |
| `.map { }` | Transform items | Extract values, normalize tuples |
| `.view()` | Print channel contents | Debug channel contents |
| `.dump()` | Detailed channel info | Advanced debugging |
| `.set { }` | Assign to variable | Store channel for reuse |

## Input Qualifiers

| Qualifier | Channel Type | Example |
|-----------|--------------|---------|
| `val` | Value channel | `val sample_id from id_ch` |
| `path` | File channel | `path reads from reads_ch` |
| `tuple` | Tuple channel | `tuple val(id), path(file) from tuple_ch` |
| `env` | Environment variable | `env MY_VAR from env_ch` |
| `stdin` | Standard input | `stdin from input_ch` |
| `each` | Iterate over channel | `each item from items_ch` |

## publishDir Modes

| Mode | Description | When to Use |
|------|-------------|-------------|
| `copy` | Copy files (default) | Production, safest option |
| `move` | Move files | Save disk space, faster than copy |
| `link` | Symbolic link | Same filesystem, fastest |
| `rellink` | Relative symlink | Same filesystem, portable |

## Common Channel Mismatch Fixes

### Error: "expecting a value channel"
```nextflow
// ❌ Wrong
val sample_id from file_ch

// ✅ Fix: Extract value
path file from file_ch
val sample_id = file.baseName
```

### Error: "expecting a file channel"
```nextflow
// ❌ Wrong
path file from value_ch

// ✅ Fix: Use correct qualifier
val file_path from value_ch
// Or convert value to file path
```

### Error: "Tuple structure mismatch"
```nextflow
// ❌ Wrong: Different tuple sizes
ch1.join(ch2)  // ch1 has 2 elements, ch2 has 3

// ✅ Fix: Normalize tuples
ch1.map { a, b -> [a, b, "default"] }
   .join(ch2)
```

## publishDir Best Practices

```nextflow
// ✅ Good: Selective publishing with pattern
publishDir "results", pattern: "*.bam", mode: 'copy'

// ✅ Good: Organize by sample
publishDir "results/${sample_id}", mode: 'copy'

// ✅ Good: Multiple publishDir for different outputs
publishDir "results/data", pattern: "*.bam"
publishDir "results/logs", pattern: "*.log"

// ❌ Bad: Publishing everything
publishDir "results"  // Publishes all outputs, including intermediates
```

## Debugging Checklist

- [ ] Use `.view()` to inspect channel contents
- [ ] Check channel types match input qualifiers
- [ ] Ensure tuple structures are consistent
- [ ] Use `.dump()` for detailed channel inspection
- [ ] Run with `-dump-channels` flag
- [ ] Verify file paths exist before processing
- [ ] Check publishDir patterns match output files

## Quick Examples

### combine() - All Combinations
```nextflow
samples_ch.combine(refs_ch)  // 3 samples × 2 refs = 6 combinations
```

### join() - One-to-One
```nextflow
samples_ch.join(refs_ch)  // Match by index: 1st with 1st, 2nd with 2nd
```

### join() - By Key
```nextflow
samples_ch.join(metadata_ch, by: 0)  // Match on first element (sample_id)
```

### Extract Value from File
```nextflow
file_ch.map { file -> file.baseName }.set { value_ch }
```

### Normalize Tuple Structure
```nextflow
ch.map { a, b -> [a, b, "default_value"] }
```

