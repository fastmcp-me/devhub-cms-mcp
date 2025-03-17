import json
import os
import unittest
from unittest.mock import patch, MagicMock

from devhub_cms_mcp.server import get_hours_of_operation, update_hours, upload_image
from devhub_cms_mcp.server import get_blog_post, create_blog_post, update_blog_post, get_nearest_location


class TestMcpIntegration(unittest.TestCase):
    """Tests for the DevHub CMS MCP integration."""

    def setUp(self):
        """Set up test environment with environment variables."""
        os.environ['DEVHUB_API_KEY'] = 'test_key'
        os.environ['DEVHUB_API_SECRET'] = 'test_secret'
        os.environ['DEVHUB_BASE_URL'] = 'https://devhub.example.com'
        
    @patch('requests_oauthlib.OAuth1Session.get')
    def test_get_hours_of_operation_endpoint(self, mock_get):
        """Test get_hours_of_operation MCP endpoint."""
        # Mock response
        mock_response = MagicMock()
        mock_response.content = json.dumps({
            'hours_by_type': {
                'primary': [
                    [["09:00:00", "17:00:00"]],  # Monday
                    [["09:00:00", "17:00:00"]],  # Tuesday
                    [["09:00:00", "17:00:00"]],  # Wednesday
                    [["09:00:00", "17:00:00"]],  # Thursday
                    [["09:00:00", "17:00:00"]],  # Friday
                    [],  # Saturday (closed)
                    []   # Sunday (closed)
                ]
            }
        }).encode()
        mock_get.return_value = mock_response
        
        # Call function directly
        result = get_hours_of_operation(location_id=123, hours_type='primary')
        
        # Verify response
        self.assertEqual(len(result), 7)  # One entry per day
        self.assertEqual(result[0], [["09:00:00", "17:00:00"]])  # Monday
        
    @patch('requests_oauthlib.OAuth1Session.put')
    def test_update_hours_endpoint(self, mock_put):
        """Test update_hours MCP endpoint."""
        # Mock response
        mock_response = MagicMock()
        mock_response.content = json.dumps({
            'success': True
        }).encode()
        mock_put.return_value = mock_response
        
        # Test data
        new_hours = [
            [["09:00:00", "17:00:00"]],  # Monday
            [["09:00:00", "17:00:00"]],  # Tuesday
            [["09:00:00", "17:00:00"]],  # Wednesday
            [["09:00:00", "17:00:00"]],  # Thursday
            [["09:00:00", "17:00:00"]],  # Friday
            [["10:00:00", "15:00:00"]],  # Saturday
            []                            # Sunday (closed)
        ]
        
        # Call function directly
        result = update_hours(location_id=123, new_hours=new_hours, hours_type="primary")
        
        # Verify response
        self.assertEqual(result, 'Updated successfully')
        
    @patch('requests_oauthlib.OAuth1Session.post')
    def test_upload_image_endpoint(self, mock_post):
        """Test upload_image MCP endpoint."""
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'id': 456,
            'absolute_path': '/media/uploads/image.jpg'
        }
        mock_post.return_value = mock_response
        
        # Call function directly
        result = upload_image(
            base64_image_content='base64encodedcontent',
            filename='test.jpg'
        )
        
        # Verify response
        self.assertIn('Image ID: 456', result)
        self.assertIn('/media/uploads/image.jpg', result)
        
    @patch('requests_oauthlib.OAuth1Session.get')
    def test_get_blog_post_endpoint(self, mock_get):
        """Test get_blog_post MCP endpoint."""
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'id': 789,
            'title': 'Test Blog Post',
            'date': '2025-03-17',
            'content': '<p>This is a test blog post.</p>'
        }
        mock_get.return_value = mock_response
        
        # Call function directly
        result = get_blog_post(post_id=789)
        
        # Verify response
        self.assertIn('Post ID: 789', result)
        self.assertIn('Title: Test Blog Post', result)
        
    @patch('requests_oauthlib.OAuth1Session.post')
    def test_create_blog_post_endpoint(self, mock_post):
        """Test create_blog_post MCP endpoint."""
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'id': 999,
            'title': 'New Test Post',
            'date': '2025-03-17',
            'content': '<p>This is a new test blog post.</p>'
        }
        mock_post.return_value = mock_response
        
        # Call function directly
        result = create_blog_post(
            site_id=42,
            title="New Test Post",
            content="<p>This is a new test blog post.</p>"
        )
        
        # Verify response
        self.assertIn('Post ID: 999', result)
        self.assertIn('Title: New Test Post', result)
        
    @patch('requests_oauthlib.OAuth1Session.put')
    def test_update_blog_post_endpoint(self, mock_put):
        """Test update_blog_post MCP endpoint."""
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'id': 789,
            'title': 'Updated Test Post',
            'date': '2025-03-17',
            'content': '<p>This is an updated test blog post.</p>'
        }
        mock_put.return_value = mock_response
        
        # Call function directly
        result = update_blog_post(
            post_id=789,
            title="Updated Test Post",
            content="<p>This is an updated test blog post.</p>"
        )
        
        # Verify response
        self.assertIn('Post ID: 789', result)
        self.assertIn('Title: Updated Test Post', result)
        
    @patch('requests_oauthlib.OAuth1Session.get')
    def test_get_nearest_location_endpoint(self, mock_get):
        """Test get_nearest_location MCP endpoint."""
        # Mock response
        mock_response = MagicMock()
        mock_response.content = json.dumps({
            'objects': [{
                'id': 123,
                'location_name': 'Test Location',
                'location_url': 'https://example.com/location/123',
                'street': '123 Main St',
                'city': 'Test City',
                'state': 'TS',
                'country': 'Test Country'
            }]
        }).encode()
        mock_get.return_value = mock_response
        
        # Call function directly
        result = get_nearest_location(
            business_id=42,
            latitude=37.7749,
            longitude=-122.4194
        )
        
        # Verify response
        self.assertIn('Location ID: 123', result)
        self.assertIn('Location name: Test Location', result)


if __name__ == '__main__':
    unittest.main()