<template>
  <div id="RetriveImage" class="image-gallery">
    <H1 class="headretrive">Memories..</H1>
    <!-- Search bar -->
    <input type="text" v-model="searchQuery" placeholder="Search by ID" class="search-bar" />
    
    <div v-for="image in filteredImages" :key="image.id" class="image-item">
      <div class="image-wrapper" @mouseover="showIcons(image.id)" @mouseleave="hideIcons()">
        <div class="image-id">{{ image.id }}</div>
        <img :src="getImage(image.images[0])" :alt="image.caption" class="image">
        
        <div v-if="image.caption" class="caption">{{ truncateCaption(image.caption) }}</div>
        <div v-if="hoveredItem === image.id" class="image-icons">
          <span class="edit-icon" @click="editImage(image.id)">✎</span>
          <span class="delete-icon" @click="deleteImage(image.id)">🗑️</span>
          <span>+{{ image.images.length -1 }} more</span>
        </div>
      </div>
    </div>
    <div style="display: none" class="image-carousel" id="gallery-blank">
     <div class="BgBlur">
      <span class="DataId">{{ dataId }}</span>
      <div class="image-container">
          <!-- Apply styles to the images to make them smaller -->
          <img :src="`http://localhost:8000${imagesDataimg[currentIndex]}`" :alt="`Image ${currentIndex + 1}`" class="carousel-image">
          <div class="image-icons-additional">
        <label for="imageInput" class="add-icon">➕</label>
        <input type="file" id="imageInput" style="display: none" @change="handleImageSelection($event ,dataId)">
        <span class="delete-icon" @click="DeleteSingleImage(imagesDataimg[currentIndex], dataId)">🗑️</span>
        <span class="fileName" style="color: white">{{ selectedFileName }}</span>
      </div>
        </div>
        <span class="NextImageCaro" @click="nextImage()">Next</span>
        <span class="PrevImageCaro" @click="prevImage()">Prev</span>
        <span class="closeImageCaro"  @click="closeImageCarousel()">❌</span>
        <textarea name="caption" v-model="captionValue" cols="30" rows="10" class="EditCaption"></textarea>
        <span class="submitEditImage" @click="submitAddonImage(dataId)">Submit</span>
  </div>
  </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      images: [],
      searchQuery: '',
      hoveredItem: null,
      captionValue: '',
      dataId: '',
      imagesDataimg:[],
      currentIndex: 0,
      selectedFileName: '',
      file:'' 

    };
  },
  mounted() {
    // Make an API request to retrieve images and captions
    this.fetchImages();
  },
  methods: {
    fetchImages() {
      // Replace 'YOUR_BACKEND_URL' with the actual URL of your backend endpoint
      fetch('http://localhost:8000/media/images/')
        .then(response => response.json())
        .then(data => {
          this.images = data;
        })
        .catch(error => {
          console.error('Error fetching images:', error);
        });
    },
    getImage(file) {
      // Assuming file path is relative to the base URL
      return `http://localhost:8000${file}`;
    },
    showIcons(id) {
      this.hoveredItem = id;
    },
    hideIcons() {
      this.hoveredItem = null;
    },
    editImage(id) {
  // Fetch all images for the specified ID and caption
  fetch(`http://localhost:8000/get-images/${id}/`, {
    method: 'GET'
  })
  .then(response => response.json())
  .then(data => {
    // Display the fetched images in a modal popup carousel
    this.showImageCarousel(data);
  })
  .catch(error => {
    console.error(`Error fetching images for ID ${id}:`, error);
  });
},

  deleteImage(id) {
  // Send a DELETE request to the backend API endpoint with the image ID
  fetch(`http://localhost:8000/delete/${id}/`, {
    method: 'POST' // Use DELETE method for deleting resources
  })
  .then(response => {
    if (response.ok) {
      // Image deleted successfully
      console.log(`Image with ID ${id} deleted successfully.`);
      
      // Remove the deleted image from the frontend list
      this.images = this.images.filter(image => image.id !== id);
    } else {
      // Handle error deleting the image
      console.error(`Error deleting image with ID ${id}: ${response.statusText}`);
    }
  })
  .catch(error => {
    console.error(`Error deleting image with ID ${id}:`, error);
  });
},

closeImageCarousel() {
  const gallery = document.getElementById('gallery-blank');
  if (gallery) {
    // Clear the gallery content
    gallery.style.display = 'none';
  }
},
 
showImageCarousel(imageData) {
      const galleryblank = document.getElementById('gallery-blank');

      if (galleryblank.style.display === 'block') {
        galleryblank.style.display = 'none';
      } else {
        galleryblank.style.display = 'block';
        console.log(imageData);

        // Set captionValue and dataId
        this.captionValue = imageData.caption;
        this.dataId = imageData.id;

        this.imagesDataimg = imageData.images
      }
    },
    nextImage() {
      // Increment currentIndex to navigate to the next image
      this.currentIndex = (this.currentIndex + 1) % this.imagesDataimg.length;
    },
    prevImage() {
      // Decrement currentIndex to navigate to the previous image
      this.currentIndex = (this.currentIndex - 1 + this.imagesDataimg.length) % this.imagesDataimg.length;
    },
    handleImageSelection(event, id) {
      console.log(id);
      const fileimage = event.target.files[0];
      if (fileimage) {
        // Set the selected file name
        this.selectedFileName = fileimage.name;
        console.log(fileimage);
        this.file = fileimage;

      }
    },
    submitAddonImage(id) {
    const formData = new FormData();
    if (this.file) {
        formData.append('image', this.file);
    }
    formData.append('caption', this.captionValue);

    fetch(`http://localhost:8000/addonimage/${id}/`, {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            // Image uploaded successfully
            console.log('Image uploaded successfully');
            this.selectedFileName = '';
            alert(`Image Added successfully.`);
            window.location.reload();
        } else {
            // Handle error uploading image
            console.error('Error uploading image:', response.statusText);
        }
    })
    .catch(error => {
        console.error('Error uploading image:', error);
    });
},

    DeleteSingleImage(url, id) {
  fetch(`http://localhost:8000/DeleteSingleImage/${id}/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ url: url }) // Send the image URL in the request body
  })
  .then(response => {
    if (response.ok) {
      // Image deleted successfully
      console.log(`Image with URL ${url} and ID ${id} deleted successfully.`);
      alert(`Image deleted successfully.`)
      window.location.reload();
    } else {
      // Handle error deleting the image
      console.error(`Error deleting image with URL ${url} and ID ${id}: ${response.statusText}`);
    }
  })
  .catch(error => {
    console.error(`Error deleting image with URL ${url} and ID ${id}:`, error);
  });
},

    truncateCaption(caption) {
      // Truncate the caption if it's too long
      const maxLength = 20;
      if (caption.length > maxLength) {
        return caption.substring(0, maxLength) + '...';
      }
      return caption;
    }
  },
  computed: {
    filteredImages() {
      // Filter images based on search query
      return this.images.filter(image => {
        return image.id.toString().includes(this.searchQuery);
      });
    }
  }
};
</script>

<style scoped>
.image-gallery {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  margin-left:4.5rem;
}

.image-item {
  margin: 20px;
}

.image-wrapper {
  position: relative;
}

.image {
  max-width: 300px;
  max-height: auto;
  border-radius: 10px;
}
.image-id {
  position: absolute;
  top: 10px;
  left: 10px;
  background-color: rgba(0, 0, 0, 0.5);
  color: white;
  padding: 5px;
  border-radius: 5px;
}

.caption {
  font-family: 'Pacifico', cursive;
  text-align: center;
  margin-top: 5px;
  font-size: 14px;
}

.image-icons {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(18, 17, 17, 0.679);
  color: white;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.image-wrapper:hover .image-icons {
  opacity: 3; 
}

.edit-icon,
.delete-icon {
  margin: 0 5px;
  cursor: pointer;
}

.edit-icon:hover,
.delete-icon:hover {
  font-weight: bolder;
  color:red;
  font-size:25px;
}

.search-bar {
  position: absolute;
  right: 0;
  margin-top: -40px; /* Adjust as needed */
  margin-right: 20px; /* Adjust as needed */
  width: 20%; /* Set width to 20% of the container */
  height: 40px; /* Set height to 40px */
  padding: 5px; /* Padding inside the input field */
  box-sizing: border-box; /* Include padding and border in the element's total width and height */
  border-radius: 10px; /* Add border-radius for rounded corners */
}
.caption{
  border-radius: 10px;
  margin-top: -30px;
  background-color: white;
  filter: grayscale(100%);
  overflow: hidden;
  padding: 10px 10px;
  position: relative;
}
.headretrive{
  left: 4.5rem;
  margin-top: -50px;
  position: absolute;
  font-family: 'Pacifico', cursive;
  text-shadow: 3px 3px 6px rgba(250, 243, 243, 0.929);
}
.BgBlur {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(8, 8, 8, 0.749);
}

.closeImageCaro {
  position: absolute;
  top: 20px;
  right: 20px;
  cursor: pointer;
  z-index: 9999; /* Ensure it's above other elements */
}
.closeImageCaro:hover{
  font-size: 30px;
  color: red;
}

.PrevImageCaro,
.NextImageCaro {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  cursor: pointer;
  padding: 10px;
  border-radius: 10px;
  background-color: #ffffff; /* Bright background color */
  color: #333333; /* Dark text color */
  font-weight: bold;
  z-index: 9999; /* Ensure it's above other elements */
}

.PrevImageCaro {
  left: 25%;
}

.NextImageCaro {
  right: 25%;
}

.EditCaption {
  margin-top: auto; /* Adjust as needed */
  width: calc(100% - 120px);
  height: 100px; /* Adjust for padding and margin */
  padding: 10px; /* Add padding for better appearance */
  border: 1px solid #ccc; /* Add border for clarity */
  border-radius: 5px;
  margin-left: 60px; /* Adjust as needed */
  margin-right: 60px; /* Adjust as needed */
  resize: none; /* Disable textarea resizing */
}

.submitEditImage {
  font-size:bolder;
  border-radius: 20px;
  background-color: rgba(22, 22, 217, 0.775);
  padding: 10px;
  color: #ccc;
  padding-right:20px;
  padding-left: 20px;
  cursor: pointer;
  position: relative;
  bottom: -25px;
  left: 45%;
  transform: translateX(-50%);
  margin-top: 20px;
  margin-bottom: 20px;
}

.DataId {
  padding: 10px;
  background-color: #333333;
  border-radius: 5px;
  position: absolute;
  color: white;
  top: 20px;
  left: 20px;
  z-index: 9999; /* Ensure it's above other elements */
}

.image-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  overflow: hidden; /* Set a maximum height for the carousel */
  position: relative; /* Position for the navigation buttons */
}

.carousel-image {
  width:600px; /* Adjust the width of each image */
  height:500px;
  margin: 5px; /* Adjust the margin between images */
  transition: transform 0.3s ease;
  position: relative;
  border: 2px solid rgba(0, 0, 0, 0.2); /* Border with opacity */
  border-radius: 10px;
}
.image-icons-additional {
  position: absolute;
  top: 70px;
  left: 100px;
  display: flex;
  z-index: 1; /* Ensure it's above other elements */
  background-color: rgba(0, 0, 0, 0.833);
  border-radius: 20px;
  padding: 10px;
  justify-content: space-between;
  margin: 10px;
}

.add-icon,
.crop-icon,
.delete-icon {
  margin: 0 5px;
  cursor: pointer;
  font-size: 20px;
}

.add-icon:hover,
.crop-icon:hover,
.delete-icon:hover {
  font-weight: bolder;
  color: red;
  font-size: +30px;
}
.AddonImage{
  border-radius: 20px;
  background-color: rgba(47, 47, 215, 0.703);
  position:relative;
  padding: 5px;
  color: #ccc;
  padding-right:20px;
  padding-left: 20px;
  cursor: pointer;
}
</style>
