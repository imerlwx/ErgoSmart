// Defines all basic properties and methods to correspond to the server side
// const url = "http://localhost:5000";
const url = "/api";
export function login(userInfo) {
   return fetch(url + "/login", {
      method: "POST",
      body: JSON.stringify(userInfo),
      headers: {
         "Content-Type": "application/json",
      },
   })
      .then(resp => resp.json())
      .catch((err) => console.error(err));
}

export function register(userInfo) {
   return fetch(url + "/register", {
      method: "POST",
      body: JSON.stringify(userInfo),
      headers: {
         "Content-Type": "application/json",
      },
   })
      .then(resp => resp.json())
      .catch((err) => console.error(err));
}

export function getTrainResult(file) {
   const formdata = new FormData()
   formdata.append('file', file)
   return fetch(url + "/training/caption", {
      method: "POST",
      body: formdata
   })
      .then(resp => resp.json())
      .catch((err) => console.error(err));
}

export function submitResult(payload) {
   const endpoint = payload.satisfied ? '/submit/satisfied' : '/submit/unsatisfied'
   const formdata = new FormData()
   for (const key in payload) {
      formdata.append(key, payload[key])
   }
   return fetch(url + endpoint, {
      method: "POST",
      body: formdata
   })
      .then(resp => resp.json())
      .catch((err) => console.error(err));
}

export function getTrainings() {
   return fetch(url + "/training", {
      method: "GET"
   })
      .then(resp => resp.json())
      .catch((err) => console.error(err));
}

export function saveTrainingResult(id, file, result, uploader_id) {
   return fetch(url + "/training", {
      method: "PUT",
      body: JSON.stringify({ id, file, result, uploader_id }),
      headers: {
         "Content-Type": "application/json",
      }
   })
      .then(resp => resp.json())
      .catch((err) => console.error(err));
}

export function getRetrainStatus() {
   return fetch(url + "/training/retrain", {
      method: "GET"
   })
      .then(resp => resp.json())
      .catch((err) => console.error(err));
}

export function retrain() {
   return fetch(url + "/training/retrain/start", {
      method: "GET"
   })
      .then(resp => resp.json())
      .catch((err) => console.error(err));
}

export function saveNewSol(prob_id, newSol) {
   console.log(newSol);
   return fetch(url + "/newsol", {
      method: "POST",
      body: JSON.stringify({prob_id, newSol})
   })
      .then(resp => resp.json())
      .catch((err) => console.error(err));
}
