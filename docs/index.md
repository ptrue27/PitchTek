# PitchTek: The Baseball Pitch Prediction Dashboard

CS 426 Senior Project in Computer Science, Spring 2023 \
University of Nevada, Reno \
Department of Computer Science and Engineering \

Team 23: Davis Dunkley, Parker True, Ethan Carroll \
Instructors: David Feil-Seifer, Devrin Lee, Sara Davis, Zach Estreito, Vinh Le \
Advisor: Dr. Emily Hand, Assistant Professor, UNR

## Project Description
PitchTek is a baseball analytics application that allows users to view player statistics, record a game’s progress, and predict upcoming pitch classifications using a proprietary machine learning model. The main Dashboard displays a high-level overview of the predictions and relevant baseball statistics pertaining to a game’s current state, while the Statistics and History pages allow users to visualize and further explore the data.
As a tool, PitchTek offers lots of different systems to help analyze a baseball game. The primary focus is our machine learning model that can be used to predict the type, speed, and location of an upcoming pitch during a game. Users can input the current state of the game and then quickly receive the top three potential outcomes of the next pitch. Additionally, PitchTek will provide pages for logging in-game history and general statistics, allowing users to create an identity, save the state of games, and access players’ information all from the same dashboard.
PitchTek uses a front-end back-end framework as its foundation. For the front-end, The Vue framework is used to simplify the HTML design and server interaction. The baskend uses the Flask framework to process HTML requests and send responses to the front-end. Python is used for building the machine learning models and SQLite is used for the database.
Professional teams have their own prediction systems and statistical resources that they use to gain an edge in the sport. However they do not release their expensive tools to the public. PitchTek will help even the playing field between private teams and the public through its accessible analytics. This tool has the potential to help further coaches’ understanding of player performance and provides a new way for fans to engage with the sport.
