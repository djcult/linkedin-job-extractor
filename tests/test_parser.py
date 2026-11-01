import unittest
from linkedin_extractor.parser import job_id_from_url


class JobUrlTests(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(job_id_from_url("https://www.linkedin.com/jobs/view/4478287225/"), "4478287225")

    def test_invalid_domain(self):
        with self.assertRaises(ValueError):
            job_id_from_url("https://example.com/jobs/view/4478287225/")

    def test_invalid_path(self):
        with self.assertRaises(ValueError):
            job_id_from_url("https://www.linkedin.com/feed/")


if __name__ == "__main__":
    unittest.main()
