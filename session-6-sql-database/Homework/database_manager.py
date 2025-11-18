# database_manager.py
from __future__ import annotations

from contextlib import contextmanager
from datetime import datetime, timedelta, date
from typing import Generator, List, Optional

from sqlalchemy import create_engine, select, or_, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, sessionmaker

from models import (
    Base,
    LibraryItemModel, BookModel, DVDModel,
    MemberModel, MembershipModel,
    BorrowedItemModel, WaitingListModel, NotificationModel
)


class DatabaseManager:
    """Singleton DB manager with context-managed sessions and full CRUD."""
    _instance: Optional["DatabaseManager"] = None

    def __new__(cls, url: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/librarydb"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init(url)
        return cls._instance

    def _init(self, url: str):
        self.engine = create_engine(url, echo=False, future=True)
        self.SessionLocal = sessionmaker(bind=self.engine, autoflush=False, autocommit=False, expire_on_commit=False)

    @contextmanager
    def session_scope(self) -> Generator[Session, None, None]:
        s = self.SessionLocal()
        try:
            yield s
            s.commit()
        except Exception:
            s.rollback()
            raise
        finally:
            s.close()

    # ---------- schema ----------
    def drop_all(self) -> None:
        Base.metadata.drop_all(self.engine)

    def create_all(self) -> None:
        Base.metadata.create_all(self.engine)

    # ---------- items ----------
    def add_book(self, title: str, author: str, copies: int, isbn: str, num_pages: int) -> BookModel:
        with self.session_scope() as s:
            item = LibraryItemModel(title=title, creator=author, item_type="book",
                                    total_copies=copies, available_copies=copies)
            s.add(item); s.flush()
            book = BookModel(id=item.id, isbn=isbn, num_pages=num_pages)
            s.add(book)
            return book

    def add_dvd(self, title: str, director: str, copies: int, duration: int, genre: str) -> DVDModel:
        with self.session_scope() as s:
            item = LibraryItemModel(title=title, creator=director, item_type="dvd",
                                    total_copies=copies, available_copies=copies)
            s.add(item); s.flush()
            dvd = DVDModel(id=item.id, duration_minutes=duration, genre=genre)
            s.add(dvd)
            return dvd

    def remove_item(self, item_id: int) -> bool:
        with self.session_scope() as s:
            obj = s.get(LibraryItemModel, item_id)
            if not obj:
                return False
            s.delete(obj)
            return True

    def get_item_by_id(self, item_id: int) -> Optional[LibraryItemModel]:
        with self.session_scope() as s:
            return s.get(LibraryItemModel, item_id)

    def search_items(self, query: str) -> List[LibraryItemModel]:
        with self.session_scope() as s:
            stmt = select(LibraryItemModel).where(
                or_(
                    LibraryItemModel.title.ilike(f"%{query}%"),
                    LibraryItemModel.creator.ilike(f"%{query}%")
                )
            ).order_by(LibraryItemModel.title.asc())
            return list(s.scalars(stmt).all())

    def get_all_items(self) -> List[LibraryItemModel]:
        with self.session_scope() as s:
            return list(s.scalars(select(LibraryItemModel)).all())

    # ---------- members ----------
    def add_member(self, name: str, email: str, member_type: str, borrow_limit: int, expiry: Optional[str] = None) -> MemberModel:
        with self.session_scope() as s:
            m = MemberModel(name=name, email=email)
            s.add(m); s.flush()

            expiry_date = None
            if member_type == "premium":
                if not expiry:
                    raise ValueError("Premium membership requires an expiry date (YYYY-MM-DD).")
                expiry_date = date.fromisoformat(expiry)

            ms = MembershipModel(member_id=m.id, membership_type=member_type,
                                 borrow_limit=borrow_limit, expiry_date=expiry_date)
            s.add(ms); s.flush()
            m.membership_id = ms.id
            s.add(m)
            return m

    def remove_member(self, member_id: int) -> bool:
        with self.session_scope() as s:
            m = s.get(MemberModel, member_id)
            if not m:
                return False
            s.delete(m)
            return True

    def get_member_by_id(self, member_id: int) -> Optional[MemberModel]:
        with self.session_scope() as s:
            return s.get(MemberModel, member_id)

    def get_all_members(self) -> List[MemberModel]:
        with self.session_scope() as s:
            return list(s.scalars(select(MemberModel)).all())

    # ---------- memberships ----------
    def create_membership(self, member_id: int, membership_type: str, borrow_limit: int, expiry: Optional[str] = None) -> MembershipModel:
        with self.session_scope() as s:
            m = s.get(MemberModel, member_id)
            if not m:
                raise ValueError("Member not found")
            if m.membership_id:
                raise ValueError("Member already has a membership")

            expiry_date = None
            if membership_type == "premium":
                if not expiry:
                    raise ValueError("Premium membership requires an expiry date")
                expiry_date = date.fromisoformat(expiry)

            ms = MembershipModel(member_id=member_id, membership_type=membership_type,
                                 borrow_limit=borrow_limit, expiry_date=expiry_date)
            s.add(ms); s.flush()
            m.membership_id = ms.id
            s.add(m)
            return ms

    def update_membership(self, member_id: int, membership_type: Optional[str] = None,
                          borrow_limit: Optional[int] = None, expiry: Optional[str] = None) -> bool:
        with self.session_scope() as s:
            m = s.get(MemberModel, member_id)
            if not m or not m.membership_id:
                return False
            ms = s.get(MembershipModel, m.membership_id)
            if not ms:
                return False
            if membership_type is not None:
                ms.membership_type = membership_type
            if borrow_limit is not None:
                ms.borrow_limit = borrow_limit
            if expiry is not None:
                ms.expiry_date = date.fromisoformat(expiry)
            s.add(ms)
            return True

    def renew_membership(self, member_id: int, days: int) -> bool:
        with self.session_scope() as s:
            m = s.get(MemberModel, member_id)
            if not m or not m.membership_id:
                return False
            ms = s.get(MembershipModel, m.membership_id)
            if not ms or ms.membership_type != "premium":
                return False
            base = ms.expiry_date or date.today()
            ms.expiry_date = base + timedelta(days=days)
            s.add(ms)
            return True

    def get_membership(self, member_id: int) -> Optional[MembershipModel]:
        with self.session_scope() as s:
            return s.scalars(select(MembershipModel).where(MembershipModel.member_id == member_id)).first()

    def check_membership_expiry(self, member_id: int) -> bool:
        with self.session_scope() as s:
            ms = s.scalars(select(MembershipModel).where(MembershipModel.member_id == member_id)).first()
            if not ms:
                return True
            if ms.membership_type == "regular":
                return False
            return ms.expiry_date is not None and ms.expiry_date < date.today()

    # ---------- borrowing ----------
    def borrow_item(self, member_id: int, item_id: int) -> bool:
        with self.session_scope() as s:
            m = s.get(MemberModel, member_id)
            it = s.get(LibraryItemModel, item_id)
            if not m or not it:
                return False

            ms = s.scalars(select(MembershipModel).where(MembershipModel.member_id == m.id)).first()
            if not ms:
                return False
            if ms.membership_type == "premium" and (ms.expiry_date is None or ms.expiry_date < date.today()):
                return False

            active = s.scalar(
                select(func.count(BorrowedItemModel.id)).where(
                    BorrowedItemModel.member_id == m.id,
                    BorrowedItemModel.status == "borrowed"
                )
            ) or 0
            if active >= ms.borrow_limit:
                return False

            if it.available_copies <= 0:
                return False

            s.add(BorrowedItemModel(member_id=m.id, item_id=it.id, status="borrowed"))
            it.available_copies -= 1
            s.add(it)
            return True

    def return_item(self, member_id: int, item_id: int) -> bool:
        with self.session_scope() as s:
            br = s.scalars(
                select(BorrowedItemModel).where(
                    BorrowedItemModel.member_id == member_id,
                    BorrowedItemModel.item_id == item_id,
                    BorrowedItemModel.status == "borrowed"
                ).limit(1)
            ).first()
            if not br:
                return False

            br.status = "returned"
            br.return_date = datetime.utcnow()
            it = s.get(LibraryItemModel, item_id)
            if it:
                it.available_copies += 1
                s.add(it)
                self._notify_waiting_members_session(s, item_id)

            s.add(br)
            return True

    def get_member_borrowed_items(self, member_id: int) -> List[LibraryItemModel]:
        with self.session_scope() as s:
            stmt = (
                select(LibraryItemModel)
                .join(BorrowedItemModel, BorrowedItemModel.item_id == LibraryItemModel.id)
                .where(BorrowedItemModel.member_id == member_id, BorrowedItemModel.status == "borrowed")
            )
            return list(s.scalars(stmt).all())

    def get_item_borrow_history(self, item_id: int) -> List[BorrowedItemModel]:
        with self.session_scope() as s:
            stmt = select(BorrowedItemModel).where(BorrowedItemModel.item_id == item_id).order_by(
                BorrowedItemModel.borrow_date.desc()
            )
            return list(s.scalars(stmt).all())

    # ---------- waiting list ----------
    def join_waiting_list(self, member_id: int, item_id: int) -> bool:
        with self.session_scope() as s:
            it = s.get(LibraryItemModel, item_id)
            if not it:
                return False
            if it.available_copies > 0:
                return False
            try:
                s.add(WaitingListModel(member_id=member_id, item_id=item_id))
                return True
            except IntegrityError:
                return False

    def leave_waiting_list(self, member_id: int, item_id: int) -> bool:
        with self.session_scope() as s:
            wl = s.scalars(
                select(WaitingListModel).where(
                    WaitingListModel.member_id == member_id,
                    WaitingListModel.item_id == item_id
                )
            ).first()
            if not wl:
                return False
            s.delete(wl)
            return True

    def get_waiting_list(self, item_id: int) -> List[MemberModel]:
        with self.session_scope() as s:
            stmt = (
                select(MemberModel)
                .join(WaitingListModel, WaitingListModel.member_id == MemberModel.id)
                .where(WaitingListModel.item_id == item_id)
                .order_by(WaitingListModel.joined_at.asc())
            )
            return list(s.scalars(stmt).all())

    def notify_waiting_members(self, item_id: int) -> None:
        with self.session_scope() as s:
            self._notify_waiting_members_session(s, item_id)

    def _notify_waiting_members_session(self, s: Session, item_id: int) -> None:
        it = s.get(LibraryItemModel, item_id)
        if not it or it.available_copies <= 0:
            return
        queue = list(s.scalars(
            select(WaitingListModel)
            .where(WaitingListModel.item_id == item_id)
            .order_by(WaitingListModel.joined_at.asc())
            .limit(it.available_copies)
        ).all())
        if not queue:
            return
        for entry in queue:
            s.add(NotificationModel(member_id=entry.member_id, message=f"'{it.title}' is now available!"))
            s.delete(entry)

    # ---------- notifications ----------
    def create_notification(self, member_id: int, message: str) -> NotificationModel:
        with self.session_scope() as s:
            note = NotificationModel(member_id=member_id, message=message, is_read=False)
            s.add(note); s.flush()
            return note

    def get_member_notifications(self, member_id: int, unread_only: bool = False) -> List[NotificationModel]:
        with self.session_scope() as s:
            stmt = select(NotificationModel).where(NotificationModel.member_id == member_id)
            if unread_only:
                stmt = stmt.where(NotificationModel.is_read == False)  # noqa
            stmt = stmt.order_by(NotificationModel.created_at.desc())
            return list(s.scalars(stmt).all())

    def mark_notification_read(self, notification_id: int) -> bool:
        with self.session_scope() as s:
            note = s.get(NotificationModel, notification_id)
            if not note:
                return False
            note.is_read = True
            s.add(note)
            return True
