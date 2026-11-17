# Stage 1 validation record

Initial implementation record: **2026-11-17** (Europe/Istanbul).
The results in the sections below describe the original five-test implementation.
The separate publication-review run at the end supersedes them for the revised code.

## Environment actually used

- Windows 11, reported as `Windows-11-10.0.26200-SP0`, x64.
- CPython **3.12.10**, project-local `.venv`.
- pip **25.0.1**.
- `qblox-scheduler==1.0.1`, `qblox-instruments==1.4.1`, `matplotlib==3.11.2`.
- All 130 resolved runtime packages are pinned in `requirements.txt`; direct
  dependencies are listed in `requirements.in`.

Packages were installed from PyPI into a newly created virtual environment.
The instruments source distribution built successfully. No additional system
HDF5 or C++ build-tools installation was needed on this host. This does not remove
the vendor's platform-specific requirements for other installation routes.

## Commands actually run and results

| Check | Result |
| --- | --- |
| `.\.venv\Scripts\python.exe -m pip check` | Passed: `No broken requirements found.` |
| `.\.venv\Scripts\python.exe -m pip install --no-index -r requirements.txt` | Passed: all frozen versions matched the installed environment. This was not a second fresh-environment install. |
| `.\.venv\Scripts\python.exe .\examples\dummy_cluster.py` | Passed: dummy Cluster compilation and Q1ASM, sequence JSON, timing CSV, PNG and version metadata exports. |
| `.\.venv\Scripts\python.exe -m unittest discover -s tests -v` | Passed: 5 tests, 65.561 seconds reported by unittest. |
| Workflow YAML parsing | Passed using the installed PyYAML BaseLoader. This is syntax parsing, not a GitHub-hosted workflow run. |
| Pulse diagram visual inspection | Passed: two pulse envelopes at amplitudes 0.5 and 0.25 with a 20 ns gap. |

The five tests check:

1. Compilation with no non-loopback Python socket connection attempts.
2. Rejection of a non-null instrument IP before initialization.
3. Non-empty Q1ASM matching sequence JSON, two `play` commands, synchronization,
   final `stop`, and no acquisition instructions or acquisition entries.
4. Compiler-transformed timing entries, PNG format, and compile-only metadata.
5. Valid waveform references, 4/80-sample waveforms, gains, 96 ns offset segment,
   and 24/80 ns real-time playback advances.

## Observed compiler behavior

The requested 100 ns first pulse becomes a 96 ns offset followed by a 4 ns
waveform. The second pulse uses an 80-sample waveform. The first `play` advances
24 ns, leaving a 20 ns gap after its four samples. A 4 ns phase-update interval
shifts the compiled table/diagram to first-pulse start 4 ns, second-pulse start
124 ns and end 204 ns. See the annotated program in [architecture.md](architecture.md).

## Environment issues encountered

The initial sandboxed pip request failed DNS resolution (`getaddrinfo failed`).
Installation succeeded with approved network access.

The initial sandboxed dummy initialization hung in Windows
`asyncio.new_event_loop()` -> `_make_self_pipe()` -> `socket._fallback_socketpair()`
-> `accept()`. It was interrupted. A standalone Windows asyncio check succeeded
outside that sandbox, and compilation/tests were then run outside the sandbox.
No physical hardware was used. The example also forces dummy connections and
checks each Cluster's `is_dummy` property. The test guard permits loopback for
asyncio's internal wakeup pipe, while rejecting other Python socket connections.

Scientific-library imports were slow on this host, including later runs; diagnostic stack dumps
showed progress through SciPy imports. They were not Q1ASM execution. The
diagnostic wrapper is not part of the example, and no vendor files were modified.

## Remaining limits

- No upload, assembly acceptance on firmware, sequencer start or real-time
  execution was tested. No measurements were requested or reported.
- The dummy environment does not validate qubit dynamics, RF quality,
  calibration, physical wiring or hardware synchronization.
- The frozen environment targets Windows x64 / Python 3.12.10. Other Python
  versions and operating systems have not been validated here.
- GitHub Actions has not run remotely. The workflow is ready locally; no remote
  repository was created, and nothing was pushed.

## Publication review run — 2026-11-17

A separate, newly created `.venv-validation` environment was used (no system
site-packages). Windows 11 x64, CPython 3.12.10, pip 25.0.1;
scheduler 1.0.1, instruments 1.4.1, matplotlib 3.11.2, QCoDeS 0.63.0.
All 130 installed runtime versions were checked against `requirements.txt`.

| Command/check actually executed | Result |
| --- | --- |
| `python -m venv .venv-validation` | Passed; new isolated environment created. |
| `.\.venv-validation\Scripts\python.exe -m pip install --index-url https://pypi.org/simple -r requirements.txt --quiet` | Passed, exit 0; fresh installation from the pinned requirements. |
| `.\.venv-validation\Scripts\python.exe -m pip check` | Passed: no broken requirements. |
| `.\.venv-validation\Scripts\python.exe examples\dummy_cluster.py` | Passed, exit 0; dummy-only compilation and five output files. |
| `.\.venv-validation\Scripts\python.exe -m unittest discover -s tests -v` | Passed: 10 tests in 17.915 seconds. |
| Staged diff whitespace check | Passed: `git diff --cached --check`. |
| README/local Markdown links | Passed: no broken file links. |
| Shipped license text comparison | Passed: both complete texts in THIRD_PARTY_NOTICES.md match installed distribution license files. |
| Staged file allowlist and credential-pattern scan | 17 intended files; no credential-pattern matches. Virtual environments, caches, artifacts and the existing 7z archive excluded. This is not a guarantee against every possible secret format. |
| Workflow YAML and required commands | Parsed and verified Windows, Python 3.12.10, pinned install, pip check and unittest commands locally. Not a GitHub Actions run. |

The ten tests comprise the five retained compiler/output checks, four lifecycle
failure checks and one experiment-intent check. The integration test also verifies
that the QCoDeS registry returns to its pre-run state. Exact Q1ASM opcodes,
waveform lowering and setup timing are pinned-compiler assumptions. The separate
experiment test checks pulse amplitudes, durations, port/clock and the 20 ns gap
without depending on those compiler decisions.

The example and full test suite ran with approved local loopback access outside
the restricted sandbox. Lifecycle tests use in-memory QCoDeS instruments; they
do not inject failures into or communicate with physical hardware. The cleanup
policy covers newly registered instruments, not inaccessible vendor resources
whose constructor fails before registration, and assumes no concurrent instrument
creation in the same process.

### Historical publication status before authentication and provenance review

The repository initially had no commits and no remotes, on branch `master`.
GitHub CLI was not installed, GH_TOKEN/GITHUB_TOKEN were absent, and an
unsandboxed `git credential-manager github list` returned no accounts (exit 0).
No authenticated personal GitHub destination was established.

The official tutorial download was inspected but contains no license declaration.
The affected adaptations and publication hold are documented in
[THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md). The verified package licenses
are not being assumed to license that separate tutorial.

Local preparation is complete. No public repository was created and no push was
attempted because authentication and tutorial reuse terms remain unresolved.
Remote branch verification and GitHub Actions execution therefore have not taken
place. Stage 2 remains unimplemented.

## Provenance resolution and publication rerun — 2026-11-17

The previous publication status above is historical. GitHub authentication is now
available for personal account `Berkovi`. The section-level
[provenance audit](provenance.md) supersedes the earlier blanket tutorial hold:
ordinary API usage and acknowledged configuration choices were retained, and no
copied tutorial implementation or explanatory text was identified. The package
licenses and tutorial acknowledgement remain intact. No functional code changed
during this review, and Stage 2 remains unimplemented.

The existing clean-install `.venv-validation` environment from the preceding run
was reused: Windows 11 x64, Python 3.12.10, pip 25.0.1, and the same 130 pinned
runtime dependencies. This rerun was not another fresh installation.

| Command actually rerun | Result |
| --- | --- |
| `.\.venv-validation\Scripts\python.exe -m pip check` | Passed: `No broken requirements found.` |
| `.\.venv-validation\Scripts\python.exe examples\dummy_cluster.py` | Passed: Q1ASM, sequence JSON, timing CSV, pulse PNG and run metadata exported under ignored `artifacts/stage1`. |
| `.\.venv-validation\Scripts\python.exe -m unittest discover -s tests -v` | Passed: all 10 tests; unittest reported 1.424 seconds. |

The vendor's dummy-instantiation warning was expected. No physical connection,
upload, instrument execution, acquisition or qubit simulation took place. The
same loopback sandbox exception and hardware-validation limitations apply.
GitHub Actions is a separate remote check; these local results do not claim a
successful CI run. Its run history will be available on the published repository.
