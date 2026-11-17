# Sources and version selection

Access date for all links: **2026-11-17** (Europe/Istanbul).

| Official source | Used for |
| --- | --- |
| [Scheduler Hello Quantum World](https://docs.qblox.com/en/main/quickstart/QBS_helloworld/qbloxscheduler_helloworld.html) | Starting page still exists; pulse-level Schedule, hardware mapping, `HardwareAgent.compile`, `ip=None` dummy selection. |
| [Software installation](https://docs.qblox.com/en/main/quickstart/installation/software/python.html) | Python >=3.10; virtual environment; driver dependency; Windows HDF5/build guidance. |
| [Qblox's scheduler 1.0.1 release](https://pypi.org/project/qblox-scheduler/1.0.1/) | Released 2026-10-12; Python >=3.10; scheduler >=1,<2 supports instruments >=1,<2. |
| [Qblox's instruments 1.4.1 release](https://pypi.org/project/qblox-instruments/1.4.1/) | Released 2026-10-12; Python >=3.10; driver release and firmware compatibility information. |
| [Instruments Hello Quantum World](https://docs.qblox.com/en/main/quickstart/QBI_helloworld/qblox_instruments_helloworld.html) | Explicit `Cluster(..., dummy_cfg=...)` alternative; sequence dictionary and driver responsibilities. |
| [Q1 sequencer architecture](https://docs.qblox.com/en/main/products/architecture/sequencers/sequencer.html) | FPGA implementation; Q1 core and real-time core distinction. |
| [Q1ASM instruction guide](https://docs.qblox.com/en/main/products/qblox_instruments/q1/index.html) | Instruction semantics used to interpret generated output. |
| [Scheduler API](https://docs.qblox.com/en/main/autoapi/qblox_scheduler/index.html) | Schedule timing references, compiled instructions and plotting. |
| [GitHub Actions: Python](https://docs.github.com/en/actions/tutorials/build-and-test-code/python) | Checkout/setup actions and Python check workflow structure. |

The rolling documentation displayed release 2026.10.2 on the starting and installation pages (some linked pages displayed 2026.10.1). This is a documentation release label, not a Python package version. The installation page still recommends `--pre`, while PyPI already lists the stable 1.0.1 scheduler release. We explicitly select 1.0.1 with instruments 1.4.1 instead of assuming the newest rolling example and every historical release have the same API. Python 3.12.10 is the interpreter available on this Windows host and lies within the published requirements.

The installed package source and executable checks are the final authority for this example's concrete API and output. No physical firmware version is validated. `requirements.txt` records the resolved environment; `docs/validation.md` records what actually ran.
