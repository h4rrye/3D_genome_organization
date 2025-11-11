### Genomics Packages



Best Python libraries to prepare 3D genomic data

1. pyGenomeTracks

Generate genome tracks → export as arrays to overlay on your 3D model.
2. cooltools / cooler

For Hi-C contact matrices → build 3D models downstream.
3. pastis / Chrom3D / miniMDS

To convert Hi-C → 3D coordinates.
4. PyVista / Vedo (for offline 3D debugging)

Before sending to web.
5. NetworkX or custom adjacency

If you want to represent domains as 3D graph segments.

____

# 3D Chromosome Model — Network / Graph Properties (Markdown)

Below is a copyable **Markdown** version of the summary describing graph-theory and spatial-network features you can compute from XYZ coordinates of a chromosome model.

------

# ✅ Overview

3D chromosome models (e.g., Hi-C–based polymer reconstructions) can be treated as **spatial networks**. From XYZ coordinates you first choose how to build edges (distance threshold, k-NN, weighted by distance or Hi-C), then compute local, global, spatial, polymer-specific and centrality properties to gain biological insight.

------

# ✅ 1. Basic graph construction choices

From XYZ coordinates you must define edges. Common approaches:

- **Distance threshold graph**
   Connect nodes (genomic bins) if `distance < d`. Good for local chromatin compaction studies.
- **k-nearest neighbor graph**
   Each node links to its `k` closest nodes. Creates more uniform connectivity useful for comparing nodes.
- **Contact probability / distance-weighted graph**
   Edge weight = `1 / distance` or `weight = exp(−distance^2 / σ^2)`.
- **Hi-C–weighted graph (if you also have Hi-C)**
   Use Hi-C frequency as edge weight; you can combine geometry + experimental contact frequency.

------

# ✅ 2. Local network properties

- **Degree** — number of contacts a bin has. Higher degree → locally compact regions; can indicate heterochromatin.
- **Weighted degree (strength)** — sum of contact weights; correlates with compaction.
- **Clustering coefficient** — fraction of neighbors that are connected; high values indicate globular/compact subregions (e.g., TAD-like structures).

------

# ✅ 3. Global graph properties

- **Average path length & diameter** — how far signals travel through the polymer; informs on looping and connectivity.
- **Modularity / community detection** — algorithms like Louvain or Leiden reveal compartments (A/B), TADs, subcompartments.
- **Assortativity** — do high-degree nodes preferentially connect to other high-degree nodes? Measures hierarchical folding.

------

# ✅ 4. Spatial network properties

- **Radius of gyration (Rg)** — global compaction measure; useful for comparing conditions or cell types.
- **Spatial clustering / Ripley’s K-function** — detects clustering across spatial scales; good for domain boundary detection.
- **Radial positioning** — distance from nuclear center; loci near periphery often correlate with repression (requires nucleus geometry).

------

# ✅ 5. Polymer-specific properties

Because chromosomes are polymers, compute:

- **Contact decay exponent**
   Fit `P(s) ~ s^(−α)` where `s` is genomic separation. Typical interpretation: α ≈ 1 for open, α > 1 for compact polymers.
- **Local curvature & bending angles**
   Measure flexibility/stiffness. Biological meaning: nucleosome density, transcriptional state.
- **Loop detection**
   Identify locus pairs with anomalously close spatial distance relative to genomic separation — analogous to Hi-C loops (e.g., CTCF loops).

------

# ✅ 6. Centrality measures (and biological meaning)

- **Betweenness centrality** — nodes on many shortest paths; often structural anchors or TAD borders.
- **Closeness centrality** — how close a locus is to all other loci; higher closeness can correlate with gene-rich, active regions.
- **Eigenvector centrality** — captures hierarchical architecture; useful for separating A vs B compartments.

------

# ✅ 7. Multiscale / hierarchical structure

- **Multi-resolution communities** — run community detection with different resolution (`γ`) values:
  - small `γ` → compartments
  - medium `γ` → TADs
  - large `γ` → microdomains
- **Core–periphery structure** — identify central “core” loci vs peripheral ones; active genes often lie in cores.

------

# ✅ 8. Dynamic / ensemble properties

If you have multiple conformations (an ensemble):

- **Structural variability** — RMSD between structures; regions with high variability are flexible and often transcriptionally active.
- **Temporal / ensemble networks** — analyze how network properties change across conformations or cells.

------

# ✅ Top 10 features to compute (quick list)

1. Degree / strength (local compaction)
2. Clustering coefficient (domain structure)
3. Path length (polymer connectivity)
4. Modularity (TADs / compartments)
5. Betweenness centrality (anchors + TAD boundaries)
6. Eigenvector centrality (compartment signal)
7. Radius of gyration (global compaction)
8. Contact decay exponent `α`
9. Loop detection via distance anomalies
10. Radial positioning (if nucleus geometry available)

___

## Graph Construction

First, define nodes (chromatin beads/loci) and edges (typically by distance threshold or contact frequency). Common approaches:

- **Distance-based**: edges between nodes within a cutoff distance (e.g., spatial neighbors)
- **Contact-based**: if you have Hi-C data alongside coordinates
- **Polymer chain**: sequential connectivity along the chromosome

## Core Network Properties

**Local measures:**

- **Degree distribution**: number of spatial contacts per locus
- **Clustering coefficient**: how neighbors of a node are connected (indicates local compaction)
- **Betweenness centrality**: nodes acting as bridges between different regions
- **Closeness centrality**: identifies accessible/central genomic regions

**Global measures:**

- **Average path length**: typical separation between loci
- **Network diameter**: maximum shortest path
- **Modularity/Community detection**: identify TADs (Topologically Associating Domains) or compartments
- **Small-world coefficient**: ratio of clustering to path length (chromatin often shows small-world properties)

## Chromosome-Specific Properties

**Structural:**

- **Contact enrichment**: ratio of observed to expected contacts at different genomic distances
- **Radius of gyration**: measure of chromatin territory compactness
- **Fractal dimension**: scaling properties of chromosome folding

**Functional:**

- **Persistent homology**: topological features at multiple spatial scales
- **Graph Laplacian eigenvectors**: spectral analysis can reveal compartmentalization
- **Minimum spanning tree**: backbone of chromosome organization

**Dynamic (if you have multiple conformations):**

- **Edge persistence**: which contacts are stable across structures
- **Network rewiring**: how topology changes between conditions