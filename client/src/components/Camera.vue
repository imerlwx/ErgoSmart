<template>
  <div class="camera-container">
    <video width="480" height="360" ref="video" autoplay></video>
    <br>
    <el-button type="primary" @click="capture">Capture</el-button>
    <br>
    <canvas width="0" height="0" ref="canvas"></canvas>

    
    <!-- <el-button type="primary" @click="recapture">Recapture</el-button> -->
  </div>
</template>

<script>

export default {
  name: "Camera",
  data() {
    return {
      mediaStream: null,
      photoTaken: false,
      dataURL: null,
      isCaptured: false,
    }
  },
  mounted() {
    // Request access to the camera
    navigator.mediaDevices.getUserMedia({ video: true })
      .then(stream => {
        // Set the mediaStream to the camera stream
        this.mediaStream = stream;
        // Set the video source to the camera stream
        this.$refs.video.srcObject = stream;
      })
      .catch(err => {
        console.log("Unable to access camera", err);
      });
  },
  // props: {
  //   isCaptured: Boolean
  // },
  methods: {
    capture() {
      // Set photoTaken to true to show the captured photo
      this.photoTaken = true;
      // Pause the video stream
      // this.$refs.video.pause();
      // Get the canvas element
      const canvas = this.$refs.canvas;
      // Set the canvas dimensions to match the video dimensions
      // canvas.width = this.$refs.video.videoWidth;
      // canvas.height = this.$refs.video.videoHeight;
      canvas.width = '480';
      canvas.height = '360';
      // Draw the video frame onto the canvas
      const ctx = canvas.getContext("2d");
      ctx.drawImage(this.$refs.video, 0, 0, canvas.width, canvas.height);
      // Stop the camera stream
      // this.mediaStream.getTracks()[0].stop();
      this.dataURL = canvas.toDataURL();
      localStorage.setItem('dataURL', this.dataURL);
      this.isCaptured = true;
      this.$emit('eventname', this.isCaptured)

    },
    // recapture() {
    //   this.photoTaken = false;
    // }
  }
}

</script>
