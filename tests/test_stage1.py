"""Integration checks against real compiler output, with no physical hardware."""

import csv
import io
import json
import socket
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch
from qcodes.instrument import Instrument

from examples.dummy_cluster import ROOT, load_dummy_config, main


class Stage1Tests(unittest.TestCase):
    """Compiler regression contract: scheduler 1.0.1 / instruments 1.4.1.

    Exact opcodes, waveform lengths and the 4 ns setup shift are version-specific.
    They must be reviewed on upgrades; they are not hardware timing measurements.
    """
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.temp.cleanup)
        cls.output = Path(cls.temp.name)
        cls.external_attempts = []
        original_connect = socket.socket.connect
        original_connect_ex = socket.socket.connect_ex

        def guard(original):
            def connect(sock, address):
                # Windows asyncio uses loopback sockets for its internal wakeup pipe.
                if not isinstance(address, tuple) or address[0] not in ("127.0.0.1", "::1"):
                    cls.external_attempts.append(address)
                    raise AssertionError(f"External connection attempted: {address}")
                return original(sock, address)
            return connect

        cls.stdout = io.StringIO()
        cls.registry_before = dict(Instrument._all_instruments)
        with (
            patch("sys.argv", ["dummy_cluster.py", "--output-dir", str(cls.output)]),
            patch.object(socket.socket, "connect", guard(original_connect)),
            patch.object(socket.socket, "connect_ex", guard(original_connect_ex)),
            redirect_stdout(cls.stdout),
        ):
            main()
        cls.registry_after = dict(Instrument._all_instruments)
        cls.sequence = json.loads((cls.output / "sequence.json").read_text())
        cls.program = (cls.output / "cluster0_module2_seq0.q1asm").read_text()
        cls.instructions = []
        for line in cls.program.splitlines():
            code = line.split("#", 1)[0].strip()
            if ":" in code:
                code = code.split(":", 1)[1].strip()
            if code:
                cls.instructions.append(code.split())

    def test_compile_without_external_connections(self):
        self.assertEqual(self.external_attempts, [])
        self.assertEqual(self.registry_after, self.registry_before)
        self.assertIn("Compiled with a dummy Cluster", self.stdout.getvalue())

    def test_program_contains_two_pulses_and_terminates(self):
        self.assertTrue(self.program.strip())
        self.assertEqual(self.sequence["program"], self.program)
        opcodes = [instruction[0] for instruction in self.instructions]
        self.assertEqual(opcodes.count("play"), 2)
        self.assertIn("wait_sync", opcodes)
        self.assertEqual(opcodes[-1], "stop")
        self.assertFalse(any(opcode.startswith("acquire") for opcode in opcodes))
        self.assertEqual(self.sequence["acquisitions"], {})

    def test_waveform_references_and_amplitudes(self):
        waveforms = {wave["index"]: wave["data"] for wave in self.sequence["waveforms"].values()}
        plays = [instruction for instruction in self.instructions if instruction[0] == "play"]
        gains = [instruction for instruction in self.instructions if instruction[0] == "set_awg_gain"]
        self.assertEqual(len(gains), 2)
        # The 100 ns pulse is lowered to 96 ns offset plus 4 waveform samples.
        offsets = [instruction for instruction in self.instructions if instruction[0] == "set_awg_offs"]
        self.assertEqual(["".join(item[1:]) for item in offsets], ["16384,0", "0,0"])
        self.assertIn(["upd_param", "96"], self.instructions)
        self.assertEqual([int("".join(play[1:]).split(",")[-1]) for play in plays], [24, 80])
        for play, gain, duration, amplitude in zip(plays, gains, (4, 80), (0.5, 0.25)):
            indices = [int(value) for value in "".join(play[1:]).split(",")[:2]]
            gain_i, gain_q = [int(value) for value in "".join(gain[1:]).split(",")]
            self.assertEqual(len(waveforms[indices[0]]), duration)
            self.assertTrue(all(abs(sample * gain_i / 32768 - amplitude) < 1e-4
                                for sample in waveforms[indices[0]]))
            self.assertTrue(all(abs(sample * gain_q / 32768) < 1e-4
                                for sample in waveforms[indices[1]]))

    def test_resolved_timing_and_artifacts(self):
        with (self.output / "timing.csv").open(newline="") as source:
            rows = list(csv.DictReader(source))
        self.assertTrue(all(row["is_acquisition"] == "False" for row in rows))
        pulses = [row for row in rows if row["port"] == "q0:mw"]
        self.assertEqual(len(pulses), 4)
        # A compiler-added 4 ns phase-update interval shifts experiment timing.
        for row, start, duration in zip(pulses, (4, 100, 100, 124), (0, 0, 4, 80)):
            self.assertAlmostEqual(float(row["abs_time"]) * 1e9, start, delta=1e-6)
            self.assertAlmostEqual(float(row["duration"]) * 1e9, duration, delta=1e-6)
            self.assertEqual(row["clock"], "q0.01")
        self.assertTrue((self.output / "pulse_diagram.png").read_bytes().startswith(b"\x89PNG\r\n\x1a\n"))
        info = json.loads((self.output / "run_info.json").read_text())
        self.assertEqual(info["mode"], "dummy_compile_only")
        self.assertFalse(info["measurements"])

    def test_physical_configuration_is_rejected(self):
        config = json.loads((ROOT / "config" / "dummy_hardware.json").read_text())
        config["hardware_description"]["cluster0"]["ip"] = "192.0.2.1"
        path = self.output / "physical_config.json"
        path.write_text(json.dumps(config))
        with self.assertRaisesRegex(ValueError, "only accepts dummy"):
            load_dummy_config(path)


if __name__ == "__main__":
    unittest.main()
