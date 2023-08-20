from snakemake_shellify.wrapper import shellify

@shellify
def get_rule(output):
    file, = output
    if file == "a.txt":
        return f"echo 'hello world' > {file}"
    else:
        return f"echo 'hello borld' > {file}"


rule all:
    input: "a.txt", "b.txt"

rule get_a:
    output: "a.txt"
    shell: get_rule()

rule get_b:
    output: "b.txt"
    shell: get_rule()
