from typing import Any, Callable, Dict

import snakemake


class SnakemakeLogger:
    def __init__(self) -> None:
        self.lines = []

    @property
    def log_handler(self) -> Callable[[Dict[str, Any]], None]:
        """Returns a log handler for use with snakemake."""

        def fn(d: Dict[str, Any]) -> None:
            if d["level"] != "shellcmd":
                return
            self.lines.append(d["msg"])

        return fn


def test_default():
    logger = SnakemakeLogger()

    if int(snakemake.__version__[0]) >= 5:
        log_handler = [logger.log_handler]
    else:
        log_handler = logger.log_handler

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
