"""Compile two pulses for a dummy QRM-RF; never connect to physical hardware."""

from __future__ import annotations

import argparse
import json
import platform
from importlib.metadata import version
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # Save diagrams without a desktop display (also works in CI).

from matplotlib import pyplot as plt
from qcodes.instrument import Instrument
from qblox_scheduler import ClockResource, CompiledSchedule, HardwareAgent, Schedule
from qblox_scheduler.operations import SquarePulse

ROOT = Path(__file__).resolve().parents[1]


def build_schedule() -> Schedule:
    """Define the experiment in seconds and normalized pulse amplitudes."""
    schedule = Schedule("Stage 1: two square pulses", repetitions=1)
    schedule.add_resource(ClockResource(name="q0.01", freq=5.0e9))
    first = schedule.add(
        SquarePulse(amplitude=0.5, duration=100e-9, port="q0:mw", clock="q0.01"),
        label="first_pulse",
    )
    schedule.add(
        SquarePulse(amplitude=0.25, duration=80e-9, port="q0:mw", clock="q0.01"),
        ref_op=first,
        ref_pt="end",
        rel_time=20e-9,
        label="second_pulse",
    )
    return schedule


def load_dummy_config(path: Path = ROOT / "config" / "dummy_hardware.json") -> dict:
    """Reject physical instruments before the scheduler can create connections."""
    config = json.loads(path.read_text(encoding="utf-8"))
    for description in config["hardware_description"].values():
        if description["instrument_type"] != "Cluster" or description.get("ip") is not None:
            raise ValueError("Stage 1 only accepts dummy Clusters with ip=null.")
    return config


def export_compiled(compiled: CompiledSchedule, output_dir: Path) -> None:
    """Export the actual compiler output for this one-module, one-sequencer example."""
    module = compiled.compiled_instructions["cluster0"]["cluster0_module2"]
    sequencers = module["sequencers"]
    if set(sequencers) != {"seq0"}:
        raise ValueError(f"Expected only seq0, got {list(sequencers)}")
    sequence = sequencers["seq0"].sequence
    program = sequence["program"]
    if not program.strip():
        raise ValueError("The compiler returned an empty Q1ASM program.")

    (output_dir / "cluster0_module2_seq0.q1asm").write_text(program, encoding="utf-8")
    (output_dir / "sequence.json").write_text(
        json.dumps(sequence, indent=2) + "\n", encoding="utf-8"
    )
    compiled.timing_table.data[
        ["port", "clock", "abs_time", "duration", "is_acquisition"]
    ].to_csv(output_dir / "timing.csv", index=False)

    # Includes compiler-added timing; not an oscilloscope trace or RF simulation.
    fig, ax = compiled.plot_pulse_diagram(plot_backend="mpl", modulation="off")
    try:
        fig.set_size_inches(9, 3)
        ax.set_title("Compiled pulse envelope (no hardware measurements)")
        ax.set_ylabel("Normalized amplitude")
        fig.tight_layout()
        fig.savefig(output_dir / "pulse_diagram.png", dpi=150)
    finally:
        plt.close(fig)

    run_info = {
        "mode": "dummy_compile_only",
        "python": platform.python_version(),
        "platform": platform.platform(),
        "packages": {name: version(name) for name in (
            "qblox-scheduler", "qblox-instruments", "matplotlib", "qcodes"
        )},
        "target": "cluster0.module2.seq0",
        "measurements": False,
    }
    (output_dir / "run_info.json").write_text(
        json.dumps(run_info, indent=2) + "\n", encoding="utf-8"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "artifacts" / "stage1")
    args = parser.parse_args()
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    schedule = build_schedule()
    # QCoDeS 0.63.0 registers Clusters and coordinator components independently.
    # Snapshot before construction to cover constructors and partial connections.
    # This standalone script must not run concurrently with instrument creation.
    existing = dict(Instrument._all_instruments)
    if "cluster0" in existing:
        raise RuntimeError("cluster0 already exists; refusing to replace an instrument.")
    failure = None
    try:
        agent = HardwareAgent(
            load_dummy_config(),
            output_dir=output_dir / "scheduler",
            create_dummy_connections=True,
            recreate_instruments=False,
        )
        # Initialization errors must not be downgraded to compilation warnings.
        agent.connect_clusters()
        clusters = agent.get_clusters()
        if not clusters or not all(cluster.is_dummy for cluster in clusters.values()):
            raise RuntimeError("Expected only dummy Clusters.")
        compiled = agent.compile(schedule)
        export_compiled(compiled, output_dir)
    except BaseException as error:
        failure = error
        raise
    finally:
        owned = [resource for name, resource in list(Instrument._all_instruments.items())
                 if existing.get(name) is not resource]
        cleanup_errors = []
        for resource in reversed(owned):
            try:
                resource.close()
            except BaseException as error:
                cleanup_errors.append(error)
        if cleanup_errors:
            if failure is not None:
                for error in cleanup_errors:
                    failure.add_note(f"Cleanup also failed: {type(error).__name__}: {error}")
            else:
                raise BaseExceptionGroup("Instrument cleanup failed", cleanup_errors)

    print("Compiled with a dummy Cluster; no upload, execution or measurements.")
    print("Requested envelope: 100 ns pulse, 20 ns gap, 80 ns pulse.")
    print(f"Artifacts: {output_dir}")


if __name__ == "__main__":
    main()
