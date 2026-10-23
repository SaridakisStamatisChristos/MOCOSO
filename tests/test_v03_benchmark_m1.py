"""Research harness falsification, independent of performance outcomes."""
import copy
import itertools
import json
import subprocess
import unittest
from unittest.mock import patch

from experiments.v03 import benchmark_expanded as bench
from experiments.v03.workloads_expanded import build_cases, canonical_hash, values


class WorkloadContract(unittest.TestCase):
    def test_reproducible_inputs_and_explicit_boundaries(self):
        cases = build_cases('ci')
        self.assertEqual(cases, build_cases('ci'))
        self.assertEqual(len(cases), len({c['case_id'] for c in cases}))
        self.assertEqual(sum(c['cohort'] == 'legacy_original' for c in cases), 8)
        self.assertEqual(sum(c['cohort'] == 'legacy_posthoc' for c in cases), 5)
        for c in cases:
            self.assertEqual(c['input_sha256'], canonical_hash([c['a'], c['m']]))
            self.assertEqual(c['n'], len(c['a']))
            self.assertTrue(all(type(x) is int for x in c['a']))
        boundary = [c for c in cases if c['cohort'] == 'modulus_boundary']
        self.assertTrue(any(2*c['m'] == c['n']*(c['n']+1)//2 for c in boundary))
        self.assertTrue(any(c['h'] < 0 for c in boundary))
        self.assertTrue(any(c['h'] > c['n'] for c in cases))

    def test_seed_order_and_sample_independence(self):
        one, two = build_cases('ci', 101), build_cases('ci', 102)
        self.assertNotEqual(canonical_hash(one), canonical_hash(two))
        self.assertEqual(values(24, 'uniform', 101), values(24, 'uniform', 101))
        self.assertNotEqual(values(24, 'uniform', 101), values(24, 'uniform', 102))
        # Deterministic controls are represented only once in the new cohort.
        controls = [c for c in one if c['cohort'] == 'distribution' and
                    c['family'] == 'convex']
        self.assertEqual(len(controls), 2)

    def test_legacy_inputs_are_exactly_retained(self):
        from experiments.v03.benchmark import case_data
        for c in build_cases('ci'):
            if c['cohort'].startswith('legacy_'):
                self.assertEqual(c['a'], case_data(c['n'], c['family']))

    def test_planned_skips_are_domain_and_size_based(self):
        cases = build_cases('ci')
        for c in cases:
            high = 2*c['m'] > c['n']*(c['n']+1)//2 and c['h'] >= 0
            reason = bench.skip_reason(c, 'deficit')
            self.assertEqual(reason is None, high)
        self.assertTrue(any(bench.skip_reason(c, 'mask_isolated') ==
                            'registered mask cap q>12' for c in cases))


class OracleContract(unittest.TestCase):
    def test_analytic_oracle_against_all_subsets(self):
        for n in range(3, 9):
            a = values(n, 'superconvex', 1)
            for m in range(2, n*(n+1)//2+2):
                self.assertEqual(bench.superconvex_oracle(a, m),
                                 bench.exhaustive_oracle(a, m), (n, m))
        with self.assertRaises(ValueError):
            bench.superconvex_oracle([1, 2, 3], 3)

    def test_all_algorithms_on_signed_tiny_cases(self):
        for a in itertools.product((-1, 0, 1), repeat=4):
            for m in (2, 5, 6, 9, 10, 11):
                case = dict(n=4, m=m, h=10-m)
                expected = bench.exhaustive_oracle(a, m)
                for name in bench.ALGORITHMS:
                    if bench.skip_reason(case, name):
                        continue
                    status, result, _ = bench.call_algorithm(name, a, m)
                    self.assertEqual((status, result), ('OPTIMAL', expected), (a, m, name))

    def test_predicate_rejects_invalid_certificates(self):
        for w in ((0,), (4,), (2, 1), (1, 1), (True,), (1.0,), (1, 2, 3)):
            self.assertFalse(bench.valid_witness([0, 0, 0], 6, w))
        self.assertTrue(bench.valid_witness([0, 1, 4], 6, (1, 2, 3)))


class EvidenceContract(unittest.TestCase):
    def test_deadline_failure_and_bad_json_are_retained(self):
        cfg = dict(algorithm='deficit', a=[1, 3, 9], m=6, repetitions=1)
        with patch.object(bench.subprocess, 'run', side_effect=subprocess.TimeoutExpired('x', 1)):
            self.assertEqual(bench.run_cell(cfg, 1)['status'], 'TIMEOUT')
        for code, output in ((1, ''), (0, '{}'), (0, 'not JSON')):
            proc = subprocess.CompletedProcess([], code, stdout=output, stderr='failure')
            with patch.object(bench.subprocess, 'run', return_value=proc):
                self.assertEqual(bench.run_cell(cfg, 1)['status'], 'ERROR')

    def test_absent_resource_and_separate_timing(self):
        with patch.object(bench, 'resource', None):
            row = bench.worker(dict(algorithm='deficit', a=[1, 3, 9], m=6, repetitions=2))
        self.assertEqual(row['status'], 'OK')
        self.assertEqual(len(row['runtime_ns']), 2)
        self.assertIsNone(row['peak_rss_kib_linux'])
        self.assertEqual(row['witness'], (1, 2, 3))

    def test_mismatch_and_single_algorithm_are_not_certified(self):
        case = dict(case_id='x')
        rows = [dict(case_id='x', status='OK', algorithm='deficit', witness=[1])]
        refs = {'x': dict(kind='cross_algorithm_only', witness=None)}
        bench.verify_rows([case], rows, refs)
        self.assertEqual(rows[0]['status'], 'UNVERIFIED')
        rows = [dict(case_id='x', status='OK', algorithm='deficit', witness=[1]),
                dict(case_id='x', status='OK', algorithm='v02', witness=[2])]
        bench.verify_rows([case], rows, refs)
        self.assertEqual({r['status'] for r in rows}, {'MISMATCH'})
        rows = [dict(case_id='x', status='OK', algorithm='deficit', witness=[1])]
        bench.verify_rows([case], rows, {'x': dict(kind='all_selected_subsets', witness=[2])})
        self.assertEqual(rows[0]['status'], 'MISMATCH')

    def test_summary_keeps_losses_and_incomplete_pairs(self):
        report = dict(complete=True, blocks=2, cases=[dict(case_id='x', cohort='distribution',
                                          family='uniform', n=8, h=7)], rows=[])
        for block in range(2):
            for name, median in (('deficit', 20), ('v02', 10)):
                report['rows'].append(dict(case_id='x', block=block, algorithm=name,
                                          status='OK', verification='independent_oracle', median_ns=median))
        result = bench.summary(report)
        pair = next(p for p in result['pairs'] if p['baseline'] == 'v02')
        self.assertTrue(pair['complete'])
        self.assertEqual(pair['median_ratio'], 0.5)
        group = next(p for p in result['strata'] if p['baseline'] == 'v02')
        self.assertEqual(group['slower'], 1)
        broken = copy.deepcopy(report)
        broken['rows'][-1]['status'] = 'TIMEOUT'
        result = bench.summary(broken)
        group = next(p for p in result['strata'] if p['baseline'] == 'v02')
        self.assertEqual(group['complete_pairs'], 0)
        self.assertEqual(group['planned_cases'], 1)
        report['complete'] = False
        self.assertTrue(all(p['median_ratio'] is None for p in bench.summary(report)['pairs']))

    def test_frozen_source_gate_detects_dirty_solver(self):
        original = bench.ROOT
        from tempfile import TemporaryDirectory
        from pathlib import Path
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            for p in bench.SOURCES + ('experiments/v03/benchmark.py',):
                (root/p).parent.mkdir(parents=True, exist_ok=True)
                (root/p).write_bytes((original/p).read_bytes())
            (root/'modconvex.py').write_text('# tampered\n', encoding='utf-8')
            # Mock only Git's expected bytes; the disk comparison is real.
            with patch.object(bench, 'ROOT', root), patch.object(
                    bench.subprocess, 'check_output',
                    side_effect=lambda *a, **k: (original/'modconvex.py').read_bytes()):
                with self.assertRaisesRegex(ValueError, 'frozen source changed'):
                    bench.provenance()


if __name__ == '__main__':
    unittest.main()
