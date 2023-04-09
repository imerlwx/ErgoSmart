<!-- 

<template>
    <div>
      <video ref="video" width="640" height="480"></video>
      <button @click="takePhoto">Take Photo</button>
      <canvas ref="canvas" width="640" height="480"></canvas>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        stream: null,
        photoDataUrl: null
      }
    },
    mounted() {
      this.startCamera();
    },
    methods: {
      async startCamera() {
        try {
          this.stream = await navigator.mediaDevices.getUserMedia({video: true});
          this.$refs.video.srcObject = this.stream;
          this.$refs.video.play();
          
        } catch (error) {
          console.log(error);
        }
      },
      takePhoto() {
        const context = this.$refs.canvas.getContext('2d');
        context.drawImage(this.$refs.video, 0, 0, this.$refs.canvas.width, this.$refs.canvas.height);
        this.photoDataUrl = this.$refs.canvas.toDataURL('image/jpeg');
      }
    },
    beforeDestroy() {
      if (this.stream) {
        this.stream.getTracks().forEach(function (track) {
          track.stop();
        });
      }
    }
  }
  </script>
   -->

<template>
  <div class="camera-container">
    <video width="480" height="360" v-if="photoTaken === false" ref="video" autoplay></video>
    <canvas width="0" height="0" ref="canvas"></canvas>
    <br>
    <el-button type="primary" @click="capture">Capture</el-button>
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
      this.$refs.video.pause();
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
      this.mediaStream.getTracks()[0].stop();
      this.dataURL = canvas.toDataURL();
      localStorage.setItem('dataURL', this.dataURL);
      this.isCaptured = true;
      this.$emit('eventname', this.isCaptured)

    }
  }
}

</script>
