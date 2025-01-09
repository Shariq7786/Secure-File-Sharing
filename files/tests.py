from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import File
from django.core.files.uploadedfile import SimpleUploadedFile
import os
import time

class FileTestCase(TestCase):
    def setUp(self):
        # Set up a test client and a test user
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        # Create a test file
        self.test_file_content = b"Test file content"
        self.test_file = SimpleUploadedFile("testfile.txt", self.test_file_content, content_type="text/plain")

    def test_file_upload(self):
        # Test file upload functionality
        response = self.client.post(reverse('file_upload'), {'file': self.test_file})
        self.assertEqual(response.status_code, 302)  # Assuming a redirect occurs after upload
        self.assertEqual(File.objects.count(), 1)  # Check if the file is saved

    def test_file_list(self):
        # Test file list functionality
        self.client.post(reverse('file_upload'), {'file': self.test_file})
        response = self.client.get(reverse('file_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn("testfile.txt", response.content.decode())  # Check if the file appears in the list

    def test_file_download(self):
        # Test file download functionality
        self.client.post(reverse('file_upload'), {'file': self.test_file})
        uploaded_file = File.objects.first()
        response = self.client.get(reverse('file_download', args=[uploaded_file.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, self.test_file_content)  # Check if the downloaded content is correct

    def tearDown(self):
        # Ensure consistent indentation here
        self.files_to_delete = []
        for file in File.objects.all():
            file_path = file.uploaded_file.path
            if os.path.exists(file_path):
                self.files_to_delete.append(file_path)
        time.sleep(1)  # Delay to allow file system to release any locks
        for file in File.objects.all():
            file_path = file.uploaded_file.path
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except PermissionError:
                    print(f"Could not delete file at {file_path}. It may be locked.")