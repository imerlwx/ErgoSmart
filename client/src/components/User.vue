<script setup>
import { reactive, ref } from 'vue'
import { submitResult, getTrainResult } from "../service/user";
import { ElMessageBox } from 'element-plus'
import { reasonMap } from '../config'
import { Plus } from '@element-plus/icons-vue'
const formdata = reactive({
    fileList: [],
    satisfied: null,
    reason: '',
    result: "",
    feedback: "",
    rating: 0,
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
        formdata.result = res.result
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
            const { fileList, reason, feedback, result, satisfied, rating } = formdata
            const file = fileList[fileList.length - 1].raw;
            const res = await submitResult({ file, result, satisfied, rating, reason, feedback, userId })
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

<template>
    <main>
        <el-form ref="formRef" :model="formdata">
            <div class="upload-container">
                <el-form-item prop="fileList" :rules="[{
                    required: true,
                    message: 'Please upload a picture'
                }]" class="upload">
                    <el-upload :show-file-list="false" class="upload-area" :auto-upload="false" :on-change="getResult"
                        v-model:file-list="formdata.fileList">
                        <img v-if="imgSrc" :src="imgSrc" />
                        <!-- <img v-if="imgSrc" :src="imgSrc" />
                                <div v-else class="upload-placeholder"></div>
                                <el-button class="upload-button" type="primary">select file</el-button> -->
                        <el-icon v-else class="avatar-uploader-icon">
                            <Plus />
                        </el-icon>
                        <template #tip>
                            <div class="el-upload__tip">
                                upload a file
                            </div>
                        </template>
                    </el-upload>
                </el-form-item>
            </div>
            <div class="result">
                <h1>AI-generated results</h1>
                <div class="result-box">{{ formdata.result }}</div>
                <el-form-item prop="satisfied" :rules="[{
                    required: true,
                    message: 'Please give a reason'
                }]">
                    <el-radio-group v-model="formdata.satisfied">
                        <el-radio :label="1">Looks good</el-radio>
                        <el-radio :label="0">I don't like the result</el-radio>
                    </el-radio-group>
                </el-form-item>
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
    height: 200px;
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
</style>