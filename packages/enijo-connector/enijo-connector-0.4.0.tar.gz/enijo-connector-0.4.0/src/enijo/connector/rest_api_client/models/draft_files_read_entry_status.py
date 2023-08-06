from enum import Enum


class DraftFilesReadEntryStatus(str, Enum):
    COMPLETED = "completed"
    PENDING = "pending"

    def __str__(self) -> str:
        return str(self.value)
