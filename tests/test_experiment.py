"""Experiment intent, independent of the compiler's chosen Q1ASM lowering."""

import unittest
from examples.dummy_cluster import build_schedule


class ExperimentTests(unittest.TestCase):
    def test_two_pulses_have_requested_parameters_and_gap(self):
        schedule = build_schedule()
        self.assertEqual(len(schedule.schedulables), 2)
        for label, amplitude, duration in (
            ('first_pulse', 0.5, 100e-9), ('second_pulse', 0.25, 80e-9)
        ):
            item = schedule.schedulables[label]
            operation = schedule.operations[item['operation_id']]
            pulse = operation.data['pulse_info']
            self.assertEqual(pulse['amplitude'], amplitude)
            self.assertAlmostEqual(pulse['duration'], duration, delta=1e-15)
            self.assertEqual((pulse['port'], pulse['clock']), ('q0:mw', 'q0.01'))
            self.assertFalse(operation.data['acquisition_info'])
        timing = schedule.schedulables['second_pulse']['timing_constraints'][0]
        self.assertEqual(timing.ref_schedulable, 'first_pulse')
        self.assertEqual(timing.ref_pt, 'end')
        self.assertAlmostEqual(timing.rel_time, 20e-9, delta=1e-15)
