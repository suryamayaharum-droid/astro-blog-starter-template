import unittest
from core.meaw.harum_meta_coordinator import build_meta_plan

class MetaCoordinatorTests(unittest.TestCase):
    def test_healthy_prefers_product_over_support_priority(self):
        dispatch={"assignments":[
          {"work_id":"MEAW-VALIDATE","state":"available","priority":100,"candidate_roles":["coding-instance"],"write_scope":[]},
          {"work_id":"HN-CONTENT","state":"available","priority":90,"candidate_roles":["editorial-director"],"write_scope":[]}
        ]}
        tree={"root":{"id":"HARUM","children":[
          {"id":"HARUM-NOIR","children":[{"id":"HN-CONTENT","state":"open","priority":90}]},
          {"id":"MEAW","children":[{"id":"MEAW-VALIDATE","state":"open","priority":100}]}
        ]}}
        jev={"open_work":[{"work_id":"MEAW-VALIDATE"},{"work_id":"HN-CONTENT"}],"open_help_requests":[]}
        policy={"focus_roots":["HARUM-NOIR"],"support_roots":["MEAW"],"scoring":{"focus_bonus":20,"support_penalty_when_healthy":30,"dependency_unblock_weight":8}}
        plan=build_meta_plan(dispatch=dispatch,tree=tree,health={"status":"healthy"},jev=jev,policy=policy,now=0)
        self.assertEqual(plan["primary_move"]["work_id"],"HN-CONTENT")
        self.assertEqual(plan["mode"],"product-first")
        self.assertTrue(plan["rules"]["never_auto_claim"])

    def test_existing_help_becomes_collaboration(self):
        dispatch={"assignments":[{"work_id":"HN-X","state":"available","priority":50,"candidate_roles":["visual-curator"],"max_helpers":2,"write_scope":[]}]}
        tree={"root":{"id":"HARUM","children":[{"id":"HARUM-NOIR","children":[{"id":"HN-X","state":"open"}]}]}}
        jev={"open_work":[{"work_id":"HN-X"}],"open_help_requests":[{"work_id":"HN-X","target_role":"visual-curator","question":"review mobile"}]}
        plan=build_meta_plan(dispatch=dispatch,tree=tree,health={"status":"healthy"},jev=jev,policy={},now=0)
        self.assertEqual(plan["collaboration_suggestions"][0]["mode"],"existing-help-request")

    def test_recovery_candidate_is_visible_in_primary_move(self):
        dispatch={"assignments":[{
          "work_id":"HN-X","state":"available","priority":90,
          "candidate_roles":["narrative-editor"],"write_scope":[],
          "recovery_candidate":True,"reason":"expired-lease-recovery"
        }]}
        tree={"root":{"id":"HARUM","children":[
          {"id":"HARUM-NOIR","children":[{"id":"HN-X","state":"open","priority":90}]}
        ]}}
        jev={"open_work":[{"work_id":"HN-X","status":"executing","owner":"old-owner"}],"open_help_requests":[]}
        plan=build_meta_plan(dispatch=dispatch,tree=tree,health={"status":"healthy"},jev=jev,policy={},now=0)
        self.assertTrue(plan["primary_move"]["recovery_candidate"])
        self.assertEqual(plan["primary_move"]["dispatch_reason"],"expired-lease-recovery")
        self.assertIn("recovery-candidate",plan["primary_move"]["reason"])

    def test_unroutable_recovery_is_exposed_without_becoming_primary_move(self):
        dispatch={"assignments":[{
          "work_id":"HN-X","state":"unroutable","priority":106,
          "candidate_roles":["narrative-editor"],"candidate_instances":[],
          "write_scope":[],"recovery_candidate":True,
          "reason":"expired-lease-recovery",
          "recovery":{"previous_owner":"old-owner","previous_fencing_token":2}
        }]}
        tree={"root":{"id":"HARUM","children":[
          {"id":"HARUM-NOIR","children":[{"id":"HN-X","state":"open","priority":91}]}
        ]}}
        jev={"open_work":[{"work_id":"HN-X","status":"executing","owner":"old-owner"}],"open_help_requests":[]}
        plan=build_meta_plan(
            dispatch=dispatch,tree=tree,health={"status":"degraded"},
            jev=jev,policy={},now=0
        )
        self.assertIsNone(plan["primary_move"])
        self.assertEqual(plan["primary_recovery"]["work_id"],"HN-X")
        self.assertTrue(plan["primary_recovery"]["recovery_candidate"])
        self.assertEqual(plan["primary_recovery"]["candidate_instances"],[])
        self.assertEqual(plan["primary_recovery"]["recovery"]["previous_owner"],"old-owner")
        self.assertEqual(plan["recovery_queue"][0]["work_id"],"HN-X")
        self.assertEqual(plan["coordination_budget"]["open_product"],1)


if __name__=="__main__":unittest.main()
