import unittest
from scan_watcher import Detector, parse

A, B = '192.0.2.2', '192.0.2.3'
PAIR = ('TCP', 65000)

class Tests(unittest.TestCase):
    def burst(self, d, source, now, count=30):
        return [d.feed(source, PAIR, now) for _ in range(count)]

    def test_29_30_31(self):
        d = Detector()
        self.assertFalse(any(self.burst(d, A, 0, 29)))
        self.assertIsNotNone(d.feed(A, PAIR, 1))
        self.assertIsNone(d.feed(A, PAIR, 2))

    def test_distinct(self):
        d = Detector()
        for p in range(7):
            self.assertIsNone(d.feed(A, ('TCP', p+1), 0))
        self.assertIsNotNone(d.feed(A, ('UDP', 1), 1))

    def test_sources(self):
        d = Detector()
        self.burst(d, A, 0, 29)
        self.assertIsNone(d.feed(B, PAIR, 1))
        self.assertIsNotNone(d.feed(A, PAIR, 2))
        self.assertTrue(any(self.burst(d, B, 3)))

    def test_window_edges(self):
        for age, expected in [(59.999, True), (60, False), (60.001, False)]:
            d = Detector()
            self.burst(d, A, 0, 29)
            self.assertEqual(d.feed(A, PAIR, age) is not None, expected)

    def test_carry_over(self):
        d = Detector()
        self.burst(d, A, 0, 29)
        self.assertIsNone(d.feed(A, PAIR, 60.001))
        self.assertFalse(any(self.burst(d, A, 60.002, 28)))
        self.assertIsNotNone(d.feed(A, PAIR, 60.003))

    def test_cooldown_edges(self):
        for age, expected in [(599.999, False), (600, True), (600.001, True)]:
            d = Detector()
            self.assertTrue(any(self.burst(d, A, 0)))
            self.assertEqual(any(self.burst(d, A, age)), expected)

    def test_suppression_does_not_extend_cooldown(self):
        d = Detector()
        self.burst(d, A, 0)
        self.assertFalse(any(self.burst(d, A, 599)))
        self.assertIsNotNone(d.feed(A, PAIR, 600))

    def test_no_input_no_alert_and_no_stale_threshold(self):
        d = Detector()
        self.burst(d, A, 0)
        self.assertIsNone(d.feed(A, PAIR, 600.001))

    def test_bounded_records(self):
        d = Detector()
        self.burst(d, A, 0, 10000)
        self.assertEqual(len(d.sources[A]['events']), 30)

    def test_parser(self):
        msg = '[UFW BLOCK] IN=eth0 OUT= SRC=192.0.2.2 PROTO=TCP DPT=65000'
        self.assertEqual(parse(msg), (A, PAIR))
        for invalid in [msg.replace('IN=eth0', 'IN='), msg.replace('OUT=', 'OUT=eth1'),
                        msg.replace('UFW BLOCK', 'UFW AUDIT'), msg.replace('TCP', 'ICMP'),
                        msg.replace('65000', 'oops'), msg.replace(A, '0.0.0.0')]:
            self.assertIsNone(parse(invalid))

if __name__ == '__main__':
    unittest.main()
