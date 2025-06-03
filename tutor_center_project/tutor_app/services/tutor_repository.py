from .base import BaseRepository
from ..models.tutor import Tutor

class TutorRepository(BaseRepository):
    model = Tutor