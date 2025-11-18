# demo_cli.py
from library_integrated import Library, Book, DVD, RegularMember, PremiumMember
from database_manager import DatabaseManager

DB_URL = "postgresql+psycopg2://postgres:mypassword@localhost:5432/postgres"

def main():
    print("=" * 70)
    print("LIBRARY MANAGEMENT SYSTEM - DATABASE INTEGRATION DEMO")
    print("=" * 70)

    # Fresh DB
    db = DatabaseManager(DB_URL)
    db.drop_all()
    db.create_all()

    # Create library (Singleton)
    library = Library()

    # Add items
    book1 = Book("Python Crash Course", "Eric Matthes", 2, "978-1593279288", 544)
    book2 = Book("Clean Code", "Robert Martin", 1, "978-0132350884", 464)
    dvd1 = DVD("The Matrix", "Wachowski Brothers", 1, 136, "Sci-Fi")

    library.add_item(book1)
    library.add_item(book2)
    library.add_item(dvd1)

    print(f"\n--- Added Items to Database ---")
    print(f"Total items in library: {len(library)}")

    # Add members
    alice = RegularMember("Alice", "alice@email.com")
    bob = PremiumMember("Bob", "bob@email.com", "2026-12-31")

    library.add_member(alice)
    library.add_member(bob)

    print(f"\n--- Added Members ---")
    print(f"Alice (Regular): Max {alice.get_max_borrow_limit()} items")
    print(f"Bob (Premium): Max {bob.get_max_borrow_limit()} items")

    # Borrowing
    print(f"\n--- Testing Borrow Operations ---")
    ok = library.borrow_item(alice.member_id, book1.id)
    print(f"Alice borrows '{book1.title}': {ok}")
    print(f"Alice's borrowed count: {alice.get_borrowed_count()}")

    # Waiting list
    print(f"\n--- Testing Waiting List ---")
    library.borrow_item(bob.member_id, dvd1.id)  # consume the only copy
    success = library.borrow_item(alice.member_id, dvd1.id)
    print(f"Alice tries to borrow '{dvd1.title}': {success}")

    library.join_waiting_list(alice.member_id, dvd1.id)
    print(f"Alice joined waiting list for '{dvd1.title}'")

    # Return & notify
    print(f"\n--- Testing Return & Notifications ---")
    library.return_item(bob.member_id, dvd1.id)
    print(f"Bob returned '{dvd1.title}'")

    notifications = alice.get_notifications()
    print(f"Alice's notifications: {notifications}")

    print("\n" + "=" * 70)
    print("DEMO COMPLETED!")
    print("=" * 70)


if __name__ == "__main__":
    main()
