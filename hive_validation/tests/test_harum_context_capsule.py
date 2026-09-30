import unittest
from core.meaw.harum_context_capsule import build_capsule

class ContextCapsuleTests(unittest.TestCase):
    def test_capsule_is_small_and_actionable(self):
        panel={"current_focus":{"project":"HARUM NOIR","internal_name":"Harumverso","rule":"focus","next_layer":"visual"},"public_web":{"github_pages":{"url":"g"},"vercel":{"url":"v"},"atlas":{"artists":50}}}
        jev={"last_event":"evt-capsule","checkpoint":{"event_id":"c1"},"open_help_requests":[{"request_id":"h1","work_id":"w1","target_role":"research-scout","question":"verify"}]}
        dispatch={"assignments":[
          {"work_id":"w2","state":"available","priority":90,"candidate_roles":["visual-curator"],"reason":"explicit-target-role"},
          {"work_id":"w1","state":"available","priority":100,"candidate_roles":["research-scout"],"reason":"explicit-target-role"},
          {"work_id":"w3","state":"blocked","priority":120}
        ],"summary":{"available":2,"blocked":1}}
        health={"status":"healthy","counts":{"issues":0,"warnings":0},"next_safe_action":"claim"}
        validation={"components":{"x":{"validation_state":"passed"}}}
        meta={
            "mode":"repair-first",
            "primary_move":None,
            "primary_recovery":{"work_id":"w-recover","state":"unroutable","recovery_candidate":True},
            "recovery_queue":[{"work_id":"w-recover","state":"unroutable","recovery_candidate":True}],
            "parallel_wave":[],
            "coordination_budget":{"open_product":1},
        }
        value=build_capsule(panel=panel,jev=jev,dispatch=dispatch,health=health,validation=validation,meta=meta)
        self.assertEqual(value["available_work"][0]["work_id"],"w1")
        self.assertEqual(value["meta_advice"]["primary_recovery"]["work_id"],"w-recover")
        self.assertEqual(value["meta_advice"]["recovery_queue"][0]["work_id"],"w-recover")
        self.assertEqual(value["health"]["status"],"healthy")
        self.assertTrue(value["content_sha256"])
        self.assertTrue(value["rules"]["canonical_files_override_capsule"])
        self.assertEqual(value["source_last_event"],"evt-capsule")

if __name__=="__main__":
    unittest.main()
