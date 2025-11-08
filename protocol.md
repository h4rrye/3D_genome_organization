# 🧬 Chromosome SASA Analysis Pipeline - Complete Implementation Guide

**Project Duration:** 4 weeks (75-95 hours)
 **Start Date:** [Fill in after exams]
 **Target Completion:** [4 weeks from start]
 **Expected Job Impact:** 70-85% interview rate for computational biology positions

------

# 📋 TABLE OF CONTENTS

1. [Project Overview](https://claude.ai/chat/cc0c3219-dbe0-4d70-97fa-807ed087739a#project-overview)
2. [Prerequisites & Environment Setup](https://claude.ai/chat/cc0c3219-dbe0-4d70-97fa-807ed087739a#prerequisites--environment-setup)
3. [Week 1: Core Algorithm Development](https://claude.ai/chat/cc0c3219-dbe0-4d70-97fa-807ed087739a#week-1-core-algorithm-development)
4. [Week 2: Nextflow Pipeline Development](https://claude.ai/chat/cc0c3219-dbe0-4d70-97fa-807ed087739a#week-2-nextflow-pipeline-development)
5. [Week 3: AWS Cloud Deployment](https://claude.ai/chat/cc0c3219-dbe0-4d70-97fa-807ed087739a#week-3-aws-cloud-deployment)
6. [Week 4: Documentation & Portfolio](https://claude.ai/chat/cc0c3219-dbe0-4d70-97fa-807ed087739a#week-4-documentation--portfolio)
7. [Testing Strategy](https://claude.ai/chat/cc0c3219-dbe0-4d70-97fa-807ed087739a#testing-strategy)
8. [Troubleshooting Guide](https://claude.ai/chat/cc0c3219-dbe0-4d70-97fa-807ed087739a#troubleshooting-guide)
9. [Resources & Learning Materials](https://claude.ai/chat/cc0c3219-dbe0-4d70-97fa-807ed087739a#resources--learning-materials)

------

## 🎯 PROJECT OVERVIEW

### What You're Building

A **production-grade, cloud-native bioinformatics pipeline** that:

- Analyzes 3D chromosome structures from PDB files
- Calculates Solvent Accessible Surface Area (SASA) to identify accessible genomic regions
- Maps accessibility to genomic coordinates
- Identifies potential mutation hotspots
- Generates interactive visualizations
- Deploys on AWS Batch for scalable cloud execution
- Demonstrates modern computational biology infrastructure skills

### Why This Project Matters



**For Job Applications:**

- Demonstrates cloud infrastructure skills (AWS Batch, S3, ECR)
- Shows workflow management expertise (Nextflow DSL2)
- Proves containerization capability (Docker)
- Exhibits bioinformatics domain knowledge
- Displays software engineering practices (CI/CD, testing, documentation)

**Market Alignment:**

- AWS required in 67% of computational biology jobs
- Nextflow required in 64% of bioinformatics positions
- Docker required in 82% of computational roles
- This single project addresses all three

### Final Deliverables

By the end of 4 weeks, you will have:

1. **Working Python Package** - Modular, well-documented library
2. **Nextflow Pipeline** - DSL2 workflow with multiple processes
3. **Docker Container** - Published on Docker Hub
4. **AWS Deployment** - Running on AWS Batch
5. **Interactive Dashboard** - Plotly visualization hosted online
6. **GitHub Repository** - Professional documentation and examples
7. **Portfolio Website** - Showcase with live demos
8. **Resume-Ready Project** - With quantifiable metrics

------

## 🛠️ PREREQUISITES & ENVIRONMENT SETUP

### STEP 1: Verify Current Progress

**What to check:**

- Locate your existing `chromosome_surface.ipynb` notebook
- Verify you have the PDB data source URL working
- Confirm you can run the basic SASA calculation
- Check that visualization code produces output

**Why this matters:** You're not starting from scratch. You have working algorithm code that needs to be refactored into production format. Understanding what works now saves time later.

**Time estimate:** 30 minutes

------

### STEP 2: Install Development Tools

**What to install:**

**A. Python Development Environment**

- Python 3.10 or 3.11 (not 3.12 - some packages incompatible)
- Virtual environment manager (venv or conda)
- Package manager (pip)

**B. Code Editor/IDE**

- Cursor (recommended) - AI-assisted coding
- OR VS Code with Python extension
- Install Python linting extensions (flake8, black)

**C. Version Control**

- Git (if not already installed)
- GitHub account (create if needed)
- Configure git with your name and email

**D. Docker**

- Docker Desktop (Mac/Windows) or Docker Engine (Linux)
- Docker Hub account (free tier sufficient)
- Verify Docker works: `docker run hello-world`

**E. AWS Account**

- Create AWS account (free tier)
- Install AWS CLI v2
- Set up billing alerts (to avoid surprise charges)

**Why this matters:** Having the right tools installed before you start coding prevents frustrating interruptions. Docker and AWS setup in particular can take time due to account verification and download sizes.

**Time estimate:** 2-3 hours (includes downloads and account setup)

------

### STEP 3: Create Project Structure

**What to create:**

**Directory hierarchy:**

```
3D_genome_organization/
├── src/                          # Source code
│   ├── sasa_calculator/          # Core algorithm library
│   ├── visualization/            # Plotting and dashboard code
│   └── analysis/                 # Analysis and reporting
├── bin/                          # Executable scripts
├── modules/                      # Nextflow modules
├── workflows/                    # Nextflow workflows
├── docker/                       # Docker configurations
├── config/                       # Configuration files
├── data/                         # Data directory (gitignored)
│   ├── raw/                      # Raw PDB files
│   └── processed/                # Analysis results
├── tests/                        # Test files
├── notebooks/                    # Jupyter notebooks
├── docs/                         # Documentation
├── scripts/                      # Utility scripts
├── .github/workflows/            # CI/CD workflows
└── results/                      # Output directory (gitignored)
```

**Why this matters:** Professional project structure makes your code easy to navigate for hiring managers. It shows you understand software engineering principles beyond just "making it work." This structure is industry-standard for bioinformatics pipelines.

**Time estimate:** 30 minutes

------

### STEP 4: Set Up Python Virtual Environment

**What to do:**

**A. Create isolated environment**

- Use venv to create environment specific to this project
- Keeps dependencies separate from system Python
- Prevents version conflicts between projects

**B. Install core dependencies**

- Scientific computing: numpy, scipy, pandas
- Bioinformatics: mdtraj (for PDB parsing)
- Visualization: plotly, kaleido (for static exports)
- Utilities: tqdm (progress bars)
- Development: pytest, black, flake8

**C. Create requirements.txt**

- Pin dependency versions for reproducibility
- Include both production and development dependencies
- Document any system-level dependencies needed

**Why this matters:** Reproducible environments are crucial in scientific computing. If someone (or you, 6 months later) can't reproduce your results because of dependency issues, your work loses credibility. This is especially important for cloud deployment where you'll need exact version matching.

**Time estimate:** 1 hour

------

### STEP 5: Initialize Git Repository

**What to do:**

**A. Initialize version control**

- Create git repository
- Make initial commit with project structure
- Create meaningful .gitignore (exclude data, results, cache files)

**B. Connect to GitHub**

- Create GitHub repository (public for portfolio)
- Link local repository to GitHub remote
- Push initial structure

**C. Set up branch strategy**

- Main branch for stable code
- Development branch for work in progress
- Feature branches for major additions

**Why this matters:** Version control isn't just backup - it's your development history that proves you can work professionally. Employers will look at your commit history to see: do you make incremental progress? Do you write meaningful commit messages? Do you use branches properly? This is software engineering hygiene.

**Time estimate:** 30 minutes

------

## 📅 WEEK 1: CORE ALGORITHM DEVELOPMENT

**Goal:** Transform notebook code into production-ready Python library
 **Time:** 20-25 hours
 **End State:** Working SASA calculator as installable package

------

### STEP 6: Extract and Refactor Notebook Code

**What to do:**

**A. Analyze existing notebook**

- Identify distinct functional blocks (PDB loading, sphere generation, voxelization, surface detection)
- Note which code is exploratory vs. essential
- Identify hard-coded values that should be parameters
- Find repeated code that should be functions

**B. Create core module structure**

- Create `src/sasa_calculator/core.py` for main classes
- Create `src/sasa_calculator/utils.py` for helper functions
- Create `src/sasa_calculator/__init__.py` for package interface

**C. Convert to classes and functions**

- Transform notebook cells into methods
- Add type hints to all function signatures
- Remove print statements (replace with logging)
- Eliminate magic numbers (make them named constants)

**Why this matters:** Notebook code is for exploration. Production code is for reliability. The refactoring process forces you to think about: What are the inputs? What are the outputs? What can go wrong? What should be configurable? This transforms "it works on my machine" into "it works anywhere."

**Key principle:** If you can't explain what a function does in one sentence, it's doing too much and needs to be split.

**Time estimate:** 8-10 hours

------

### STEP 7: Implement SASA Quantification

**What to do:**

**A. Add calculation methods**

- Calculate total surface area from voxel count
- Compute surface area per genomic region
- Calculate volume and surface-to-volume ratio
- Implement density metrics

**B. Add validation**

- Verify calculations against known benchmarks
- Check edge cases (empty regions, single beads)
- Validate that results make biological sense

**C. Add error handling**

- Handle missing PDB data gracefully
- Validate input parameters
- Provide informative error messages

**Why this matters:** Right now your code identifies surface voxels but doesn't quantify them. Quantification is what makes your results scientific - you need numbers you can report, compare, and analyze. Without this, you have pretty pictures but no data. This is the difference between a visualization project and a scientific analysis tool.

**Time estimate:** 4-6 hours

------

### STEP 8: Implement Genomic Coordinate Mapping

**What to do:**

**A. Create mapping logic**

- Map chromosome bead indices to genomic positions (bp)
- Associate surface accessibility with genomic coordinates
- Handle different genome resolutions (500kb, 1Mb, etc.)

**B. Implement spatial indexing**

- Use KD-tree for efficient nearest-neighbor searches
- Map surface voxels to nearby genomic regions
- Calculate accessibility scores per region

**C. Generate structured output**

- Create DataFrame with genomic coordinates
- Add accessibility scores and percentiles
- Include physical coordinates for visualization
- Categorize regions (high/medium/low accessibility)

**Why this matters:** 3D structural data means nothing without genomic context. A region might be highly accessible, but where in the genome is it? What genes are there? Can we look up mutations in that region later? This step connects your structural analysis to biological databases and enables downstream interpretation.

**Time estimate:** 6-8 hours

------

### STEP 9: Calculate Physical Properties

**What to do:**

**A. Implement structural metrics**

- Radius of gyration (compactness measure)
- Asphericity (deviation from spherical shape)
- Surface roughness (local surface variation)
- Compactness ratio (volume/surface)

**B. Add statistical methods**

- Mean, median, standard deviation of accessibility
- Percentile calculations
- Correlation between properties

**C. Validate results**

- Compare with literature values for similar structures
- Check that metrics scale appropriately with structure size
- Verify mathematical correctness

**Why this matters:** Physical properties provide biological context. A highly accessible chromosome might be that way because it's unfolded (high radius of gyration) or because it has a rough surface (high roughness). These metrics help you tell a biological story, not just report numbers. They also demonstrate quantitative rigor in your analysis.

**Time estimate:** 4-6 hours

------

### STEP 10: Add Comprehensive Testing

**What to do:**

**A. Write unit tests**

- Test each function with known inputs/outputs
- Test edge cases and error conditions
- Aim for >80% code coverage

**B. Create integration tests**

- Test full pipeline with sample data
- Verify output format and structure
- Check that results are reproducible

**C. Add test data**

- Create small test PDB file (10-20 beads)
- Generate expected outputs manually
- Include tests in repository

**Why this matters:** Tests prove your code works. When you deploy to AWS and something breaks, tests tell you what's wrong. When you modify code later, tests ensure you didn't break existing functionality. In interviews, being able to say "95% test coverage" shows professional-level software engineering. Most biologists don't write tests - you'll stand out.

**Time estimate:** 4-6 hours

------

### STEP 11: Create Command-Line Interface

**What to do:**

**A. Build CLI script**

- Create `bin/calculate_sasa.py` executable
- Use argparse for command-line arguments
- Support all configurable parameters
- Provide helpful --help documentation

**B. Add input validation**

- Verify PDB file exists and is readable
- Check parameter ranges (positive numbers, etc.)
- Provide clear error messages for invalid inputs

**C. Structure output**

- Save results to organized directory structure
- Generate multiple output formats (JSON, CSV, NPY)
- Create metadata file with run parameters
- Log progress to console and file

**Why this matters:** A CLI makes your tool usable by others (and by automated systems like Nextflow). It's the difference between "here's my code" and "here's my tool." CLIs also force you to think about user experience: What information does someone need to run this? What defaults make sense? What could go wrong? This transforms a library into a product.

**Time estimate:** 3-4 hours

------

### WEEK 1 CHECKPOINT

**By end of Week 1, you should have:**

✅ Clean, modular Python package in `src/`
 ✅ Working SASA calculation with quantification
 ✅ Genomic coordinate mapping functional
 ✅ Physical properties calculated correctly
 ✅ Test suite passing (pytest shows green)
 ✅ CLI script that runs end-to-end
 ✅ Sample results in `results/` directory

**Test command that should work:**

```bash
python bin/calculate_sasa.py \
    --pdb [URL or file] \
    --chromosome chr1 \
    --output-dir results/chr1_test
```

**If this fails, don't proceed to Week 2** - fix Week 1 first.

------

## 📅 WEEK 2: NEXTFLOW PIPELINE DEVELOPMENT

**Goal:** Package your Python code into a Nextflow workflow
 **Time:** 20-25 hours
 **End State:** Multi-process pipeline executing locally with Docker

------

### STEP 12: Learn Nextflow Fundamentals

**What to do:**

**A. Complete official tutorials**

- Nextflow basic training (3-4 hours)
- Channels and operators (2-3 hours)
- Processes and workflows (2-3 hours)
- Understanding DSL2 syntax (1-2 hours)

**B. Study example pipelines**

- Look at nf-core pipelines (popular framework)
- Understand common patterns and best practices
- Note how they handle parameters and configuration
- See how they structure error handling

**C. Practice exercises**

- Create simple "hello world" Nextflow workflow
- Build a pipeline that processes multiple files
- Practice channel operations (map, filter, collect)
- Test locally before integrating your code

**Why this matters:** Nextflow is different from regular Python scripting. It's declarative (you describe what you want, not how to do it), it manages dataflow automatically, and it thinks in terms of processes and channels. Skipping the learning phase means you'll spend hours debugging cryptic errors. The 8-10 hours of structured learning saves 20+ hours of frustrated trial-and-error.

**Key concepts to understand:**

- Processes are isolated (they can't share memory)
- Channels pass data between processes
- Work directories are temporary
- Outputs must be explicitly published

**Time estimate:** 8-10 hours

------

### STEP 13: Build Docker Container

**What to do:**

**A. Create Dockerfile**

- Base image selection (continuumio/miniconda3 recommended)
- Install system dependencies
- Copy your Python package
- Install Python dependencies
- Set up environment variables and paths
- Define entrypoint and default command

**B. Optimize container size**

- Use multi-stage builds if needed
- Clean up temporary files
- Minimize layers
- Use .dockerignore to exclude unnecessary files

**C. Test container locally**

- Build image: `docker build -t sasa-pipeline:test .`
- Run interactively to verify environment
- Test your CLI script inside container
- Verify all dependencies present

**D. Push to Docker Hub**

- Tag with semantic version (v1.0.0)
- Push to your Docker Hub account
- Verify it's public and pullable
- Test pulling and running from Hub

**Why this matters:** Docker guarantees your code runs the same everywhere - your laptop, AWS, a collaborator's machine. It's the foundation of reproducible science and production deployment. The container you build now is what will run on AWS Batch in Week 3. If it works in Docker locally, it will work in the cloud (mostly).

**Common pitfall:** Forgetting to install system dependencies (build tools, libraries). Your laptop has them, Docker container doesn't. Test thoroughly.

**Time estimate:** 6-8 hours

------

### STEP 14: Create Nextflow Processes

**What to do:**

**A. Define CALCULATE_SASA process**

- Takes PDB file path as input
- Runs your CLI script inside Docker container
- Outputs results directory
- Specifies resource requirements (CPUs, memory)
- Handles errors appropriately

**B. Define GENERATE_VISUALIZATIONS process**

- Takes results directory as input
- Creates dashboard and plots
- Outputs HTML files
- Lighter resource requirements than SASA calculation

**C. Define CREATE_SUMMARY process**

- Collects results from multiple chromosomes
- Generates comparative summary report
- Creates final dashboard

**D. Add process directives**

- Container specification
- Resource requirements (cpus, memory, time)
- Error strategy (retry, ignore, terminate)
- Publishing directives (where outputs go)
- Labels for organization

**Why this matters:** Processes are the building blocks of Nextflow. Each process should do ONE thing and do it well (single responsibility principle). Well-defined processes make your pipeline modular - you can test each piece independently, reuse processes in other pipelines, and debug issues easily. Bad process design = unmaintainable pipeline.

**Key principle:** If a process takes more than 5 input parameters, consider splitting it into multiple processes or using a config file.

**Time estimate:** 6-8 hours

------

### STEP 15: Build Nextflow Workflow

**What to do:**

**A. Create main.nf**

- Define workflow structure (which processes run when)
- Set up input channels (from file paths, URLs, or parameters)
- Connect processes with channels
- Handle multiple chromosomes in parallel
- Collect results for summary

**B. Implement proper dataflow**

- Use tuples to keep related data together (chr, pdb_file)
- Use collect() to gather results from parallel processes
- Use map() to transform data between processes
- Handle optional inputs (ATAC-seq, mutations) gracefully

**C. Add workflow logic**

- Conditional execution (skip if files exist)
- Error handling between processes
- Progress reporting
- Final summary generation

**Why this matters:** The workflow is where your pipeline comes alive. It defines the order of operations, handles parallelization automatically, and manages data dependencies. Good workflow design means efficient execution - Nextflow will run everything it can in parallel without you explicitly programming threads or queues. Bad design means sequential execution (slow) or race conditions (errors).

**Time estimate:** 4-6 hours

------

### STEP 16: Create Configuration Files

**What to do:**

**A. Create nextflow.config**

- Default parameter values
- Process-level defaults (error handling, resources)
- Execution profiles (docker, aws, test)
- Reporting configuration (timeline, report, trace)

**B. Define execution profiles**

- **standard** - Local execution with Docker
- **test** - Small data, low resources for testing
- **aws** - AWS Batch configuration (Week 3)

**C. Add parameter schemas**

- Document all parameters
- Specify types and valid ranges
- Provide help text
- Set sensible defaults

**D. Create helper configs**

- Resource configuration (memory, CPU by process)
- Retry strategies
- Time limits
- Module organization

**Why this matters:** Configuration separates "what to run" from "how to run it." Same pipeline, different configs: local testing vs. AWS production. Good configuration makes your pipeline flexible and maintainable. Users can override defaults without modifying code. This is professional pipeline development.

**Time estimate:** 3-4 hours

------

### STEP 17: Test Pipeline Locally

**What to do:**

**A. Create test dataset**

- Small PDB file (single chromosome, low resolution)
- Reduces parameters for fast testing (d=10, b=30)
- Expected runtime: 2-5 minutes

**B. Run test pipeline**

- Execute with test profile: `nextflow run main.nf -profile test`
- Monitor execution in real-time
- Check work directories for intermediate files
- Verify outputs are created correctly

**C. Debug issues**

- Read Nextflow error messages carefully (they're verbose but informative)
- Check work directories (.command.log, .command.err)
- Verify Docker container works independently
- Test processes individually if needed

**D. Validate results**

- Compare with Week 1 Python package output
- Verify numbers match
- Check visualization quality
- Ensure metadata is correct

**Why this matters:** Testing locally before deploying to cloud saves money and time. AWS debugging is slow (pipeline runs in cloud, you watch from laptop) and costs money. Local testing is fast, free, and allows rapid iteration. Fix all bugs locally before Week 3.

**Common issues:**

- Path problems (files not where Nextflow expects)
- Docker mounting issues (volumes not accessible)
- Channel mismatches (wrong data types between processes)

**Time estimate:** 4-6 hours (including debugging)

------

### WEEK 2 CHECKPOINT

**By end of Week 2, you should have:**

✅ Docker container on Docker Hub (public)
 ✅ Nextflow pipeline running locally
 ✅ All processes executing successfully
 ✅ Results matching Week 1 output
 ✅ Configuration files for multiple profiles
 ✅ Test profile completes in <5 minutes

**Test command that should work:**

```bash
nextflow run main.nf -profile test
```

**Check these outputs exist:**

- `results/chr*/sasa_metrics.json`
- `results/chr*/accessibility.csv`
- `results/chr*/visualizations/dashboard.html`
- `results/timeline.html`

**If test fails, don't proceed to Week 3** - AWS will fail too, costing money.

------

## 📅 WEEK 3: AWS CLOUD DEPLOYMENT

**Goal:** Deploy your Nextflow pipeline to AWS Batch
 **Time:** 20-25 hours
 **End State:** Pipeline running on cloud infrastructure

------

### STEP 18: AWS Account Setup and Configuration

**What to do:**

**A. Create AWS account**

- Sign up for AWS (requires credit card, but free tier covers most usage)
- Enable MFA (multi-factor authentication) for security
- Set up billing alerts ($10, $25, $50 thresholds)
- Create IAM user (don't use root account for daily work)

**B. Install and configure AWS CLI**

- Install AWS CLI v2
- Configure with access keys: `aws configure`
- Set default region (us-west-2 recommended)
- Test connection: `aws s3 ls` (should work even if empty)

**C. Understand AWS services you'll use**

- **S3**: File storage (inputs, outputs, work directory)
- **Batch**: Compute jobs (where Nextflow processes run)
- **ECR**: Docker image registry (alternative to Docker Hub)
- **EC2**: Virtual machines (Batch uses these under the hood)
- **IAM**: Permissions (what can access what)

**Why this matters:** AWS is complex - hundreds of services, intricate permissions, and easy to misconfigure. Taking time to understand the basics prevents costly mistakes. Billing alerts are crucial - misconfigured pipelines can rack up charges quickly. The free tier covers learning and small-scale testing, but you need to stay within limits.

**Security note:** Never commit AWS credentials to GitHub. Use environment variables or AWS CLI configuration.

**Time estimate:** 2-3 hours

------

### STEP 19: Learn AWS Batch Fundamentals

**What to do:**

**A. Study AWS Batch concepts**

- **Compute Environments**: Pools of compute resources
- **Job Queues**: Where jobs wait to run
- **Job Definitions**: Blueprints for jobs (like Docker image + parameters)
- **Jobs**: Actual execution instances

**B. Understand Nextflow + AWS Batch integration**

- Nextflow acts as job submission system
- Each Nextflow process becomes one or more Batch jobs
- Nextflow manages dependencies automatically
- Work directory must be in S3 (not local)

**C. Study cost optimization**

- Spot instances (70% cheaper, can be interrupted)
- Right-sizing (don't request more resources than needed)
- Auto-scaling (compute environment scales with workload)
- Monitoring usage in AWS Cost Explorer

**D. Review tutorials**

- AWS Batch official getting started guide (1 hour)
- Nextflow AWS Batch documentation (2 hours)
- nf-core AWS tutorial (1 hour)

**Why this matters:** AWS Batch is not intuitive - it has multiple layers of configuration and complex interactions. Understanding these concepts before you start clicking in the AWS Console prevents hours of "why isn't this working?" frustration. The Nextflow-specific knowledge is crucial because Nextflow expects things configured a certain way.

**Key insight:** AWS Batch does not run containers directly. It launches EC2 instances, pulls your container, runs it, then terminates the instance. This takes 1-3 minutes of setup before your code runs.

**Time estimate:** 4-5 hours

------

### STEP 20: Set Up AWS Infrastructure

**What to do:**

**A. Create S3 bucket**

- Name: `sasa-pipeline-[your-account-id]` (must be globally unique)
- Region: us-west-2 (same as Batch for performance)
- Block public access (yes, keep private)
- Enable versioning (optional but recommended)

**B. Create IAM roles**

- **Batch execution role**: Allows Batch to run containers
- **S3 access policy**: Allows reading/writing your bucket
- Attach policies: `AmazonECS-TaskExecutionRolePolicy`
- Create inline policy for S3 bucket access

**C. Create Compute Environment**

- Type: Managed
- Provisioning model: Spot (70% cheaper)
- Instance types: Optimal (let AWS choose)
- Min vCPUs: 0 (scales to zero when idle)
- Max vCPUs: 256 (maximum parallel capacity)
- Desired vCPUs: 0 (start at zero)

**D. Create Job Queue**

- Connect to compute environment
- Priority: 100 (higher = more important)
- State: Enabled

**E. Automated setup script**

- Create `setup_aws.sh` script for reproducibility
- Script creates all infrastructure via AWS CLI
- Idempotent (safe to run multiple times)
- Documents exact configuration

**Why this matters:** Manual AWS Console setup is error-prone and not reproducible. A script documents exactly what you created and allows you (or others) to recreate the environment. This is infrastructure-as-code - a key DevOps practice. In interviews, having a setup script shows you think about reproducibility and automation.

**Cost consideration:** Compute environment scales to zero - you only pay when jobs are running. S3 storage costs ~$0.023 per GB per month.

**Time estimate:** 6-8 hours (including learning AWS Console)

------

### STEP 21: Configure Nextflow for AWS

**What to do:**

**A. Update nextflow.config**

- Add AWS profile section
- Configure executor: 'awsbatch'
- Set job queue name
- Specify S3 work directory
- Add AWS-specific process settings

**B. Update process requirements**

- Specify memory in GB (AWS needs specific amounts)
- Set CPU count (1, 2, 4, 8, 16, etc.)
- Add time limits (prevents runaway jobs)
- Configure retry strategy for spot interruptions

**C. Handle data transfer**

- Input files: Either upload to S3 or provide public URLs
- Output files: Automatically saved to S3 work directory
- Published results: Sync back to local or keep in S3
- Large files: Use S3 multipart upload

**D. Add AWS-specific error handling**

- Retry on spot interruption
- Fail fast on out-of-memory
- Log to CloudWatch (optional but useful)
- Handle S3 rate limits

**Why this matters:** AWS Batch has different constraints than local execution. Memory must be in specific increments (powers of 2), time limits prevent infinite loops, spot instances need retry logic. Good configuration means reliable execution. Poor configuration means intermittent failures and wasted time debugging.

**Common pitfall:** Requesting too little memory. Your local machine might have 32GB RAM and you never notice your process using 10GB. AWS will kill it immediately if you requested 8GB.

**Time estimate:** 3-4 hours

------

### STEP 22: Test AWS Deployment

**What to do:**

**A. Upload test data to S3**

- Create test-data prefix in your S3 bucket
- Upload small PDB file
- Verify it's accessible (use AWS CLI: `aws s3 ls`)

**B. Run small test job**

- Single chromosome, low resolution
- Monitor in AWS Console (Batch → Jobs)
- Check CloudWatch logs for errors
- Verify S3 work directory populated

**C. Debug AWS-specific issues**

- IAM permission errors (most common)
- S3 access problems (bucket policies)
- Docker pull errors (check ECR/Docker Hub access)
- Resource exhaustion (need more vCPUs in compute environment)

**D. Run full-scale test**

- Multiple chromosomes in parallel
- Standard resolution parameters
- Monitor costs in Cost Explorer
- Verify parallel execution working

**E. Retrieve results**

- Use AWS CLI to sync S3 results locally
- Verify output format matches local execution
- Check that visualizations render correctly
- Validate data integrity (compare checksums)

**Why this matters:** First AWS run always has problems. That's normal. Testing incrementally (single job → multiple jobs) helps isolate issues. AWS error messages are often cryptic ("InternalServerError"), but systematic debugging works: Does IAM allow this? Can Batch reach Docker Hub? Is S3 path correct? Fix one issue at a time.

**Cost monitoring:** Check Cost Explorer daily during testing. A misconfigured pipeline can cost $50-100 if left running. Billing alerts should catch this, but manual checks are good practice.

**Time estimate:** 6-8 hours (including debugging)

------

### STEP 23: Optimize for Cost and Performance

**What to do:**

**A. Right-size resources**

- Profile actual memory usage (CloudWatch metrics)
- Don't over-request resources (wastes money)
- Use spot instances wherever possible
- Set appropriate time limits

**B. Optimize S3 usage**

- Use S3 lifecycle policies (delete old work directories)
- Compress large files
- Batch small files together
- Use intelligent tiering for long-term storage

**C. Minimize data transfer**

- Keep data in same region as compute
- Use S3 VPC endpoints (free transfer)
- Only download final results, not intermediate files
- Use S3 sync instead of cp for large directories

**D. Implement caching**

- Nextflow can cache results (avoid re-running unchanged processes)
- Use version control for cache invalidation
- Store reusable intermediate results

**E. Monitor and iterate**

- Check Cost Explorer weekly
- Identify most expensive operations
- Optimize high-cost processes first
- Document cost per analysis run

**Why this matters:** First deployment focus on "does it work?" Now focus on "does it work efficiently?" A pipeline that costs $50 per run is not production-ready if it could cost $5 with optimization. Employers want to see you think about operational costs, not just technical implementation. This shows business awareness.

**Real example:** Reducing memory allocation from 16GB to 8GB (because profiling showed you only used 6GB) can cut costs 50% with zero impact on results.

**Time estimate:** 3-4 hours

------

### WEEK 3 CHECKPOINT

**By end of Week 3, you should have:**

✅ AWS account configured with Batch setup
 ✅ Pipeline running successfully on AWS
 ✅ Results syncing to S3 correctly
 ✅ Cost per run documented and optimized
 ✅ AWS configuration script (`setup_aws.sh`)
 ✅ Updated nextflow.config with AWS profile

**Test command that should work:**

```bash
nextflow run main.nf -profile aws \
    --s3_bucket sasa-pipeline-[account-id]
```

**Cost check:**

- ###### Total AWS charges: Should be <$10 for





