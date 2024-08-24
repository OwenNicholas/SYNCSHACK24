### File Descriptions

1. **`app.py`**: This is the main application file for the Flask web server. It contains the following:
    - Initialization of the Flask app and configuration settings for SQLAlchemy.
    - Routes for handling the main pages (`home`, `login`, `signup`).
    - Logic for user authentication and registration.
    - Uses `Flask-Bcrypt` for hashing passwords securely.

2. **`models.py`**: This file defines the database model for the application. It includes:
    - The `db` object, which is an instance of `SQLAlchemy` used to interact with the SQLite database.
    - The `User` class, which represents the users of the application and includes fields for `id`, `email`, and `password`.

3. **`/templates`**: This directory contains HTML files used by Flask to render the frontend pages.
    - **`home.html`**: The home page that users see after logging in. It displays a welcome message and a logout link.
    - **`login.html`**: The login page where users can enter their email and password to log into the application.
    - **`signup.html`**: The sign-up page where new users can register by providing an email and password.

4. **`/static/css/styles.css`**: This file contains the CSS styles for the application. It is used to style the HTML pages, making the user interface more appealing. It includes styles for elements like body, form fields, buttons, and links.

5. **`README.md`**: This file. It provides an overview of the project, explains the purpose of each file, and gives instructions on how to set up and run the application.

## Installation and Setup

1. **Clone the Repository**: 
    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2. **Install Dependencies**: 
    Make sure you have Python installed. Then, install the required Python packages using pip:
    ```bash
    pip install Flask Flask-SQLAlchemy Flask-Bcrypt
    ```

3. **Run the Application**: 
    Execute the following command to start the Flask web server:
    ```bash
    python app.py
    ```

4. **Access the Application**: 
    Open a web browser and go to `http://127.0.0.1:5000` to access the home page. From here, you can navigate to the login and signup pages.

## Features

- **User Registration**: New users can register by providing an email and password.
- **User Login**: Registered users can log in using their email and password.
- **Home Page**: Authenticated users are redirected to a welcome home page.
- **Password Security**: Passwords are hashed using `Flask-Bcrypt` before storing them in the database.

## Future Improvements

- Add a user session management to track logged-in users and handle logout.
- Connect to a more robust database system like PostgreSQL for production use.
- Implement email verification for new user registrations.
- Add additional pages and features (e.g., user profile, password reset).

## License

This project is licensed under the MIT License. You can freely use, modify, and distribute this code as long as you include the original license file.

