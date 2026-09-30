import json
import tempfile
import unittest
from pathlib import Path

from core.meaw.harum_coord import HarumCoord, CoordinationError

class HarumCoordTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.root=Path(self.tmp.name)
        def w(rel,value):
            p=self.root/rel;p.parent.mkdir(parents=True,exist_ok=True)
            p.write_text(json.dumps(value,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        w(".harum-assembly/state.json",{
            "schema":"harum.assembly-state/v2","version":2,"last_event":None,"assets":{},"incidents":[],
            "instances":{
                "actor-a":{
                    "role":"visual-curator",
                    "roles":["visual-curator"],
                    "last_seen":"2026-09-30T20:00:00+00:00",
                    "expires_at":"2099-01-01T00:00:00+00:00",
                    "capabilities":[],
                    "connectors":[],
                    "skills":[],
                    "reachability":"active",
                    "dispatch_modes":["local-runtime"]
                }
            },"work_items":{"W1":{"work_id":"W1","events":[],"status":"available"}},
            "help_requests":{},"decisions":{},"conflicts":[],"inboxes":{},"idempotency":{},"current_checkpoint":{"event_id":"c1","payload":{"project":"HARUM NOIR"}}
        })
        (self.root/".harum-assembly/events.jsonl").write_text("",encoding="utf-8")
        w(".harum-assembly/jev_view.json",{"schema":"harum.jev-coordination-view/v1","rules":{"custom":"keep-me"}})
        w("systems/harum_project_tree.json",{
            "root":{"id":"HARUM","state":"active","children":[{"id":"W1","title":"Visual audit","state":"open","target_role":"visual-curator","required_capabilities":[],"priority":100,"intent_key":"visual-audit"}]}
        })
        w("systems/harum_capability_registry.json",{"roles":[{"role":"visual-curator","capabilities":[]}]})
        w("state/coordination/work_leases.json",{"schema":"harum.work-leases/v2","default_ttl_seconds":900,"leases":{}})
        w("systems/harum_dispatch_policy.json",{"capacity":{"global_max_active_leases":4,"default_per_role_max_active":2,"per_role_max_active":{},"per_branch_max_active":{}},"collaboration":{"default_max_helpers":2}})
        w("systems/harum_instance_panel.json",{"current_focus":{"project":"HARUM NOIR"},"public_web":{"github_pages":{"url":"g"},"vercel":{"url":"v"}}})
        w("systems/harum_bootstrap_manifest.json",{
            "global_continuity":"docs/GLOBAL_CONTINUITY_INSTRUCTION.md",
            "startup_order":["JEV.md","START_HERE.md","systems/harum_instance_panel.json",".harum-assembly/jev_view.json","systems/harum_project_tree.json","systems/harum_capability_registry.json"]
        })
        w("state/coordination/validation.json",{})
        w("state/coordination/instance_passports.json",{"schema":"harum.instance-passports/v1","passports":[]})
        self.coord=HarumCoord(self.root)

    def tearDown(self):
        self.tmp.cleanup()

    def test_claim_progress_complete_updates_all_layers(self):
        self.coord.sync()
        claimed=self.coord.claim("W1","actor-a","visual-curator",ttl_seconds=300)
        self.assertTrue(claimed["ok"])
        leases=json.loads((self.root/"state/coordination/work_leases.json").read_text())
        self.assertIn("W1",leases["leases"])
        progressed=self.coord.progress("W1","actor-a","visual-curator","checking mobile",ttl_seconds=300)
        self.assertTrue(progressed["ok"])
        completed=self.coord.complete("W1","actor-a","visual-curator","done",["evidence.md"],["commit:1"])
        self.assertTrue(completed["ok"])
        leases=json.loads((self.root/"state/coordination/work_leases.json").read_text())
        self.assertNotIn("W1",leases["leases"])
        tree=json.loads((self.root/"systems/harum_project_tree.json").read_text())
        self.assertEqual(tree["root"]["children"][0]["state"],"succeeded")
        jev=json.loads((self.root/".harum-assembly/jev_view.json").read_text())
        self.assertEqual(jev["rules"]["custom"],"keep-me")
        self.assertFalse(any(x.get("work_id")=="W1" for x in jev["open_work"]))

    def test_second_actor_cannot_take_active_lease(self):
        self.coord.sync()
        self.coord.claim("W1","actor-a","visual-curator",ttl_seconds=300)
        with self.assertRaises(CoordinationError):
            self.coord.claim("W1","actor-b","visual-curator",ttl_seconds=300)

    def test_sync_writes_capability_board(self):
        result=self.coord.sync()
        self.assertIn("capability_board",result)
        board=json.loads((self.root/"state/coordination/capability_board.json").read_text())
        self.assertEqual(board["schema"],"harum.capability-board/v1")

    def test_hello_accepts_sanitized_passport(self):
        self.coord.sync()
        result=self.coord.hello(
            "actor-pass","visual-curator",passport={
                "actor_id":"ignored",
                "roles":["visual-curator"],
                "connectors":[{"id":"github","provider":"GitHub","status":"verified","capabilities":["repo-read"],"token":"SECRET"}],
                "skills":[],
                "reachability":"active","dispatch_modes":["local-runtime"],
            }
        )
        self.assertTrue(result["ok"])
        state=json.loads((self.root/".harum-assembly/state.json").read_text())
        self.assertEqual(state["instances"]["actor-pass"]["connectors"][0]["id"],"github")
        self.assertNotIn("SECRET",str(state["instances"]["actor-pass"]))


    def test_guard_write_blocks_other_owner(self):
        tree=json.loads((self.root/"systems/harum_project_tree.json").read_text())
        tree["root"]["children"][0]["state"]="claimed"
        tree["root"]["children"][0]["owner"]="actor-a"
        tree["root"]["children"][0]["write_scope"]=["astro:src/data/references.ts"]
        (self.root/"systems/harum_project_tree.json").write_text(json.dumps(tree))
        jev={"open_work":[{"work_id":"w1","status":"claimed","owner":"actor-a"}]}
        # Make first node id line up with projected work id.
        tree=json.loads((self.root/"systems/harum_project_tree.json").read_text())
        tree["root"]["children"][0]["id"]="w1"
        (self.root/"systems/harum_project_tree.json").write_text(json.dumps(tree))
        (self.root/".harum-assembly/jev_view.json").write_text(json.dumps(jev))
        result=self.coord.guard_write("actor-b",["astro:src/data/references.ts"])
        self.assertFalse(result["allowed"])
        self.assertEqual(result["mode"],"support-only")

    def test_stale_projection_blocks_next_and_guard_write(self):
        self.coord.sync()
        jev=json.loads((self.root/".harum-assembly/jev_view.json").read_text())
        jev["last_event"]="evt-newer-than-projections"
        (self.root/".harum-assembly/jev_view.json").write_text(json.dumps(jev))

        status=self.coord.status()
        self.assertFalse(status["projection_freshness"]["fresh"])
        self.assertEqual(status["available_work"],[])
        self.assertTrue(status["advice"]["stale"])

        guarded=self.coord.guard_write("actor-a",["chatbot:app/noir/page.tsx"])
        self.assertFalse(guarded["allowed"])
        self.assertEqual(guarded["mode"],"sync-required")
        self.assertEqual(guarded["blockers"][0]["kind"],"stale-coordination-projection")

        with self.assertRaises(CoordinationError):
            self.coord.next_work()

    def test_sync_restores_projection_freshness(self):
        self.coord.sync()
        freshness=self.coord.projection_freshness()
        self.assertTrue(freshness["fresh"])


if __name__=="__main__":
    unittest.main()
