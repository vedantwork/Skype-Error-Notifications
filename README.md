<div align="center">
  <h1><b>SKYPE ERROR NOTIFICATION SERVICE</b></h1>
  <h4>Microservice for handling error notifications via Skype in a Django application</h4>
</div>

## 📗 Table of Contents

- [📖 About the Project](#about-project)
- [👀 Overview](#overview)
- [🛠 Built With](#built-with)
  - [🔥 Tech Stack](#tech-stack)
- [🔑 Key Features](#key-features)
- [💻 Getting Started](#getting-started)
  - [📜 Prerequisites](#prerequisites)
  - [⚙️ Setup](#setup)
  - [▶️ Run Application](#run-application)
  - [🕹️ Usage](#usage)
- [👥 Author](#author)

## 📖 About the Project

This service is a backend microservice integrated into a Django application, designed to notify error messages via Skype. It provides a mechanism to send error messages directly to a Skype chat from your backend when specific conditions or exceptions occur.

## 👀 Overview

- The service provides a method (`notifyerrormessage`) to send error messages from your Django application to a specified Skype chat.
- It handles incoming POST requests, processes the error data, and sends the details as a message to a configured Skype account.

## 🛠 Built With

- Python
- Django
- Requests
- JSON

### 🔥 Tech Stack

- Django
- Skype API

### 🔑 Key Features

- Sends error notifications directly to Skype.
- Handles both encoded and plain JSON data in POST requests.
- Uses SQL queries to fetch user details for personalized error reporting.

## 💻 Getting Started

### 📜 Prerequisites

To use this service, you will need:

- Python 3.x
- Django
- Skype account credentials
- Required Python libraries: `requests`, `json`, `Skype API` (if using Skype integration).

### ⚙️ Setup

1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-repo/skype-error-notification-service.git
    ```

2. **Navigate to the project directory**:
    ```bash
    cd skype-error-notification-service
    ```

3. **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Update Configuration**:
    - Replace `'yourskypeemail'` and `'yourskypepassword'` with your actual Skype email and password.
    - Update the `urls.BASE_URL` in `main/constants.py` with your application's base URL.

### ▶️ Run Application

1. **Run the Django development server**:
    ```bash
    python manage.py runserver
    ```

### 🕹️ Usage

1. The `notifyerrormessage` method accepts a POST request with error details in JSON format.
2. To trigger the error notification, send a POST request to the endpoint with the necessary payload.
3. The method will process the request and send the error message to the configured Skype chat.

- [👥 Author](#author)
  - Vedant Vartak
    - Email ✉️: vedantvartakworkk@gmail.com
    - Country 🌍: India 🇮🇳

**Example Request**:

```json
{
    "email": "user@example.com"
}


