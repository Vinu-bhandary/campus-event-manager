# Campus Event Manager

This is my prototype project for the Webknot Technologies campus drive assignment.  
The main idea was to build a **Campus Event Manager** where both **Admins** and **Students** can interact with events in a structured way. I used **Django (backend APIs)** and **React (frontend)** to implement the MVP features.


## Overview

The project is meant to handle the complete cycle of an event:
- Admins can create and manage events, view registrations, mark attendance, and check reports.
- Students can browse events, register for them, see their participation, and give feedback.



## Roles with Features

### Admin
- Create and manage events  
- View list of registered students for an event  
- Mark attendance  
- Generate reports (event popularity, student participation, feedback summary)

### Student
- Browse and register for events  
- View "My Registrations" (with attendance status)  
- Submit feedback after attending events  


## Tech Stack

- **Backend:** Django + Django Ninja 
- **Frontend:** React   
- **Database:** SQLite   


## Setup 

### 1. Clone the repo
```bash
git clone https://github.com/Vinu-bhandary/campus-event-manager.git
cd campus-event-manager
````

### 2. Backend

```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata seed.json
python manage.py runserver
```

Go to http://127.0.0.1:8000/api/docs for checking API


### 3. Frontend (React)

```bash
cd frontend
npm install
npm run dev
```
Go to http://localhost:5173



## Screenshots
Both Result and AI Conversation
[Here](https://github.com/Vinu-bhandary/campus-event-manager/tree/main/screenshots)



## What I learned in this project
While working on this project, I learned how to design my own database models and link them together for things like registrations, attendance, and feedback. I also got to use Django Ninja for the first time, which made creating APIs much easier.

I practiced connecting a React frontend with the Django backend, and along the way I had to fix setup problems with Tailwind, npm, and Node.js. Solving those issues helped me understand the development environment better.
