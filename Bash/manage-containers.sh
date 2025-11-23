#!/usr/bin/env bash
set -euo pipefail

# Educational setup script for Apptainer bioinformatics demos
# Downloads data, creates demo scripts, builds/pulls images, runs demos into separate results dirs,
# and performs comparison in demo4.

echo "=== Starting educational demo setup ==="

# 1. Download data and reference
echo "[1/5] Downloading data and reference..."
mkdir -p raw
wget -nc -P raw/ ftp://ftp.sra.ebi.ac.uk/vol1/fastq/ERR769/ERR769583/ERR769583.fastq.gz
curl -L -o raw/hg38.fa.gz https://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/hg38.fa.gz
gunzip -c raw/hg38.fa.gz > raw/ref.fasta
echo "  OK: Data and ref ready in raw/."

# Create ref.sh for students to re-run if needed
cat > ref.sh << 'EOF'
curl -L -o raw/hg38.fa.gz https://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/hg38.fa.gz
gunzip -c raw/hg38.fa.gz > raw/ref.fasta
EOF
chmod +x ref.sh

# Create results directories
mkdir -p results{1..4}

# 2. Prepare demo scripts (with adjustments for separate results dirs)
echo "[2/5] Preparing demo scripts..."

# demo1.sh: Ubuntu verification (adjusted for RES_DIR propagation)
cat > demo1.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail

cat > verify_ubuntu_sif.sh <<'INNER_EOF'
set -euo pipefail

RES_DIR="${RES_DIR:-.}"

SIF=${1:-ubuntu-22.04.sif}

echo "[1/6] Identity check (host vs container UID)…"
host_uid=$(id -u)
cont_uid=$(apptainer exec "$SIF" sh -lc 'id -u')
test "$host_uid" = "$cont_uid"
echo "  OK: UID preserved ($cont_uid)."

echo "[2/6] OS release check (Ubuntu 22.04)…"
apptainer exec "$SIF" sh -lc 'grep -q "Ubuntu 22.04" /etc/os-release'
echo "  OK: Ubuntu 22.04 detected."

echo "[3/6] Root filesystem immutability…"
if apptainer exec "$SIF" sh -lc 'touch /should_fail 2>/dev/null'; then
  echo "  FAIL: root FS unexpectedly writable"; exit 1
else
  echo "  OK: root FS read-only."
fi

echo "[4/6] Bind-mount writable workspace…"
workdir=$(mktemp -d)
trap 'rm -rf "$workdir"' EXIT
apptainer exec -B "$workdir":/work -W /work "$SIF" sh -lc 'echo hello > /work/hello.txt'
test -f "$workdir/hello.txt"
echo "  OK: bind + write succeeded."

echo "[5/6] Clean environment determinism…"
apptainer exec --cleanenv "$SIF" sh -lc 'true'
echo "  OK: --cleanenv works."

echo "[6/6] Record provenance (inspect + checksum)…"
apptainer inspect "$SIF" | tee "$RES_DIR/ubuntu-22.04.inspect.txt" >/dev/null
sha256sum "$SIF" | tee "$RES_DIR/ubuntu-22.04.sif.sha256" >/dev/null
echo "  OK: inspect + sha256 saved."

echo "[DONE] All checks passed."
INNER_EOF

chmod +x verify_ubuntu_sif.sh
RES_DIR=results1 ./verify_ubuntu_sif.sh ubuntu-22.04.sif
EOF
chmod +x demo1.sh

# demo2_fastqc.sh: As provided (uses RES_DIR env)
cat > demo2_fastqc.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail

RAW_DIR="${RAW_DIR:-$(pwd)/raw}"
RES_DIR="${RES_DIR:-$(pwd)/results}"
mkdir -p "$RAW_DIR" "$RES_DIR"

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

INPUT="${RAW_DIR}/ERR769583.fastq.gz"
[[ -s "$INPUT" ]] || { echo "Missing input: $INPUT"; exit 1; }

echo "[2/5] Run FastQC…"
apptainer exec \
  --env LC_ALL=C.UTF-8 --env LANG=C.UTF-8 \
  -B "$RAW_DIR":/raw -B "$RES_DIR":/results --pwd /results "$SIF" \
  sh -lc 'fastqc -o /results /raw/ERR769583.fastq.gz'

echo "[3/5] Verify outputs…"
HTML="$RES_DIR/ERR769583_fastqc.html"
ZIP="$RES_DIR/ERR769583_fastqc.zip"
test -s "$HTML" && test -s "$ZIP" && echo "  OK: reports present"

echo "[4/5] Provenance…"
apptainer inspect "$SIF" | tee "$RES_DIR/fastqc.inspect.txt" >/dev/null
sha256sum "$SIF" | tee "$RES_DIR/fastqc.sif.sha256" >/dev/null

echo "[5/5] Done."
EOF
chmod +x demo2_fastqc.sh

# demo3_samtools.sh: Updated with better minimap2 candidates
cat > demo3_samtools.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail

RAW_DIR="${RAW_DIR:-$(pwd)/raw}"
RES_DIR="${RES_DIR:-$(pwd)/results}"
mkdir -p "$RAW_DIR" "$RES_DIR"

FASTQ="${RAW_DIR}/ERR769583.fastq.gz"
REF="${RAW_DIR}/ref.fasta"

[[ -s "$FASTQ" ]] || { echo "Missing FASTQ: $FASTQ"; exit 1; }
[[ -s "$REF"  ]] || { echo "Missing reference FASTA: $REF"; exit 1; }

# --- Build containers (version-pinned, with fallbacks) -----------------------
SAMTOOLS_SIF="samtools.sif"
MINIMAP2_SIF="minimap2.sif"

SAMTOOLS_CAND=(
  "docker://quay.io/biocontainers/samtools:1.19.2--h50ea8bc_1"
  "docker://biocontainers/samtools:v1.17-4-deb_cv1"
)
MINIMAP2_CAND=(
  "docker://quay.io/biocontainers/minimap2:2.28--h577a1d6_4"
  "docker://quay.io/biocontainers/minimap2:2.26--he4a0461_2"
)

echo "[1/8] Build SIF (samtools)…"
built=0
for ref in "${SAMTOOLS_CAND[@]}"; do
  echo "  Trying: $ref"
  if apptainer build "$SAMTOOLS_SIF" "$ref" >/dev/null 2>&1; then
    echo "$ref" > "$RES_DIR/samtools.source.txt"; built=1; break
  fi
done
[[ $built -eq 1 ]]

echo "[2/8] Build SIF (minimap2)…"
built=0
for ref in "${MINIMAP2_CAND[@]}"; do
  echo "  Trying: $ref"
  if apptainer build "$MINIMAP2_SIF" "$ref" >/dev/null 2>&1; then
    echo "$ref" > "$RES_DIR/minimap2.source.txt"; built=1; break
  fi
done
[[ $built -eq 1 ]]

# --- Index reference (minimap2) ----------------------------------------------
echo "[3/8] Index reference with minimap2…"
apptainer exec -B "$RAW_DIR":/raw -B "$RES_DIR":/results --pwd /results "$MINIMAP2_SIF" \
  sh -lc 'test -s /raw/ref.mmi || minimap2 -d /raw/ref.mmi /raw/ref.fasta'
test -s "$RAW_DIR/ref.mmi"

# --- Align FASTQ → BAM (pipe minimap2 -> samtools view) ----------------------
echo "[4/8] Align FASTQ to reference → BAM (unsorted)…"
apptainer exec -B "$RAW_DIR":/raw -B "$RES_DIR":/results --pwd /results "$MINIMAP2_SIF" \
  sh -lc 'minimap2 -t 2 -ax map-ont /raw/ref.mmi /raw/ERR769583.fastq.gz' | \
apptainer exec -B "$RAW_DIR":/raw -B "$RES_DIR":/results --pwd /results "$SAMTOOLS_SIF" \
  sh -lc 'samtools view -bS - > align.bam'
test -s "$RES_DIR/align.bam"

# --- Sort & Index ------------------------------------------------------------
echo "[5/8] Sort BAM…"
apptainer exec -B "$RAW_DIR":/raw -B "$RES_DIR":/results --pwd /results "$SAMTOOLS_SIF" \
  sh -lc 'samtools sort -o align.sorted.bam align.bam'
test -s "$RES_DIR/align.sorted.bam"

echo "[6/8] Index BAM…"
apptainer exec -B "$RAW_DIR":/raw -B "$RES_DIR":/results --pwd /results "$SAMTOOLS_SIF" \
  sh -lc 'samtools index align.sorted.bam'
test -s "$RES_DIR/align.sorted.bam.bai"

# --- Stats outputs for quick sanity -----------------------------------------
echo "[7/8] Mapping stats…"
apptainer exec -B "$RAW_DIR":/raw -B "$RES_DIR":/results --pwd /results "$SAMTOOLS_SIF" \
  sh -lc 'samtools flagstat align.sorted.bam | head -n 10'

# --- Provenance --------------------------------------------------------------
echo "[8/8] Provenance…"
apptainer inspect "$SAMTOOLS_SIF" | tee "$RES_DIR/samtools.inspect.txt" >/dev/null
sha256sum "$SAMTOOLS_SIF" | tee "$RES_DIR/samtools.sif.sha256" >/dev/null
apptainer inspect "$MINIMAP2_SIF" | tee "$RES_DIR/minimap2.inspect.txt" >/dev/null
sha256sum "$MINIMAP2_SIF" | tee "$RES_DIR/minimap2.sif.sha256" >/dev/null
echo "Done."
EOF
chmod +x demo3_samtools.sh

# demo4_build_compare.sh: As provided, but adjusted for RES_DIR3 (demo3 results)
cat > demo4_build_compare.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail

RAW_DIR="${RAW_DIR:-$(pwd)/raw}"
RES_DIR="${RES_DIR:-$(pwd)/results}"
RES_DIR3="${RES_DIR3:-$(pwd)/results3}"
mkdir -p "$RAW_DIR" "$RES_DIR"

SIF_BASE="samtools.sif"               # from demo3
SIF_NEW="samtools_2.sif"              # new image to compare
DEF_LOCAL="samtools_from_local.def"   # auto-created if missing
BAM_BASE="${RES_DIR3}/align.sorted.bam"   # produced by demo3
BAI_BASE="${RES_DIR3}/align.sorted.bam.bai"

[[ -s "$SIF_BASE" ]] || { echo "Missing $SIF_BASE (run demo3 first)."; exit 1; }
[[ -s "$BAM_BASE" ]] || { echo "Missing $BAM_BASE (run demo3 first)."; exit 1; }
[[ -s "$BAI_BASE" ]] || { echo "Missing $BAI_BASE (run demo3 first)."; exit 1; }

# Create localimage def if absent
if [[ ! -f "$DEF_LOCAL" ]]; then
  cat > "$DEF_LOCAL" <<'DEF'
Bootstrap: localimage
From: samtools.sif

%labels
    app.name "samtools"
    app.version "1.19.2"
    build.source "localimage:samtools.sif"
    build.date "%DATE%"

%environment
    export LC_ALL=C
    export LANG=C

%runscript
    exec samtools "$@"
DEF
fi

# Build new image if needed
if [[ -s "$SIF_NEW" ]]; then
  echo "[1/6] Using existing $SIF_NEW."
else
  echo "[1/6] Building $SIF_NEW from $DEF_LOCAL (localimage)…"
  apptainer build "$SIF_NEW" "$DEF_LOCAL"
fi

# Versions
echo "[2/6] samtools versions:"
echo -n "  base: "; apptainer exec "$SIF_BASE" samtools --version | head -n1 || true
echo -n "  new : "; apptainer exec "$SIF_NEW"  samtools --version | head -n1 || true

# Re-run sort/index with NEW SIF on the full BAM to get a new artifact
echo "[3/6] NEW sort/index on the real BAM…"
cp -f "$BAM_BASE" "${RES_DIR}/align2.bam"
apptainer exec -B "$RAW_DIR":/raw -B "$RES_DIR":/results --pwd /results "$SIF_NEW" \
  sh -lc 'samtools sort -o align2.sorted.bam align2.bam && samtools index align2.sorted.bam'
test -s "$RES_DIR/align2.sorted.bam" && test -s "$RES_DIR/align2.sorted.bam.bai"
echo "  OK: NEW outputs created."

# idxstats compare (should match byte-for-byte)
echo "[4/6] idxstats compare…"
apptainer exec -B "$RES_DIR3":/results3 --pwd /results3 "$SIF_BASE" \
  sh -lc 'samtools idxstats align.sorted.bam' > "$RES_DIR/idxstats_base.txt"
apptainer exec -B "$RES_DIR":/results --pwd /results "$SIF_NEW" \
  sh -lc 'samtools idxstats align2.sorted.bam' > "$RES_DIR/idxstats_new.txt"
diff -u "$RES_DIR/idxstats_base.txt" "$RES_DIR/idxstats_new.txt" >/dev/null && echo "  OK: idxstats identical."

# Alignment content md5 (strip headers to ignore @PG differences)
echo "[5/6] Alignment content md5 (headers stripped)…"
H1=$(apptainer exec -B "$RES_DIR3":/results3 --pwd /results3 "$SIF_BASE" \
      sh -lc 'samtools view align.sorted.bam | md5sum | cut -d" " -f1')
H2=$(apptainer exec -B "$RES_DIR":/results --pwd /results "$SIF_NEW" \
      sh -lc 'samtools view align2.sorted.bam | md5sum | cut -d" " -f1')
if [[ "$H1" = "$H2" ]]; then
  echo "  OK: alignments identical ($H1)."
else
  echo "  MISMATCH: base=$H1 new=$H2" >&2
  exit 1
fi

# Provenance
echo "[6/6] Provenance (NEW image)…"
apptainer inspect "$SIF_NEW" | tee "$RES_DIR/samtools_2.inspect.txt" >/dev/null
sha256sum "$SIF_NEW" | tee "$RES_DIR/samtools_2.sif.sha256" >/dev/null
echo "[DONE] Demo 4 passed on real data."
EOF
chmod +x demo4_build_compare.sh

# 3. Prepare images and run demos (populating results_{1..4})
echo "[3/5] Preparing images and running demos..."

# Demo 1: Pull Ubuntu image and run
echo "  Demo 1: Pulling ubuntu-22.04.sif..."
apptainer pull ubuntu-22.04.sif docker://ubuntu:22.04
echo "  Demo 1: Running..."
sh demo1.sh
echo "  OK: Demo 1 complete (results in results1/)."

# Demo 2: Run (builds fastqc.sif)
echo "  Demo 2: Running (builds fastqc.sif)..."
RAW_DIR=./raw RES_DIR=results2 sh demo2_fastqc.sh
echo "  OK: Demo 2 complete (results in results2/)."

# Demo 3: Run (builds samtools.sif and minimap2.sif)
echo "  Demo 3: Running (builds samtools.sif, minimap2.sif)..."
RAW_DIR=./raw RES_DIR=results3 sh demo3_samtools.sh
echo "  OK: Demo 3 complete (results in results3/)."

# Demo 4: Run (builds samtools_2.sif, compares with demo3)
echo "  Demo 4: Running (builds samtools_2.sif, compares with demo3)..."
RAW_DIR=./raw RES_DIR=results4 RES_DIR3=results3 sh demo4_build_compare.sh
echo "  OK: Demo 4 complete (comparison passed, results in results4/)."

# 4-5. Results populated and comparison done (via demo4)
echo "[4/5] Results directories populated: results1/, results2/, results3/, results4/."
echo "[5/5] Images prepared: ubuntu-22.04.sif, fastqc.sif, samtools.sif, minimap2.sif, samtools_2.sif."

echo "=== Setup complete! ==="
echo "Students can:"
echo "  - Re-run 'sh demoN.sh' (with env vars if needed) to repeat."
echo "  - Modify for exercises (e.g., change versions, add steps)."
echo "  - Use 'tree' to inspect structure."
