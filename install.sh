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
echo "[0/7]: Removing .git internal directory..."
rm -rf .git

# create and activate main bindz conda env
echo "[1/7]: Creating main conda env for bindz..."
conda env create --file envs/main.yml
SHELLNAME=$(echo $0 | sed 's|-||g')
conda init $SHELLNAME
conda activate bindz
conda list

echo "[2/7]: Building all workflow-specific conda envs..."

echo "[3/7]: Parsing ATtRACT db..."

echo "[4/7]: Generating sequence logos..."

echo "[5/7]: Adjusting config template..."
# sed?

echo "[6/7]: Adjusting \$PATH..."
# hook up /bin/bindz to PATH
# separate for mac, linux

echo "[7/7]: Testing installation..."
bindz

echo "SUCCESS!"

# print error msg on error!
