# PitchTek
Project for CS 426, Spring 2024
University of Nevada, Reno
Team 23: Parker True, Davis Dunkley, Ethan Carroll

## Setup

### Frontend
1. Download and install Node.js
2. Navigate to **/PitchTek/frontend**
3. Install packages \
    ```npm install```

### Backend
1. Download and install Python3
2. Navigate to **/PitchTek/backend**
3. Create virtual environment \
    ```python3 -m venv env```
4. Activate virtual environment \
    Windows: ```.\env\Scripts\activate``` \
    Linux: ```source env/bin/activate```
6. Install packages \
    ```pip install -r requirements.txt```
7. Create **.env** file and fill in credentials

## Run for Development

### Frontend
1. Navigate to **/PitchTek/frontend**
2. Serve the frontend \
    ```npm run serve```

### Backend
1. Navigate to **/PitchTek/backend**
2. Activate virtual environment \
    Windows: ```.\env\Scripts\activate``` \
    Linux: ```source env/bin/activate```
3. Serve the backend \
    ```flask run --debug```

## Run for Production

### Frontend
1. Navigate to **/PitchTek/frontend**
2. Build the frontend \
    ```npm run build```
3. Retart Nginx \
    ```sudo systemctl restart nginx```
4. Restart Gunicorn \
    ```sudo systemctl restart gunicorn```
