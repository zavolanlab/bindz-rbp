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

CWD="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
echo $CWD

# remove git repository
rm -rf .git

# create and activate main bindz conda env
echo "[1/3]: Creating main conda env for bindz..."
conda env create --file envs/main.yml
conda activate bindz
conda list

echo "[2/3]: Building all workflow-specific conda envs..."

echo "[3/3]: Parsing ATtRACT db..."

echo "[4/3]: Generating sequence logos..."

# populate config with paths to repo
# sed?

# hook up /bin/bindz to PATH
# separate for mac, linux

# test exection?
# bindz

# print error msg on error!
