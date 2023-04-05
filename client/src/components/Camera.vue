<script>
export default {
    data() {
        return {
            mediaStream: null,
            imageCapture: null,
        };
    },
    mounted() {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(stream => {
                this.mediaStream = stream;
                this.$refs.video.srcObject = stream;
                this.$refs.video.play();
                const track = stream.getVideoTracks()[0];
                this.imageCapture = new ImageCapture(track);
            })
            .catch(err => {
                console.error(`Failed to access camera: ${err}`);
            });
    },
    beforeDestroy() {
        this.mediaStream.getTracks().forEach(track => {
            track.stop();
        });
    },
    methods: {
        async takePhoto() {
            const blob = await this.imageCapture.takePhoto();
            // Do something with the captured photo blob, e.g. display it
            // console.log(blob);
            return blob;
        },
    },
}
</script>

<template>
    <div>
        <video id="camera-stream" ref="video"></video>
        <button @click="takePhoto">Take Photo</button>
    </div>
</template>