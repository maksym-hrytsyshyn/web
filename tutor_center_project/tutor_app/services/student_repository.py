from .base import BaseRepository
from ..models.student import Student

class StudentRepository(BaseRepository):
    model = Student