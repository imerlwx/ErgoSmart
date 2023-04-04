<script>
import { getTrainings, saveTrainingResult, retrain, getRetrainStatus, saveNewSol } from "../service/user";
import { ElMessage } from "element-plus";
import { reasonMap } from '../config';
import jsonSolutions from '../../../file.json';

export default {
    data() {
        return {
            trainings: [],
            retrainDisabled: false,
            solutions: jsonSolutions,
            newSol: ""
        }
    },
    created() {
        this.init()
    },
    methods: {
        saveResult(t, newSol) {
            saveTrainingResult(t.id, t.file, t.result,t.uploader_id).then(res => {
                if (res.code === 0) {
                    ElMessage({
                        type: 'success',
                        message: 'Save successfully',
                    })
                }
            }),
            saveNewSol(t.prob_id, newSol)
        },
        getReason(type) {
            return reasonMap[type]
        },
        handleRetrain() {
            if (this.retrainDisabled) return
            retrain().then(res => console.log(res))
        },
        async init() {
            const trainingsRes = await getTrainings();
            this.trainings = trainingsRes
            const status = await getRetrainStatus();
            if (status.code === 0) {
                this.retrainDisabled = false
            } else {
                this.retrainDisabled = true
            }
        }
    }
}
</script>

<template>
    <main>
        <el-empty v-if="trainings && trainings.length === 0" description="No submission yet" />
        <ul v-else>
            <li v-for='t in trainings' :key='t.id'>
                <div class="list-item">
                    <div><img :src="'images/' + t.file" alt="" /></div>
                    <div class="result">
                        <p>Problem:</p>
                        <el-input type="textarea" resize="none" rows="4" v-model="t.result" :style="{fontSize: '16px'}"></el-input>
                        <p>New Solution:</p>
                        <el-input type="textarea" resize="none" rows="8" v-model="newSol" :style="{fontSize: '16px'}"></el-input>
                        <!-- <el-input type="textarea" resize="none" rows="4" v-model="t.result"></el-input> -->
                        <!-- <el-input type="textarea" resize="none" rows="4">{{ solutions }}</el-input> -->
                        <!-- <div v-for="(num, sol) in solutions[t.prob_id]">{{ sol }}</div> -->
                        
                        <div class="save"><el-button type="info" @click="saveResult(t, newSol)">Save</el-button></div>
                    </div>
                    <div>
                        <p>Original Solutions:</p>
                        <el-card class="scrollable">
                            <ol>
                                <li v-for="(num, sol) in solutions[t.prob_id]" :key="sol">
                                    <p>{{ sol.split("@")[0] }}</p>
                                </li>
                            </ol>
                        </el-card>
                        <br>
                        <p>User Feedback:</p>
                        <el-card class="feedback">
                            <p>
                                <el-radio :checked="true">
                                    {{ getReason(t.reason) }}</el-radio>
                            </p>
                            <div>
                                Other feedback:
                            </div>
                            <p class="other-feedback">
                                {{ t.feedback }}
                            </p>
                            <div class="rating">Rating: <el-rate disabled :model-value="t.rating" show-score /></div>
                        </el-card>
                    </div>
                    
                </div>
                <el-divider />
            </li>

        </ul>
    </main>
    <div v-if="trainings.length > 0" class="retrain">
        <el-tooltip effect="dark" content="Training is in process. Please wait..." placement="top"
            :disabled="!retrainDisabled">
            <div class="retrain-button-wrapper">
                <el-button type="info" :disabled="retrainDisabled" @click="handleRetrain">Retrain the model</el-button>
            </div>
        </el-tooltip>
    </div>
</template>

<style scoped>
main {
    max-width: 1200px;
    margin: 0 auto;
    box-sizing: border-box;
    padding: 30px 50px;
    position: relative;
    height: calc(100% - 140px);
    overflow-y: auto;
}

ul {
    width: 100%;
}

.list-item {
    display: flex;
    justify-content: space-between;
    height: 400px;
}

.list-item>* {
    flex-basis: 32%;
}

.list-item img {
    width: 100%;
    height: 100%;
    object-fit: contain;
}

.result {
    position: relative;
}

.result .save {
    position: absolute;
    bottom: 0;
    right: 0;
}

.feedback {
    width: 100%;
    height: 170px;
    border-radius: 5px;
    box-sizing: border-box;
    line-height: 1.5;
    overflow-y: auto;
}

.feedback p {
    margin-bottom: 8px;
    word-break: break-all;
}

.feedback p .el-radio {
    white-space: break-spaces;
    word-break: break-word;
}

.retrain {
    position: absolute;
    bottom: 12px;
    right: 0;
    text-align: center;
    left: 0;
}

.retrain-button-wrapper {
    display: inline-block;
}

.scrollable {
    height: 170px;
    overflow: auto;
}
</style>
