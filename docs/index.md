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

## References and Online Sources

Here is a artcle on the use of data science, machine learning and coding the sport of baseball to take accurate stats and possibly predict the game and some of the outcomes of the smaller parts of it. 
Pette, J. (2021, May 17). Baseball and machine learning: A data science approach to 2021 hitting projections. Medium. https://towardsdatascience.com/baseball-and-machine-learning-a-data-science-approach-to-2021-hitting-projections-4d6eeed01ede 

This is a research paper on the use of machine learning in baseball. This showed a great example of how to approach the data for data scrubbing and looking at what elements can predict a game on a large scale.
Huang, M L & Li, Yun-Zhi. (2021). Use of Machine Learning and Deep Learning to Predict the Outcomes of Major League Baseball Matches. Applied Sciences. 11. 4499. 10.3390/app11104499. 