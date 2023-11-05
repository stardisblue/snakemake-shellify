from typing import Any

import snakemake


class SnakemakeLogger:
    def __init__(self) -> None:
        self.lines = []

    def __call__(self, d: dict[str, Any]) -> Any:
        if d["level"] != "shellcmd":
            return
        self.lines.append(d["msg"])


def test_default():
    logger = SnakemakeLogger()

    log_handler = [logger]

    if int(snakemake.__version__[0]) < 5:
        log_handler = logger

    assert snakemake.snakemake(
        snakefile="test/simple.smk",
        dryrun=True,
        printshellcmds=True,
        log_handler=log_handler,
    )

    assert sorted(logger.lines) == [
        "echo 'hello borld' > b.txt",
        "echo 'hello corld' > c.txt",
        "echo 'hello world' > a.txt",
    ]
