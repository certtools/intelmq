from intelmq.lib.test import TestPipeline

import unittest

class TestTestPipeline(unittest.TestCase):

    def test_source_pipeline_behaviour(self):
        """Tests if a TestPipeline behaves 
            like a source Pipeline should"""

        state = {"my-queue": ["A", "B", "C"]}
        src = TestPipeline(state)

        src.set_source_queues("my-queue")

        self.assertEqual(src.receive(), "A")
        self.assertEqual(src.state, state)

        self.assertIn("my-queue", state)
        self.assertIn("my-queue-internal", state)
        self.assertListEqual(["B", "C"], state["my-queue"])
        self.assertListEqual(["A"], state["my-queue-internal"])

        self.assertEqual("A", src.acknowledge())
        self.assertListEqual([], state["my-queue-internal"])

    def test_destination_pipeline_behaviour(self):
        """Tests if the basic 1:N sending capability of a normal pipeline
            works also for a TestPipeline"""
        dst = TestPipeline({})
        
        dst.set_destination_queues(["tiger", "cat", "cow"])
        dst.send("sandwhich")
        dst.send("gras")
        dst.send("meat")
        
        self.assertListEqual(["sandwhich", "gras", "meat"], dst.state["tiger"])
        self.assertListEqual(["sandwhich", "gras", "meat"], dst.state["cat"])
        self.assertListEqual(["sandwhich", "gras", "meat"], dst.state["cow"])

        counted = dst.count_queued_messages(["tiger", "cat", "cow", "foo"])
        self.assertDictEqual({"tiger": 3, "cat": 3, "cow": 3, "foo": 0},
                             counted)

if __name__ == "__main__":
    unittest.main()
