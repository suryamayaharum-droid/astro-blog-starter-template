import datetime, unittest
from core.meaw.harum_coordination_doctor import diagnose
from core.meaw.harum_federation import build_bundle
from core.meaw.portable_crdt import PortableCRDT

class CoordinationDoctorTests(unittest.TestCase):
    def base(self):
        panel={"current_focus":{"project":"HARUM NOIR","next_layer":"visual"},"public_web":{"github_pages":{"url":"g"},"vercel":{"url":"v"}}}
        jev={"checkpoint":{"event_id":"c1"},"last_event":"e1","open_work":[{"work_id":"w1","status":"available"}],"open_help_requests":[{"request_id":"r1","target_role":"visual-curator","created_at":"2026-09-27T20:00:00Z"}]}
        tree={"root":{"id":"HARUM","children":[{"id":"w1","state":"open","target_role":"visual-curator"}]}}
        registry={"roles":[{"role":"visual-curator","capabilities":["mobile-visual-audit"]}]}
        leases={"leases":{}}
        bootstrap={"global_continuity":"docs/GLOBAL_CONTINUITY_INSTRUCTION.md","startup_order":["JEV.md","START_HERE.md","systems/harum_instance_panel.json",".harum-assembly/jev_view.json","systems/harum_project_tree.json","systems/harum_capability_registry.json"]}
        policy={"capacity":{"global_max_active_leases":4,"default_per_role_max_active":1,"per_role_max_active":{}}}
        return panel,jev,tree,registry,leases,bootstrap,policy

    def test_healthy_minimum(self):
        panel,jev,tree,registry,leases,bootstrap,policy=self.base()
        report=diagnose(panel=panel,jev=jev,tree=tree,registry=registry,leases=leases,bootstrap=bootstrap,dispatch_policy=policy,now=datetime.datetime(2026,9,27,20,10,tzinfo=datetime.timezone.utc))
        self.assertEqual(report["status"],"healthy")

    def test_unknown_target_is_attention(self):
        panel,jev,tree,registry,leases,bootstrap,policy=self.base()
        jev["open_help_requests"][0]["target_role"]="missing"
        report=diagnose(panel=panel,jev=jev,tree=tree,registry=registry,leases=leases,bootstrap=bootstrap,dispatch_policy=policy,now=datetime.datetime(2026,9,27,20,10,tzinfo=datetime.timezone.utc))
        self.assertEqual(report["status"],"attention")

    def test_detects_stale_instance_and_unroutable_dispatch(self):
        panel,jev,tree,registry,leases,bootstrap,policy=self.base()
        assembly={"instances":{"peer-old":{"last_seen":"2026-09-27T18:00:00Z"}}}
        dispatch={"summary":{"unroutable":1}}
        report=diagnose(panel=panel,jev=jev,tree=tree,registry=registry,leases=leases,bootstrap=bootstrap,assembly_state=assembly,dispatch_plan=dispatch,dispatch_policy=policy,now=datetime.datetime(2026,9,27,20,10,tzinfo=datetime.timezone.utc),instance_stale_seconds=3600)
        codes={x["code"] for x in report["warnings"]}
        self.assertIn("stale-instance-heartbeat",codes)
        self.assertIn("dispatcher-has-unroutable-work",codes)

    def test_dependency_cycle_is_attention(self):
        panel,jev,tree,registry,leases,bootstrap,policy=self.base()
        tree["root"]["children"]=[
            {"id":"w1","state":"open","target_role":"visual-curator","depends_on":["w2"]},
            {"id":"w2","state":"open","target_role":"visual-curator","depends_on":["w1"]}
        ]
        jev["open_work"].append({"work_id":"w2","status":"available"})
        report=diagnose(panel=panel,jev=jev,tree=tree,registry=registry,leases=leases,bootstrap=bootstrap,dispatch_policy=policy,now=datetime.datetime(2026,9,27,20,10,tzinfo=datetime.timezone.utc))
        self.assertEqual(report["status"],"attention")
        self.assertIn("dependency-cycle",{x["code"] for x in report["issues"]})

    def test_write_scope_collision_is_attention(self):
        panel,jev,tree,registry,leases,bootstrap,policy=self.base()
        tree["root"]["children"].append({"id":"w2","state":"open","target_role":"visual-curator"})
        jev["open_work"].append({"work_id":"w2","status":"claimed","owner":"b"})
        leases["leases"]={
            "w1":{"owner":"a","role":"visual-curator","lease_id":"l1","expires_at":9999999999,"write_scope":["src/app"]},
            "w2":{"owner":"b","role":"visual-curator","lease_id":"l2","expires_at":9999999999,"write_scope":["src/app/home"]}
        }
        report=diagnose(panel=panel,jev=jev,tree=tree,registry=registry,leases=leases,bootstrap=bootstrap,dispatch_policy=policy,now=datetime.datetime(2026,9,27,20,10,tzinfo=datetime.timezone.utc))
        self.assertEqual(report["status"],"attention")
        self.assertIn("active-write-scope-collision",{x["code"] for x in report["issues"]})

    def test_federation_bundle_roundtrip_crdt(self):
        panel,jev,tree,registry,leases,bootstrap,policy=self.base()
        bundle=build_bundle(actor_id="peer-a",canonical_commit="abc",panel=panel,jev=jev,project_tree=tree,capability_registry=registry)
        restored=PortableCRDT.restore(bundle["crdt_state"],"peer-b")
        materialized=restored.materialize()
        self.assertEqual(materialized["registers"]["checkpoint.event_id"],"c1")
        self.assertIn("w1",materialized["sets"]["open_work"])

    def test_duplicate_intent_is_attention(self):
        panel,jev,tree,registry,leases,bootstrap,policy=self.base()
        tree["root"]["children"].append({"id":"w2","state":"open","target_role":"visual-curator","intent_key":"same"})
        tree["root"]["children"][0]["intent_key"]="same"
        jev["open_work"].append({"work_id":"w2","status":"available"})
        report=diagnose(panel=panel,jev=jev,tree=tree,registry=registry,leases=leases,bootstrap=bootstrap,dispatch_policy=policy,now=datetime.datetime(2026,9,27,20,10,tzinfo=datetime.timezone.utc))
        self.assertEqual(report["status"],"attention")
        self.assertIn("duplicate-work-intent",{x["code"] for x in report["issues"]})

    def test_wait_for_cycle_is_attention(self):
        panel,jev,tree,registry,leases,bootstrap,policy=self.base()
        tree["root"]["children"].append({"id":"w2","state":"open","target_role":"visual-curator"})
        jev["open_work"]=[
            {"work_id":"w1","status":"blocked","blocker":"waiting","waits_for":["w2"]},
            {"work_id":"w2","status":"blocked","blocker":"waiting","waits_for":["w1"]}
        ]
        report=diagnose(panel=panel,jev=jev,tree=tree,registry=registry,leases=leases,bootstrap=bootstrap,dispatch_policy=policy,now=datetime.datetime(2026,9,27,20,10,tzinfo=datetime.timezone.utc))
        self.assertEqual(report["status"],"attention")
        self.assertIn("wait-for-cycle",{x["code"] for x in report["issues"]})

    def test_active_work_with_expired_lease_is_recovery_candidate(self):
        panel,jev,tree,registry,leases,bootstrap,policy=self.base()
        jev["open_work"][0].update({"status":"executing","owner":"old-owner"})
        leases["leases"]["w1"]={
            "owner":"old-owner",
            "role":"visual-curator",
            "lease_id":"expired-1",
            "fencing_token":3,
            "expires_at":100,
        }
        report=diagnose(
            panel=panel,jev=jev,tree=tree,registry=registry,leases=leases,
            bootstrap=bootstrap,dispatch_policy=policy,
            now=datetime.datetime.fromtimestamp(101,datetime.timezone.utc)
        )
        codes={x["code"] for x in report["warnings"]}
        self.assertIn("expired-work-lease",codes)
        self.assertIn("orphaned-active-work-expired-lease",codes)
        self.assertEqual(report["recovery_candidates"][0]["work_id"],"w1")
        self.assertEqual(report["recovery_candidates"][0]["fencing_token"],3)


    def test_explicitly_expired_instance_is_dormant_not_stale_warning(self):
        panel,jev,tree,registry,leases,bootstrap,policy=self.base()
        assembly={"instances":{
            "expired-peer":{
                "role":"visual-curator",
                "reachability":"active",
                "last_seen":"2026-09-27T18:00:00Z",
                "expires_at":"2026-09-27T19:00:00Z",
            }
        }}
        report=diagnose(
            panel=panel,jev=jev,tree=tree,registry=registry,leases=leases,
            bootstrap=bootstrap,assembly_state=assembly,dispatch_policy=policy,
            now=datetime.datetime(2026,9,27,20,10,tzinfo=datetime.timezone.utc),
            instance_stale_seconds=3600,
        )
        codes={x["code"] for x in report["warnings"]}
        self.assertNotIn("stale-instance-heartbeat",codes)
        self.assertEqual(report["counts"]["dormant_instances"],1)
        self.assertEqual(report["dormant_instances"][0]["instance"],"expired-peer")
        self.assertEqual(report["dormant_instances"][0]["reason"],"ttl-expired")

    def test_recovery_candidate_drives_next_safe_action(self):
        panel,jev,tree,registry,leases,bootstrap,policy=self.base()
        jev["open_work"][0].update({"status":"executing","owner":"old-owner"})
        leases["leases"]["w1"]={
            "owner":"old-owner",
            "role":"visual-curator",
            "lease_id":"expired-1",
            "fencing_token":4,
            "expires_at":100,
        }
        dispatch={
            "assignments":[{
                "work_id":"w1",
                "state":"unroutable",
                "recovery_candidate":True,
            }],
            "summary":{"unroutable":1},
        }
        report=diagnose(
            panel=panel,jev=jev,tree=tree,registry=registry,leases=leases,
            bootstrap=bootstrap,dispatch_plan=dispatch,dispatch_policy=policy,
            now=datetime.datetime.fromtimestamp(101,datetime.timezone.utc),
        )
        self.assertEqual(
            report["next_safe_action"],
            "recover or close orphaned work before expanding scope",
        )
        repair_actions={x["action"] for x in report["suggested_repairs"]}
        self.assertIn("activate-compatible-instance-for-recovery-or-owner-close",repair_actions)


if __name__=="__main__":
    unittest.main()
