# Snakemake Shellify

Make functions for shell commands

## Usage

```python
# Snakefile
from snakemake_shellify import shellify

@shellify
def write_hello_world(output): # all snakemake parameters are supported (input, output, params, ...)
    file, = output
    if file == "a.txt":
        return f"echo 'hello world a' > {file}"
    else:
        return f"echo 'hello world b' > {file}"

rule all:
    input: "a.txt", "b.txt", "c.txt"

rule get_a:
    output: "a.txt"
    shell: write_hello_world()

rule get_b:
    output: "b.txt"
    shell: write_hello_world() # shellified functions are reusable
rule get_c:
    output: "c.txt"
    shell: "echo 'hello world c' > {output}"
```

## Installation

Requires python >= 3.6

Tested with snakemake 4-7

For the moment, there is no pip package of this.

```sh
$ git clone https://github.com/stardisblue/snakemake-shellify.git
$ cd snakemake-shellify
$ pip install .
```

## Motivation

Shell commands are complicated when using snakemake and third-party tools (STAR, fastp, ...). This project aims to simplify this process.



