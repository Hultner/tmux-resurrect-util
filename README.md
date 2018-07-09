# <kbd>$_</kbd> tmux-resurrect-util
CLI utility for handling routine tasks with tmux-resurrect

```shell
» tmux-res --help
Usage: tmux-res [OPTIONS] COMMAND [ARGS]...

  TMUX Resurrect utility, simplifies and automates common tasks

Options:
  --version      Show the version and exit.
  -v, --verbose  Enables verbose mode
  --help         Show this message and exit.

Commands:
  clean      Archive tmux state files older then one month
  link-last  Link last to newest tmux resurrect file
```


## Install
*In below examples I use unopionated `pip` for installation. I recommend installing it into a virtualenv, there are multiple tools to achive this.*

**Requirements**  
To use this utility you need Python 3.7. See [app.py](app.py) for specifics.
```shell
» python --version
Python 3.7.0
» pip --version
pip 10.0.1 from /…/lib/python3.7/site-packages/pip (python 3.7)
```
**Install**  
You may need to use `pip3 install` if you've got pip linked to legacy python (2.x)
```shell
git clone git@github.com:Hultner/tmux-resurrect-util.git
pip install ./tmux-resurrect-util
```

## Development & contributions
*Fork and send a PR!*
For formatting I use [black](https://github.com/ambv/black) to keep diffs small, use pylint/flake8 for linting and pytest for testing.
Code is currently in prototype-phase, simplifications, refactoring and other quality improvements are welcome.

### Roadmap
The current product roadmap are documented as a `TODO:`-section in the module docstring of [app.py](app.py). Highlevel test psuedo code are found in [test.py](test.py).

### Get started
I use pipenv for development. Make sure you update the `Pipfile` and `Pipefile.lock` if you add or update dependencies.
Avoid adding external packages if they aren't needed, especially low activity ones. 
Consult with me if you're planning to create a PR where you want to pull in something new and fancy.
```shell
» git clone git@github.com:Hultner/tmux-resurrect-util.git
...
» cd tmux-resurrect-util
» pipenv install -e .
...
» vi .
```
Enjoy!

---
*”Inpsiring qoutes aren't for everyone”* — Some One, Somewhere (sometime).

```
 .
..:
```
