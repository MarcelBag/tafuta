import unittest
from app import app

class TestLocationServices(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_store_location(self):
        """Test storing a location."""
        response = self.app.post('/api/store-location', json={
            "phone_number": "+243994855684",
            "latitude": -1.67409,
            "longitude": 29.22845
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("success", response.get_json()["status"])

    def test_send_tracking_link(self):
        """Test sending a tracking link."""
        response = self.app.post('/api/send-tracking-link', json={
            "phone_number": "+243994855684"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("success", response.get_json()["status"])

    def test_track_link_metadata(self):
        """Test capturing metadata when a tracking link is opened."""
        response = self.app.get('/track-link/test-unique-id')
        self.assertEqual(response.status_code, 200)
        self.assertIn("success", response.get_json()["status"])

if __name__ == '__main__':
    unittest.main()
