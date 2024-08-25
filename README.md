# Flask User Profile Management System

This project is a web-based user profile management system built using Flask, where users can manage their profiles, send and receive friend requests, and join events. The project uses SQLAlchemy for database management, Jinja2 for templating, and HTML/CSS for frontend styling.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Running the Project](#running-the-project)
- [Features and Functionalities](#features-and-functionalities)
- [CSS Styling](#css-styling)
- [Troubleshooting](#troubleshooting)
- [Acknowledgments](#acknowledgments)

## Features

- User authentication (sign up, log in, log out).
- User profile management (update profile details).
- Friend request system (send, accept, decline requests).
- List of friends.
- Event management (view and join events).
- Responsive design using CSS.


## Setup Instructions

1. **Clone the repository**:

    ```bash
    git clone https://github.com/yourusername/flask-user-profile.git
    cd flask-user-profile
    ```

2. **Create a virtual environment**:

    ```bash
    python3 -m venv venv
    ```

3. **Activate the virtual environment**:

    - On Windows:

        ```bash
        venv\Scripts\activate
        ```

    - On Mac/Linux:

        ```bash
        source venv/bin/activate
        ```

4. **Install required dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

5. **Set up the database**:

    Run the following command to initialize the database:

    ```python
    from app import db
    db.create_all()
    ```

6. **Run the application**:

    ```bash
    python app.py
    ```

7. **Access the application**:

    Open your web browser and navigate to `http://127.0.0.1:5001` to view the application.

## Features and Functionalities

### 1. **User Authentication**

- Users can sign up with a unique username and password.
- Users can log in using their credentials.
- Passwords are hashed for security.

### 2. **User Profile Management**

- Users can view their profile, including their username and description.
- Profile descriptions are stored in the `q5` field of the `User` model.
- Users can update their profile details, including their username and description.

### 3. **Friend Request System**

- Users can send friend requests to other users.
- Users can accept or decline friend requests.
- The list of friend requests is displayed on the profile page.

### 4. **Friend List**

- Users can view a list of their friends.
- Friends are displayed under the "My Friends" section.

### 5. **Event Management**

- Users can view a list of events.
- Users can filter events by date.
- Users can join events, and the list of joined events is displayed on their profile page.
- Joined events are managed through a `UserEvent` model.

### 6. **Responsive Design**

- CSS is used to style the profile and event pages, providing a responsive and user-friendly interface.



