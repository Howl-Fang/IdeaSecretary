import shutil
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import settings
from app.models import OperationCounter


def _ensure_counter(db: Session) -> OperationCounter:
    counter = db.scalar(select(OperationCounter).where(OperationCounter.id == 1))
    if not counter:
        counter = OperationCounter(id=1, count=0)
        db.add(counter)
        db.flush()
    return counter


def tick_operation_and_backup_if_needed(db: Session) -> None:
    counter = _ensure_counter(db)
    counter.count += 1

    if counter.count % settings.backup_every_operations != 0:
        return

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    backup_file = settings.backup_dir / f"backup_{timestamp}.db"
    if settings.sqlite_path.exists():
        shutil.copy2(settings.sqlite_path, backup_file)

    backups = sorted(settings.backup_dir.glob("backup_*.db"), reverse=True)
    for old in backups[settings.backup_keep_latest :]:
        old.unlink(missing_ok=True)
