# cybersecuritybase24-project - insecure-tsoha-keskusteluapp

> [!CAUTION]
> This is insecure and vulnernable version of my [tsoha-keskusteluapp](https://github.com/PaulusParssinen/tsoha-keskusteluapp) project for Cyber Security Base 2024. Do not use any parts of the project or expose it to the public internet.

## Test account credentials:

To ease reviewers experience, built-in seeded accounts that are added.

- Admin:admin123
- Demo:demo123

KeskusteluApp is classic chat-forum, where users can create new chat threads on "boards" and post new and edit messages.

KeskusteluApp is implemented using Python and the [Flask](https://palletsprojects.com/p/flask/) library.

## Features

- The user can create a new account and use it to log in and out.
- The user can give himself a profile picture.
- On the front page of the application, the user can see a list of areas, the number of threads and messages in each area and the time of the last message sent.
- The user can create a new thread in a region by entering the thread title and the content of the initial message.
- The user can post a new message in an existing thread.
- The user can edit the title of the thread he/she has created and the content of the message he/she has posted. The user can also delete a thread or a message.
- The user can search for all messages with a given word as part of the message.
- The administrator can add and delete discussion areas.
- The administrator can create a secret area and specify which users should have access to it.

## Setup & Usage

Prerequisites: [Git](https://git-scm.com/) & [Python (3.10+)](https://www.python.org/downloads/)

1. **Clone the repository and navigate to the project directory**:
   ```bash
   git clone https://github.com/PaulusParssinen/cybersec24-project.git
   cd cybersec24-project
   ```
2. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   ```
3. **Activate the virtual environment**:
   - **Linux/Mac**:
     ```bash
     source .venv/bin/activate
     ```
   - **Windows** (Command Prompt):
     ```bash
     .venv\Scripts\activate
     ```
   - **Windows** (PowerShell):
     ```bash
     .venv\Scripts\Activate.ps1
     ```
4. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
5. **Set up the base configuration file. (Should works as is for testing purposes)**:
   - **Linux/Mac**:
     ```bash
     cp .env.example .env
     ```
   - **Windows**:
     ```bash
     copy .env.example .env
     ```
6. **Run the application**:
   ```bash
   flask run
   ```

Now navigate to the local URL that is shown printed out by the server process.
