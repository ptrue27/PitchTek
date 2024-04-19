<template>
  <div class="container">
    <h1>PitchTek: The Baseball Pitch Prediction Dashboard</h1>
    <p>
      CS 426 Senior Project in Computer Science, Spring 2024<br/>
      University of Nevada, Reno<br/>
      Department of Computer Science and Engineering
    </p>
    <p>
      <strong>Team 23:</strong> Davis Dunkley, Parker True, Ethan Carroll<br/>
      <strong>Instructors:</strong> David Feil-Seifer, Devrin Lee, Sara Davis, Zach Estreito, Vinh Le<br/>
      <strong>Advisor:</strong> Dr. Emily Hand, Assistant Professor, UNR
    </p>

    <h2>Dashboard View</h2>

    <v-img :src="require('@/assets/dashboard.png')" style="margin-top: 5px; margin-bottom: 1px; height: 392px;"></v-img>
    <h2>Project Description</h2>
    <p>
      PitchTek is a baseball analytics application that allows users to view player statistics, record a game’s progress,
      and predict upcoming pitch classifications using a proprietary machine learning model. The main Dashboard displays
      a high-level overview of the predictions and relevant baseball statistics pertaining to a game’s current state, while
      the Statistics and History pages allow users to visualize and further explore the data.
    </p>
    <p>
      As a tool, PitchTek offers lots of different systems to help analyze a baseball game. The primary focus is our machine
      learning model that can be used to predict the type, speed, and location of an upcoming pitch during a game. Users can
      input the current state of the game and then quickly receive the top three potential outcomes of the next pitch. Additionally,
      PitchTek will provide pages for logging in-game history and general statistics, allowing users to create an identity, save
      the state of games, and access players’ information all from the same dashboard.
    </p>
    <p>
      PitchTek uses a front-end back-end framework as its foundation. For the front-end, The Vue framework is used to simplify the
      HTML design and server interaction. The backend uses the Flask framework to process HTML requests and send responses to the front-end.
      Python is used for building the machine learning models and SQLite is used for the database.
    </p>

    <h2>References and Online Sources</h2>
    <ul>
      <li><a href="https://towardsdatascience.com/baseball-and-machine-learning-a-data-science-approach-to-2021-hitting-projections-4d6eeed01ede">Baseball and machine learning: A data science approach to 2021 hitting projections - Medium</a></li>
      <li><a href="https://www.mdpi.com/2076-3417/11/10/4499">Use of Machine Learning and Deep Learning to Predict the Outcomes of Major League Baseball Matches - Applied Sciences</a></li>
      <li><a href="https://community.fangraphs.com/no-pitch-is-an-island-pitch-prediction-with-sequence-to-sequence-deep-learning/">No pitch is an island: Pitch prediction with sequence-to-sequence deep learning - FanGraphs Community</a></li>
    </ul>

    <h2>Team Members</h2>
  <div class="image-row">
    <img v-for="(image, index) in images" :key="index" :src="image.src" :alt="image.alt" class="image">
  </div>
  </div>
</template>

<script>

export default {
  name: 'PitchTekPage',

 data() {
    return {
      images: [
        { src: require('@/assets/default.jpg'), alt: 'Davis' },
        { src: require('@/assets/default.jpg'), alt: 'Parker' },
        { src: require('@/assets/default.jpg'), alt: 'Ethan' }
      ]
    };
  }
}
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: auto;
  padding: 20px;
}
.team-members figure {
  display: flex;
  margin-bottom: 10px;
}
.team-members img {
  width: 33.33%;
  margin-right: 10px;
}
</style>
