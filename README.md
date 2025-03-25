
# Insurance Management System

## Project Overview

The **Insurance Management System** is a web-based application designed to manage and streamline the customer lifecycle within an insurance company. The system allows customers to sign up, apply for insurance policies, manage premium distributions, track policy histories, and submit questions to the company. It also provides a comprehensive customer dashboard and aggregates key data for both customers and the insurance company.

## Features

- **Customer Sign-Up**: Customers can register an account, set a username and password, and upload a profile photo.
- **Policy Application**: Customers can browse available insurance policies and apply for them.
- **Premium Distribution**: Monthly premium details, sum assurance, and policy status are calculated and displayed via stored procedures.
- **Policy History**: Customers can view the history of all policies they have applied for.
- **Question Management**: Customers can ask questions about policies, and view past queries and responses.
- **Customer Dashboard**: A personalized dashboard that shows the total number of policies, premiums, and any questions asked.
- **Data Analytics**: Views and stored procedures to aggregate and display data such as total policies, premiums, and customer statistics.

## Technologies Used

- **Django (Python)**: The backend framework for handling customer interactions, form handling, and user authentication.
- **SQL**: Used for creating and managing the database, including stored procedures, views, and indexes for efficient data retrieval.
- **HTML/CSS**: For building the user interface and ensuring a seamless experience.
- **MySQL**: For storing all customer and policy data, with indexing and optimization techniques applied to enhance performance.
- **Bootstrap**: For responsive web design and layout.

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd <project-folder>
   ```

2. **Create and Activate Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Required Packages**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Database**
   - Create a MySQL database for the project and configure the database settings in `settings.py`.
   - Run database migrations:
     ```bash
     python manage.py migrate
     ```

5. **Create Superuser**
   - To access the Django admin panel, create a superuser:
     ```bash
     python manage.py createsuperuser
     ```

6. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```

7. **Access the Application**
   - Visit `http://127.0.0.1:8000/` to access the application in your browser.


## Database

### Key Tables:

- **customer**: Stores customer information (name, username, profile photo).
- **insurance_policy**: Stores insurance policy details (policy name, premium, coverage).
- **insurance_policyrecord**: Stores records linking customers to their policies (customer ID, policy ID).
- **questions**: Stores questions asked by customers related to policies.

### Stored Procedures and Views

- **Stored Procedure (`GetPremium`)**: Retrieves premium distribution details for a customer, including policy names, premium amounts, monthly payments, and policy status.
- **View (`customer_policy_overview`)**: Aggregates total premium amounts and total policy count for each customer.


### Indexing

To optimize query performance, indexing has been applied to important fields, including those used in the stored procedures and views. These indexes are essential for improving the retrieval speed of data like customer policy details and premium distributions.



## License

This project is licensed under the MIT License.
