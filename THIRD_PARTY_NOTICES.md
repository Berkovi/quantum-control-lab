# Third-party notices and provenance

Reviewed on 2026-11-17. The license texts below were read from the installed,
version-pinned distribution files, not inferred from package metadata. Vendor
packages and repositories are not distributed in this repository.

## Tutorial provenance and publication hold

`examples/dummy_cluster.py` (`build_schedule` and the HardwareAgent usage) and
`config/dummy_hardware.json` were adapted from Qblox's
[Scheduler Hello Quantum World tutorial](https://docs.qblox.com/en/main/quickstart/QBS_helloworld/qbloxscheduler_helloworld.html).
Changes include two pulses, different amplitudes/durations/gap, compile-only
execution, configuration guards, artifact export, cleanup and regression tests.
The tutorial page states copyright 2026 Qblox BV.

The [official notebook download](https://docs.qblox.com/en/main/_downloads/6dc328607393e67724ece25d95802d0e/qbloxscheduler_helloworld.zip)
was inspected on 2026-11-17. Its ZIP contains only
`qbloxscheduler_helloworld.ipynb`; neither notebook cells nor metadata specify a
license. The page also does not specify a reuse license. The Python package
licenses below do **not** establish the license of that separately published
tutorial. Permission or an authoritative documentation-license statement covering
these adaptations remains unresolved. Do not publish the affected files until
this is resolved. No claim is made that the MIT license relicenses these portions.

`docs/architecture.md` is original explanatory prose referencing official docs.
Its Q1ASM excerpt comes from this project's compiler output, with original
annotations; it was not copied from a vendor tutorial. Other project docs,
workflow and tests were authored for this project. No vendor source implementation
was copied. The API/source references were used to understand behavior.

The original contributions are covered by LICENSE. Third-party materials retain
their applicable terms. Transitive dependencies are installed by pip, not vendored;
this notice is not an exhaustive license inventory for redistributing an entire
Python environment.

## qblox-scheduler 1.0.1

Official source: [qblox-scheduler](https://gitlab.com/qblox/packages/software/qblox-scheduler).
Release: [PyPI 1.0.1](https://pypi.org/project/qblox-scheduler/1.0.1/).
Verified installed file: `qblox_scheduler-1.0.1.dist-info/licenses/LICENSES/BSD-3-Clause.txt`.

The package license carries copyright 2026 Qblox. Inspected source headers
also credit Copyright 2020-2025, Quantify Consortium, and Qblox (2020/2025).

Complete shipped license text:

```text
Copyright (c) 2026, Qblox.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```

## qblox-instruments 1.4.1

Official source: [qblox-instruments](https://gitlab.com/qblox/packages/software/qblox_instruments).
Release: [PyPI 1.4.1](https://pypi.org/project/qblox-instruments/1.4.1/).
Verified installed file: `qblox_instruments-1.4.1.dist-info/licenses/LICENSES/BSD-4-Clause.txt`.

Complete shipped license text:

```text
Copyright (c) 2020, Qblox BV
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.
3. All advertising materials mentioning features or use of this software must
   display the following acknowledgement:
   This product includes software developed by Qblox.
4. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY COPYRIGHT HOLDER "AS IS" AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
EVENT SHALL COPYRIGHT HOLDER BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```
