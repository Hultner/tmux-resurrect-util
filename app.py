"""tmux-res – TMUX Resurrect utility tool

Author: Alexander Hultnér
 .
..:

I have not tested this yet but an idea I've had is to run the clean command as
a weekly cronjob, that way we can keep our resurrect-directory clean and tidy
without manual intervention. Maybe also run link-last on boot (recover crash)

This is currently in a working state for me but I have some future improvements
which I've considered. Listing them below.

TODO:
    - [x] Recover `last` link to latest state
    - [x] Archive resurrect files older then given treshold (clean up)
    - [x] Publish to Github
    - [ ] Write tests (pytest+hypothesis)
    - [ ] Travis CI/CD
    - [ ] Codacy code quality, coverage
    - [ ] Move helpers/utils to sperate files
    - [ ] Move TmuxResFile class to file?
    - [ ] Improve docstrings
    - [ ] Lint and refactor
    - [ ] See if there's a better way to handle `verbose()` function
    - [x] Publish to PyPa/pip
    - [ ] Investigate if asyncio can give any benefit, parseing res files
    - [ ] Investigate globals replacement (especially for async)
    - [ ] Pass ENV/constants through args via click.option envvar
        http://click.pocoo.org/5/options/#values-from-environment-variables
        http://click.pocoo.org/5/options/#multiple-values-from-environment-values
        - [ ] RESURRECT_PATH = "~/.tmux/resurrect"
        - [ ] ARCHIVE_DAYS_THRESHOLD = 7 || 30
        - [ ] ARCHIVE_FILES_THRESHOLD = 10
    - [ ] Create a wrapper class for List[TmuxResFile]
        - [ ] Balanced/sorted insert
            https://github.com/grantjenks/python-sortedcontainers/
        - [ ] Get most recent state
        - [ ] Get oldest state
        - [ ] Get all states in time frame (start=None, end=None), None=unbound
            - [ ] Returns instance of wrapper class with subset
        - [ ] Refresh/update state (can be done after archive)
        - [ ] Get List[pathlib.Path]-collection
    - [ ] Improve typeannotatins, test with mypy
    - [ ] Generate sphinx docs
    - [ ] Add pycov-coverage reporting
    - [ ] Archive files atomically/safer, eg. if someone for some reason runs
        multiple instances of tmux-res simantainously (bad)
        I don't know if people actually ever access old state files, my initial
        idea was to delete them completely but since they're quite small I
        decided on archiving.
        - [ ] Maybe copy files first, use random UUID/tmp for archive directory
            then remove them once archive is done and working


Warning: This module uses several features introduced in 3.7 and 3.6.
    I've built this tool purely for personaly usage. I use it as a oppertunity
    to try out new features which makes development more convenient.

    Feel free to backport if you want to use it with older versions, to simplify
    this process I've listed new features from 3.7 I know that I use.

Python 3.7 features:
    Forward annotation references
    - Quote or remove for backwards compability
    Dataclasses
    - Install package on 3.6, expand for older
    datetime.fromisoformat
    - Define format manually or use library for older versions


"""
from __future__ import annotations
import os
from datetime import datetime, timedelta
import shutil
from typing import List
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv
import click
from click import echo, FileError


ARCHIVE_DAYS_THRESHOLD: int = 7
res_states: List[TmuxResFile] = []


@dataclass(order=True)
class TmuxResFile:
    added: datetime
    path: Path

    @staticmethod
    def factory(state: Path) -> TmuxResFile:
        """Returns a TmuxResFile object from given Path"""
        # YYYY-MM-DDTHH:MM:SS -> 19 chars
        date_str = state.stem[-19:]
        dt = datetime.fromisoformat(date_str)

        verbose(f"Parsed file date: {state.stem[-19:]} -> {dt}")
        return TmuxResFile(added=dt, path=state)


def verbose(*args, **kwargs) -> None:
    """Does nothing by default"""
    pass


def load_conf() -> None:
    """Loads configuration from .env file"""
    env_path = Path(".") / ".env"
    load_dotenv(dotenv_path=env_path)

    global RESURRECT_PATH
    RESURRECT_PATH = (
        Path(os.getenv("RESURRECT_PATH", default="~/.tmux/resurrect"))
        .expanduser()
        .resolve()
    )
    verbose(RESURRECT_PATH)

    if not RESURRECT_PATH.is_dir():
        raise FileError(str(RESURRECT_PATH), hint="Not a valid directory")


def main(verbose_on: bool) -> None:
    """Entry point for CLI"""
    if verbose_on:
        global verbose
        verbose = click.echo
        verbose("Verbose mode enabled")
    load_conf()


def parse_states() -> None:
    """Parses tmux state files from resurrect

    Adds them to module variable `res_states` sorted by date

    """
    # This is pretty much instant for >500 lines, consider doing this in a
    # seperate state process with message passing or async if it ever gets slow
    # It's currently invoked when needed to delay unecessary work.
    # Do this at startup instead if we move it to a process/thread
    # tmux_resurrect_2018-07-03T11:34:54.txt
    # tmux_resurrect_{datetime}.txt
    states = RESURRECT_PATH.glob("tmux_resurrect_*-*-*T*:*:*.txt")
    state_objs = (TmuxResFile.factory(state=state) for state in states)
    res_states.extend(sorted(state_objs))


def archive_files(files: List[TmuxResFile], name: str) -> None:
    """Archives a collection of TmuxResFile´s"""
    # Make dir
    target = RESURRECT_PATH / name
    if target.exists():
        raise FileError(str(target), hint="archive target already exists")

    target.mkdir()
    for f in files:
        # str() due to shutil bug, can be removed when below is merged
        # PR: https://github.com/python/cpython/pull/5393
        # Issue: https://bugs.python.org/issue32689
        shutil.move(str(f.path), str(target))
    shutil.make_archive(target, "gztar", root_dir=target)
    if target.exists():
        shutil.rmtree(target)
    echo(f"Old states compressed and archived in: {target}.tar.gz")
    # Refresh res_state


@click.group()
@click.version_option()
@click.option("-v", "--verbose", is_flag=True, help="Enables verbose mode")
def cli(verbose):
    """TMUX Resurrect utility, simplifies and automates common tasks"""
    main(verbose)


@cli.command()
def clean():
    """Archive tmux state files older then one month"""
    # parse tmux files
    # if > 10 files: add to archive if older then 1 month
    parse_states()
    if len(res_states) < 10:
        return echo("Less then 10 resurrect states, no need to clean up")

    to_archive: List[TmuxResFile] = []

    verbose("Will clean:")
    for state in res_states:
        if (datetime.now() - state.added).days < ARCHIVE_DAYS_THRESHOLD:
            # Threshold reached, don't archive newer files
            break
        verbose(str(state.path))
        to_archive.append(state)

    if len(to_archive) < 10:
        return echo("Less then 10 files to archive, skipping")

    # Archiving files
    start = to_archive[0].added.isoformat()
    end = to_archive[-1].added.isoformat()
    # Double hypen instead of solidues (forward slash "/") due to file system
    # https://en.wikipedia.org/wiki/ISO_8601#Time_intervals
    archive_folder = f"tmux_resurrect_{start}--{end}"
    verbose(f"Archive destination: {archive_folder}")
    archive_files(files=to_archive, name=archive_folder)


@cli.command("link-last")
def link_last():
    """Link last to newest tmux resurrect file"""
    last = RESURRECT_PATH / "last"
    verbose(f"Checking if link exists:\n - {last}\n - {last.exists()}")

    if last.exists():
        return echo(f"Link to last already exists:\n {last} \n  -> {last.resolve()}")
    elif last.is_symlink():
        # Symlink exists but links to non-existant file
        # This can happen if tmux terminated while saving resurrect state
        last.unlink()

    parse_states()

    # last doesn't contain a valid link, rebuilding
    latest_state = res_states[-1]
    echo(f"Latest known state (recovering): {latest_state.path.name}")
    last.symlink_to(latest_state.path)
    echo(f"Recovery completed to state at: {latest_state.added}")


if __name__ == "__main__":
    main()
