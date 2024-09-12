<template>
  <div class="dashboard-container">
    <v-col>
      <v-card class="container" style="border: 1px solid #43A047;" elevation="3">
        <h1>PitchTek: The Baseball Pitch Prediction Dashboard</h1>
        <p>
          CS 426 Senior Project in Computer Science, Spring 2024<br/>
          University of Nevada, Reno<br/>
          Department of Computer Science and Engineering
        </p>
        <p>
          <strong>Team 23:</strong> Parker True, Davis Dunkley, Ethan Carroll<br/>
          <strong>Instructors:</strong> David Feil-Seifer, Devrin Lee, Sara Davis, Zach Estreito, Vinh Le<br/>
          <strong>Advisor:</strong> Dr. Emily Hand, Assistant Professor - Machine Learning, UNR
        </p>
      </v-card>

      <v-card class="container" elevation="3"
        style="margin-top: 15px; border: 1px solid #43A047;"
      >
        <h2 style="margin-top: -5px;">Make Predictions with PitchTek</h2>
        <ol style="padding-left: 15px;">
          <li>Select a season. The 5 most recent MLB seasons are available by default.</li>
          <li>Select a home team and away team.</li>
          <li>Click the <strong>Start Game</strong> button.</li>
          <li>Ensure the game state is up-to-date (score, runners, inning, count).</li>
          <li>Click the <strong>Record Pitch</strong> button.</li>
          <li>Input the previous pitch's data if available.</li>
          <li>Click the <strong>Save Pitch</strong> button.</li>
          <li>View the predicted upcoming pitch on the Dashboard.</li>
        </ol>
      </v-card>

      <v-card class="container" style="margin-top: 15px; border: 1px solid #43A047;" elevation="3">
        <h2 style="margin-top: -5px;">What is PitchTek?</h2>
        <p style="text-indent: 2em;">
          PitchTek is a baseball analytics application that allows users to view player statistics, record a game’s progress,
          and predict upcoming pitch classifications using a proprietary machine learning model. The main Dashboard displays
          a high-level overview of the predictions and relevant baseball statistics pertaining to a game’s current state, while
          the Matchup and Statistics pages allow users to visualize and further explore the data.
        </p>
        <p style="text-indent: 2em;">
          As a tool, PitchTek offers lots of different systems to help analyze a baseball game. The primary focus is our machine
          learning model that can be used to predict the type, speed, and location of an upcoming pitch during a game. Users can
          input the current state of the game and then quickly receive the top three potential outcomes of the next pitch. Additionally,
          PitchTek will provide pages for logging in-game history and general statistics, allowing users to create an identity, save
          the state of games, and access players’ information all from the same dashboard.
        </p>
        <p style="text-indent: 2em;">
          PitchTek uses a front-end back-end framework as its foundation. For the front-end, The Vue framework is used to simplify the
          HTML design and server interaction. The backend uses the Flask framework to process HTML requests and send responses to the front-end.
          Python is used for building the machine learning models and SQLite is used for the database.
        </p>
      </v-card>

      <v-card class="container" style="margin-top: 15px; border: 1px solid #43A047;" elevation="3">
        <h2 style="margin-top: -5px;">
          References and Online Sources
        </h2>
        <p style="margin-bottom: 5px;">
          Read more about the groundbreaking baseball research that inspired PitchTek's pitch prediction model.
        </p>
        <ul style="margin-left: 15px;">
          <li><a href="https://towardsdatascience.com/baseball-and-machine-learning-a-data-science-approach-to-2021-hitting-projections-4d6eeed01ede">Baseball and machine learning: A data science approach to 2021 hitting projections - Medium</a></li>
          <li><a href="https://www.mdpi.com/2076-3417/11/10/4499">Use of Machine Learning and Deep Learning to Predict the Outcomes of Major League Baseball Matches - Applied Sciences</a></li>
          <li><a href="https://community.fangraphs.com/no-pitch-is-an-island-pitch-prediction-with-sequence-to-sequence-deep-learning/">No pitch is an island: Pitch prediction with sequence-to-sequence deep learning - FanGraphs Community</a></li>
        </ul>
      </v-card>

        <v-card class="container" style="margin-top: 15px; border: 1px solid #43A047;" elevation="3">
        <h2 style="margin-bottom: 15px; margin-top: -5px;">Team Members</h2>
        <div style="margin-left: 25px;">
          <div v-for="(image, index) in images" :key="index" class="image-wrapper">
            <img :src="image.src" :alt="image.alt" class="image">
            <span class="label">{{ image.label }}</span>
          </div>
        </div>
      </v-card>

    </v-col>
  </div>
</template>

<script>

export default {
  name: 'PitchTekPage',

 data() {
    return {
      images: [
        { src: require('@/assets/Parker_True_-_Head_Shot.jpg'), label: 'Parker True' },
        { src: require('@/assets/davis.jpg'), label: 'Davis Dunkley' },
        { src: require('@/assets/ethan.jpg'), label: 'Ethan Carroll' }
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
.image {
  max-width: 220px; /* Adjust the maximum width as needed */
  max-height: 220px; /* Adjust the maximum height as needed */
}

.image-wrapper {
  display: inline-block;
  margin-right: 20px; /* Adjust spacing between images */
}

.label {
  display: block;
  text-align: center;
  font-weight: bold; /* Apply bold font weight */
}

</style>
