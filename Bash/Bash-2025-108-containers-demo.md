# Apptainer Bioinformatics Demos: Hands-On Containerization for Reproducible Workflows

## Introduction

Welcome to this educational tutorial on using **Apptainer** (formerly Singularity) for bioinformatics workflows! This demo series is designed to give you **real hands-on experience** with container technology in a scientific computing context. We'll start from the basics of container verification and progressively build up to a full alignment pipeline, emphasizing reproducibility, provenance tracking, and customization.

### Why Containers in Bioinformatics?
Bioinformatics pipelines often involve complex dependencies (e.g., specific versions of Python, R, or tools like SAMtools). Installing these on shared clusters or laptops can lead to "it works on my machine" issues. **Containers** package everything—code, libraries, and environment—into a portable, immutable image. Apptainer excels in HPC environments because it:
- Runs as your user (no root needed).
- Supports bind mounts for data sharing.
- Ensures reproducibility via checksums and inspectable metadata.
- Integrates seamlessly with tools like SLURM.

By the end of these demos, you'll:
- Verify container basics (security, isolation).
- Run quality control (QC) on sequencing data.
- Build a multi-tool pipeline for read alignment.
- Customize and compare images for reproducibility.

**Rationale for Incremental Approach**: We build step-by-step to reinforce concepts. Demo 1 ensures your Apptainer setup works. Demo 2 introduces tool execution. Demo 3 chains tools into a pipeline. Demo 4 tests reproducibility—key for publications and collaboration. This progression mirrors real-world workflow development: start simple, validate, scale, and audit.

### Prerequisites
- **Apptainer** installed (v1.0+; check with `apptainer --version`).
- Internet access (for pulling Docker images).
- Bash shell on a Linux/macOS system (HPC cluster recommended).
- ~2 GB disk space (for data/images).

## Quick Setup: Run the Preparer Script

To bootstrap everything (data, scripts, images, results), run the provided `manage-containers.sh`:

```bash
chmod +x manage-containers.sh
./manage-containers.sh
```

This script automates the entire setup for efficiency, allowing you to focus on learning rather than boilerplate. It handles:
1. **Data Acquisition**: Downloads a real-world Oxford Nanopore (ONT) FASTQ dataset (ERR769583.fastq.gz, ~274 MB, from EBI SRA) and the human reference genome (hg38). This dataset is chosen for its realistic size—small enough for quick demos but large enough to show performance (e.g., ~6.4M reads).
2. **Script Generation**: Dynamically creates the four demo scripts with environment-aware paths (e.g., via `RAW_DIR` and `RES_DIR` vars) to support isolated re-runs.
3. **Image Building and Execution**: Pulls/builds all SIF images and executes demos in sequence, using fallbacks for robustness (e.g., if a Docker tag is unavailable).
4. **Structure Output**: Ensures a clean directory layout for easy inspection.

After running, use `tree` (or `ls -la`) to explore the generated structure:
```
.
├── manage-containers.sh
├── demo1.sh
├── demo2_fastqc.sh
├── demo3_samtools.sh
├── demo4_build_compare.sh
├── raw/                  # Data: FASTQ, ref.fasta, ref.mmi
├── ref.sh                # Re-download script
├── results1/             # Demo 1 outputs (e.g., inspect.txt)
├── results2/             # Demo 2: FastQC reports
├── results3/             # Demo 3: BAM files, stats
├── results4/             # Demo 4: Comparison artifacts
├── fastqc.sif
├── minimap2.sif
├── samtools.sif
├── samtools_2.sif
└── ubuntu-22.04.sif
```

**Time**: ~5-10 min (downloads/builds). Now, let's dive deeper into each demo. For every demo, we'll cover:
- **Philosophy**: The core guiding principle.
- **Idea & Why This Example**: The conceptual motivation and rationale for choosing this specific scenario.
- **Learning Aspects**: Key takeaways and skills you'll gain.
- **What It Does**: High-level overview of the workflow.
- **Code Breakdown**: Detailed section-by-section explanation of the generated script (`demoX.sh`), including what each part does and why it's structured that way.
- **Why This Matters**: Broader implications.
- **How to Run**: Command to execute.
- **Expected Output**: Sample console logs.
- **Inspect Results**: Key files and how to use them.
- **Hands-On Tip**: Quick modification idea.

You can re-run individual demos with env vars (e.g., `RAW_DIR=./raw RES_DIR=my_results sh demo2_fastqc.sh`) to experiment without resetting everything.

## Demo 1: Verifying Container Basics (ubuntu-22.04.sif)

### Philosophy
The foundation of trustworthy computing is verification: before trusting a container for critical analysis, confirm it behaves as expected in isolation. This demo embodies "trust but verify"—ensuring Apptainer's security model (e.g., unprivileged execution) holds without assumptions.

### Idea & Why This Example
We chose a plain Ubuntu base image because it's the "hello world" of containers—ubiquitous, minimal, and representative of any OS layer in a bioinformatics stack. This example demystifies Apptainer's internals early, preventing later frustrations (e.g., permission errors in HPC). It's the "safety net" demo: if this fails, your setup is broken; if it passes, you're ready for tools.

### Learning Aspects
- Understand Apptainer's user-mode execution and isolation primitives.
- Appreciate provenance as a habit for auditing (e.g., for grants or papers).
- Gain debugging confidence: simple tests build intuition for complex failures.
- Hands-on: Modify the verifier to probe deeper, fostering exploratory learning.

### What It Does
Pulls a base Ubuntu 22.04 image and runs a verification script (`verify_ubuntu_sif.sh`) that checks core Apptainer features. Each step below builds trust incrementally.

1. **UID Preservation**: Ensures the container runs as *your* user (not root).  
   **Essence**: Apptainer maps your host UID/GID into the container via namespaces, avoiding root escalation risks. This is crucial for multi-user HPC—prevents one user's container from overwriting another's data. In practice, it enables seamless file ownership (e.g., outputs stay yours).

2. **OS Detection**: Confirms the image contents (Ubuntu 22.04).  
   **Essence**: Validates the image's integrity and contents without unpacking. This catches corrupted pulls or wrong tags early. In bio workflows, mismatched OS versions can break compiled binaries (e.g., glibc mismatches).

3. **Read-Only Root FS**: Tests immutability—can't write to container's root.  
   **Essence**: Enforces the container's "black box" principle: changes don't persist across runs, reducing drift. Essential for reproducibility—your pipeline won't accidentally install packages mid-run, altering future executions.

4. **Bind Mounts**: Mounts a temp dir as writable workspace (simulates data sharing).  
   **Essence**: Demonstrates `-B host_dir:container_dir` for I/O without copying large files (e.g., genomes). In HPC, this is key for performance: mount `/scratch` for temp writes, keeping containers lightweight.

5. **Clean Environment**: Verifies `--cleanenv` isolates host vars.  
   **Essence**: Prevents host pollution (e.g., a rogue `$PATH` breaking tools). Critical for determinism—ensures the same image yields identical results on different machines.

6. **Provenance**: Saves `inspect` metadata and SHA256 checksum.  
   **Essence**: `apptainer inspect` extracts build history/labels; `sha256sum` verifies no tampering. This is the "audit trail" for science: cite exact images in methods sections.

### Code Breakdown
The `demo1.sh` script is a thin wrapper that generates and runs `verify_ubuntu_sif.sh`. Here's a section-by-section explanation:

- **Shebang and Strict Mode**:  
  ```bash
  #!/usr/bin/env bash
  set -euo pipefail
  ```  
  **What it does**: Declares Bash as the interpreter and enables strict error handling (`-e`: exit on error, `-u`: error on unset vars, `-o pipefail`: fail if any pipe command fails).  
  **Why**: Ensures the script halts on issues, preventing partial runs that could corrupt state—core to robust scripting in education/HPC.

- **Generate Inner Script**:  
  ```bash
  cat > verify_ubuntu_sif.sh <<'INNER_EOF'
  set -euo pipefail

  RES_DIR="${RES_DIR:-.}"
  SIF=${1:-ubuntu-22.04.sif}
  # ... (all checks)
  INNER_EOF
  ```  
  **What it does**: Uses a here-document to write the verifier script to disk, defaulting `RES_DIR` to current dir and `SIF` to the Ubuntu image. Includes all 6 checks as inline commands.  
  **Why**: Allows the inner script to be standalone/executable, promoting modularity—students can run it separately for testing.

- **Make Executable and Run**:  
  ```bash
  chmod +x verify_ubuntu_sif.sh
  RES_DIR=results1 ./verify_ubuntu_sif.sh ubuntu-22.04.sif
  ```  
  **What it does**: Sets execute permissions and runs the verifier, overriding `RES_DIR` to isolate outputs.  
  **Why**: Demonstrates env var propagation for flexibility (e.g., change `results1` for new runs), teaching configurable scripts.

### Why This Matters
Containers must be secure and predictable. UID matching avoids permission issues; immutability prevents tampering; binds enable data I/O without copying. Without these basics, advanced pipelines crumble.

### How to Run
```bash
sh demo1.sh  # Auto-runs verify_ubuntu_sif.sh with RES_DIR=results1
```

### Expected Output
```
[1/6] Identity check... OK: UID preserved (your_uid).
...
[DONE] All checks passed.
```

### Inspect Results (`results1/`)
- `ubuntu-22.04.inspect.txt`: Image metadata (labels, env).
- `ubuntu-22.04.sif.sha256`: File integrity checksum.

**Hands-On Tip**: Edit `verify_ubuntu_sif.sh` to add `apptainer exec ubuntu-22.04.sif apt list --installed | grep -i curl`. Re-run—see installed packages without host pollution. Why? Teaches querying container state safely.

## Demo 2: Quality Control with FastQC (fastqc.sif)

### Philosophy
Quality control is the gatekeeper of data integrity: garbage in, garbage out. This demo treats containers as "versioned tools," ensuring QC results are comparable across labs or time, aligning with FAIR principles (Findable, Accessible, Interoperable, Reusable).

### Idea & Why This Example
FastQC is a staple first step in NGS analysis—universal yet insightful (plots reveal biases). We use ONT data because it's noisy/realistic, highlighting container benefits (e.g., Java deps for plots). This example bridges basics to analysis: "Now that containers work, let's analyze real data."

### Learning Aspects
- Master image building from registries with fallbacks (robustness in unstable nets).
- Learn bind mounts for input/output separation.
- Interpret bio outputs (e.g., QC metrics) in a containerized context.
- Emphasize verification: always check artifacts exist and match expectations.

### What It Does
Builds a FastQC container from BioContainers (tries v0.12.1, falls back to v0.11.9). Runs it on the FASTQ. Steps focus on execution reliability.

1. **Build Image**: Pulls from Docker Hub (quay.io/biocontainers).  
   **Essence**: `apptainer build` converts OCI (Docker) to SIF format. Fallbacks (loop over candidates) ensure success if a tag 404s. In practice, this teaches "defense in depth"—pin versions but plan for mirrors.

2. **Run QC**: Analyzes base quality, GC content, adapters (binds `raw/` and `results2/`).  
   **Essence**: `--env` sets UTF-8 for plots; `-B`/`--pwd` directs I/O. Progress logs show real-time feedback. Essential for scaling: containers hide Java/Perl deps, letting you focus on biology.

3. **Verify Outputs**: Checks HTML/ZIP reports exist.  
   **Essence**: `test -s` confirms non-empty files. This "fail-fast" pattern catches runtime errors (e.g., OOM). In workflows, it enables CI/CD-like automation.

4. **Provenance**: Saves source URI, inspect, and checksum.  
   **Essence**: Logs the exact URI used, plus metadata. Ties back to Demo 1: now provenance includes *runtime* details, enabling full audit (e.g., "This plot from FastQC v0.12.1").

FastQC processes ~6.4M reads, outputting progress (e.g., "Approx 50% complete").

### Code Breakdown
The `demo2_fastqc.sh` script is self-contained, using env vars for paths. Sections align with the steps:

- **Shebang, Strict Mode, and Path Setup**:  
  ```bash
  #!/usr/bin/env bash
  set -euo pipefail

  RAW_DIR="${RAW_DIR:-$(pwd)/raw}"
  RES_DIR="${RES_DIR:-$(pwd)/results}"
  mkdir -p "$RAW_DIR" "$RES_DIR"
  ```  
  **What it does**: Enables strict Bash mode; defaults dirs to subdirs under pwd, creates them if missing.  
  **Why**: Makes the script portable—run anywhere with overrides; `mkdir -p` prevents dir errors.

- **Candidates and Build Loop**:  
  ```bash
  CANDIDATES=(
    "docker://quay.io/biocontainers/fastqc:0.12.1--0"
    "docker://biocontainers/fastqc:v0.11.9_cv8"
  )
  SIF="fastqc.sif"
  built=0
  echo "[1/5] Build SIF (FastQC)…"
  for ref in "${CANDIDATES[@]}"; do
    echo "  Trying: $ref"
    if apptainer build "$SIF" "$ref" >/dev/null 2>&1; then
      echo "$ref" > "$RES_DIR/fastqc.source.txt"
      built=1; break
    fi
  done
  [[ $built -eq 1 ]]
  ```  
  **What it does**: Defines fallback URIs; loops to build until success, logs source, asserts build happened.  
  **Why**: Handles transient failures (e.g., network); `>/dev/null` suppresses noise, but echoes progress for feedback.

- **Input Check and Run**:  
  ```bash
  INPUT="${RAW_DIR}/ERR769583.fastq.gz"
  [[ -s "$INPUT" ]] || { echo "Missing input: $INPUT"; exit 1; }

  echo "[2/5] Run FastQC…"
  apptainer exec \
    --env LC_ALL=C.UTF-8 --env LANG=C.UTF-8 \
    -B "$RAW_DIR":/raw -B "$RES_DIR":/results --pwd /results "$SIF" \
    sh -lc 'fastqc -o /results /raw/ERR769583.fastq.gz'
  ```  
  **What it does**: Validates input size; execs FastQC with env for locale, binds dirs, runs via `sh -lc` for login shell.  
  **Why**: Env fixes encoding issues; binds isolate I/O; `-lc` ensures PATH is set.

- **Verify and Provenance**:  
  ```bash
  echo "[3/5] Verify outputs…"
  HTML="$RES_DIR/ERR769583_fastqc.html"
  ZIP="$RES_DIR/ERR769583_fastqc.zip"
  test -s "$HTML" && test -s "$ZIP" && echo "  OK: reports present"

  echo "[4/5] Provenance…"
  apptainer inspect "$SIF" | tee "$RES_DIR/fastqc.inspect.txt" >/dev/null
  sha256sum "$SIF" | tee "$RES_DIR/fastqc.sif.sha256" >/dev/null

  echo "[5/5] Done."
  ```  
  **What it does**: Tests file existence; pipes inspect/sha256 to files (tee for logging, null for quiet).  
  **Why**: Short-circuit `&&` for quick OK; provenance ties to runs, enabling traceability.

### Why This Matters
Raw sequencing data needs QC before analysis. Containers ensure the exact FastQC version (e.g., for reproducible plots). Fallback candidates handle registry downtime.

### How to Run
```bash
RAW_DIR=./raw RES_DIR=results2 sh demo2_fastqc.sh
```

### Expected Output
```
[1/5] Build SIF... Trying: docker://quay.io/biocontainers/fastqc:0.12.1--0
[2/5] Run FastQC... Analysis complete...
[3/5] Verify... OK: reports present
...
[5/5] Done.
```

### Inspect Results (`results2/`)
- `ERR769583_fastqc.html`: Interactive report (open in browser: per-base quality ~Q10-15, no severe issues).
- `ERR769583_fastqc.zip`: Raw data.
- `fastqc.source.txt`: Which image was used.

**Hands-On Tip**: Subset data (`zcat raw/ERR769583.fastq.gz | head -400000 > raw/sub.fastq.gz`) and re-run. Compare HTMLs—what drops in "Per sequence quality"? Why? Explores data scale effects.

## Demo 3: Alignment Pipeline (minimap2.sif + samtools.sif)

### Philosophy
Pipelines are the backbone of scalable science: compose tools like Lego blocks. This demo promotes "modular reproducibility"—each tool in its container, piped for efficiency, ensuring the whole exceeds the sum.

### Idea & Why This Example
Alignment is a core NGS task, using minimap2 (fast for long ONT reads) + SAMtools (BAM manipulation). hg38 ref adds realism (455 chromosomes). Chosen because it's non-trivial (multi-tool, threading) but quick, showing containers solve dep hell (e.g., HTSlib versions).

### Learning Aspects
- Handle multi-image workflows (build, exec across them).
- Use pipes/bind for low-overhead chaining.
- Generate/interpret standard outputs (BAMs, stats).
- Version pinning + fallbacks for production robustness.

### What It Does
Builds two images (minimap2 v2.28 fallback to v2.26; samtools v1.19.2 fallback to v1.17). Builds a pipeline. Steps mirror a minimal aligner.

1-2. **Build Images**: From BioContainers (version-pinned for reproducibility).  
   **Essence**: Separate loops ensure each tool's deps are isolated (e.g., minimap2's custom allocators). Pinning prevents "upstream" breaks; fallbacks add resilience. In practice, this scales to 10+ tools without conflicts.

3. **Index Ref**: `minimap2 -d ref.mmi ref.fasta` (hashes hg38 for fast lookup).  
   **Essence**: Pre-computes minimizers (k-mers) for O(1) queries. Idempotent (`test -s`) avoids re-work. Essential for speed: full hg38 index takes ~1 min, reused across runs.

4. **Align**: Pipe `minimap2 -ax map-ont` (ONT mode) → `samtools view -bS` → unsorted BAM.  
   **Essence**: `-t 2` uses threads; pipe avoids disk I/O for intermediates. ONT preset handles long/error-prone reads. Teaches streaming: containers make this seamless across images.

5. **Sort/Index**: `samtools sort` + `samtools index` (coordinate-sorted, queryable BAM).  
   **Essence**: Sorting enables region queries (e.g., IGV viewing); index speeds random access. Coordinate sort is standard for callers. In workflows, this creates "shareable" artifacts.

6. **Stats**: `samtools flagstat` (e.g., 71.87% mapped, 6.4M primary alignments).  
   **Essence**: Quick sanity (head -n10 limits output). Quantifies success (e.g., low map rate flags issues). Builds habit: always log metrics for QC.

7-8. **Provenance**: Inspect/checksum both images.  
   **Essence**: Extends to pipeline: now track *all* components. Enables "replay" (e.g., re-align with new data).

This processes the full ~274 MB FASTQ in ~2-3 min (2 threads).

### Code Breakdown
The `demo3_samtools.sh` script is modular, with comments separating phases. It uses consistent patterns from prior demos.

- **Shebang, Strict Mode, and Input Validation**:  
  ```bash
  #!/usr/bin/env bash
  set -euo pipefail

  RAW_DIR="${RAW_DIR:-$(pwd)/raw}"
  RES_DIR="${RES_DIR:-$(pwd)/results}"
  mkdir -p "$RAW_DIR" "$RES_DIR"

  FASTQ="${RAW_DIR}/ERR769583.fastq.gz"
  REF="${RAW_DIR}/ref.fasta"

  [[ -s "$FASTQ" ]] || { echo "Missing FASTQ: $FASTQ"; exit 1; }
  [[ -s "$REF"  ]] || { echo "Missing reference FASTA: $REF"; exit 1; }
  ```  
  **What it does**: Sets strict mode/paths; checks file existence/size with `[[ -s ]]` and exits if missing.  
  **Why**: Fail-fast on prerequisites; braces `{}` group error handling for clarity.

- **Build Loops (Steps 1-2)**:  
  ```bash
  # --- Build containers (version-pinned, with fallbacks) -----------------------
  SAMTOOLS_SIF="samtools.sif"
  MINIMAP2_SIF="minimap2.sif"

  SAMTOOLS_CAND=( ... )  # Array of URIs
  MINIMAP2_CAND=( ... )

  echo "[1/8] Build SIF (samtools)…"
  built=0
  for ref in "${SAMTOOLS_CAND[@]}"; do
    # ... try build, log source, break on success
  done
  [[ $built -eq 1 ]]

  # Similar for minimap2 [2/8]
  ```  
  **What it does**: Defines SIF names and URI arrays; loops try builds quietly (`>/dev/null`), logs successful URI, asserts success.  
  **Why**: Reuses pattern for multi-tool; separate sections for readability; `[[ ]]` is Bash's robust test.

- **Index, Align, Sort/Index (Steps 3-6)**:  
  ```bash
  echo "[3/8] Index reference with minimap2…"
  apptainer exec -B "$RAW_DIR":/raw -B "$RES_DIR":/results --pwd /results "$MINIMAP2_SIF" \
    sh -lc 'test -s /raw/ref.mmi || minimap2 -d /raw/ref.mmi /raw/ref.fasta'
  test -s "$RAW_DIR/ref.mmi"

  echo "[4/8] Align FASTQ to reference → BAM (unsorted)…"
  apptainer exec ... "$MINIMAP2_SIF" sh -lc 'minimap2 -t 2 -ax map-ont ...' | \
  apptainer exec ... "$SAMTOOLS_SIF" sh -lc 'samtools view -bS - > align.bam'
  test -s "$RES_DIR/align.bam"

  # Similar for [5/8] sort and [6/8] index
  ```  
  **What it does**: Exec with binds/pwd; inner `sh -lc` for commands; pipe for align; `test -s` post-checks.  
  **Why**: Binds enable shared data; pipe streams to save space; idempotent index avoids recompute.

- **Stats and Provenance (Steps 7-8)**:  
  ```bash
  echo "[7/8] Mapping stats…"
  apptainer exec ... sh -lc 'samtools flagstat align.sorted.bam | head -n 10'

  echo "[8/8] Provenance…"
  apptainer inspect "$SAMTOOLS_SIF" | tee "$RES_DIR/samtools.inspect.txt" >/dev/null
  # ... similar for sha256sum and minimap2
  echo "Done."
  ```  
  **What it does**: Runs flagstat with `head` for brevity; tees inspect/sha256 to files quietly.  
  **Why**: Logs key metrics to console; provenance per-tool for granular audits.

### Why This Matters
Alignment turns reads into genomic coordinates. Chaining tools via pipes avoids intermediates. Containers isolate deps (e.g., minimap2's custom k-mers). Outputs enable downstream (e.g., variant calling).

### How to Run
```bash
RAW_DIR=./raw RES_DIR=results3 sh demo3_samtools.sh
```

### Expected Output
```
[1/8] Build SIF (samtools)... OK
[2/8] Build SIF (minimap2)... OK
[3/8] Index... [M::mm_idx_stat] 455 sequences
[4/8] Align... mapped 6402975 sequences
[5/8] Sort... [bam_sort_core] merging...
[6/8] Index...
[7/8] Mapping stats... 71.87% : N/A
[8/8] Provenance... Done.
```

### Inspect Results (`results3/`)
- `align.sorted.bam` / `.bai`: Core output (use `samtools view align.sorted.bam | head` to peek).
- `*.source.txt`: Image URIs.
- `*.inspect.txt` / `*.sha256`: Metadata/checksums.

**Hands-On Tip**: Change `-ax map-ont` to `-ax sr` (short-read). Re-run—mapping rate drops? Add `samtools markdup` for duplicates. Why? Tests parameter sensitivity.

## Demo 4: Custom Image Building & Reproducibility (samtools_2.sif)

### Philosophy
Reproducibility isn't accidental—it's engineered. This demo asserts "same input, same image, same output," using custom builds to layer metadata without altering behavior, embodying open science's auditability.

### Idea & Why This Example
Building from a def file on a prior BAM tests "round-trip" fidelity: re-process and compare. SAMtools sort is deterministic (given env), making it ideal for bit-level checks. Chosen to cap the series: from verification to validation.

### Learning Aspects
- Craft def files for customization (labels, env).
- Implement quantitative comparisons (diff, MD5).
- Debug non-determinism (e.g., headers vs. body).
- Value layered provenance for collaboration.

### What It Does
Uses Demo 3's outputs to build/test a custom image. Steps validate equivalence.

1. **Prep Def File**: Creates `samtools_from_local.def` (localimage bootstrap from `samtools.sif` + labels/env/runscript).  
   **Essence**: "Localimage" embeds an existing SIF as base. Adds non-functional layers (e.g., `%runscript exec samtools`). Essential for "extending" pre-built images without forking.

2. **Build Custom**: `apptainer build samtools_2.sif def` (adds metadata without changing binaries).  
   **Essence**: Fakeroot runs post-sections safely. Idempotent (checks existing). In practice, this allows site-specific tweaks (e.g., custom paths) while inheriting BioContainers' work.

3. **Versions**: Compares `samtools --version` (both 1.19.2).  
   **Essence**: Quick functional smoke test. Catches build errors early. Teaches: metadata ≠ binaries; versions confirm equivalence.

4. **Re-run Sort/Index**: On copy of BAM → new artifacts.  
   **Essence**: `cp` isolates; re-executes to simulate re-run. Uses same binds for parity. Essential: proves pipeline idempotence.

5. **Compare idxstats**: `diff` on per-chr stats (identical).  
   **Essence**: `samtools idxstats` is lightweight, chr-specific. Byte-for-byte match flags sorting bugs. Builds to full verification.

6. **MD5 Alignments**: Hashes body (ignores headers) → match confirms bit-for-bit reproducibility.  
   **Essence**: `samtools view | md5sum` strips @PG (provenance) diffs. Cut extracts hash. Gold standard: if this matches, the analysis is identical.

7. **Provenance**: Inspect/checksum new image.  
   **Essence**: Compares to base (e.g., via diff on inspects). Closes loop: now you have "before/after" for customs.

Fails if mismatch (e.g., version change).

### Code Breakdown
The `demo4_build_compare.sh` script depends on Demo 3 outputs, using conditionals for idempotence. It emphasizes comparisons.

- **Shebang, Strict Mode, and Prereqs**:  
  ```bash
  #!/usr/bin/env bash
  set -euo pipefail

  RAW_DIR="${RAW_DIR:-$(pwd)/raw}"
  RES_DIR="${RES_DIR:-$(pwd)/results}"
  RES_DIR3="${RES_DIR3:-$(pwd)/results3}"
  mkdir -p "$RAW_DIR" "$RES_DIR"

  SIF_BASE="samtools.sif"  # ...
  BAM_BASE="${RES_DIR3}/align.sorted.bam"  # ...

  [[ -s "$SIF_BASE" ]] || { echo "Missing $SIF_BASE (run demo3 first)."; exit 1; }
  # Similar checks for BAM/BAI
  ```  
  **What it does**: Sets mode/paths (adds `RES_DIR3` for cross-demo); validates prereqs with exits.  
  **Why**: Enforces dependencies; teaches script chaining.

- **Def File Generation**:  
  ```bash
  if [[ ! -f "$DEF_LOCAL" ]]; then
    cat > "$DEF_LOCAL" <<'DEF'
  Bootstrap: localimage
  From: samtools.sif
  %labels
      # ...
  %environment
      # ...
  %runscript
      # ...
  DEF
  fi
  ```  
  **What it does**: Checks existence; writes def with here-doc if missing (localimage embeds base SIF).  
  **Why**: Idempotent—avoids overwrites; def sections add metadata without rebuilds.

- **Build and Version Check**:  
  ```bash
  if [[ -s "$SIF_NEW" ]]; then
    echo "[1/6] Using existing $SIF_NEW."
  else
    echo "[1/6] Building $SIF_NEW from $DEF_LOCAL (localimage)…"
    apptainer build "$SIF_NEW" "$DEF_LOCAL"
  fi

  echo "[2/6] samtools versions:"
  echo -n "  base: "; apptainer exec "$SIF_BASE" samtools --version | head -n1 || true
  # Similar for new
  ```  
  **What it does**: Builds if needed; execs version with `head`/`|| true` for safety.  
  **Why**: Conditional skips rebuilds; `-n` for inline echo; handles potential failures.

- **Re-run and Comparisons (Steps 4-6)**:  
  ```bash
  echo "[3/6] NEW sort/index on the real BAM…"
  cp -f "$BAM_BASE" "${RES_DIR}/align2.bam"
  apptainer exec ... sh -lc 'samtools sort -o align2.sorted.bam align2.bam && samtools index align2.sorted.bam'
  test -s ... && echo "  OK: NEW outputs created."

  echo "[4/6] idxstats compare…"
  apptainer exec ... 'samtools idxstats ...' > "$RES_DIR/idxstats_base.txt"
  # Similar for new
  diff -u ... >/dev/null && echo "  OK: idxstats identical."

  echo "[5/6] Alignment content md5 (headers stripped)…"
  H1=$(apptainer exec ... 'samtools view ... | md5sum | cut -d" " -f1')
  # Similar for H2
  if [[ "$H1" = "$H2" ]]; then ... else exit 1; fi
  ```  
  **What it does**: Copies input; chains sort/index; diffs idxstats quietly; subshells capture MD5 (cut parses).  
  **Why**: `&&` chains commands; `>/dev/null` for clean output; conditional fail enforces reproducibility.

- **Provenance**:  
  ```bash
  echo "[6/6] Provenance (NEW image)…"
  apptainer inspect "$SIF_NEW" | tee "$RES_DIR/samtools_2.inspect.txt" >/dev/null
  sha256sum "$SIF_NEW" | tee "$RES_DIR/samtools_2.sif.sha256" >/dev/null
  echo "[DONE] Demo 4 passed on real data."
  ```  
  **What it does**: Tees inspect/sha256 for new image.  
  **Why**: Consistent with prior; final echo signals success.

### Why This Matters
Reproducibility is science's cornerstone. Custom defs allow tweaks (e.g., env vars) while preserving core. Comparisons detect subtle bugs (e.g., sorting order).

### How to Run
```bash
RAW_DIR=./raw RES_DIR=results4 RES_DIR3=results3 sh demo4_build_compare.sh
```

### Expected Output
```
[1/6] Building samtools_2.sif... INFO: Build complete
[2/6] Versions... base: samtools 1.19.2 / new: samtools 1.19.2
[3/6] NEW sort... OK
[4/6] idxstats... OK: identical
[5/6] MD5... OK: alignments identical (e5c533c1...)
[6/6] Provenance... [DONE] Demo 4 passed
```

### Inspect Results (`results4/`)
- `align2.sorted.bam`: Re-sorted BAM (should match Demo 3's).
- `idxstats_*.txt`: Diff-able stats.
- `samtools_2.*`: Custom image metadata.

**Hands-On Tip**: Edit def's `%labels` (e.g., version="1.20"). Rebuild—MD5 mismatches? Add `-m 1G` to sort and debug. Why? Reveals env's role in determinism.

## Overall Rationale & Hands-On Experience

These demos progressively teach:
- **Isolation/Security** (Demo 1): Containers as safe sandboxes.
- **Tool Execution** (Demo 2): Bind mounts for I/O, fallbacks for robustness.
- **Pipelines** (Demo 3): Chaining, versioning for scalability.
- **Customization/Reproducibility** (Demo 4): Def files, checksums for audits.

By running/modifying, you'll gain confidence in Apptainer for real workflows (e.g., extend to GATK). Track changes with Git; share images via SFTP. The philosophy ties to education: each demo scaffolds the next, turning passive reading into active experimentation.

## Next Steps & Exercises
1. **Chain Demos**: Filter low-Q reads from FastQC ZIP, re-align, compare rates.
2. **HPC Submit**: Wrap in SLURM script (e.g., `#SBATCH -c 4` for threads).
3. **Version Hunt**: Change candidates—how does samtools 1.17 affect stats?

Questions? Run `apptainer inspect *.sif` or ping the instructor. Happy containerizing!
