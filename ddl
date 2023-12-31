CREATE TABLE libraries
(
    library_id SERIAL PRIMARY KEY,
    library_name VARCHAR(25) NOT NULL UNIQUE
);

CREATE TABLE categories
(
    category_id SERIAL PRIMARY KEY,
    category VARCHAR(25)
);

CREATE TABLE authors
(
    author_id SERIAL PRIMARY KEY,
    author VARCHAR(50)
);

CREATE TABLE publishers
(
    publisher_id SERIAL PRIMARY KEY,
    publisher VARCHAR(100)
);

CREATE TABLE books
(
    books_id SERIAL PRIMARY KEY,
    category_id INTEGER NOT NULL,
    title VARCHAR(250) NOT NULL,
    author_id INTEGER NOT NULL,
    publisher_id INTEGER NOT NULL,
    relese_date INTEGER,
    languages VARCHAR(20),
    copies INTEGER NOT NULL CHECK(copies >= 0),
    CONSTRAINT fk_books_category
        FOREIGN KEY (category_id)
        REFERENCES categories(category_id),
    CONSTRAINT fk_books_author
        FOREIGN KEY (author_id)
        REFERENCES authors(author_id),
    CONSTRAINT fk_books_publisher
        FOREIGN KEY (publisher_id)
        REFERENCES publishers(publisher_id)
);

CREATE TABLE library_books
(
    library_books_id SERIAL PRIMARY KEY,
    library_id INTEGER NOT NULL,
    books_id INTEGER NOT NULL,
    title VARCHAR(250) NOT NULL,
    copies INTEGER NOT NULL CHECK(copies >= 0),
    CONSTRAINT fk_library_books_lib
        FOREIGN KEY(library_id)
        REFERENCES libraries(library_id)
        ON DELETE RESTRICT,
    CONSTRAINT fk_library_books_bk
        FOREIGN KEY(books_id)
        REFERENCES books(books_id)
		ON DELETE RESTRICT
);

CREATE TABLE customers
(
    customers_id SERIAL PRIMARY KEY,
    first_name VARCHAR(20) NOT NULL,
    last_name VARCHAR(20) NOT NULL,
    address VARCHAR(100),
    email VARCHAR(35) NOT NULL UNIQUE
);

CREATE TABLE loans
(
    loans_id SERIAL PRIMARY KEY,
    customers_id INTEGER NOT NULL,
    books_id INTEGER NOT NULL,
    loans_time TIMESTAMP NOT NULL DEFAULT NOW(),
    return_time TIMESTAMP,
    is_returned BOOLEAN DEFAULT FALSE,
    CONSTRAINT fk_loans_cust
        FOREIGN KEY(customers_id)
        REFERENCES customers(customers_id),
    CONSTRAINT fk_loans_books
        FOREIGN KEY(books_id)
        REFERENCES books(books_id)
);

CREATE TABLE holds
(
    holds_id SERIAL PRIMARY KEY,
    customers_id INTEGER NOT NULL,
    books_id INTEGER NOT NULL,
    holds_time TIMESTAMP NOT NULL DEFAULT NOW(),
    holds_end TIMESTAMP,
    CONSTRAINT fk_holds_cust
        FOREIGN KEY(customers_id)
        REFERENCES customers(customers_id),
    CONSTRAINT fk_holds_books
        FOREIGN KEY(books_id)
        REFERENCES books(books_id)
);
