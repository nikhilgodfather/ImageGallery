<template>
  <div id="AddImage" class="upload-image" @dragover.prevent @drop="handleDrop" :class="{ 'drag-over': isDragging }">
    <H1 class="headadd">Capture Moments, Create Memories.</H1>
    <div class="drag-drop-text">
      <p>Drag & Drop your images here</p>
    
      <input type="file" id="file-upload" multiple @change="handleFileChange" style="display: none;">
      <label for="file-upload" class="upload-button">Select Images</label>
      <br>
      <!-- Optional: Caption Input -->
      <textarea class="caption-textarea" v-model="caption" placeholder="Enter image caption (optional)"></textarea>

      <div v-if="imageUrls.length > 0" class="preview">
        <div v-for="(url, index) in imageUrls" :key="index" class="preview-item">
          <img :src="url" alt="Uploaded Image">
          <button @click="removeImage(index)" class="close-button">&times;</button>
          <br>
        </div>
        <button @click="uploadImages" class="upload-all-button">Upload All Images</button>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      imageUrls: [],
      isDragging: false,
      filesToUpload: [],
      caption: '',
      csrfToken: null,
    };
  },
  mounted() {
    // Fetch CSRF token from Django backend
    fetch('http://127.0.0.1:8000/get_csrf_token/')
      .then(response => response.json())
      .then(data => {
        this.csrfToken = data.csrf_token;
      })
      .catch(error => {
        console.error('Error fetching CSRF token:', error);
      });
  },
  methods: {
    handleFileChange(event) {
      const files = event.target.files;
      if (!files || files.length === 0) return;

      for (let i = 0; i < files.length; i++) {
        this.processFile(files[i]);
      }
    },
    handleDrop(event) {
      event.preventDefault();
      this.isDragging = false;

      const files = event.dataTransfer.files;
      if (!files || files.length === 0) return;

      for (let i = 0; i < files.length; i++) {
        this.processFile(files[i]);
      }
    },
    processFile(file) {
      // Validate if the file is an image
      if (!file.type.startsWith('image/')) {
        alert('Please select an image file.');
        return;
      }

      // Read the image file as a Data URL
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => {
        this.imageUrls.push(reader.result);
        this.filesToUpload.push(file);
      };
    },
    removeImage(index) {
      this.imageUrls.splice(index, 1);
      this.filesToUpload.splice(index, 1);
    },
    uploadImages() {
      const formData = new FormData();
      this.filesToUpload.forEach(file => {
        formData.append('images', file);
        formData.append('caption', this.caption);
      });

      formData.append('imageTitle', this.imageTitle); // Append imageTitle to FormData
      
      const headers = new Headers({
        'X-CSRFToken': this.csrfToken
      });
      
      fetch('http://localhost:8000/upload/', {
        method: 'POST',
        body: formData,
        headers: headers,
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to upload images.');
        }
        this.imageUrls = [];
        this.filesToUpload = [];
        this.imageTitle = '';
        this.caption='';
        alert('Images uploaded successfully.');
        window.location.reload();

      })
      .catch(error => {
        console.error('Error uploading images:', error);
        alert('Failed to upload images.');
      });
    }
  }
};
</script>

<style scoped>
.upload-image {
  text-align: center;
  padding: 400px;
  position: relative;
}
.upload-image.drag-over {
  background-color: #f0f0f0;
}
.preview {
  margin-top: 20px;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}
.preview-item {
  position: relative;
  margin: 10px;
}
.preview img {
  max-width: 200px;
  max-height: 200px;
}
.close-button {
  position: absolute;
  top: 5px;
  right: 5px;
  background: transparent;
  border: none;
  color: red;
  font-weight: bolder;
  font-size: 24px;
  cursor: pointer;
  outline: none;
}
.upload-button, .upload-all-button {
  margin-top: 10px;
  padding: 10px 20px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  outline: none;
}
.drag-drop-text {
  position: absolute;
  top: 50%;
  left: 50%;
  padding: 50px 100px;
  transform: translate(-50%, -50%);
  background-color: #fff;
  border-radius: 10px;
}
.drag-drop-text p {
  margin: 0;
  font-size: 18px;
  color: #999;
}
.headadd{
  position: absolute;
  left: 4.5rem;
  margin-top:-300px;
  text-shadow: 3px 3px 6px rgba(250, 243, 243, 0.929);
  font-family: 'Pacifico', cursive;
}
.caption-textarea {
  width: 100%; /* Set the width to 100% of its container */
  min-height: 100px; /* Set a minimum height to ensure it's visible */
  padding: 10px; /* Add padding for better readability */
  box-sizing: border-box; /* Include padding and border in the element's total width */
}
</style>
