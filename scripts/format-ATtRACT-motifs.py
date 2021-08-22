"""
Convert motifs into MotEvo compatible format.

Author & Copyright: Maria Katsantoni
Modified by: Maciej Bak
Contact: maciej.bak@unibas.ch
"""

# ________________________________________________________________________________________
# ----------------------------------------------------------------------------------------
# import needed (external) modules
# ----------------------------------------------------------------------------------------
import sys
import os
from argparse import ArgumentParser, RawTextHelpFormatter
import pandas as pd


# ________________________________________________________________________________________
# ----------------------------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------------------------


def main():
    """main body of the script"""

    parser = ArgumentParser(description=__doc__, formatter_class=RawTextHelpFormatter)

    parser.add_argument(
        "--pwms",
        dest="pwms",
        help="ATtRACT db file: pwm's of motifs",
        required=True,
        metavar="FILE",
    )

    parser.add_argument(
        "--names",
        dest="names",
        help="ATtRACT db file: list of records",
        required=True,
        metavar="FILE",
    )

    parser.add_argument(
        "--organism",
        dest="organism",
        help="Organism field in the ATtRACT record list",
        required=False,
        default="0",
    )

    parser.add_argument(
        "--experiments",
        dest="experiments",
        help="Comma-separated list of experiments to filter from the database",
        required=False,
        default="0",
    )

    parser.add_argument(
        "--outdir",
        dest="outdir",
        help="Output directory for the motifs",
        required=True,
        default="0",
    )

    # ____________________________________________________________________________________
    # ------------------------------------------------------------------------------------
    # get the arguments
    # ------------------------------------------------------------------------------------
    try:
        options = parser.parse_args()
    except Exception:
        parser.print_help()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    get_motifs(options.names, options.pwms, options.outdir, options.organism, options.experiments)


def get_motifs(names, pwm, outdir, organism, experiments):
    """main logic of the script - reformat motifs"""
    attract_info = pd.read_csv(
        names, header=0, sep="\t", index_col=None, comment="#", engine="python"
    )

    if organism != "0":
        attract_info = attract_info[attract_info["Organism"] == organism]

    if experiments != "0":
        attract_info = attract_info[attract_info["Experiment_description"].isin(experiments.split(","))]

    motifs = open(pwm, "r")
    each_motif = pd.DataFrame()
    info = ""
    counter_motif = 0
    for line in motifs.readlines():
        if line.startswith(">"):
            if counter_motif >= 1:
                each_motif = each_motif.round(3)
                each_motif.index = each_motif.index.map("{:02}".format)
                outfile = os.path.join(outdir, str(info))
                template = """//\nNA """ + str(info) + """\n{}//"""
                with open(outfile, "w") as fp:
                    fp.write(
                        template.format(
                            each_motif.to_csv(sep="\t", index=True, header=True)
                        )
                    )
            count = 1
            each_motif = pd.DataFrame()
            name = line.strip("\n").strip(">").split("\t")
            each_motif = pd.DataFrame()
            if name[0] in attract_info["Matrix_id"].values:
                info = attract_info[["Gene_name", "Matrix_id"]][
                    attract_info["Matrix_id"] == name[0]
                ].values[0]
            else:
                counter_motif = 0
                continue
            info = "_".join(info)
            info = info.replace(" ", "")
            info = info.replace("(", "")
            info = info.replace(")", "")
            info = info.replace("]", "")
            info = info.replace("[", "")
            info = info.replace("-", "_")
            counter_motif += 1
        else:
            line = line.strip("\n")
            values = line.split("\t")
            values = [float(v) for v in values]
            # test that the values add up to 1.0
            # if not (big deviation): print a warning message to stderr
            # normalize so that they add up to exatly 1.0
            # (there might be numerical issues so round(x,10) for the test)
            # This normalization takes care of the inaccuracies in the databse.
            # Remember that we later round % values to 3 decimal places too.
            sumvalues = sum(values)
            if sumvalues > 1.01 or sumvalues < 0.99:
                sys.stderr.write(
                    "### [INFO] Record: "
                    + info
                    + ". Columns add up to: "
                    + str(sumvalues)
                    + ". Normalizing anyway."
                    + os.linesep
                )
            values = [v / sumvalues for v in values]
            assert round(sum(values), 10) == 1.0
            # save in % form in the df
            each_motif.loc[count, "A"] = values[0] * 100
            each_motif.loc[count, "C"] = values[1] * 100
            each_motif.loc[count, "G"] = values[2] * 100
            each_motif.loc[count, "T"] = values[3] * 100
            count += 1
    each_motif.index = each_motif.index.map("{:02}".format)
    outfile = os.path.join(outdir, str(info))
    template = """//\nNA """ + str(info) + """\n{}//"""
    with open(outfile, "w") as fp:
        fp.write(template.format(each_motif.to_csv(sep="\t", index=True, header=True)))
    motifs.close()


# ________________________________________________________________________________________
# ----------------------------------------------------------------------------------------
# Call the Main function and catch Keyboard interrups
# ----------------------------------------------------------------------------------------
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.stderr.write("User interrupt!\n")
        sys.exit(0)
