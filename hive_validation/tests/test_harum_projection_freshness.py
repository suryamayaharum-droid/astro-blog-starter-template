import unittest

from core.meaw.harum_projection_freshness import assess_projection_freshness


class ProjectionFreshnessTests(unittest.TestCase):
    def test_all_matching_watermarks_are_fresh(self):
        projections={
            name:{"source_last_event":"evt-2"}
            for name in ("dispatch","health","meta","capsule","capability_board")
        }
        result=assess_projection_freshness(
            jev={"last_event":"evt-2"},
            projections=projections,
        )
        self.assertTrue(result["fresh"])
        self.assertEqual(result["action"],"continue")
        self.assertEqual(result["stale"],[])
        self.assertEqual(result["missing_watermark"],[])

    def test_stale_and_missing_watermarks_fail_closed(self):
        result=assess_projection_freshness(
            jev={"last_event":"evt-2"},
            projections={
                "dispatch":{"source_last_event":"evt-1"},
                "health":{"source_last_event":"evt-2"},
                "meta":{},
                "capsule":{"source_last_event":"evt-2"},
                "capability_board":{"source_last_event":"evt-2"},
            },
        )
        self.assertFalse(result["fresh"])
        self.assertEqual(result["stale"],["dispatch"])
        self.assertEqual(result["missing_watermark"],["meta"])
        self.assertEqual(result["action"],"run-harum-coord-sync")

    def test_empty_initial_state_can_be_fresh(self):
        result=assess_projection_freshness(
            jev={"last_event":None},
            projections={
                name:{} for name in
                ("dispatch","health","meta","capsule","capability_board")
            },
        )
        self.assertTrue(result["fresh"])


if __name__=="__main__":
    unittest.main()
