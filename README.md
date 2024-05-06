# Personal Assistant Project

## Overview

This Django project serves as a personal assistant web application, aimed at efficiently managing contacts, notes,
files, user profiles, and providing news updates.

## Features

### Contacts

- **Manage Contacts**: Users can add, edit, delete, and search for contacts.
- **Upcoming Birthdays**: Users can view upcoming birthdays of their contacts within a specified number of days.

### Notes

- **Manage Notes**: Users can add, edit, delete, and search for notes.
- **Tagging**: Notes can be tagged for better organization.
- **Top Tags**: Users can see the top tags used across all notes.

### Filemanager

- **Upload and Manage Files**: Users can upload various types of files (videos, images, documents, audio) and manage
  them.
- **Categorization**: Files can be categorized for better organization.
- **Download Files**: Users can download uploaded files.

### News

- **View News and Statistics**: Users can view news articles and statistics, with the information being updated on a
  daily basis.

### Users

- **User Registration**: Users can register for an account.
- **User Authentication**: Registered users can log in to access the application.
- **User Profiles**: Users have profiles where they can manage their personal information.

### Profiles

- **User Profiles**: Users can view and edit their profiles.
- **Avatar Upload**: Users can upload avatars for their profiles.

## Installation

1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd <repository-name>
    ```
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Set up environment variables:
    - Create a `.env` file in the project root directory.
    - Define the following environment variables in the `.env` file:
        - `CLOUD_NAME`: Your Cloudinary cloud name.
        - `CLOUD_API_KEY`: Your Cloudinary API key.
        - `CLOUD_API_SECRET`: Your Cloudinary API secret.
4. Run migrations:
    ```bash
    python manage.py migrate
    ```
5. Start the development server:
    ```bash
    python manage.py runserver
    ```
6. Access the application at [http://localhost:8000/](http://localhost:8000/).

## Usage

1. Register for an account or log in if you already have one.
2. Navigate through the different sections (Contacts, Notes, Files, Profile) to manage your personal information.
3. Use the provided forms and functionalities to add, edit, delete, and search for items.
4. Explore additional features such as upcoming birthdays, top tags, and file categorization.
5. Switch between languages: Users can switch between Ukrainian and English languages by selecting the desired language option from the language switcher provided in the web application interface.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/<feature-name>`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/<feature-name>`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License.
