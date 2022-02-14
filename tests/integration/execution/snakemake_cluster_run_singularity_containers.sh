# Run the pipeline on the sciCORE computational cluster with singularity containers

cleanup () {
    rc=$?
    rm -rf .snakemake/
    rm -rf ../output/
    cd "$user_dir"
    echo "Exit status: $rc"
}
trap cleanup SIGINT

set -eo pipefail  # ensures that script exits at first command that exits with non-zero status
set -u  # ensures that script exits when unset variables are used
set -x  # facilitates debugging by printing out executed commands

user_dir=$PWD
repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)/../../.."
cd "$repo_dir"

snakemake \
    --snakefile="workflow/Snakefile" \
    --configfile="tests/integration/config.yml" \
    --cluster-config="tests/integration/SLURM-cluster-config.json" \
    --use-singularity \
    --cores=128 \
    --local-cores 1 \
    --printshellcmds \
    --verbose \
    --latency-wait 60 \
    --cluster \
    "sbatch \
    --cpus-per-task={cluster.threads} \
    --mem={cluster.mem} \
    --qos={cluster.queue} \
    --time={cluster.time} \
    --output={params.LOG_cluster_log}-%j-%N.log \
    -p scicore"
