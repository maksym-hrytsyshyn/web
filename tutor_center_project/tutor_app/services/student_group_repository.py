from .base import BaseRepository
from ..models.student_group import StudentGroup

class StudentGroupRepository(BaseRepository):
    model = StudentGroup