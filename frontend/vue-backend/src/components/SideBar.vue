<template>
  <div class="container px-0 my-0 sticky-left">
    <div class="d-flex flex-column  bg-light sub-container" style="width: 4.5rem;">
      <a href="/" class="d-block p-3 link-dark text-decoration-none" title="LOGO" data-bs-toggle="tooltip" data-bs-placement="right" data-bs-original-title="Icon-only">
        <img class="bi" width="50" height="40" src="../assets/images .png">
      </a>
      <ul class="nav nav-pills nav-flush flex-column mb-auto text-center">
        <li v-for="(button, index) in buttons" :key="index" class="nav-item">
          <a :href="button.url" :class="['nav-link', { 'active': activeButton === index }]" class="py-3 border-bottom" :title="button.title" data-bs-toggle="tooltip" data-bs-placement="right" :data-bs-original-title="button.title" @mouseenter="showText(index)" @mouseleave="hideText">
            <div class="icon-container">
              <span :class="button.iconClass" style="font-size: 24px; color: black;"></span>
              <span v-if="hoveredIndex === index" class="icon-text">{{ button.title }}</span>
            </div>
          </a>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      hoveredIndex: null,
      activeButton: 0, // Index of the active button
      buttons: [
        { title: "Home", url: "#Home", iconClass: "e-icons e-home" },
        { title: "Add Image", url: "#AddImage", iconClass: "e-icons e-plus" },
        { title: "Uploaded Images", url: "#RetriveImage", iconClass: "e-icons e-image" },
      ]
    };
  },
  methods: {
    showText(index) {
      this.hoveredIndex = index;
    },
    hideText() {
      this.hoveredIndex = null;
    },
    activateButton(index) {
      this.activeButton = index; // Set the active button index
    }
  }
};
</script>

<style scoped>
.container {
  float: left;
  width: 4.5rem;
  position: fixed;
}
.sub-container{
  padding-bottom:1000px;
  float: left;
  width: 4.5rem;
}

.icon-container {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  height: 100%;
}

.icon-text {
  background-color: rgba(255, 255, 255, 0.8);
  padding: 0.2em 0.5em;
  border-radius: 4px;
  font-size: 14px;
  font-weight: bold;
  display: none;
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  right: calc(100% + 8px); /* Adjust the distance from the icon */
  white-space: nowrap; /* Prevent text from wrapping */
  z-index: 9999;
}

.nav-link:hover .icon-text {
  display: block;
}

/* Add styles for nav items */
.nav-item {
  height: 60px; /* Set a fixed height for each navigation item */
}
.border-bottom{
  cursor: pointer;
}
</style>
