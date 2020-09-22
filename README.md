<img align="right" width="50" height="50" src="images/logo.128px.png">

# BindingScanner

BindingScanner is a tool for predicting binding sites of RNA-binding proteins in a given input RNA sequence, implemented in a snakemake pipeline.

## Table of Contents

- [BindingScanner](#bindingscanner)
  - [Table of Contents](#table-of-contents)
  - [General information](#general-information)
  - [Installation instructions](#installation-instructions)
    - [Step 1: Download and install Miniconda3](#step-1-download-and-install-miniconda3)
    - [Step 2: Clone the repository](#step-2-clone-the-repository)
    - [Step 3: Build and activate virtual environment for BindingScanner](#step-3-build-and-activate-virtual-environment-for-bindingscanner)
  - [Optional: Download and parse PWMs from ATtRACT database](#optional-download-and-parse-pwms-from-attract-database)
  - [Workflow execution](#workflow-execution)
  - [Contributing](#contributing)
  - [Contact](#contact)

## General information

BindingScanner infers binding sites of distinct regulators by calculating their binding probabilities with [MotEvo].

The tool is implemented as a [Snakemake] computational workflow.

> ![rule_graph][rule-graph]

## Installation instructions

Snakemake is a workflow management system that helps to create and execute data processing pipelines. It requires [Python 3] and can be most easily installed via the [bioconda] channel from the [anaconda cloud] service.

### Step 1: Download and install Miniconda3

To install the latest version of [miniconda] please execute:  

[Linux]:

```bash
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
source .bashrc
```

[macOS]:

```bash
wget https://repo.continuum.io/miniconda/Miniconda3-latest-MacOSX-x86_64.sh
bash Miniconda3-latest-MacOSX-x86_64.sh
source .bashrc
```

### Step 2: Clone the repository

Cloning repositories requires [git] to be installed (available via `conda`): 

```bash
conda install git
```

Clone this git repository into a desired location (here: binding_scanner_git) with the following command:

```bash
git clone https://github.com/zavolanlab/binding-scanner.git binding_scanner_git
```

### Step 3: Build and activate virtual environment for BindingScanner

To help the users in the installation process we have prepared a recipe for a *conda* virtual environment that contains all the software needed to run BindingScanner. This environment can be created by the following script:

```bash
bash binding_scanner_git/scripts/create-conda-environment-main.sh
```

The built *conda* environment may then be activated with:

```bash
conda activate binding-scanner
```

## Optional: Download and parse PWMs from ATtRACT database

Inside this repository we have included a snapshot of a database of Position Weight Matrices for distinct RNA binding proteins ([ATtRACT]: 26-08-2020). We suggest to use the pre-formatted files which we have already prepared: `resources/ATtRACT_hsa` and `resources/ATtRACT_mmu` for *Homo sapiens* and *Mus musculus*, respectively.

However, if the user would like to download the and parse a new version of matrices from ATtRACT we describe the procedure below:

Please change directory to the pipeline's root directory:

```bash
cd binding_scanner_git
```

To utilise Position Weight Matrices from the ATtRACT database of known RBPs' binding motifs we provide two scripts:

1. Download and extract the database into a directory `ATtRACT` under `resources`:
   ```bash
   bash scripts/download-ATtRACT-motifs.sh -o resources/ATtRACT
   ```
2. Parse the database and reformat the PWMs into a TRANSFAC format (currently supported species are *Homo_sapiens* or *Mus_musculus*):
   
   *Homo sapiens*
   ```bash
    mkdir resources/ATtRACT/ATtRACT_hsa
    python scripts/format-ATtRACT-motifs.py \
    --pwms resources/ATtRACT/pwm.txt \
    --names resources/ATtRACT/ATtRACT_db.txt \
    --organism Homo_sapiens \
    --outdir resources/ATtRACT/ATtRACT_hsa
   ```

   *Mus musculus*
   ```bash
    mkdir resources/ATtRACT/ATtRACT_mmu
    python scripts/format-ATtRACT-motifs.py \
    --pwms resources/ATtRACT/pwm.txt \
    --names resources/ATtRACT/ATtRACT_db.txt \
    --organism Mus_musculus \
    --outdir resources/ATtRACT/ATtRACT_mmu
   ```

    To print information about the script's arguments please type:

    ```
    python scripts/format-ATtRACT-motifs.py --help
    ```

## Workflow execution

Please change directory to the pipeline's root directory:

```bash
cd binding_scanner_git
```

All the input, output and parameters for the pipeline execution should be specified in a snakemake configuration file in YAML format. Such a file can be created based on our prepared template located at `workflow/config/config-template.yml`. Assuming that the user created a `config.yml` and saved it in the repository's root directory (and that it is the current working directory) the workflow can be executed on the local machine with:

```bash
snakemake \
    --snakefile="workflow/Snakefile" \
    --configfile="config.yml" \
    --use-conda \
    --cores=1 \
    --printshellcmds \
    --verbose
```

We also provide a integration test for the pipeline on a small input dataset to examine if the installation was successful:

```bash
bash tests/integration/execution/snakemake_local_run_conda_environments.sh
```

## Contributing

This project lives off your contributions, be it in the form of bug reports,
feature requests, discussions, or fixes and other code changes. Please refer
to the [contributing guidelines](CONTRIBUTING.md) if you are interested to
contribute. Please mind the [code of conduct](CODE_OF_CONDUCT.md) for all
interactions with the community.

## Contact

For questions or suggestions regarding the code, please use the
[issue tracker][res-issue-tracker]. For any other inquiries, please contact us
by email: <zavolab-biozentrum@unibas.ch>

(c) 2020 [Zavolan lab, Biozentrum, University of Basel][res-zavolab]

[MotEvo]: https://academic.oup.com/bioinformatics/article/28/4/487/212418
[Snakemake]: https://snakemake.readthedocs.io/en/stable/
[rule-graph]: images/rulegraph.svg
[Python 3]: https://www.python.org/download/releases/3.0/
[bioconda]: https://bioconda.github.io/
[anaconda cloud]: https://anaconda.org/
[miniconda]: https://docs.conda.io/en/latest/miniconda.html
[git]: https://git-scm.com/
[ATtRACT]: https://attract.cnic.es/index
[res-issue-tracker]: <https://github.com/zavolanlab/binding-scanner/issues>
[res-zavolab]: <https://zavolan.biozentrum.unibas.ch/>
