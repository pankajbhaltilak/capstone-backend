**Amazon Sales Data Analytics Backend**

This is the backend API for the E-commerce Data Analytics project.
It powers the dashboard, providing endpoints for sales data, KPI metrics, CSV file uploads, and user authentication.
The backend is built using Django REST Framework (DRF) with MySQL as the database and is fully documented with Swagger.

**Features**
Sales API with pagination and filtering
KPI Dashboard API:
Total Sales
Total Orders
Average Order Value
Total Quantity Sold
CSV Upload API with:
File storage

Logging details:
File name
Upload timestamp
Uploaded by which user
Total number of rows (via Pandas)
JWT Authentication for secure access
Swagger-based API documentation
Centralized logging and error handling


**Tech Stack**
Django :	Web framework
Django REST Framework	REST API development
MySQL	Relational database
drf-yasg :Swagger documentation


**1. Setup Instructions**
git clone https://github.com/yourusername/ecommerce-analytics-backend.git
cd ecommerce-analytics-backend

**2. Create Virtual Environment**
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

**3. Install Dependencies**
pip install -r requirements.txt

**4. Configure Database**
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=mysql://username:password@127.0.0.1:3306/ecommerce_db

**5. Run Migrations**
python manage.py makemigrations
python manage.py migrate

**6. Create Superuser**
python manage.py createsuperuser

**7. Run the Server**
python manage.py runserver

**API Documentation :
Swagger documentation is available at: http://127.0.0.1:8000/swagger/**


**Best Practices Followed**
Clean architecture with separation of concerns:
views/ for API views
Pagination for large datasets
JWT Authentication
Logging
Swagger for auto-generated API documentation

**Screenshots**
Screenshot for : Dahsboard
<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/5a28db49-a05e-4aa3-9191-dd0fec5785ca" />

<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/0cd8c57a-d3c9-46d1-9382-1c59f5411856" />

<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/dee5469d-5fae-4e2a-ad8a-242cc2fbc68f" />

Screenshot for CSV Upload :
<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/0688b92f-6767-4719-ae29-cea69f66ad1b" />

Screenshot for Sales Records
<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/c89ba2b0-7dc8-4ebe-9a76-be87cd5a90fe" />

Screenshot for API documention :
<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/e4ae1379-ae4e-494b-8188-c8f5b7ec6f1c" />

<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/7ca56a92-6358-4eb4-a1b4-75fd5185a19e" />

<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/c0fb2aa1-2c0b-4931-8958-eda4935e98b4" />

<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/b87f48ea-153c-4d7f-9768-37e07b68177d" />


**👥 Contributors**
Pankaj Bhaltilak - Full Stack Developer








