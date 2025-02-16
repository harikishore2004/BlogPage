# Flask Blog Website

## Overview
This is a Flask-based blogging website that allows users to create, read, update, and delete blog posts. It includes user authentication, pagination, file uploads, and email services using Flask-Mail.

## Features
- User authentication (Admin Login)
- Create, edit, and delete blog posts
- Pagination for blog posts
- Contact form with email notifications
- File upload functionality
- SQLite database integration using Flask-SQLAlchemy

## Technologies Used
- **Flask**: Web framework
- **Flask-SQLAlchemy**: Database ORM
- **Flask-Mail**: Email service
- **HTML/CSS**: Frontend templates
- **Bootstrap**: Styling
- **Werkzeug**: Secure file uploads
- **Math & JSON Modules**: Handling pagination and configuration

## Installation
### Prerequisites
Ensure you have Python installed on your system. Install required dependencies using:
```sh
pip install flask flask-sqlalchemy flask-mail werkzeug
```

### Setup
1. Clone this repository:
2. Configure the `config.json` file with your database and email settings.
3. Set up environment variables for security:
   ```sh
   export Mail_Username='your-email@gmail.com'
   export Mail_Pswd='your-email-app_password'
   export SECRET_KEY='your-secret-key'
   export ADMIN_EMAIL='your-admin-email@example.com'
   ```
4. Run the application:
   ```sh
   python main.py
   ```
5. Open the browser and go to `http://127.0.0.1:5000`

## Usage
### Admin Panel
- Access the admin panel at `/dashboard`
- Use credentials from `config.json` to log in
- Manage blog posts and uploads

### Contact Form
- Visitors can send messages via `/contact`
- Emails will be sent to the configured admin email stored in environment variables

## Database Models
### **Posts Table**
| Column  | Type |
|---------|------|
| sno     | Integer (Primary Key) |
| title   | String |
| tagline | String |
| subtitle | String |
| slug    | String (Unique) |
| content | String |
| date    | String |
| name    | String |

### **Contacts Table**
| Column  | Type |
|---------|------|
| sno     | Integer (Primary Key) |
| name    | String |
| ph_num  | String |
| msg     | String |
| date    | String |
| email   | String |

## Contributing
Feel free to fork the repository and make improvements. Create a pull request with a description of your changes.

