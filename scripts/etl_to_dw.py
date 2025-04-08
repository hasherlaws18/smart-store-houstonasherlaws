import pandas as pd
import sqlite3
import pathlib
import sys

# For local imports, temporarily add project root to sys.path
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# Constants
DW_DIR = pathlib.Path("data").joinpath("dw")
DB_PATH = DW_DIR.joinpath("smart_sales.db")
PREPARED_DATA_DIR = pathlib.Path("data").joinpath("prepared")

def create_schema(cursor: sqlite3.Cursor) -> None:
    """Create tables in the data warehouse if they don't exist."""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customer  (
            CustomerID INTEGER PRIMARY KEY,
            name TEXT,
            region TEXT,
            join_date TEXT,
            loyalty_points INTEGER,
            preferred_contact_method TEXT,
            standard_date_time TEXT
                  
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS product (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT,
            category TEXT,
            unit_price REAL,
            stock_quantity INTEGER,
            supplier TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sale (
            sale_id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            product_id INTEGER,
            store_id INTEGER,
            campaign_id INTEGER,
            discount_percent REAL,
            sale_amount REAL,
            payment_type TEXT,
            sale_date TEXT,
            promotion TEXT,
            quantity INTEGER,
            FOREIGN KEY (customer_id) REFERENCES customer (customer_id),
            FOREIGN KEY (product_id) REFERENCES product (product_id)
        )
    """)

def delete_existing_records(cursor: sqlite3.Cursor) -> None:
    """Delete all existing records from the customer, product, and sale tables."""
    cursor.execute("DELETE FROM customer")
    cursor.execute("DELETE FROM product")
    cursor.execute("DELETE FROM sale")



def insert_customers(customers_df: pd.DataFrame, cursor: sqlite3.Cursor) -> None:
    """Insert customer data into the customer table."""
    customers_df.to_sql("customer", cursor.connection, if_exists="append", index=False)

def insert_products(products_df: pd.DataFrame, cursor: sqlite3.Cursor) -> None:
    """Insert product data into the product table."""
    products_df.to_sql("product", cursor.connection, if_exists="append", index=False)

def insert_sales(sales_df: pd.DataFrame, cursor: sqlite3.Cursor) -> None:
    """Insert sales data into the sales table."""
    sales_df.to_sql("sale", cursor.connection, if_exists="append", index=False)

def load_data_to_db() -> None:
    try:
        # Connect to SQLite – will create the file if it doesn't exist
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Create schema and clear existing records
        create_schema(cursor)
        delete_existing_records(cursor)

        # Load prepared data using pandas
        customers_df = pd.read_csv(PREPARED_DATA_DIR.joinpath("customers_data_prepared.csv"))
        products_df = pd.read_csv(PREPARED_DATA_DIR.joinpath("products_data_prepared.csv"))
        sales_df = pd.read_csv(PREPARED_DATA_DIR.joinpath("sales_data_prepared.csv"))

         # Rename columns in the DataFrame to match the database schema
        #customers_df.rename(columns={"CustomerID": "customer_id"}, inplace=True)
        customers_df.rename(columns={"JoinDate": "join_date"}, inplace=True)
        customers_df.rename(columns={"LoyaltyPoints": "loyalty_points"}, inplace=True)
        customers_df.rename(columns={"PreferredContactMethod": "preferred_contact_method"}, inplace=True)
        customers_df.rename(columns={"StandardDateTime": "standard_date_time"}, inplace=True)
        # Rename columns in the DataFrame to match the database schema
        products_df.rename(columns={"ProductID": "product_id"}, inplace=True)
        products_df.rename(columns={"ProductName": "product_name"}, inplace=True)
        products_df.rename(columns={"Category": "category"}, inplace=True)
        products_df.rename(columns={"UnitPrice": "unit_price"}, inplace=True)
        products_df.rename(columns={"StockQuantity": "stock_quantity"}, inplace=True)
        products_df.rename(columns={"Supplier": "supplier"}, inplace=True)
        # Rename columns in the DataFrame to match the database schema
        sales_df.rename(columns={"TransactionID": "sale_id"}, inplace=True)
        sales_df.rename(columns={"CustomerID": "customer_id"}, inplace=True)
        sales_df.rename(columns={"ProductID": "product_id"}, inplace=True)
        sales_df.rename(columns={"StoreID": "store_id"}, inplace=True)
        sales_df.rename(columns={"CampaignID": "campaign_id"}, inplace=True)
        sales_df.rename(columns={"Discount percent": "discount_percent"}, inplace=True)
        sales_df.rename(columns={"CampaignID": "campaign_id"}, inplace=True)
        sales_df.rename(columns={"SaleAmount": "sale_amount"}, inplace=True)
        sales_df.rename(columns={"SaleDate": "sale_date"}, inplace=True)
        sales_df.rename(columns={"Quantity": "quantity"}, inplace=True)
        sales_df.rename(columns={"Payment Type": "payment_type"}, inplace=True)

        # Insert data into the database
        insert_customers(customers_df, cursor)
        insert_products(products_df, cursor)
        insert_sales(sales_df, cursor)

        conn.commit()
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    load_data_to_db()