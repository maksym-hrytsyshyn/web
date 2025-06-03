
import unittest
from tutor_app.services.base_service import BaseService
from tutor_app.repositories.student_repository import StudentRepository

class TestStudentService(unittest.TestCase):
    def setUp(self):
        self.repository = StudentRepository()
        self.service = BaseService(self.repository)

    def test_get_all_students(self):
        result = self.repository.get_all()
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) >= 0)

    def test_add_student(self):
        student = {"name": "John", "age": 15}
        self.repository.add(student)
        self.assertIn(student, self.repository.get_all())

if __name__ == '__main__':
    unittest.main()
