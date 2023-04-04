from flask import Flask
from flask import request, jsonify, send_file
from flask_cors import CORS
from db import user_register, user_login, db_init, submitSatisfied, submitUnSatisfied, getAllUnsatisfied, saveTrainingResult, retrain_model, getUserById
from util.index import random_filename
from util.send import sendEmail
from model.main import TrainingModel
import asyncio
from util.send import sendEmail
import json
import os


app = Flask(__name__)
CORS(origins='http://localhost:3000')
model = TrainingModel()
loop = asyncio.get_event_loop()
is_running = False


async def work1():
    global is_running
    is_running = True
    retrain_model()
    model.retrain()
    is_running = False


def getImagePath(fname):
    return './model/__src/Images/' + fname

def getPath(filename):
    return os.path.join(CUR_DIR, filename)

CUR_DIR = os.path.dirname(__file__)


def writeJson(maxIndex, userChoice, filePath):
    with open(filePath, "r") as f:
        data = json.load(f)

    data[maxIndex][userChoice] += 1
    with open(filePath, "w") as f:
        json.dump(data, f)

def writeNewSol(prob_id, new_sol, filePath):
    with open(filePath, "r") as f:
        data = json.load(f)

    data[prob_id][new_sol] = 0
    with open(filePath, "w") as f:
        json.dump(data, f)

@app.post('/login')
def login():
    # print(request.form)
    user_data = request.get_json()
    # add here the code to create the user
    user = user_login(user_data)
    if user:
        id, email, role, password = user
        res = jsonify({"code": 0, "result":  {
            "id": id,
            "email": email,
            "role": role
        }})
    else:
        res = jsonify({"code": 1, 'error': 'user not found'})
    res.status_code = 200
    return res


@app.post('/register')
def register():
    user_data = request.get_json()
    # add here the code to create the user
    user = user_register(user_data)

    if user == None:
        res = jsonify({'error': 'user already registered', "code": 1})
    else:
        id, email, role, password = user
        res = jsonify({"code": 0, "result": {
            "id": id,
            "email": email,
            "role": role
        }})
    res.status_code = 200
    return res


@app.post('/submit/satisfied')
def submitSatisfiedResult():
    # file, result, satisfied, rating, reason, feedback
    formdata = request.form
    file = request.files.get('file')
    fname = random_filename(file.filename)
    path = getImagePath(fname)
    file.save(path)
    data = {
        "file": fname,
        "result": formdata.get('result'),
        "rating": formdata.get('rating'),
        "reason": formdata.get('reason'),
        "userId": formdata.get('userId')
    }
    userChoice = formdata.get('userChoice')
    maxIndex = formdata.get('maxIndex')
    DATA_DIR = getPath('../file.json')
    writeJson(maxIndex, userChoice, filePath=DATA_DIR)
    submitSatisfied(data)
    return {"code": 0}


@app.post('/submit/unsatisfied')
def submitUnsatisfiedResult():
    # file, result, satisfied, rating, reason, feedback
    formdata = request.form
    file = request.files.get('file')
    fname = random_filename(file.filename)
    path = getImagePath(fname)
    file.save(path)
    model.modify_cap_expert(fname,formdata.get('result'))
    data = {
        "file": fname,
        "result": formdata.get('result'),
        "rating": formdata.get('rating'),
        "reason": formdata.get('reason'),
        "feedback": formdata.get('feedback'),
        "userId": formdata.get('userId'),
        "uploader_id": formdata.get('userId'),
        "prob_id": formdata.get('maxIndex')
    }
    submitUnSatisfied(data)
    return {"code": 0}

@app.post('/newsol')
def submitNewSol():
    data = request.get_json()
    DATA_DIR = getPath('../file.json')
    writeNewSol(data.prob_id, data.newSol, DATA_DIR)


@app.get('/training')
def getAllTraining():
    return getAllUnsatisfied()


@app.post('/training/caption')
def generateCaption():
    file = request.files.get('file')
    result = model.get_caption(file)
    return {"code" : 0, "result": result}


@app.get('/images/<path>')
def getFile(path=None):
    return send_file(getImagePath(path))


@app.put('/training')
def updateTraining():
    data = request.get_json()
    model.modify_cap_expert(data['file'],data['result'])
    saveTrainingResult(data['id'], data['result'])
    email = getUserById(data['uploader_id'])[1]
    sendEmail(sender='eecs598humanai@outlook.com',
              password="humanaieecs598",
              subject="Training Result",
              receivers=[email],
              content=data['result'],
              image_path=getImagePath(data['file']))
    return {"code": 0}


@app.get('/training/retrain')
def getRetrainStatus():
    global is_running
    if is_running:
        return {"code": 1, "result": 'Training is still running'}
    else:
        return {"code": 0, "result": 'Training hasn\'t started'}


@app.get('/training/retrain/start')
def startRetrain():
    global is_running
    if is_running:
        return {"code": 1, "result": 'still training'}
    else:
        loop.run_until_complete(work1())
        return {"code": 0, "result": 'retrain started'}


if __name__ == '__main__':
    db_init()
    app.run(debug=True, threaded=True)
