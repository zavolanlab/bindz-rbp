###############################################################################
#
#   Download ATtRACT database and extract PWMs
#   for a given organism (supported: hsa/mmu).
#
#   AUTHOR: Maciej_Bak
#   AFFILIATION: University_of_Basel
#   AFFILIATION: Swiss_Institute_of_Bioinformatics
#   CONTACT: maciej.bak@unibas.ch
#   CREATED: 21-03-2020
#   LICENSE: Apache_2.0
#   USAGE:
#   bash download-ATtRACT-motifs.sh -s {hsa|mmu} -o {}
#
###############################################################################

###############################################################################
# parse command line arguments
###############################################################################

POSITIONAL=()
while [[ $# -gt 0 ]]
do
    key="$1"
    case $key in
        -s|--species)
            SPECIES="$2"
            shift # past argument
            shift # past value
            ;;
        -o|--output-directory)
            OUTDIR="$2"
            shift # past argument
            shift # past value
            ;;
        *) # unknown option
            POSITIONAL+=("$1") # save it in an array for later
            shift # past argument
            ;;
    esac
done
set -- "${POSITIONAL[@]}" # restore positional parameters

###############################################################################
# MAIN
###############################################################################

# check arguments
if [ -z "$SPECIES" ] || [ -z "$OUTDIR" ]; then
    echo "Invalid arguments. Please provide --species and --output-directory"
    exit 1
fi

# check species option value
if [ ! "${SPECIES}" == "hsa" ] && [ ! "${SPECIES}" == "mmu" ]; then
    echo $"Invalid species option. Currently supported are: 'hsa', 'mmu'"
    exit 1
fi

# exit if output directory exists
if [ -d "${OUTDIR}" ]; then
    echo "Output directory already exists!"
    exit 1
fi

# create directories
mkdir "${OUTDIR}"

# download and unzip ATtRACT database
curl https://attract.cnic.es/attract/static/ATtRACT.zip \
    --output "${OUTDIR}"/ATtRACT.zip
unzip "${OUTDIR}"/ATtRACT.zip -d "${OUTDIR}"
