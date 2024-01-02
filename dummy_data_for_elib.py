#import library
from faker import Faker
import pandas as pd
import random
from datetime import datetime, timedelta

#set localization into Indonesia
fake = Faker('id_ID')

def libraries(library_names):
    """
    create a DataFrame for libraries.

    Parameters:
    - library_names (list): list of library names, it has 3 names.

    Returns:
    - pd.DataFrame: DataFrame containing library information such as library_id and library_name.
    """
    libraries = {
        "library_id": [i + 1 for i in range(len(library_names))],
        "library_name": library_names
    }

    df = pd.DataFrame(libraries)
    return df

library_names = ["Microlibrary", "Grahatama Pustaka", "Pustakalana"]
libraries_df = libraries(library_names)
print(libraries_df)


def categories(category_names):
    """
    create a DataFrame for categories.

    Parameters:
    - category_names (list): list of category names.

    Returns:
    - pd.DataFrame: DataFrame containing category information such as category_id and category_name.
    """
    categories = {
        "category_id": [i + 1 for i in range(len(category_names))],
        "category_name": category_names
    }

    df = pd.DataFrame(categories)
    return df

category_names = ["Mystery", "Thriller", "Science Fiction", "Fantasy", "Romance", "Non-Fiction", "Biography"]
category_df = categories(category_names)
print(category_df)


# read the CSV file and make subset containing the first 3000 rows
books_data = pd.read_csv('books_dataset.csv', sep=";", 
                    error_bad_lines=False, encoding="latin-1");

books_data_subset = books_data.head(3000)
books_data_subset


def publishers(data_subset, column_name):
    """
    create a DataFrame for publishers and make a mapping between publisher_name and publisher_id.

    Parameters:
    - data_subset (pd.DataFrame): subset that containing publisher information.
    - column_name (str): name of the column containing publisher name.

    Returns:
    - pd.DataFrame: DataFrame containing publisher information.
    - dict: Mapping between publisher_name and publisher_id.
    """
    unique_publishers = data_subset['Publisher'].unique()
    n_publishers = len(unique_publishers)

    publishers = {
        "publisher_id": [i + 1 for i in range(n_publishers)],
        "publisher": unique_publishers
    }

    publishers_df = pd.DataFrame(publishers)
    publishers_mapping = dict(zip(publishers_df['publisher'], publishers_df['publisher_id']))

    return publishers_df, publishers_mapping


data_subset = books_data_subset
publishers_df, publishers_mapping = publishers(books_data_subset, 'Publisher')
print(publishers_df)



def authors(data_subset, column_name):
    """
    create a DataFrame for authors and make a mapping between author_name and author_id.

    Parameters:
    - data_subset (pd.DataFrame): Subset of the data containing author information.
    - column_name (str): Name of the column containing author_name.

    Returns:
    - pd.DataFrame: DataFrame containing author information.
    - dict: Mapping between author_name and author_id.
    """
    unique_authors = data_subset[column_name].unique()
    n_authors = len(unique_authors)

    authors = {
        "author_id": [i + 1 for i in range(n_authors)],
        "author": unique_authors
    }

    authors_df = pd.DataFrame(authors)
    author_mapping = dict(zip(authors_df['author'], authors_df['author_id']))

    return authors_df, author_mapping

data_subset = books_data_subset

#create authors DataFrame and Mapping
authors_df, author_mapping = authors(books_data_subset, 'Book-Author')
print(authors_df)


def customers(n_customers):
    """
    create a DataFrame for customers using faker library.

    Parameters:
    - n_customers (int): number of customers.

    Returns:
    - pd.DataFrame: DataFrame containing customer information.
    """
    customers = {
        "customer_id": [i + 1 for i in range(n_customers)],
        "first_name": [],
        "last_name": [],
        "address": [],
        "email": []
    }

    for i in range(n_customers):
        first_name = fake.first_name()
        last_name = fake.last_name()
        address = fake.address()
        email = f"{first_name.lower()}.{last_name.lower()}@xmail.com"

        customers["first_name"].append(first_name)
        customers["last_name"].append(last_name)
        customers["address"].append(address)
        customers["email"].append(email)

    customers_df = pd.DataFrame(customers)
    return customers_df

n_customers = 1000
customers_df = customers(n_customers)
print(customers_df)


def books(n_books, category_df, author_mapping, publishers_mapping, books_data_subset):
    """
    create a DataFrame for books.

    Parameters:
    - n_books (int): number of book.
    - category_df (pd.DataFrame): DataFrame containing category information.
    - author_mapping (dict): mapping between author_name and author_id.
    - publishers_mapping (dict): Mapping between publisher_name and publisher_id.
    - books_data_subset (pd.DataFrame): subset of the data containing book information.

    Returns:
    - pd.DataFrame: DataFrame containing book information.
    """
    books = {
        "book_id": [i + 1 for i in range(n_books)],
        "category_id": [],
        "title": [],
        "author_id": [],
        "publisher_id": [],
        "release_date": [],
        "language": [],
        "copies": []
    }

    for i in range(n_books):
        books["category_id"].append(random.choice(category_df['category_id']))
        books["title"].append(books_data_subset['Book-Title'].iloc[i])
        books["author_id"].append(author_mapping[books_data_subset['Book-Author'].iloc[i]])
        books["publisher_id"].append(publishers_mapping[books_data_subset['Publisher'].iloc[i]])
        books["release_date"].append(books_data_subset['Year-Of-Publication'].iloc[i])
        books["language"].append(random.choices(['Bahasa', 'English'], weights=[0.1, 0.9])[0])
        books["copies"].append(random.randint(1, 3))

    books_df = pd.DataFrame(books)
    return books_df

n_books = len(books_data_subset)
books_df = books(n_books, category_df, author_mapping, publishers_mapping, books_data_subset)
print(books_df)



def library_books(n_library_books, libraries_df, books_df):
    """
    create a DataFrame for library books.

    Parameters:
    - n_library_books (int): number of library books.
    - libraries_df (pd.DataFrame): DataFrame containing library information.
    - books_df (pd.DataFrame): DataFrame containing book information.

    Returns:
    - pd.DataFrame: DataFrame containing library book information.
    """
    library_books = {
        "library_books_id": [i + 1 for i in range(n_library_books)],
        "library_id": [],
        "book_id": [],
        "title": [],
        "copies": []
    }
    
    for i in range(n_library_books):
        library_books["library_id"].append(random.choice(libraries_df['library_id']))
        library_books["book_id"].append(books_df['book_id'].iloc[i])
        library_books["title"].append(books_df['title'].iloc[i])
        library_books["copies"].append(books_df['copies'].iloc[i])

    df = pd.DataFrame(library_books)
    return df

n_library_books = n_books
library_books_df = library_books(n_library_books, libraries_df, books_df)
print(library_books_df)


def loans(n_loans, customers_df, books_df):
    """
    create a DataFrame for loans.

    Parameters:
    - n_loans (int): number of loans.
    - customers_df (pd.DataFrame): DataFrame containing customer information.
    - books_df (pd.DataFrame): DataFrame containing book information.

    Returns:
    - pd.DataFrame: DataFrame containing loan information.
    """
    loans_table = {
        "loan_id": [i + 1 for i in range(n_loans)],
        "customer_id": [random.choice(customers_df["customer_id"]) for i in range(n_loans)],
        "book_id": [random.choice(books_df["book_id"]) for i in range(n_loans)],
        "loan_time": [],
        "return_time": [],
        "is_returned": []
    }

    # create empty list for loan time and return time
    loan_time_data = []
    return_time_data = []

    # count of loans book per customer
    customer_loans_count = {}

    for i in range(n_loans):
        customer_id = loans_table["customer_id"][i]

        # count number of books by customer loans that hasn't been returning
        loans_count = customer_loans_count.get(customer_id, 0)

        # if the customer loans less than 2 books, allow to get another
        if loans_count < 2:
            book_id = random.choice(books_df["book_id"])
            loans_table["book_id"][i] = book_id
            customer_loans_count[customer_id] = loans_count + 1

        # generate loan time
        loan_time = fake.date_time_between(start_date=datetime(2023, 1, 1), end_date=datetime.now())
        loan_time_data.append(loan_time)

        # generate return time
        return_time = (
            None if loan_time is None
            else (loan_time + timedelta(days=random.randint(1, 30))) if (datetime.now() - loan_time).days < 14
            else loan_time + timedelta(days=14)
        )
        return_time_data.append(return_time)

    # is_returned are updated based on return_time
    loans_table["is_returned"] = [return_time is not None and return_time <= datetime.now() for return_time in return_time_data]

    # append to loan_time and return_time columns
    loans_table["loan_time"] = loan_time_data
    loans_table["return_time"] = return_time_data

    # create DataFrame
    loans_df = pd.DataFrame(loans_table)
    return loans_df

n_loans = 10000
loans_df = loans(n_loans, customers_df, books_df)
print(loans_df)


def holds(n_holds, customers_df, library_books_df):
    """
    create a DataFrame for holds.

    Parameters:
    - n_holds (int): number of holds.
    - customers_df (pd.DataFrame): DataFrame containing customer information.
    - library_books_df (pd.DataFrame): DataFrame containing library book information.

    Returns:
    - pd.DataFrame: DataFrame containing hold information.
    """
    holds_table = {
        "holds_id": [i + 1 for i in range(n_holds)],
        "customer_id": [random.choice(customers_df["customer_id"]) for i in range(n_holds)],
        "book_id": [random.choice(library_books_df["book_id"]) for i in range(n_holds)],
        "holds_time": [],
        "holds_end": []
    }

    # create empty lists for hold time and end time
    holds_time_data = []
    holds_end_data = []

    # count of holds book per customer
    customer_holds_count = {}

    for i in range(n_holds):
        customer_id = holds_table["customer_id"][i]

        # count number of books by customer holds that hasn't been returning
        holds_count = customer_holds_count.get(customer_id, 0)

        # if the customer holds less than 2 books, allow to get another
        if holds_count < 2:
            book_id = random.choice(library_books_df["book_id"])
            holds_table["book_id"][i] = book_id
            customer_holds_count[customer_id] = holds_count + 1

        # Generate hold time
        holds_time = fake.date_time_between(start_date=datetime(2023, 1, 1), end_date=datetime.now())
        holds_time_data.append(holds_time)

        # Generate holds end (50% have return time 1 week after hold time)
        if random.random() < 0.5:
            holds_end = holds_time + timedelta(days=7)
        else:
            holds_end = None
        holds_end_data.append(holds_end)

    # Update holds_time and holds_end columns
    holds_table["holds_time"] = holds_time_data
    holds_table["holds_end"] = holds_end_data

    # Create DataFrame
    holds_df = pd.DataFrame(holds_table)
    return holds_df

n_holds = 5000



# Save to CSV
libraries_df.to_csv('libraries.csv', index=False)

# Save to CSV
category_df.to_csv('category.csv', index=False)

# Save to CSV
publishers_df.to_csv('publishers.csv', index=False)

# Save to CSV
authors_df.to_csv('authors.csv', index=False)

# Save to CSV
customers_df.to_csv('customers.csv', index=False)

# Save to CSV
books_df.to_csv('books.csv', index=False)

# Save to CSV
library_books_df.to_csv('library_books.csv', index=False)

# Save to CSV
loans_df.to_csv('loans.csv', index=False)

# Save to CSV
holds_df.to_csv('holds.csv', index=False)


