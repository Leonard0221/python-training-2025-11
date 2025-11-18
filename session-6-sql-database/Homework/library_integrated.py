# library_integrated.py
from __future__ import annotations

from typing import List, Optional

from database_manager import DatabaseManager
from models import LibraryItemModel, MemberModel


# -----------------------------
# Item wrappers (keep API)
# -----------------------------
class Book:
    def __init__(self, title: str, author: str, copies: int, isbn: str, num_pages: int):
        self._db = DatabaseManager()
        bm = self._db.add_book(title, author, copies, isbn, num_pages)
        self.id: int = bm.id
        self.title: str = title
        self.author: str = author
        self.isbn: str = isbn
        self.num_pages: int = num_pages

    def get_item_info(self):
        return (
            f"Title: {self.title}\n"
            f"Author: {self.author}\n"
            f"ISBN: {self.isbn}\n"
            f"Pages: {self.num_pages}\n"
            f"Type: {self.get_item_type()}"
        )

    def get_item_type(self):
        return "Book"


class DVD:
    def __init__(self, title: str, director: str, copies: int, duration_minutes: int, genre: str):
        self._db = DatabaseManager()
        dm = self._db.add_dvd(title, director, copies, duration_minutes, genre)
        self.id: int = dm.id
        self.title: str = title
        self.director: str = director
        self.duration_minutes: int = duration_minutes
        self.genre: str = genre

    def get_item_info(self):
        return (
            f"Title: {self.title}\n"
            f"Director: {self.director}\n"
            f"Duration: {self.duration_minutes} minutes\n"
            f"Genre: {self.genre}\n"
            f"Type: {self.get_item_type()}"
        )

    def get_item_type(self):
        return "DVD"


# -----------------------------
# Member wrappers (keep API)
# -----------------------------
class Member:
    def __init__(self, name: str, email: str, member_type: str, borrow_limit: int, membership_expiry: Optional[str] = None):
        self._db = DatabaseManager()
        m = self._db.add_member(name, email, member_type, borrow_limit, expiry=membership_expiry)
        self.member_id: int = m.id
        self.name: str = name
        self.email: str = email

    # --- keep Session-4 signatures/semantics but delegate to DB ---
    def can_borrow(self):
        m = self._db.get_member_by_id(self.member_id)
        return bool(m and m.can_borrow())

    def borrow_item(self, item_id: int):
        return self._db.borrow_item(self.member_id, item_id)

    def return_item(self, item_id: int):
        return self._db.return_item(self.member_id, item_id)

    def get_borrowed_count(self) -> int:
        m = self._db.get_member_by_id(self.member_id)
        return m.get_borrowed_count() if m else 0

    def get_max_borrow_limit(self) -> int:
        m = self._db.get_member_by_id(self.member_id)
        return m.get_borrow_limit() if m else 0

    def update(self, message: str):
        # Observer hook – persist as notification
        self._db.create_notification(self.member_id, message)

    def get_notifications(self) -> List[str]:
        return [n.message for n in self._db.get_member_notifications(self.member_id)]

    def clear_notifications(self):
        notes = self._db.get_member_notifications(self.member_id)
        for n in notes:
            self._db.mark_notification_read(n.id)  # "clearing" == mark as read

    def __str__(self):
        return f"{self.name} ({self.member_id})"


class RegularMember(Member):
    MAX_BORROW_LIMIT: int = 3

    def __init__(self, name, email):
        super().__init__(name, email, member_type="regular", borrow_limit=RegularMember.MAX_BORROW_LIMIT)


class PremiumMember(Member):
    MAX_BORROW_LIMIT: int = 5

    def __init__(self, name, email, membership_expiry=None):
        super().__init__(name, email, member_type="premium",
                         borrow_limit=PremiumMember.MAX_BORROW_LIMIT,
                         membership_expiry=membership_expiry)


# -----------------------------
# Library (Singleton) orchestrator using DB
# -----------------------------
class Library:
    _instance: Optional["Library"] = None

    def __new__(cls) -> "Library":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._db = DatabaseManager()
        return cls._instance

    # keep len(library) behavior
    def __len__(self) -> int:
        return len(self._db.get_all_items())

    # -------- Items & Members management --------
    def add_item(self, item) -> bool:
        # In this integrated design, Book/DVD are persisted in their constructors.
        # Return True to preserve Session-4 semantics ("added to library").
        return True

    def remove_item(self, item_id: int) -> bool:
        # also implicitly clears waitlist via cascade
        return self._db.remove_item(item_id)

    def add_member(self, member: Member) -> bool:
        # Already persisted in constructor; return True for compatibility.
        return True

    def remove_member(self, member_id: int):
        return self._db.remove_member(member_id)

    # -------- Borrowing operations --------
    def borrow_item(self, member_id: int, item_id: int):
        return self._db.borrow_item(member_id, item_id)

    def return_item(self, member_id: int, item_id: int) -> bool:
        return self._db.return_item(member_id, item_id)

    # -------- Searching & Display --------
    def search_items(self, query: str):
        # return a light list of ORM models; your old code iterated and printed,
        # you can still format from these or just count/inspect.
        return self._db.search_items(query)

    def display_all_items(self) -> None:
        items = self._db.get_all_items()
        if not items:
            print("[No items]")
            return
        for it in items:
            print(f"- {it.title} by {it.creator} (ID: {it.id}) | {it.available_copies}/{it.total_copies} available")

    def display_all_members(self) -> None:
        members = self._db.get_all_members()
        if not members:
            print("[No members]")
            return
        for m in members:
            print(f"- {m.name} ({m.id}) | borrowed: {m.get_borrowed_count()}")

    # -------- Waiting list (Observer) --------
    def join_waiting_list(self, member_id: int, item_id: int) -> bool:
        return self._db.join_waiting_list(member_id, item_id)

    def leave_waiting_list(self, member_id: int, item_id: int) -> bool:
        return self._db.leave_waiting_list(member_id, item_id)

    def get_waiting_list(self, item_id: int):
        return self._db.get_waiting_list(item_id)

    def notify_waiting_members(self, item_id: int) -> None:
        # Called when an item returns; creates notifications for earliest waiters.
        self._db.notify_waiting_members(item_id)
