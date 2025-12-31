import unittest
import os
from app import app
from logic import generate_letter

class TestCoverLetterApp(unittest.TestCase):

    # --- PART 1: LOGIC TESTS ---
    
    def test_env_key_loading(self):
        """Check if API Key is present in environment"""
        from dotenv import load_dotenv
        load_dotenv()
        key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        self.assertIsNotNone(key, "API Key is missing from .env file")

    def test_pdf_extraction_exists(self):
        """Check if the logic can handle a missing file gracefully"""
        with self.assertRaises(Exception):
            generate_letter("non_existent_file.pdf", "Job Description")

    # --- PART 2: FLASK WEB TESTS ---

    def setUp(self):
        """Set up a test client for the Flask app"""
        self.app = app.test_client()
        self.app.testing = True

    def test_home_page_loads(self):
        """Check if the homepage returns a 200 OK status"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'AI Cover Letter Architect', response.data)

    def test_generate_route_requires_file(self):
        """Check if the /generate route handles empty submissions"""
        response = self.app.post('/generate', data={
            'job_description': 'Test Job'
        })
        # Should return 400 because 'resume' file is missing
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()