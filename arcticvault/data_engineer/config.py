SYSTEM_PROMPT_SQL_GENERATION_HUBS = """You have received a report outlining the Data Vault 2.0 model, detailing the hubs, links, and satellites tables along with their respective schemas.
Your task is to generate SQL queries to create **ONLY** Hub tables.

- **Include Primary Keys**: Ensure that each Hub table has its primary keys properly defined.
- **Naming Conventions**: Use the naming conventions mentioned in the report for consistency and clarity.
- **Output**: Only generate SQL statements.

**Example Report Details:**

- **Hub Table Examples**:
  - **Hub_Customer**: Customer_ID (PK), Load_Date
  - **Hub_Order**: Order_ID (PK), Load_Date

- **Link Table Example:**
  - **Table Name**: Link_Customer_Order
  - **Columns**: Link_ID (PK), Customer_ID (FK), Order_ID (FK), Load_Date

- **Satellite Table Example:**
  - **Satellite_Customer_Details**: Customer_ID (PK, FK), Name, Address, Load_Date

**Generated SQL Statements:**

```sql
-- Hub table for Customer
CREATE TABLE Hub_Customer (
    Customer_ID INT PRIMARY KEY,
    Load_Date TIMESTAMP
);

-- Hub table for Order
CREATE TABLE Hub_Order (
    Order_ID INT PRIMARY KEY,
    Load_Date TIMESTAMP
);
```
Adjust the schema definitions and columns based on the actual report you have. The example provided is intended to guide the Snowflake Arctic model in generating the required SQL statements for creating Hub tables.
"""

SYSTEM_PROMPT_SQL_GENERATION_LINKS = """You have received a report outlining the Data Vault 2.0 model, detailing the hubs, links, and satellites tables along with their respective schemas.
Your task is to generate SQL queries to create **ONLY** Link tables.
- **Include Primary Keys and Foreign Keys**: Ensure that each Link table has its primary keys and foreign keys properly defined.
- **Naming Conventions**: Use the naming conventions mentioned in the report for consistency and clarity.
- **Output**: Only generate SQL statements.

**Example Report Details:**

- **Hub Table Examples**:
  - **Hub_Customer**: Customer_ID (PK), Load_Date
  - **Hub_Order**: Order_ID (PK), Load_Date

- **Link Table Examples**:
  - **Link_Customer_Order**: Link_ID (PK), Customer_ID (FK), Order_ID (FK), Load_Date
  - **Link_Product_Order**: Link_ID (PK), Product_ID (FK), Order_ID (FK), Load_Date

- **Satellite Table Examples**:
  - **Satellite_Customer_Details**: Customer_ID (PK, FK), Name, Address, Load_Date
  - **Satellite_Order_Details**: Order_ID (PK, FK), Product, Quantity, Load_Date

**Generated SQL Statements:**

```sql
-- Link table for Customer and Order
CREATE TABLE Link_Customer_Order (
    Link_ID INT PRIMARY KEY,
    Customer_ID INT,
    Order_ID INT,
    Load_Date TIMESTAMP,
    FOREIGN KEY (Customer_ID) REFERENCES Hub_Customer(Customer_ID),
    FOREIGN KEY (Order_ID) REFERENCES Hub_Order(Order_ID)
);

-- Link table for Product and Order
CREATE TABLE Link_Product_Order (
    Link_ID INT PRIMARY KEY,
    Product_ID INT,
    Order_ID INT,
    Load_Date TIMESTAMP,
    FOREIGN KEY (Product_ID) REFERENCES Hub_Product(Product_ID),
    FOREIGN KEY (Order_ID) REFERENCES Hub_Order(Order_ID)
);
```

Adjust the schema definitions and columns based on the actual report you have. The example provided is intended to guide the Snowflake Arctic model in generating the required SQL statements for creating Link tables.
"""

SYSTEM_PROMPT_SQL_GENERATION_SATELLITES = """You have received a report outlining the Data Vault 2.0 model, detailing the hubs, links, and satellites tables along with their respective schemas.

Your task is to generate SQL queries to create **ONLY** Satellite tables.

- Include Primary Keys and Foreign Keys: Ensure that each Satellite table has its primary keys and foreign keys properly defined.
- Naming Conventions: Use the naming conventions mentioned in the report for consistency and clarity.
- Include all Satellite tables: Ensure that all Satellite tables are included in the generated SQL statements.
It is mandatory to include all satellite tables.

Example Report Details:
- Satellite Table Examples:
  - Satellite_Customer_Details: Customer_ID (PK, FK), Name, Address, Load_Date
  - Satellite_Order_Details: Order_ID (PK, FK), Product, Quantity, Load_Date
  - Satellite_Product_Details: Product_ID (PK, FK), Description, Price, Load_Date
  - Satellite_Supplier_Details: Supplier_ID (PK, FK), Name, Contact_Info, Load_Date

Generated SQL Statements:
```sql
-- Satellite table for Customer Details
CREATE TABLE Satellite_Customer_Details (
    Customer_ID INT PRIMARY KEY,
    Name VARCHAR(255),
    Address VARCHAR(255),
    Load_Date TIMESTAMP,
    FOREIGN KEY (Customer_ID) REFERENCES Hub_Customer(Customer_ID)
);

-- Satellite table for Order Details
CREATE TABLE Satellite_Order_Details (
    Order_ID INT PRIMARY KEY,
    Product VARCHAR(255),
    Quantity INT,
    Load_Date TIMESTAMP,
    FOREIGN KEY (Order_ID) REFERENCES Hub_Order(Order_ID)
);

-- Satellite table for Product Details
CREATE TABLE Satellite_Product_Details (
    Product_ID INT PRIMARY KEY,
    Description VARCHAR(255),
    Price DECIMAL(10, 2),
    Load_Date TIMESTAMP,
    FOREIGN KEY (Product_ID) REFERENCES Hub_Product(Product_ID)
);

-- Satellite table for Supplier Details
CREATE TABLE Satellite_Supplier_Details (
    Supplier_ID INT PRIMARY KEY,
    Name VARCHAR(255),
    Contact_Info VARCHAR(255),
    Load_Date TIMESTAMP,
    FOREIGN KEY (Supplier_ID) REFERENCES Hub_Supplier(Supplier_ID)
);

```
"""


CUSTOM_BTNS = [
 {
   "name": "Copy",
   "feather": "Copy",
   "hasText": True,
   "alwaysOn": True,
   "commands": ["copyAll",
                ["infoMessage",
                    {
                     "text": "Copied to clipboard!",
                     "timeout": 1000,
                     "classToggle": "show"
                    }
                   ]
                ],
   "style": {"top": "0.46rem", "right": "0.4rem"}
 },
 {
   "name": "Run",
   "feather": "Play",
   "primary": True,
   "hasText": True,
   "alwaysOn": True,
   "showWithIcon": True,
   "commands": ["submit"],
   "style": {"bottom": "0.44rem", "right": "0.4rem"}
 },
]

CSS_STRING = '''
font-weight: 600;

.code_editor-info.message {
   width: inherit;
   margin-right: 75px;
   order: 2;
   text-align: center;
   opacity: 0;
   transition: opacity 0.7s ease-out;
}

.code_editor-info.message.show {
   opacity: 0.6;
}

'''
CODE_STYLE = {"width": "100%"}

INFO_BAR = {
  "name": "language info",
  "css": CSS_STRING,
  "style": {
            "order": "1",
            "display": "flex",
            "flexDirection": "row",
            "alignItems": "center",
            "width": "100%",
            "height": "2.5rem",
            "padding": "0rem 0.75rem",
            "borderRadius": "8px 8px 0px 0px",
            "zIndex": "9993"
           },
  "info": [{
            "name": "☃️SnowTUI CodeEditor",
            "feather": "Database",
            "style": {"width": "250px"}
           }]
}
