#!/usr/bin/env python

"""
bioBakery Workflows: metagenomic workflow

Copyright (c) 2016 Harvard School of Public Health

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

# import the workflow class from anadama2
from anadama2 import Workflow

# import the library of biobakery_workflow tasks
from biobakery_workflows import tasks

# create a workflow instance, providing the version number and description
# the version number will appear when running this script with the "--version" option
# the description will appear when running this script with the "--help" option
workflow = Workflow(version="0.1", description="A workflow for whole metagenome shotgun sequences")

# add the custom arguments to the workflow
workflow.add_argument("kneaddata-db", desc="the kneaddata database", required=True)
workflow.add_argument("input-extension", desc="the input file extension", default="fastq")
workflow.add_argument("threads", desc="number of threads/cores for each task to use", default=1)

# get the arguments from the command line
args = workflow.parse_args()

# get all input files with the input extension provided on the command line
input_files = workflow.get_input_files(extension=args.input_extension)

### STEP #1: Run quality control on all input files ###
qc_output_files = tasks.whole_genome_shotgun.quality_control(workflow, input_files, args.threads, args.kneaddata_db)

### STEP #2: Run taxonomic profiling on all of the filtered files ###
merged_taxonomic_profile, taxonomy_tsv_files, taxonomy_sam_files = tasks.whole_genome_shotgun.taxonomic_profile(workflow,qc_output_files,args.threads)

### STEP #3: Run functional profiling on all of the filtered files ###
merged_genefamilies, merged_ecs, merged_pathabundance = tasks.whole_genome_shotgun.functional_profile(workflow,qc_output_files,args.threads,taxonomy_tsv_files)

# start the workflow
workflow.go()
