<template>
  <div id="app">
    <SlideBar/>
    <HomeMenu/>
    <AddImage/>
    <RetriveImage/>

     <!-- This will render the component corresponding to the current route -->
  </div>
</template>

<script>
import SlideBar from "@/components/SideBar.vue";
import HomeMenu from "@/components/HomeMenu.vue";
import AddImage from "@/components/AddImage.vue";
import RetriveImage from "./components/RetriveImage.vue";

export default {
  name: 'App',
  components: {
    SlideBar,
    HomeMenu,
    AddImage,
    RetriveImage,
  }
}
</script>
