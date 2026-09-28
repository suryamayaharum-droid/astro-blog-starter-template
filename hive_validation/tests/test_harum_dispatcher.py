import unittest
from core.meaw.harum_dispatcher import build_dispatch_plan

class HarumDispatcherTests(unittest.TestCase):
    def base(self):
        jev={"open_work":[{"work_id":"w1"},{"work_id":"w2"}]}
        tree={"root":{"id":"HARUM","children":[
          {"id":"w1","state":"open","target_role":"visual-curator","priority":90},
          {"id":"w2","state":"open","required_capabilities":["source-verification"],"priority":100}
        ]}}
        registry={"roles":[
          {"role":"visual-curator","capabilities":["mobile-visual-audit"]},
          {"role":"research-scout","capabilities":["source-verification","reference-enrichment"]}
        ]}
        leases={"leases":{}}
        policy={"capacity":{"global_max_active_leases":4,"default_per_role_max_active":1,"per_role_max_active":{},"per_branch_max_active":{}}}
        return jev,tree,registry,leases,policy

    def test_routes_target_and_capability(self):
        jev,tree,registry,leases,policy=self.base()
        plan=build_dispatch_plan(jev=jev,tree=tree,registry=registry,leases=leases,policy=policy,now=100)
        by={x["work_id"]:x for x in plan["assignments"]}
        self.assertEqual(by["w1"]["candidate_roles"],["visual-curator"])
        self.assertEqual(by["w2"]["candidate_roles"],["research-scout"])
        self.assertEqual(plan["assignments"][0]["work_id"],"w2")

    def test_active_lease_blocks_dispatch(self):
        jev,tree,registry,leases,policy=self.base()
        leases["leases"]["w1"]={"owner":"alpha","role":"visual-curator","lease_id":"l1","expires_at":200}
        plan=build_dispatch_plan(jev=jev,tree=tree,registry=registry,leases=leases,policy=policy,now=100)
        by={x["work_id"]:x for x in plan["assignments"]}
        self.assertEqual(by["w1"]["state"],"leased")
        self.assertEqual(by["w1"]["candidate_roles"],[])

    def test_dependency_blocks_until_done(self):
        jev,tree,registry,leases,policy=self.base()
        tree["root"]["children"][0]["depends_on"]=["w2"]
        plan=build_dispatch_plan(jev=jev,tree=tree,registry=registry,leases=leases,policy=policy,now=100)
        by={x["work_id"]:x for x in plan["assignments"]}
        self.assertEqual(by["w1"]["state"],"blocked")
        self.assertEqual(by["w1"]["reason"],"dependency-not-satisfied")
        tree["root"]["children"][1]["state"]="succeeded"
        plan=build_dispatch_plan(jev=jev,tree=tree,registry=registry,leases=leases,policy=policy,now=100)
        by={x["work_id"]:x for x in plan["assignments"]}
        self.assertEqual(by["w1"]["state"],"available")

    def test_role_capacity_creates_backpressure(self):
        jev,tree,registry,leases,policy=self.base()
        leases["leases"]["other"]={"owner":"peer","role":"visual-curator","lease_id":"l0","expires_at":200}
        plan=build_dispatch_plan(jev=jev,tree=tree,registry=registry,leases=leases,policy=policy,now=100)
        by={x["work_id"]:x for x in plan["assignments"]}
        self.assertEqual(by["w1"]["state"],"waiting-capacity")
        self.assertEqual(by["w1"]["reason"],"role-capacity")

    def test_write_scope_collision_blocks_mutation(self):
        jev,tree,registry,leases,policy=self.base()
        tree["root"]["children"][0]["write_scope"]=["src/site"]
        leases["leases"]["other"]={"owner":"peer","role":"coding-instance","lease_id":"l0","expires_at":200,"write_scope":["src/site/home"]}
        plan=build_dispatch_plan(jev=jev,tree=tree,registry=registry,leases=leases,policy=policy,now=100)
        by={x["work_id"]:x for x in plan["assignments"]}
        self.assertEqual(by["w1"]["state"],"blocked")
        self.assertEqual(by["w1"]["reason"],"write-scope-collision")

    def test_instance_passport_routes_connector_work(self):
        jev,tree,registry,leases,policy=self.base()
        tree["root"]["children"][1]["required_connectors"]=["github"]
        state={"instances":{
          "peer-a":{
            "role":"research-scout","roles":["research-scout"],"last_seen":"2026-09-27T20:00:00+00:00",
            "capabilities":["source-verification"],
            "connectors":[{"id":"github","provider":"GitHub","status":"verified","capabilities":["repo-read"]}],
            "skills":[],"reachability":"active","dispatch_modes":["local-runtime"]
          },
          "peer-b":{
            "role":"research-scout","roles":["research-scout"],"last_seen":"2026-09-27T20:00:00+00:00",
            "capabilities":["source-verification"],"connectors":[],"skills":[],
            "reachability":"manual-resume","dispatch_modes":["jev-resume"]
          }
        }}
        plan=build_dispatch_plan(
            jev=jev,tree=tree,registry=registry,leases=leases,policy=policy,
            instance_state=state,now=1790540000
        )
        by={x["work_id"]:x for x in plan["assignments"]}
        self.assertEqual(by["w2"]["candidate_instances"],["peer-a"])

    def test_old_instance_record_defaults_to_manual_resume(self):
        jev,tree,registry,leases,policy=self.base()
        state={"instances":{"legacy":{
          "role":"visual-curator","last_seen":"2026-09-27T20:00:00+00:00",
          "capabilities":["mobile-visual-audit"],"connectors":[],"skills":[]
        }}}
        plan=build_dispatch_plan(
            jev=jev,tree=tree,registry=registry,leases=leases,policy=policy,
            instance_state=state,now=1790540000
        )
        by={x["work_id"]:x for x in plan["assignments"]}
        self.assertEqual(by["w1"]["candidate_instances"],["legacy"])

    def test_verified_connector_can_be_required(self):
        jev,tree,registry,leases,policy=self.base()
        tree["root"]["children"][1]["required_connectors"]=["github"]
        tree["root"]["children"][1]["require_verified_connectors"]=True
        state={"instances":{"declared-only":{
          "role":"research-scout","roles":["research-scout"],"last_seen":"2026-09-27T20:00:00+00:00",
          "capabilities":["source-verification"],
          "connectors":[{"id":"github","provider":"GitHub","status":"declared","capabilities":["repo-read"]}],
          "skills":[],"reachability":"active","dispatch_modes":["local-runtime"]
        }}}
        plan=build_dispatch_plan(
            jev=jev,tree=tree,registry=registry,leases=leases,policy=policy,
            instance_state=state,now=1790540000
        )
        by={x["work_id"]:x for x in plan["assignments"]}
        self.assertEqual(by["w2"]["state"],"unroutable")


    def test_duplicate_intent_blocks_lower_priority_work(self):
        jev,tree,registry,leases,policy=self.base()
        tree["root"]["children"][0]["intent_key"]="same-intent"
        tree["root"]["children"][1]["intent_key"]="same-intent"
        tree["root"]["children"][0]["priority"]=90
        tree["root"]["children"][1]["priority"]=100
        plan=build_dispatch_plan(jev=jev,tree=tree,registry=registry,leases=leases,policy=policy,now=100)
        by={x["work_id"]:x for x in plan["assignments"]}
        self.assertEqual(by["w1"]["state"],"blocked")
        self.assertEqual(by["w1"]["reason"],"duplicate-work-intent")
        self.assertEqual(by["w1"]["canonical_work_id"],"w2")

    def test_expired_active_lease_becomes_recovery_candidate(self):
        jev,tree,registry,leases,policy=self.base()
        jev["open_work"][0].update({"status":"executing","owner":"old-owner"})
        leases["leases"]["w1"]={
            "owner":"old-owner",
            "role":"visual-curator",
            "lease_id":"expired-1",
            "fencing_token":2,
            "expires_at":90,
        }
        plan=build_dispatch_plan(jev=jev,tree=tree,registry=registry,leases=leases,policy=policy,now=100)
        by={x["work_id"]:x for x in plan["assignments"]}
        self.assertEqual(by["w1"]["state"],"available")
        self.assertTrue(by["w1"]["recovery_candidate"])
        self.assertEqual(by["w1"]["reason"],"expired-lease-recovery")
        self.assertEqual(by["w1"]["recovery"]["previous_owner"],"old-owner")
        self.assertEqual(by["w1"]["recovery"]["previous_fencing_token"],2)
        self.assertEqual(plan["summary"]["active_leases"],0)


if __name__=="__main__":
    unittest.main()
