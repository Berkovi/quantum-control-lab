"""Lifecycle failures, using in-memory QCoDeS instruments only."""

import tempfile
import unittest
from unittest.mock import Mock, patch

from qcodes.instrument import Instrument
from examples.dummy_cluster import main


class CleanupTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.argv = patch('sys.argv', ['example', '--output-dir', self.temp.name])
        self.argv.start()
        self.addCleanup(self.argv.stop)
        self.owned = []
        self.closers = []
        self.addCleanup(self.release_test_resources)

    def resource(self, name, fail=False):
        resource = Instrument(name)
        close = resource.close
        resource.close = Mock(side_effect=RuntimeError('close failed') if fail else close)
        self.closers.append(resource.close)
        self.owned.append((resource, close))
        return resource

    def release_test_resources(self):
        for _, close in self.owned:
            close()

    def test_constructor_failure_closes_registered_resources(self):
        failure = RuntimeError('constructor failed')

        def construct(*args, **kwargs):
            self.resource('partial_coordinator')
            raise failure

        with patch('examples.dummy_cluster.HardwareAgent', side_effect=construct):
            with self.assertRaises(RuntimeError) as caught:
                main()
        self.assertIs(caught.exception, failure)
        self.closers[0].assert_called_once()

    def test_partial_connection_failure_preserves_original_and_attempts_all_closes(self):
        existing = self.resource('preexisting')
        failure = ValueError('connection failed')
        agent = Mock()

        def connect():
            self.resource('first_dummy')
            self.resource('second_dummy', fail=True)
            raise failure

        agent.connect_clusters.side_effect = connect
        with patch('examples.dummy_cluster.HardwareAgent', return_value=agent):
            with self.assertRaises(ValueError) as caught:
                main()
        self.assertIs(caught.exception, failure)
        self.assertIn('close failed', '\n'.join(failure.__notes__))
        self.closers[0].assert_not_called()
        for close in self.closers[1:]:
            close.assert_called_once()
        agent.get_clusters.assert_not_called()

    def test_successful_body_reports_cleanup_failures_after_all_attempts(self):
        agent = Mock()

        def connect():
            self.resource('first_dummy', fail=True)
            self.resource('second_dummy', fail=True)

        agent.connect_clusters.side_effect = connect
        agent.get_clusters.return_value = {'cluster0': Mock(is_dummy=True)}
        with (patch('examples.dummy_cluster.HardwareAgent', return_value=agent),
              patch('examples.dummy_cluster.export_compiled')):
            with self.assertRaises(ExceptionGroup) as caught:
                main()
        self.assertEqual(len(caught.exception.exceptions), 2)
        for close in self.closers:
            close.assert_called_once()

    def test_existing_cluster_is_not_replaced_or_closed(self):
        existing = self.resource('cluster0')
        with patch('examples.dummy_cluster.HardwareAgent') as factory:
            with self.assertRaisesRegex(RuntimeError, 'already exists'):
                main()
        factory.assert_not_called()
        self.closers[0].assert_not_called()
