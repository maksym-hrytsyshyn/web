from .base import BaseRepository
from ..models.attendance import Attendance

class AttendanceRepository(BaseRepository):
    model = Attendance