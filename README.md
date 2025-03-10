# Project Management System

A web-based application for managing projects and tasks efficiently. This system allows administrators to create and manage projects, assign tasks to users, and track progress through various statistics.

## Features

- **User Management**
  - Register and log in as a user.
  - Role-based access control (Admin/User).
  
- **Project Management**
  - Create, edit, and delete projects.
  - View all projects in a structured table.

- **Task Management**
  - Assign tasks to specific users.
  - Update task status (Not Started, In Progress, Completed).
  - Delete tasks when completed.

- **Statistics**
  - View project progress as a bar chart.
  - View task status distribution as a pie chart.

- **Notifications**
  - Send email notifications when a task is assigned to a user.
  - Reminder emails for tasks nearing their deadline.

## Technologies Used

- **Backend**: Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-JWT-Extended
- **Frontend**: HTML, CSS, Bootstrap
- **Database**: MySQL
- **Email**: Flask-Mail (Gmail SMTP)
- **Authentication**: JWT (JSON Web Tokens)

## Installation

### Prerequisites
- Python 3.8 or later
- MySQL Server
- Node.js (optional, for frontend build tools)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/project-management-system.git
   cd project-management-system
# ProjectManagement
