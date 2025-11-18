CREATE TABLE IF NOT EXISTS library_items(
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    creator VARCHAR(255),
    item_type VARCHAR(20) NOT NULL CHECK (item_type IN ('book', 'dvd')),
    total_copies INTEGER NOT NULL DEFAULT 1 CHECK (total_copies >= 0),
    available_copies INTEGER NOT NULL DEFAULT 1 CHECK (available_copies >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    CHECK (available_copies <= total_copies)
);

CREATE TABLE IF NOT EXISTS books(
    item_id INTEGER PRIMARY KEY REFERENCES library_items(id) on DELETE CASCADE,
    isbn VARCHAR(20) NOT NULL UNIQUE,
    num_pages INTEGER NOT NULL CHECK (num_pages > 0)
);

CREATE TABLE IF NOT EXISTS dvds(
    item_id INTEGER PRIMARY KEY REFERENCES library_items(id) on DELETE CASCADE,
    duration_minutes INTEGER NOT NULL CHECK (duration_minutes > 0),
    genre VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS members(
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    membership_type VARCHAR(20) NOT NULL CHECK (membership_type IN ('regular', 'premium')),
    borrow_limit INTEGER NOT NULL CHECK (borrow_limit > 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS memberships (
  id              SERIAL PRIMARY KEY,
  member_id       INTEGER NOT NULL UNIQUE REFERENCES members(id) ON DELETE CASCADE,
  membership_type VARCHAR(20) NOT NULL CHECK (membership_type IN ('regular','premium')),
  borrow_limit    INTEGER     NOT NULL CHECK (borrow_limit >= 0),
  expiry_date     DATE NULL, 
  created_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS borrowed_items (
  id          SERIAL PRIMARY KEY,
  member_id   INTEGER NOT NULL REFERENCES members(id) ON DELETE CASCADE,
  item_id     INTEGER NOT NULL REFERENCES library_items(id) ON DELETE CASCADE,
  borrow_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  return_date TIMESTAMP NULL,
  status      VARCHAR(20) NOT NULL DEFAULT 'borrowed' CHECK (status IN ('borrowed','returned'))
);

CREATE TABLE IF NOT EXISTS waiting_list (
  id        SERIAL PRIMARY KEY,
  member_id INTEGER NOT NULL REFERENCES members(id) ON DELETE CASCADE,
  item_id   INTEGER NOT NULL REFERENCES library_items(id) ON DELETE CASCADE,
  joined_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(member_id, item_id)
);

CREATE TABLE IF NOT EXISTS notifications (
  id         SERIAL PRIMARY KEY,
  member_id  INTEGER NOT NULL REFERENCES members(id) ON DELETE CASCADE,
  message    TEXT    NOT NULL,
  is_read    BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
