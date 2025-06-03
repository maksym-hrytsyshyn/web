
import unittest
from tutor_app.services.group_repository import GroupRepository

class TestGroupIntegration(unittest.TestCase):
    def test_group_student_relation(self):
        group_repo = GroupRepository()
        groups = group_repo.get_all_groups()
        for group in groups:
            self.assertIsNotNone(group.students)

if __name__ == '__main__':
    unittest.main()
