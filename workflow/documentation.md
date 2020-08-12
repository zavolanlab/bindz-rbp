# BINDING-SCANNER: workflow documentation

This document describes the individual steps of the workflow. For instructions
on installation and usage please see [here](../README.md).

## Table of Contents
- [**Description of workflow steps**](#description-of-workflow-steps)
  - [**Rule graph**](#rule-graph)
  - [**Preparatory**](#preparatory)
    - [**Config file**](#config-file)
  - [**Snakemake Rules**](#snakemake-rules)
    - [**all**](#all)
    - [**create_results_directory**](#create_results_directory)
    - [**plot_sequence_logos**](#plot_sequence_logos)
    - [**prepare_MotEvo_parameters**](#prepare_MotEvo_parameters)
    - [**prepare_sequence_for_MotEvo**](#prepare_sequence_for_MotEvo)
    - [**run_MotEvo_analysis**](#run_MotEvo_analysis)
    - [**combine_MotEvo_results**](#combine_MotEvo_results)
    - [**plot_heatmap_of_MotEvo_results**](#plot_heatmap_of_MotEvo_results)

## Description of workflow steps

### Rule graph

![rule_graph][rule-graph]

Visual representation of workflow. Automatically prepared with
[Snakemake][docs-snakemake].

### Preparatory

#### Config file

##### Requirements

- a config file as in [`config.yml`](config/config-template.yml)
- a pwm directory containing files with binding probabilities matrices of various motifs.

Parameter name | Description | Data type(s)
--- | --- | ---
pipeline_path | Absolute path to the pipeline directory | `str`
sequence | Input Sequence | `str`
pwm_directory | Path to the directory with TRANSFAC-formatted PWM files | `str`
outdir | Path to the output directory | `str`
MotEvo_bg_binding_prior | MotEvo parameter: prior probability for the background binding | `float`
MotEvo_min_binding_posterior | MotEvo parameter: prior minimum binding posterior probability | `float`
MotEvo_Markov_chain_order | MotEvo parameter: order of the Markov chain | `float`

### Snakemake Rules

#### `all`

Target rule with final output of the pipeline

- **Input**
  - A heatmap depicting all the motifs with their sequence logos and names as y-axis tick-labels; input sequence as x-axis; and each cell representing the probability of corresponding motif and the part of the sequence.

#### `create_results_directory`

  Create directories for the results

- **Parameters**
  - Path to output directory
  - Path to local log directory
  - Path to cluster log directory  

- **Output**
  - An output directory which will be used in all the successive rules

#### `plot_sequence_logos`

   Plot sequence logo for the motifs. This rule will run as many number as times as the number of motifs or number of files in the pwm directory.

- **Input**
  - PWM file containg binding probability matrices
  - Script that processes matrices to sequence logos png [`sequence_logos.py`](../workflow/scripts/sequence_logos.py)
  - Output directory generated in the rule [**create_results_directory**](#create_results_directory)

- **Parameters**
  - Output directory for the logos
  - File path of logs for each Pwm

- **Output**
  - A png file for each motif containing the sequence logo which will be used in the rule [**plot_heatmap_of_MotEvo_results**](#plot_heatmap_of_MotEvo_results)

#### `prepare_MotEvo_parameters`

   Prepare text file with parameters for MotEvo runs

- **Input**
  - Output directory generated in the rule [**create_results_directory**](#create_results_directory)

- **Parameters**
  - Path to output directory for the logos
  - File path for the logs for each Pwm file 

- **Output**
    - A text file containing MotEvo paramaters which will be used in the rule [**run_MotEvo_analysis**](#run_MotEvo_analysis)

#### `prepare_sequence_for_MotEvo`

   Create a FASTA-formatted file with the input sequence

- **Input**
  - Output directory generated in the rule [**create_results_directory**](#create_results_directory)

- **Parameters**
  - Input sequence
  - Header tag for the sequence 
  - Path for the log of this rule

- **Output**
    - A fasta file which will be used in the rule [**run_MotEvo_analysis**](#run_MotEvo_analysis)

#### `run_MotEvo_analysis`

   Run MotEvo for a given FASTA sequence and a given PWM

- **Input**
  - MotEvo parameters file generated in rule [**prepare_MotEvo_parameters**](#prepare_MotEvo_parameters)
  - Path of the pwm files containing the binding probabilities matrices
  - Fasta file generated in the rule [**prepare_sequence_for_MotEvo**](#prepare_sequence_for_MotEvo)

- **Parameters**
  - Absolute path of MotEvo parameters file generated in rule [**prepare_MotEvo_parameters**](#prepare_MotEvo_parameters)
  - Absolute path of Fasta file generated in the rule [**prepare_sequence_for_MotEvo**](#prepare_sequence_for_MotEvo)
  - Path for the log of this rule

- **Output**
    - A directory with files containing posterior sites information which will be used in the rule [**combine_MotEvo_results**](#combine_MotEvo_results)

#### `combine_MotEvo_results`

   Combine all motevo results into one tsv file

- **Input**
  - A directory with files containing posterior sites information which is generated in [**run_MotEvo_analysis**](#run_MotEvo_analysis)
  - Script that will do the job of combinining results in one tsv file [`combine-motevo-results.py`](../workflow/scripts/combine-motevo-results.py)

- **Parameters**
  - Name of the file which would contain posterior sites information
  - Path for the log of this rule

- **Output**
    - A tsv file which gathers information of every analysed PWM directory.

#### `plot_heatmap_of_MotEvo_results`

   Plot heatmap from the combined_MotEvo_results.tsv file

- **Input**
  - A TSV file containing information of every analysed PWM directory generated from rule [**combine_MotEvo_results**](#combine_MotEvo_results)
  - Script that will plot the heatmap with sequence logos as y axis ticks [`sequence_logos.py`](../workflow/scripts/sequence_logos.py)
  - Sequence logo generated for each motif from the rule [**plot_sequence_logos**](#plot_sequence_logos)

- **Parameters**
  - Input sequence
  - Directory of all sequence logos
  - Path for the log of this rule

- **Output**
    - A heatmap depicting all the motifs with their sequence logos and names as y-axis tick-labels; input sequence as x-axis; and each cell representing the probability of corresponding motif and the part of the sequence.

[rule-graph]: ../images/rulegraph.svg
[docs-snakemake]: <https://snakemake.readthedocs.io/en/stable/>