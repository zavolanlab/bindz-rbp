###############################################################################
#
#   bindz installation script
#
#   AUTHOR: Maciej_Bak
#   AFFILIATION: University_of_Basel
#   AFFILIATION: Swiss_Institute_of_Bioinformatics
#   CONTACT: maciej.bak@unibas.ch
#   CREATED: 21-08-2021
#   LICENSE: Apache_2.0
#
###############################################################################

cleanup () {
    rc=$?
    conda env remove --name bindz
    echo "Exit status: $rc"
}
trap cleanup SIGINT

set -eo pipefail  # ensures that script exits at first command that exits with non-zero status
set -u  # ensures that script exits when unset variables are used

REPODIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

# remove git repository
echo "[0/7]: Removing .git internal directory..."
rm -rf .git

# create and activate main bindz conda env
echo "[1/7]: Creating main conda env for bindz..."
conda env create --file envs/main.yml --quiet
SHELLNAME=$(echo $SHELL | rev | cut -d '/' -f1 | rev)
echo $SHELLNAME
export PS1=
if [ $SHELLNAME=="zsh" ]
then
  eval "$(conda shell.zsh hook)"
fi
if [ $SHELLNAME=="bash" ]
then
  eval "$(conda shell.bash hook)"
fi
conda activate bindz

echo "[2/7]: Building all workflow-specific conda envs..."
snakemake --configfile tests/integration/config.yml --use-conda --conda-create-envs-only
conda env list

echo "[3/7]: Parsing ATtRACT db..."

echo "[4/7]: Generating sequence logos..."

echo "[5/7]: Adjusting config template..."
# sed?

echo "[6/7]: Adjusting \$PATH..."
# hook up /bin/bindz to PATH
# separate for mac, linux

echo "[7/7]: Testing installation..."
bindz

conda deactivate
echo "SUCCESS!"
