# quantum-control-lab

An independent learning project using qblox-scheduler and
qblox-instruments, based on Qblox's official tutorials.

This product includes software developed by Qblox.

This project is not affiliated with or endorsed by Qblox.

Original contributions use the [MIT license](LICENSE). Third-party materials
retain their own licenses; see [third-party notices](THIRD_PARTY_NOTICES.md).
The [provenance audit](docs/provenance.md) distinguishes ordinary API/configuration
usage from copied source or tutorial material and records the review outcome.

A small, runnable project for learning quantum control software architecture.
Stage 1 follows an experiment from a Python pulse schedule to Qblox Q1ASM using
an official dummy Cluster. No physical hardware or qubit measurements are involved.

## Stage 1

The experiment uses a dummy QRM-RF in slot 2 of `cluster0` and maps its first
complex output to logical port `q0:mw`. It requests two square pulse envelopes:

| Pulse | Start | Duration | Normalized amplitude |
| --- | --- | --- | --- |
| First | 0 ns | 100 ns | 0.50 |
| Second | 120 ns | 80 ns | 0.25 |

The gap is 20 ns; the experiment spans 200 ns. Both the logical clock and local
oscillator are 5 GHz, giving zero intermediate frequency. These are illustrative
settings, not calibrated qubit parameters. Amplitudes are not voltages.

## Run on Windows with PowerShell

Use 64-bit CPython **3.12.10**, the version selected for this project. Qblox
documents Python >=3.10 support; this repository validates only the pinned
Windows/Python combination. See [sources](docs/sources.md) for version reasoning.
The `py` launcher was unavailable on the development host, so commands use `python`.

From the repository directory:

```powershell
python --version
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install pip==25.0.1
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe .\examples\dummy_cluster.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

If `.venv` already exists from this task, start at `pip check` to use that installed
environment. No activation or PowerShell execution-policy change is needed.
The first installation requires network access and installs substantial vendor
dependencies, including plotting and scientific libraries. There is no need to
install Jupyter or use a notebook for this exercise.

## Inspect the output

The script writes to `artifacts/stage1/` (ignored by Git):

| File | What to inspect |
| --- | --- |
| `cluster0_module2_seq0.q1asm` | Actual generated sequencer program. |
| `sequence.json` | The same program plus waveform, weight and acquisition tables. |
| `timing.csv` | Compiler-transformed timing entries in seconds, including setup and offset changes. |
| `pulse_diagram.png` | Compiled pulse envelope; no measured or simulated qubit data. |
| `run_info.json` | Execution mode, Python and direct package versions. |

```powershell
Get-Content .\artifacts\stage1\cluster0_module2_seq0.q1asm
Import-Csv .\artifacts\stage1\timing.csv | Format-Table
Invoke-Item .\artifacts\stage1\pulse_diagram.png
```

The requested pulses start at 0 and 120 ns. The compiled plot starts them at
4 and 124 ns because the compiler adds a 4 ns phase-update interval. The first
pulse is lowered to a 96 ns offset plus a 4 ns waveform, so the CSV contains
multiple entries for it. The program contains output commands
and a final `stop`; it contains no acquisition instructions. Compiler startup and
trailer time are separate from the 200 ns experiment. A warning that a dummy
Cluster is being created is expected. The script rejects non-null IP addresses,
forces dummy connections, checks `is_dummy`, and never calls `run()`.

The tests compile into a temporary directory. They check the generated program,
waveform references/amplitudes, resolved timings, exported files and rejection of
a physical configuration. A Python socket guard rejects non-loopback connections
during compilation; loopback is allowed because Windows asyncio needs it for
internal communication. This is a regression check, not an OS network firewall.
Exact opcodes, waveform lowering and the 4 ns setup interval are compiler-version
regressions. Separate experiment tests check the requested pulse parameters and
timing relation. Lifecycle tests exercise constructor/partial-connection failures,
cleanup errors, and preservation of existing instruments with in-memory resources.
Cleanup uses the pinned QCoDeS 0.63.0 instrument registry to discover resources
created during initialization. It attempts every registered resource's close,
attaches cleanup failures to an original error, and otherwise raises a grouped
cleanup error. This standalone script assumes no concurrent instrument creation;
vendor-internal resources that never become registered remain the vendor's
constructor responsibility. Existing `cluster0` instances are never replaced.
The [Actions workflow](.github/workflows/checks.yml) runs on Windows and needs no
lab credentials. Adding it locally does not mean it has run on GitHub.

If a restricted execution sandbox hangs in `asyncio`/`socketpair` while creating
the dummy Cluster, run the commands in a normal PowerShell session: the driver
needs local loopback even though it does not connect to hardware. Do not set a
real IP to work around this. Scientific-library imports can take several minutes
on this host, including later runs. This startup time is not an instrument
real-time performance measurement.

## Read the project

- [Example](examples/dummy_cluster.py): experiment, dummy configuration guard,
  compilation and artifact export.
- [Hardware configuration](config/dummy_hardware.json): logical-to-physical mapping.
- [Architecture](docs/architecture.md): host/instrument boundary and annotated Q1ASM.
- [Validation record](docs/validation.md): checks actually executed and limitations.
- [Sources](docs/sources.md): official references and access date.
- [Decision record](docs/decisions/0001-stage1-scope.md): why this scope stays small.

Study these three places in the example first:

1. `build_schedule()`: how `ref_op`, `ref_pt="end"` and `rel_time` express the gap.
2. `main()`: how the hardware configuration and dummy instrument become inputs
   to `HardwareAgent.compile()`.
3. `export_compiled()`: how to find a particular module/sequencer's Q1ASM and
   waveform tables, then compare them with the compiled timing diagram.

`requirements.in` lists direct dependencies. `requirements.txt` freezes the
resolved packages for Windows/Python 3.12.10. Treat changes to these pins as a
separate compatibility exercise: resolve in a fresh environment, run the example
and checks, then update the freeze and validation record together. This is a
version snapshot, not a cross-platform or hash-verified lockfile.

## Roadmap (not implemented)

1. A small scheduler that detects channel and timing conflicts.
2. A device interface and simulated backend.
3. Timeouts, connection failures, and fault injection.
4. Resource limits and scaling measurements.
5. A small C++ component, if justified, to explore the Python/C++ boundary.

We will run and understand Stage 1 before selecting the next exercise.
