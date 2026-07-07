# PsychSim — Install & Run in VS Code on WSL2 (Ubuntu, Windows 10)

A complete, copy-pasteable guide to get the PsychSim package running inside VS Code,
using WSL2 Ubuntu on a Windows 10 PC. Follow the steps in order.

**Good news up front:** PsychSim is **pure Python standard library** — it has *no
third-party dependencies*. Nothing to install to make it run except Python itself.
It targets **Python 3.9+** (developed and tested on 3.12).

---

## 0. What you have

A zip file, `PsychSim_Unified_Platform.zip`, which unpacks to a folder `psychsim_x/`
containing:

```
psychsim_x/
├── core/            # the reusable platform (affect engine, world, matrices, ...)
├── extensions/      # research-specific code (sophropathy, justice)
├── tests/           # the test suite (~215 tests)
├── docs/            # architecture notes
├── run_tests.py     # runs the whole test suite
├── run_pipeline.py  # runs an end-to-end demonstration
├── project.py       # spawns a simulated world (the main entry API)
└── pyproject.toml   # package metadata (zero dependencies)
```

---

## 1. Prerequisites (verify or install)

You said WSL2 + Ubuntu is already set up. Quick checks, with install commands if any
piece is missing.

**a. WSL2 with Ubuntu.** In a Windows PowerShell:
```powershell
wsl -l -v
```
You should see Ubuntu listed with `VERSION 2`. If WSL isn't installed at all:
```powershell
wsl --install -d Ubuntu
```
(then reboot and set a Linux username/password when prompted).

**b. VS Code (on Windows).** Install from https://code.visualstudio.com if you haven't.

**c. The WSL extension for VS Code.** This is what lets VS Code work *inside* Ubuntu.
Open VS Code → Extensions (Ctrl+Shift+X) → search **"WSL"** (publisher: Microsoft) →
Install. (You'll install the Python extension later, from *within* WSL — step 4.)

**d. Python tooling inside Ubuntu.** Open your Ubuntu terminal (Start menu → Ubuntu)
and run:
```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip unzip
python3 --version        # expect 3.9 or newer
```

---

## 2. Put the code in the Linux filesystem (important)

Keep the project on the **Linux side** (your Ubuntu home, `~`), **not** under
`/mnt/c/...`. Working from `/mnt/c` is slow and causes Windows/Linux line-ending and
permission problems. We copy the zip from Windows into WSL, then unzip it there.

In the **Ubuntu terminal** (adjust the Windows path/filename if yours differs — WSL
sees your Windows drives under `/mnt/c`):

```bash
# make a projects folder in your Linux home
mkdir -p ~/projects && cd ~/projects

# copy the zip from your Windows Downloads into WSL
# (replace <WindowsUser> with your Windows account name)
cp "/mnt/c/Users/<WindowsUser>/Downloads/PsychSim_Unified_Platform.zip" .

# unzip it
unzip -q PsychSim_Unified_Platform.zip

# you now have ~/projects/psychsim_x
cd psychsim_x && ls
```

> Tip: to find your Windows username, run `ls /mnt/c/Users` and look for your folder.

---

## 3. Open the project in VS Code (attached to WSL)

From inside `~/projects/psychsim_x` in the Ubuntu terminal:

```bash
code .
```

The first time, this installs a small VS Code server into WSL and then opens VS Code
on Windows **connected to Ubuntu**. Confirm it worked: the **bottom-left green corner**
of VS Code should read **"WSL: Ubuntu"**. Everything you do in this window now runs in
Linux.

(Alternative without the terminal: in VS Code press `F1` → **"WSL: Connect to WSL"**,
then File → Open Folder → `/home/<you>/projects/psychsim_x`.)

---

## 4. Install the Python extension (in WSL) and create a virtual environment

**a. Python extension.** With the folder open (and VS Code showing "WSL: Ubuntu"), go
to Extensions (Ctrl+Shift+X). You'll see a note that extensions can be installed *in
WSL*. Search **"Python"** (Microsoft) → **Install in WSL: Ubuntu**.

**b. Virtual environment.** In the VS Code integrated terminal (Ctrl+` — it opens a
*Linux* shell), from the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

Your prompt should now start with `(.venv)`.

**c. Install PsychSim into the venv (editable).** This is the step that makes every
`import` resolve cleanly everywhere in VS Code (test explorer, debugging single files),
because the `pyproject.toml` maps the packages for you:

```bash
pip install -e .
```

Optionally add pytest for a nicer test experience and the VS Code Test Explorer:
```bash
pip install pytest
```

> **Why editable install?** The packages live under `core/` and `extensions/`.
> `pip install -e .` registers them (`affective_engine`, `sim_world`, `sophropathy`,
> …) so `import affective_engine` works from anywhere without setting `PYTHONPATH`.
> The runner scripts (`run_tests.py`, `run_pipeline.py`) *also* add those folders to
> the path themselves, so they work even without this install — but the editable
> install is what makes the VS Code tooling seamless.

---

## 5. Select the interpreter in VS Code

Press `F1` → **"Python: Select Interpreter"** → choose the one at
`./.venv/bin/python` (labelled something like *Python 3.x ('.venv': venv)*).

VS Code will remember this for the project and use it for the terminal, running, and
debugging.

---

## 6. Run it — three ways

### a. The test suite (fastest way to confirm everything works)

In the VS Code terminal (with `(.venv)` active):

```bash
python run_tests.py
```
Expected: it runs ~215 tests and ends with a line like
`TOTAL: ran 215 tests (core platform + sophropathy extension).`

Or, with pytest installed:
```bash
python -m pytest -q
```
Expected: `197 passed, 18 skipped` (the 18 skips are intentional — obsolete tests from
before an architecture change, honestly marked, not failures).

### b. The end-to-end pipeline (a full demonstration run)

```bash
python run_pipeline.py
```
This spawns a small simulated world, ages a population through the substrate and the
three matrices, and prints a summary. (A copy of a prior run is in
`PIPELINE_OUTPUT.txt` for reference.)

### c. Drive it yourself from a Python REPL

```bash
python
```
then, for example:
```python
from project import ProjectSpec, spawn_universe
from sim_world import TimeController, TimeScale
from sophropathy import make_life_stepper

uni = spawn_universe(ProjectSpec(name="demo", target_population=100,
                                 profile="england_2021", extensions=["sophropathy"],
                                 fearless_frac=0.4, seed=3),
                     place_residents=False)
step = make_life_stepper(uni, seed=1)
TimeController(step).run(TimeScale.YEAR, steps=22)

# inspect an emergent child: their group standing and their (monitored) executive state
d = next(iter(step.dev.values()))
print(d["group_matrix"].ranks(top=2))
print(d["executive"].note())
```

---

## 7. Running & debugging individual files in VS Code

- **Run a file:** open any script with a `if __name__ == "__main__":` block (e.g.
  `run_pipeline.py`) and click the **▷ Run** button (top-right), or press `F5` to run
  **with the debugger** (breakpoints, step-through, variable inspection).
- **Test Explorer:** click the **flask/beaker icon** in the left activity bar. With
  pytest installed and the interpreter selected, your tests appear as a tree you can
  run/debug individually. If they don't appear at first, see Troubleshooting → *Tests
  not discovered*.

To make test discovery reliable, create a file `.vscode/settings.json` in the project
root with:

```json
{
  "python.testing.pytestEnabled": true,
  "python.testing.unittestEnabled": false,
  "python.testing.pytestArgs": ["tests"],
  "python.analysis.extraPaths": ["core", "extensions"]
}
```

(The `extraPaths` line also tells the editor's IntelliSense/Pylance where the packages
are, so imports resolve without red squiggles even before the editable install is
picked up.)

---

## 8. Troubleshooting

**"code: command not found" in the Ubuntu terminal.**
Make sure VS Code is installed on Windows and the **WSL extension** is installed. Open
VS Code once on Windows, then re-open the Ubuntu terminal and try `code .` again. (The
`code` shim is added to your Linux PATH the first time VS Code connects to WSL.)

**Imports fail (`ModuleNotFoundError: No module named 'affective_engine'`).**
Either run via the provided scripts (`python run_tests.py`, `python run_pipeline.py`,
which set the path themselves), or make sure you ran `pip install -e .` inside the
activated `.venv`, and that the selected interpreter is `./.venv/bin/python`
(bottom-left / `F1` → Python: Select Interpreter).

**Tests not discovered in the Test Explorer.**
Confirm `pip install pytest` ran in the venv, the interpreter is the venv one, and the
`.vscode/settings.json` above exists. Then `F1` → **"Test: Refresh Tests"**. Running
`python -m pytest -q` in the terminal is always a reliable fallback.

**Line-ending or "^M" / permission oddities.**
These come from editing/keeping the project under `/mnt/c/...`. Keep it in the Linux
home (`~/projects/psychsim_x`) as in step 2. If you already have CRLF issues:
`sudo apt install -y dos2unix && find . -name "*.py" -exec dos2unix {} +`.

**`python3 -m venv` fails.**
Install the venv package: `sudo apt install -y python3-venv`, then retry.

**Wrong Python version.**
`python3 --version` must be ≥ 3.9. On older Ubuntu, install a newer Python (e.g.
`sudo apt install -y python3.12 python3.12-venv`) and create the venv with that:
`python3.12 -m venv .venv`.

**VS Code opened on Windows, not WSL.**
Check the bottom-left corner reads **"WSL: Ubuntu"**. If it says nothing/Windows,
`F1` → **"WSL: Reopen Folder in WSL"**.

---

## 9. Everyday workflow, once set up

```bash
cd ~/projects/psychsim_x
source .venv/bin/activate      # activate the environment
python -m pytest -q            # run tests
python run_pipeline.py         # run the demonstration
code .                         # open in VS Code (if not already open)
```

That's it — the prototype runs entirely offline, needs no packages beyond Python, and
is now editable and debuggable in VS Code on your local machine.
