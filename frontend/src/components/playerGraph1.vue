<template>
  <div ref="graphContainer" class="graph-container">
    <!-- HTML content from the graph file will be injected here -->
  </div>
</template>

<script>
export default {
  props: {
    fileName: {
      type: String,
      required: true,
    },
  },
  mounted() {
    this.loadGraphContent();
  },
  methods: {
    loadGraphContent() {
      const filePath = `C:/Users/davis/PitchTek-3/frontend/src/dataVisual/release_speed.html`; // Construct the file path based on the fileName prop
      fetch(filePath)
        .then((response) => response.text())
        .then((htmlContent) => {
          this.$refs.graphContainer.innerHTML = htmlContent;
        })
        .catch((error) => {
          console.error('Error loading the graph content:', error);
          this.$refs.graphContainer.innerHTML = '<p>Error loading graph.</p>';
        });
    },
  },
};
</script>


<style scoped>
.graph-container {
  /* Basic styling */
  padding: 20px;
  margin: 20px auto; /* Center the container */
  border-radius: 10px; /* Rounded corners */
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.1); /* Subtle shadow for depth */
  background-color: #ffffff; /* White background */
  max-width: 90%; /* Maximum width with some space on the sides */

  /* Responsive design */
  @media (min-width: 768px) {
    max-width: 80%; /* Less width on larger screens for better readability */
  }

  /* Animation */
  transition: transform 0.3s ease, box-shadow 0.3s ease;

  /* Interactive effect */
  &:hover {
    transform: translateY(-5px); /* Slightly raise the container */
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2); /* Enhanced shadow for raised effect */
  }

  /* Graph Title */
  .graph-title {
    margin-bottom: 15px;
    font-size: 1.5em;
    text-align: center;
    color: #333333; /* Dark gray for contrast */
  }

  /* Graph Content Styling */
  .graph-content {
    width: 100%;
    height: 400px; /* Set a fixed height for consistency, adjust based on your graph library */
    overflow: hidden; /* Hide overflow */
  }
}
</style>
