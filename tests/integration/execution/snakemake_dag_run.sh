# Create the DAG (Directed Acyclic Graph) for the workflow

cleanup () {
    rc=$?
    rm -rf ../../../images/dag.pdf
    cd "$user_dir"
    echo "Exit status: $rc"
}
trap cleanup SIGINT

set -eo pipefail  # ensures that script exits at first command that exits with non-zero status
set -u  # ensures that script exits when unset variables are used
set -x  # facilitates debugging by printing out executed commands

user_dir=$PWD
pipeline_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
cd "$pipeline_dir"

snakemake \
    --snakefile="../../../workflow/Snakefile" \
    --configfile="../config.yml" \
    --printshellcmds \
    --dryrun \
    --verbose \
    --dag \
    | dot -Tsvg \
    > ../../../images/dag.svg
