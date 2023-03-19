# ErgoSmart: Image Captioning-based Explanation of Ergonomic Problems and Solutions for Workers-AI Interaction

Many construction workers suffer from musculoskeletal disorders (e.g., back pain) due to awkward postures, repetitive tasks, etc. Identifying ergonomic problems and solutions can reduce ergonomic risks.

Ergonomics aims to reduce physical injuries and stress while improving productivity in the workplace. However, workers are unaware of ergonomics due to the lack of ergonomists and ergonomic programs. Thus, the automated explanation of ergonomic problems and solutions to workers is required.

ErgoSmart is a human-AI web application that provides an explanation of ergonomic problems and solutions for workers based on Image Captioning. It provides an interface for users to interact with and provide feedback to the ergonomists. It also provides an interface for ergonomists to correct the captions and retrain the model.

A more detailed explanation of this project can be found [here](https://docs.google.com/presentation/d/1qjgZQcWyX7kHJuNBWinw8790suzKnGE-Ca48_1SRZik/edit?usp=sharing).

## Recommended IDE Setup and Customize Configuration

These are not required but recommended. [VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur) + [TypeScript Vue Plugin (Volar)](https://marketplace.visualstudio.com/items?itemName=Vue.vscode-typescript-vue-plugin). See [Vite Configuration Reference](https://vitejs.dev/config/). These tools could help get started developing Vue 3 in Vite.

## Installation

Because the project includes training and retraining process, first download the [dataset and model](https://drive.google.com/drive/folders/1xRyO-mf217_pEb30j0b-gmRVbmhoGdtW?usp=sharing) and put them at the position as showing below.
```bash
$ pwd
/Users/username/src/ergosmart-master/server/model/__src
$ ls
ErgoSolCap.py	captions	folder		model.pth
```

Python virtual environment is not required but highly recommended. First, make sure the Python version is at least 3.9

```bash
$ python3 --version
Python 3.9.16
```

Open two terminal windows, and cd into the client and server folders separately. Create the virtual environment in the server folder and activate it. 

```bash
$ pwd
/Users/username/src/ergosmart-master/server
$ python3 -m venv env
$ source env/bin/activate
```

Then upgrade the Python tools in your virtual environment.
```bash
$ pip install --upgrade pip setuptools wheel
```

Install the package dependencies.
```bash
$ pip install -r requirements.txt
```
**Warning**: If you are using a mac, just delete the following two lines in the requirements.txt.
```txt
pywin32==305
pypiwin32==223
```

Next, set up the client in the client folder.
```bash
$ pwd
/Users/username/src/ergosmart-master/client
$ npm install
```

## Usage

In the server folder, run the main.py directly. Your output might be different.
```bash
$ pwd
/Users/username/src/ergosmart-master/server
$ python main.py
 * Serving Flask app 'main'
 * Debug mode: on
 ...
```

In the client folder, compile, and hot-reload for development. Your output might be different.

```bash
$ pwd
/Users/username/src/ergosmart-master/client
$ npm run dev
> client2@0.0.0 dev
> vite
  VITE v4.1.4  ready in 581 ms
  ...
```

If you need to compile and minify for production, run the following command.
```bash
$ npm run build
```

Then, browse to your [localhost](http://localhost:5173/) and start using ErgoSmart!

## Contributing
This work is done by Gunwoo Yong, Hongrui Liu, Sijia Li, Wengxi Li as a human-AI interaction and system project.

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)