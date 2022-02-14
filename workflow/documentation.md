# _bindz-rbp_: workflow documentation

This document describes the individual steps of the workflow. For instructions
on installation and usage please go [here](../README.md).

## Table of Contents
- [**Description of workflow steps**](#description-of-workflow-steps)
  - [**Rule graph**](#rule-graph)
  - [**Config file**](#config-file)
  - [**Snakemake Rules**](#snakemake-rules)
    - [**all**](#all)
    - [**plot_sequence_logos**](#plot_sequence_logos)
    - [**prepare_MotEvo_parameters**](#prepare_MotEvo_parameters)
    - [**prepare_sequence_for_MotEvo**](#prepare_sequence_for_MotEvo)
    - [**run_MotEvo_analysis**](#run_MotEvo_analysis)
    - [**combine_MotEvo_results**](#combine_MotEvo_results)
    - [**plot_heatmap_of_MotEvo_results**](#plot_heatmap_of_MotEvo_results)
    - [**prepare_output_bedfile**](#prepare_output_bedfile)

## Description of workflow steps

### Rule graph

![rule_graph][rule-graph]

Visual representation of workflow. Automatically prepared with
[Snakemake][docs-snakemake].

### Config file

This workflow requires a config file as in [`config.yml`](config/config-template.yml)

Parameter name | Description | Data type(s)
--- | --- | ---
pipeline_path | Absolute path to the pipeline directory | `str`
seq_name | Input Sequence ID | `str`
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
  - A heatmap depicting all the motifs with their sequence logos and names as y-axis tick-labels; input sequence as x-axis; and each cell representing per-position binding probability.
  - BED-formatted list of inferred binding sites.

#### `plot_sequence_logos`

   Plot sequence logos for the motifs. This rule will run as many times as the number of motifs in the PWM directory.

- **Input**
  - PWM file containg binding probability matrix
  - Script that generates sequence logos.[`sequence_logos.py`](../workflow/scripts/sequence_logos.py)

- **Parameters**
  - Output directory for the logos
  - File path for cluster logs

- **Output**
  - A png file containing the sequence logo which will be used in the rule [**plot_heatmap_of_MotEvo_results**](#plot_heatmap_of_MotEvo_results)

#### `prepare_MotEvo_parameters`

   Prepare text file with parameters for MotEvo runs

- **Parameters**
  - MotEvo parameters: bg binding probability, min binding posterior, Markov chain order
  - File path for cluster logs

- **Output**
    - A text file containing MotEvo paramaters which will be used in the rule [**run_MotEvo_analysis**](#run_MotEvo_analysis)

#### `prepare_sequence_for_MotEvo`

   Create a FASTA-formatted file with the input sequence

- **Parameters**
  - Input sequence (from the configuration file)
  - Header tag for the sequence (constructed from the configuration file)
  - File path for cluster logs

- **Output**
    - A fasta file which will be used in the rule [**run_MotEvo_analysis**](#run_MotEvo_analysis)

#### `run_MotEvo_analysis`

   Run MotEvo for a given FASTA sequence and a given PWM

- **Input**
  - MotEvo parameters file generated in rule [**prepare_MotEvo_parameters**](#prepare_MotEvo_parameters)
  - Path of the PWM directory containing the binding probability matrices
  - Fasta file generated in the rule [**prepare_sequence_for_MotEvo**](#prepare_sequence_for_MotEvo)

- **Parameters**
  - Absolute path of MotEvo parameters file generated in rule [**prepare_MotEvo_parameters**](#prepare_MotEvo_parameters)
  - Absolute path of FASTA file generated in the rule [**prepare_sequence_for_MotEvo**](#prepare_sequence_for_MotEvo)
  - File path for cluster logs

- **Output**
    - A directory with files containing binding posterior information which will be used in the rule [**combine_MotEvo_results**](#combine_MotEvo_results)

#### `combine_MotEvo_results`

   Combine all motevo results into one TSV file

- **Input**
  - A directory with files containing binding posterior information which is generated in [**run_MotEvo_analysis**](#run_MotEvo_analysis)
  - Script that will combine results into one TSV file [`combine-motevo-results.py`](../workflow/scripts/combine-motevo-results.py)

- **Parameters**
  - Name of the MotEvo output file which contains posterior sites information
  - File path for cluster logs

- **Output**
    - A TSV file which gathers information from every analysed PWM.

#### `plot_heatmap_of_MotEvo_results`

   Plot heatmap from the combined_MotEvo_results.tsv file

- **Input**
  - A TSV file containing information from every analysed PWM, generated from rule [**combine_MotEvo_results**](#combine_MotEvo_results)
  - Script that will plot the heatmap with sequence logos as y axis ticks [`heatmap.r`](../workflow/scripts/heatmap.r)
  - Sequence logos generated for each motif from the rule [**plot_sequence_logos**](#plot_sequence_logos)

- **Parameters**
  - Input sequence (from the configuration file)
  - Directory with the all sequence logos
  - File path for cluster logs

- **Output**
    - A heatmap depicting all the motifs with their sequence logos and names as y-axis tick-labels; input sequence as x-axis; and each cell representing per-position binding probability.

#### `prepare_output_bedfile`

   Prepare a list of all inferred binding sites in a BED format

- **Input**
  - A TSV file containing information from every analysed PWM, generated from rule [**combine_MotEvo_results**](#combine_MotEvo_results)

- **Parameters**
  - Input sequence ID (from the configuration file)
  - File path for cluster logs

- **Output**
    - A list of all inferred binding sites in a BED format

[rule-graph]: ../images/rulegraph.svg
[docs-snakemake]: <https://snakemake.readthedocs.io/en/stable/>