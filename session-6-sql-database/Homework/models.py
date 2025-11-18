# models.py
from __future__ import annotations

from datetime import datetime, date, timedelta
from typing import List, Optional

from sqlalchemy import (
    CheckConstraint, Column, Integer, String, Boolean, Text, Date, TIMESTAMP,
    ForeignKey, UniqueConstraint, func
)
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


# -----------------------------
# Library Items
# -----------------------------
class LibraryItemModel(Base):
    __tablename__ = "library_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    creator: Mapped[str] = mapped_column(String(255), nullable=False)  # author/director
    item_type: Mapped[str] = mapped_column(String(20), nullable=False)  # 'book' | 'dvd'
    total_copies: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    available_copies: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.current_timestamp())

    __table_args__ = (
        CheckConstraint("item_type in ('book','dvd')", name="ck_item_type"),
        CheckConstraint("total_copies >= 0", name="ck_total_copies_nonneg"),
        CheckConstraint("available_copies >= 0", name="ck_available_copies_nonneg"),
        CheckConstraint("available_copies <= total_copies", name="ck_available_le_total"),
    )

    book: Mapped[Optional["BookModel"]] = relationship(
        back_populates="item", cascade="all, delete-orphan", uselist=False
    )
    dvd: Mapped[Optional["DVDModel"]] = relationship(
        back_populates="item", cascade="all, delete-orphan", uselist=False
    )
    borrows: Mapped[List["BorrowedItemModel"]] = relationship(
        back_populates="item", cascade="all, delete-orphan"
    )
    waiters: Mapped[List["WaitingListModel"]] = relationship(
        back_populates="item", cascade="all, delete-orphan"
    )

    def is_available(self) -> bool:
        return self.available_copies > 0

    def get_active_borrows(self) -> List["BorrowedItemModel"]:
        return [b for b in self.borrows if b.status == "borrowed"]


class BookModel(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(ForeignKey("library_items.id", ondelete="CASCADE"), primary_key=True)
    isbn: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    num_pages: Mapped[int] = mapped_column(Integer, nullable=False)

    item: Mapped[LibraryItemModel] = relationship(back_populates="book", uselist=False)


class DVDModel(Base):
    __tablename__ = "dvds"

    id: Mapped[int] = mapped_column(ForeignKey("library_items.id", ondelete="CASCADE"), primary_key=True)
    duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    genre: Mapped[str] = mapped_column(String(50), nullable=False)

    item: Mapped[LibraryItemModel] = relationship(back_populates="dvd", uselist=False)


# -----------------------------
# Members / Memberships
# -----------------------------
class MemberModel(Base):
    __tablename__ = "members"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    membership_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("memberships.id", ondelete="SET NULL"), nullable=True, unique=True
    )
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.current_timestamp())

    membership: Mapped[Optional["MembershipModel"]] = relationship(
        back_populates="member", uselist=False, foreign_keys=[membership_id]
    )
    borrows: Mapped[List["BorrowedItemModel"]] = relationship(
        back_populates="member", cascade="all, delete-orphan"
    )
    waitlist: Mapped[List["WaitingListModel"]] = relationship(
        back_populates="member", cascade="all, delete-orphan"
    )
    notifications: Mapped[List["NotificationModel"]] = relationship(
        back_populates="member", cascade="all, delete-orphan", order_by="NotificationModel.created_at.desc()"
    )

    def get_borrowed_count(self) -> int:
        return sum(1 for b in self.borrows if b.status == "borrowed")

    def get_borrow_limit(self) -> int:
        return self.membership.borrow_limit if self.membership else 0

    def can_borrow(self) -> bool:
        return self.get_borrowed_count() < self.get_borrow_limit()


class MembershipModel(Base):
    __tablename__ = "memberships"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id", ondelete="CASCADE"), unique=True, nullable=False)
    membership_type: Mapped[str] = mapped_column(String(20), nullable=False)  # 'regular' | 'premium'
    borrow_limit: Mapped[int] = mapped_column(Integer, nullable=False)
    expiry_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.current_timestamp())

    member: Mapped[MemberModel] = relationship(back_populates="membership", uselist=False, foreign_keys=[member_id])

    __table_args__ = (
        CheckConstraint("membership_type in ('regular','premium')", name="ck_membership_type"),
        CheckConstraint(
            "(membership_type = 'regular' AND expiry_date IS NULL) OR "
            "(membership_type = 'premium' AND expiry_date IS NOT NULL)",
            name="ck_premium_expiry_enforced"
        ),
    )

    def is_expired(self) -> bool:
        if self.membership_type == "regular":
            return False
        return self.expiry_date is not None and self.expiry_date < date.today()

    def days_until_expiry(self) -> int:
        if self.membership_type == "regular" or self.expiry_date is None:
            return 10**9
        return (self.expiry_date - date.today()).days

    def renew(self, days: int) -> None:
        if self.membership_type != "premium":
            return
        base = self.expiry_date or date.today()
        self.expiry_date = base + timedelta(days=days)


# -----------------------------
# Borrowing / Waiting / Notifications
# -----------------------------
class BorrowedItemModel(Base):
    __tablename__ = "borrowed_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id", ondelete="CASCADE"), nullable=False)
    item_id: Mapped[int] = mapped_column(ForeignKey("library_items.id", ondelete="CASCADE"), nullable=False)
    borrow_date: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.current_timestamp())
    return_date: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP, nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="borrowed")

    member: Mapped[MemberModel] = relationship(back_populates="borrows")
    item: Mapped[LibraryItemModel] = relationship(back_populates="borrows")

    __table_args__ = (CheckConstraint("status in ('borrowed','returned')", name="ck_borrow_status"),)


class WaitingListModel(Base):
    __tablename__ = "waiting_list"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id", ondelete="CASCADE"), nullable=False)
    item_id: Mapped[int] = mapped_column(ForeignKey("library_items.id", ondelete="CASCADE"), nullable=False)
    joined_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.current_timestamp())

    member: Mapped[MemberModel] = relationship(back_populates="waitlist")
    item: Mapped[LibraryItemModel] = relationship(back_populates="waiters")

    __table_args__ = (UniqueConstraint("member_id", "item_id", name="uq_waiting_member_item"),)


class NotificationModel(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id", ondelete="CASCADE"), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    is_read: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.current_timestamp())

    member: Mapped[MemberModel] = relationship(back_populates="notifications")
