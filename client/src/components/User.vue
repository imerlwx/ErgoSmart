<script setup>
import { reactive, ref } from 'vue'
import { submitResult, getTrainResult } from "../service/user";
import { ElMessageBox } from 'element-plus'
import { reasonMap } from '../config'
import { UploadFilled } from '@element-plus/icons-vue'
import Camera from './Camera.vue'

const formdata = reactive({
    fileList: [],
    satisfied: null,
    reason: '',
    result: "",
    solution: "",
    feedback: "",
    rating: 0,
    userChoice: null,
    maxIndex: null,
    sortRes: "",
    // camera: null,
    // dtURL:null,
})
const imgSrc = ref('')
const formRef = ref();
const generated = ref(false)

async function getResult(uploadFile) {
    // first show image
    const reader = new FileReader();
    const f = uploadFile.raw
    reader.readAsDataURL(f);
    reader.onload = async (re) => {
        imgSrc.value = re.target.result;
        const res = await getTrainResult(f)
        const prob_ans = res.result
        const prob = prob_ans.prob
        const ans = prob_ans.res
        formdata.result = prob
        formdata.solution = ans
        formdata.maxIndex = prob_ans.maxIndex
        formdata.sortRes = prob_ans.sortRes
    };
    generated.value = true
}
function dataURLtoBlob(dataurl) {
    var arr = dataurl.split(','), mime = arr[0].match(/:(.*?);/)[1],
        bstr = atob(arr[1]), n = bstr.length, u8arr = new Uint8Array(n);
    while(n--){
        u8arr[n] = bstr.charCodeAt(n);
    }
    return new Blob([u8arr], {type:mime});
}
async function getImage () {
    console.log("aaaa")
    const reader = new FileReader();
    const f = dataURLtoBlob(localStorage.getItem('dataURL'));
    reader.readAsDataURL(f);
    reader.onload = async (re) => {
        imgSrc.value = re.target.result;
        const res = await getTrainResult(f)
        const prob_ans = res.result
        const prob = prob_ans.prob
        const ans = prob_ans.res
        formdata.result = prob
        formdata.solution = ans
        formdata.maxIndex = prob_ans.maxIndex
        formdata.sortRes = prob_ans.sortRes
    };
    generated.value = true
}

function checkRate(rule, value, callback) {
    if (value < 1) {
        callback(new Error('Please rate the result'))
    } else {
        callback()
    }
}
function handleSubmit(formEl) {
    if (!formEl) return;
    formEl.validate(async (valid) => {
        if (valid) {
            console.log('submit!')
            const userId = JSON.parse(localStorage.getItem('user')).id
            const { fileList, reason, feedback, result, satisfied, rating, userChoice, maxIndex } = formdata
            const file = fileList[fileList.length - 1].raw;
            const res = await submitResult({ file, result, satisfied, rating, reason, feedback, userId, userChoice, maxIndex })
            ElMessageBox.alert('Success! Thank you for your feedback', 'Message', {
                // if you want to disable its autofocus
                // autofocus: false,
                confirmButtonText: 'OK',
                callback: (action) => {
                    window.location.reload()
                },
            })
        } else {
            console.log('error submit!')
            return false
        }
    })
}


</script>
<script>
export default {
    data() {
        return {
            url: "",
            // dtURL: "",
        }
    },
    components: {
        Camera
    },
    methods: {
        getDTURL() {
            const dtURL = localStorage.getItem('dtURL')
            return dtURL
        },
        getURL(urlString) { return urlString.split("@")[1] },
        dataURLtoBlob(dataurl) {
            var arr = dataurl.split(','), mime = arr[0].match(/:(.*?);/)[1],
                bstr = atob(arr[1]), n = bstr.length, u8arr = new Uint8Array(n);
            while(n--){
                u8arr[n] = bstr.charCodeAt(n);
            }
            return new Blob([u8arr], {type:mime});
        },
        getImage () {
            const reader = new FileReader();
            const f = dataURLtoBlob(localStorage.getItem('dataURL'));
            reader.readAsDataURL(f);
            reader.onload = async (re) => {
                imgSrc.value = re.target.result;
                const res = await getTrainResult(f)
                const prob_ans = res.result
                const prob = prob_ans.prob
                const ans = prob_ans.res
                formdata.result = prob
                formdata.solution = ans
                formdata.maxIndex = prob_ans.maxIndex
                formdata.sortRes = prob_ans.sortRes
            };
            generated.value = true
        },
    }
    // mounted() {
    //     // setTimeout(() => {
	// 	// 		this.$nextTick(() => {
	// 	// 			console.log(this.$refs.camera.dataURL);
    //     //             this.dtURL = this.$refs.camera.dataURL
	// 	// 		})
	// 	// 	}, 100);
    //     console.log(this.$refs.camera.dataURL);
    //     formdata.dtURL = this.$refs.camera.dataURL
        
    // },
};
</script>
<template>
    <main>
        
        <div>
            <h1>Welcome!</h1>
            <el-card>
                <h3>Instructions:</h3>
                
                <ul>
                    <li>The ErgoSmart Model could detect ergonomic problems in your image and provide several solutions.</li>
                    <li>The problem and corresponding solutions will be shown on the right.</li>
                    <li>You could choose your favorite solution. That will help us improve the ErgoSmart Model!</li>
                    <li>If you are not satisfied with our results, please let us know and we will give you a new one.</li>
                </ul>
                
            </el-card>
            
            <br>
            <h3>Please upload your image below:</h3>
        </div>
        <el-radio-group v-model="formdata.camera">
                            <el-radio :label="1">Take a photo</el-radio>
                            <el-radio :label="0">Upload an image</el-radio>
        </el-radio-group>
        <template v-if="formdata.camera === 1">
            <div >
                <Camera ref="camera"/>
                <!-- <p>{{ getDTURL() }}</p> -->
                <button @click="getImage"> Use this image</button>
            </div>
        </template>
        <el-form ref="formRef" :model="formdata">
            <template v-if="formdata.camera === 0">

            <div class="upload-container">
                <el-form-item prop="fileList" :rules="[{
                    required: true,
                    message: 'Please upload a picture'
                }]" class="upload">
                    <el-upload :show-file-list="false" class="upload-area" :auto-upload="false" :on-change="getResult"
                        v-model:file-list="formdata.fileList">
                        <img v-if="imgSrc" :src="imgSrc" />
                        <el-icon v-else class="avatar-uploader-icon">
                            <p>
                                <UploadFilled />Click Here to Upload Your Image
                            </p>
                        </el-icon>
                    </el-upload>
                </el-form-item>
            </div>
            </template>
            

            <div class="result">
                <h2 class="loading" v-if="imgSrc && !formdata.result">Generating Results...</h2>
                <div v-if="formdata.result">
                    <h1>AI-generated results</h1>
                    <div class="result-box">{{ formdata.result }}</div>
                    <br>
                    <h3>Solutions:</h3>
                    <ol>
                        <!-- <li v-for="(val, keys) in formdata.solution" :key="keys"> -->
                        <li v-for="(keys, vals) in formdata.sortRes" :key="keys">
                            <!-- <p>{{ vals }}</p> -->
                            <p>{{ keys[0].split("@")[0] }}</p>
                            <div v-if="getURL(keys[0])">
                                <a v-bind:href="getURL(keys[0])">Product Link</a>
                            </div>

                        </li>
                    </ol>
                    <h3>Are you satisfied with the problem and solutions?</h3>
                    <el-form-item prop="satisfied" :rules="[{
                        required: true,
                        message: 'Please give a reason'
                    }]">
                        <el-radio-group v-model="formdata.satisfied">
                            <el-radio :label="1">Looks good</el-radio>
                            <el-radio :label="0">I don't like the result</el-radio>
                        </el-radio-group>
                    </el-form-item>

                    <template v-if="formdata.satisfied === 1">
                        <h3>Which answer do you prefer?</h3>
                        <el-form-item prop="userChoice" :rules="[{
                            required: true,
                            message: 'Please give your top choice'
                        }]">
                            <el-radio-group v-model="formdata.userChoice">
                                <!-- <el-radio v-for="(val, key, index) in Object.values(formdata.solution).sort().reverse()" :label="key">{{ index + 1 }}</el-radio> -->
                                <el-radio v-for="(key, index) in formdata.sortRes" :label="key[0]">{{ index + 1
                                }}</el-radio>
                            </el-radio-group>
                        </el-form-item>
                    </template>

                    <template v-if="formdata.satisfied === 0">
                        <el-form-item prop="feedback">
                            <el-input v-model="formdata.feedback" maxlength="150" placeholder="Give some feedback"
                                show-word-limit type="textarea" />
                        </el-form-item>
                        <el-form-item class="reason" prop="reason" :rules="[{
                            required: true,
                            message: 'Please select one of the reasons'
                        }]"><el-radio-group v-model="formdata.reason" class="ml-4">
                                <el-radio label="type-1" size="large">{{ reasonMap['type-1'] }}</el-radio>
                                <el-radio label="type-2" size="large">{{ reasonMap['type-2'] }}</el-radio>
                                <el-radio label="type-3" size="large">{{ reasonMap['type-3'] }}</el-radio>
                            </el-radio-group>
                        </el-form-item>
                    </template>
                    <h3>Rate the result</h3>
                    <el-form-item prop="rating" :rules="[{
                        validator: checkRate
                    }]"><el-rate @change="" v-model="formdata.rating"
                            :texts="['oops', 'disappointed', 'normal', 'good', 'great']" show-text />
                    </el-form-item>
                    <div class="submit">
                        <el-button type="primary" @click="handleSubmit(formRef)">Submit</el-button>
                    </div>
                </div>
            </div>
        </el-form>
    </main>
</template>

<style>
.upload-area .el-upload {
    width: 100%;
}
</style>

<style scoped>
main {
    box-sizing: border-box;
    padding: 70px 24px;
    max-width: 1200px;
    margin: 0 auto;
}

main form {
    display: flex;
}

.upload-container {
    width: 50%;
    text-align: center;
}

.upload {
    width: 100%;
    font-size: 24px;
}

.upload .upload-area {
    width: 100%;
}

.el-icon.avatar-uploader-icon {
    font-size: 28px;
    color: #8c939d;
    width: 178px;
    width: 100%;
    text-align: center;
    display: inline-flex;
    height: 100%;
    padding-top: 50%;
    padding-bottom: 50%;
    border: 1px dashed var(--el-border-color);
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    transition: var(--el-transition-duration-fast);
}

.el-icon.avatar-uploader-icon:hover {
    border-color: var(--el-color-primary);
}

.upload img {
    width: 100%;
}

.upload-button {
    margin: auto;
}

.result {
    width: 50%;
    padding: 0 24px;
    box-sizing: border-box;
}

.result>* {
    margin-bottom: 24px;
}

.result h1 {
    text-align: center;
}

.result .submit {
    text-align: center;
}

.reason .el-form-item__content .el-radio-group .el-radio .el-radio__label {
    white-space: break-spaces;
}


.result-box {
    width: 100%;
    height: 80px;
    /* margin-top: 24px; */
    border: 1px solid black;
    box-sizing: border-box;
    text-align: left;
    padding: 8px;
    overflow: auto;
}

.result .Rate {
    height: 40px;
}

.loading {
    text-align: center;
}
</style>