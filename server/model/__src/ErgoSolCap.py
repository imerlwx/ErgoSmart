import os, glob, shutil, pickle, random, time
import pandas as pd
import matplotlib.pyplot as plt
import torch
import json

from PIL import Image
from sklearn.model_selection import train_test_split
from datasets import load_dataset, Dataset
from torch.nn.functional import normalize
from torch.utils.data import Dataset, DataLoader
from transformers import AutoProcessor, BlipForConditionalGeneration, BlipForImageTextRetrieval

CUR_DIR = os.path.dirname(__file__)

def getPath(filename):
    return os.path.join(CUR_DIR, filename)


class ImageCaptioningDataset(Dataset):
    """Define the train and test dataset structure for image captioning."""
    def __init__(self, dataset, processor):
        self.dataset = dataset
        self.processor = processor

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        item = self.dataset[idx]
        encoding = self.processor(images=item["image"], text=item["text"], padding="max_length", return_tensors="pt")
        # remove batch dimension
        encoding = {k:v.squeeze() for k,v in encoding.items()}
        return encoding


class ErgoSolCap():
    """Define the model and training process."""
    def __init__(self) -> None:
        self.curDir = os.path.dirname(__file__)
        # self.cap_folderpath = r".\captions"
        self.cap_folderpath = os.path.join(CUR_DIR, "captions")
        self.random_seed = 42
        self.img_W, self.img_H = 128, 128
        self.test_ratio = 0.1
        self.epoch = 1
        self.model = None
        if not os.path.exists(os.path.join(os.getcwd(), getPath('model.pth'))):
            self.get_dataset()
            self.train()


    def get_dataset(self):
        def read_sol_caps(path, sol_cap):
            with open(path, 'r') as file:
                caps = [" ".join([line.strip(), sol_cap]) for line in file if len(line) > 1]
            return list(set(caps))
        
        def read_caps(path):
            with open(path, 'r') as file:
                caps = [line.strip() for line in file if len(line) > 1]
            return list(set(caps))
        
        def load_files(path, glob_filetype="*.jpg"):
            return glob.glob(os.path.join(path, glob_filetype))

        def build_dataset(img_files, caps, df):
            if len(img_files) <= len(caps):
                K = len(img_files)
                picked_caps = random.sample(caps, K)
                return pd.concat([df, pd.DataFrame({"image":img_files, "text":picked_caps})], ignore_index=True)
            else:
                n = len(img_files)//len(caps)
                K = len(img_files) - n*len(caps)
                picked_caps = n*caps + random.sample(caps, K)
                random.shuffle(picked_caps)
                return pd.concat([df, pd.DataFrame({"image":img_files, "text":picked_caps})], ignore_index=True)

        # caps_rebartying_back      = read_caps(os.path.join(self.cap_folderpath, "rebar_tying_back.txt"), "use a rebar tying tool with extension handle.")
        # caps_rebartying_knee      = read_caps(os.path.join(self.cap_folderpath, "rebar_tying_knee.txt"), "use a rebar tying tool with extension handle.")
        # caps_ceilingwork_shoulder = read_caps(os.path.join(self.cap_folderpath, "ceiling_shoulder.txt"), "use a bit extension shaft.")
        # caps_window_shoulder      = read_caps(os.path.join(self.cap_folderpath, "window_shoulder.txt"), "use vacuum lifters.")
        # caps_vibration_hand       = read_caps(os.path.join(self.cap_folderpath, "vibration_hand.txt"), "use reduced vibration power tools.")
        # caps_load_cart            = read_caps(os.path.join(self.cap_folderpath, "load_cart_back.txt"), "use a height adjustable cart.")
        # caps_pick_back            = read_caps(os.path.join(self.cap_folderpath, "pick_product_back.txt"), "raise shelf location.")
        # caps_pick_knee            = read_caps(os.path.join(self.cap_folderpath, "pick_product_knee.txt"), "use a kneeler tool.") + read_caps(os.path.join(self.cap_folderpath, "pick_product_knee.txt"), "use a knee pad.")
        # caps_pick_shoulder        = read_caps(os.path.join(self.cap_folderpath, "pick_product_shoulder.txt"), "use a portable ladder.")
        
        caps_rebartying_back      = read_caps(os.path.join(self.cap_folderpath, "rebar_tying_back.txt"))
        caps_rebartying_knee      = read_caps(os.path.join(self.cap_folderpath, "rebar_tying_knee.txt"))
        caps_ceilingwork_shoulder = read_caps(os.path.join(self.cap_folderpath, "ceiling_shoulder.txt"))
        caps_window_shoulder      = read_caps(os.path.join(self.cap_folderpath, "window_shoulder.txt"))
        caps_vibration_hand       = read_caps(os.path.join(self.cap_folderpath, "vibration_hand.txt"))
        caps_load_cart            = read_caps(os.path.join(self.cap_folderpath, "load_cart_back.txt"))
        caps_pick_back            = read_caps(os.path.join(self.cap_folderpath, "pick_product_back.txt"))
        caps_pick_knee            = read_caps(os.path.join(self.cap_folderpath, "pick_product_knee.txt"))
        caps_pick_shoulder        = read_caps(os.path.join(self.cap_folderpath, "pick_product_shoulder.txt"))

        files_rebartying_back      = load_files(getPath(r".\Images\rebarTying_back"))
        files_rebartying_knee      = load_files(getPath(r".\Images\rebarTying_knee"))
        files_ceilingwork_shoulder = load_files(getPath(r".\Images\overhead_shoulder"))
        files_window_shoulder      = load_files(getPath(r".\Images\window_shoulder"))
        files_vibration_hand       = load_files(getPath(r".\Images\vibration_hand"))
        files_load_cart            = load_files(getPath(r".\Images\load_cart_back"))
        files_pick_back            = load_files(getPath(r".\Images\pick_product_back"))
        files_pick_knee            = load_files(getPath(r".\Images\pick_product_knee"))
        files_pick_shoulder        = load_files(getPath(r".\Images\pick_product_shoulder"))
        print("All files are identified.")

        df = pd.DataFrame({"image":[], "text":[]})
        df = build_dataset(files_rebartying_back     , caps_rebartying_back     , df)
        df = build_dataset(files_rebartying_knee     , caps_rebartying_knee     , df)
        df = build_dataset(files_ceilingwork_shoulder, caps_ceilingwork_shoulder, df)
        df = build_dataset(files_window_shoulder     , caps_window_shoulder     , df)
        df = build_dataset(files_vibration_hand      , caps_vibration_hand      , df)
        df = build_dataset(files_load_cart           , caps_load_cart           , df)
        df = build_dataset(files_pick_back           , caps_pick_back           , df)
        df = build_dataset(files_pick_knee           , caps_pick_knee           , df)
        df = build_dataset(files_pick_shoulder       , caps_pick_shoulder       , df)

        train, test = train_test_split(df, test_size=self.test_ratio, random_state=self.random_seed)
        
        if os.path.exists(getPath("./folder")):
            shutil.rmtree(getPath("./folder"))
        os.mkdir(getPath("./folder"))
        os.mkdir(getPath("./folder/train"))
        os.mkdir(getPath("./folder/test"))
        
        filenames = []
        for file, cap in zip(train["image"], train["text"]):
            filename = file.split("\\")[-1]
            filenames.append(filename)
            new_path = os.path.join(getPath("./folder/train"), filename)
            img = Image.open(file)
            img = img.resize((self.img_W, self.img_H))
            img.save(new_path)

        metadata_train = pd.DataFrame({"file_name":filenames, "text":train["text"]})
        metadata_train.to_csv(getPath("./folder/train/metadata.csv"))

        filenames = []
        for file, cap in zip(test["image"], test["text"]):
            filename = file.split("\\")[-1]
            filenames.append(filename)
            new_path = os.path.join(getPath("./folder/test"), filename)
            img = Image.open(file)
            img = img.resize((self.img_W, self.img_H))
            img.save(new_path)
            
        metadata_test = pd.DataFrame({"file_name":filenames, "text":test["text"]})
        metadata_test.to_csv(getPath("./folder/test/metadata.csv"))
        return print("Dataset is prepared.")


    def train(self):
        """Do the first-time training and testing of the model."""
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(device)

        dataset = load_dataset("imagefolder", data_dir=getPath("./folder"), split="train")

        processor = AutoProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

        train_dataset = ImageCaptioningDataset(dataset, processor)
        train_dataloader = DataLoader(train_dataset, shuffle=True, batch_size=8)

        optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5)
        model.to(device)
        model.train()

        loss_records = []
        start = time.time()

        for epoch in range(1):
            for idx, batch in enumerate(train_dataloader):
                input_ids = batch.pop("input_ids").to(device)
                pixel_values = batch.pop("pixel_values").to(device)

                outputs = model(input_ids=input_ids,
                                pixel_values=pixel_values,
                                labels=input_ids)
                
                loss = outputs.loss

                print("Loss:", loss.item())
                loss_records.append(loss.item())
                loss.backward()

                optimizer.step()
                optimizer.zero_grad()
        print("Time for training is:", time.time() - start)

        torch.save(model, getPath("./model.pth"))
        print("Model is saved.")
        
        self.model = model
        self.processor = processor

        plt.plot(loss_records)
        plt.savefig(getPath("./loss.png"))

        test_dataset = load_dataset("imagefolder", data_dir="./folder", split="test")

        inputs = processor(images=test_dataset["image"], return_tensors="pt").to(device)
        pixel_values = inputs.pixel_values

        generated_ids = model.generate(pixel_values=pixel_values, max_length=50)
        generated_captions = processor.batch_decode(generated_ids, skip_special_tokens=True)

        df = pd.DataFrame({"image": test_dataset["image"], "text": test_dataset["text"], "generated_captions": generated_captions})
        df.to_csv(getPath("./test_result.csv"))


    def load_model(self):
        """Load the trained model."""
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(device)
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        #device = "cuda" if torch.cuda.is_available() else "cpu"
        #print(device)
        #torch.cuda.empty_cache()

        if self.model==None:
            self.model = torch.load(getPath("./model.pth"), map_location=torch.device('cpu'))
        self.processor = AutoProcessor.from_pretrained("Salesforce/blip-image-captioning-base")


    def gen_cap_worker(self, img_filepath):
        """
        Generate captions for the user's uploaded image.
        img_filepath: A single image file path. "JPEG/JPG" file type is recommended.
        This function aims to generate a caption given an image.
        """
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(device)

        img = Image.open(img_filepath)
        img = img.resize((self.img_W, self.img_H))

        inputs = self.processor(images=img, return_tensors="pt").to(device)
        pixel_values = inputs.pixel_values

        generated_ids = self.model.generate(pixel_values=pixel_values, max_length=50)
        generated_captions = self.processor.batch_decode(generated_ids, skip_special_tokens=True)

        """
        Bring ergonomic problem keys and solutions.
        """
        def read_caps(path):
            with open(path, 'r') as file:
                caps = [line.strip() for line in file if len(line) > 1]
            return list(set(caps))
        
        
        refs_rebartying_back      = read_caps(os.path.join(self.cap_folderpath, "rebar_tying_back.txt"))[:5]
        refs_rebartying_knee      = read_caps(os.path.join(self.cap_folderpath, "rebar_tying_knee.txt"))[:5]
        refs_ceilingwork_shoulder = read_caps(os.path.join(self.cap_folderpath, "ceiling_shoulder.txt"))[:5]
        refs_window_shoulder      = read_caps(os.path.join(self.cap_folderpath, "window_shoulder.txt"))[:5]
        refs_vibration_hand       = read_caps(os.path.join(self.cap_folderpath, "vibration_hand.txt"))[:5]
        refs_load_cart            = read_caps(os.path.join(self.cap_folderpath, "load_cart_back.txt"))[:5]
        refs_pick_back            = read_caps(os.path.join(self.cap_folderpath, "pick_product_back.txt"))[:5]
        refs_pick_knee            = read_caps(os.path.join(self.cap_folderpath, "pick_product_knee.txt"))[:5]
        refs_pick_shoulder        = read_caps(os.path.join(self.cap_folderpath, "pick_product_shoulder.txt"))[:5]
    
        
        DATA_DIR = getPath('../../../file.json') 
        with open(DATA_DIR,'r') as f:
            sols = json.load(f)
        print(sols)

        BLIP = BlipForImageTextRetrieval.from_pretrained("Salesforce/blip-itm-base-coco")
        processor = AutoProcessor.from_pretrained("Salesforce/blip-itm-base-coco")

        def get_sim(pred, refs):
            inputs = [pred] + refs
            inputs = processor(text=inputs, padding=True, return_tensors="pt")
            txt_embeds = BLIP.text_encoder(**inputs)["last_hidden_state"]
            txt_embeds = normalize(BLIP.text_proj(txt_embeds), dim=-1)
            txt_embeds = txt_embeds / txt_embeds.norm(p=2, dim=-1, keepdim=True)
            txt_embeds = txt_embeds.view(txt_embeds.shape[0],-1)        
            logits_per_text = torch.matmul(txt_embeds[0], txt_embeds.t())
            sum = torch.sum(logits_per_text[1:]/logits_per_text[0]).item()
            return sum/(txt_embeds.shape[0]-1)
        
        pred = generated_captions[0]
        score_rebartying_back      = get_sim(pred, refs_rebartying_back)
        score_rebartying_knee      = get_sim(pred, refs_rebartying_knee)
        score_ceilingwork_shoulder = get_sim(pred, refs_ceilingwork_shoulder)
        score_window_shoulder      = get_sim(pred, refs_window_shoulder)
        score_vibration_hand       = get_sim(pred, refs_vibration_hand)
        score_load_cart            = get_sim(pred, refs_load_cart)
        score_pick_back            = get_sim(pred, refs_pick_back)
        score_pick_knee            = get_sim(pred, refs_pick_knee)
        score_pick_shoulder        = get_sim(pred, refs_pick_shoulder)
        scores = [
                score_rebartying_back,
                score_rebartying_knee,
                score_ceilingwork_shoulder,
                score_window_shoulder,
                score_vibration_hand,
                score_load_cart,    
                score_pick_back,   
                score_pick_knee,    
                score_pick_shoulder,
            ]
        
        max_index = str(scores.index(max(scores)))
        
        sols = sols[max_index]
        sort_sols = sorted(sols.items(), key=lambda x:x[1], reverse=True)
        #sols = {k: v for k,  v in sorted(sols.items(), key=lambda item: item[1], reverse=True)}
        print(generated_captions[0])
        print(sols)
        return {"prob": generated_captions[0], "res": sols, "maxIndex": max_index, "sortRes": sort_sols}

    # def modify_cap_expert(self, img_filepath, false_cap):
    #     """
    #     img_filepath: A single image file path which has a wrong generated caption.
    #     false_cap: A string of the wrong caption.
    #     """
    #     print("This generated caption is wrong.", false_cap)
    #     print("Please modify it.")
    #     csv_path = "./folder/train/metadata.csv"
        
    #     true_cap = "aabbccadddaabbccaddd"
    #     metadata = pd.read_csv(csv_path, index_col=0)
        
    #     if img_filepath not in metadata["file_name"].values:
    #         print('file not found')
    #         metadata = metadata.append({"file_name": img_filepath, "text": true_cap}, ignore_index=True)
    #     else:
    #         print('file found')
    #         metadata.loc[metadata["file_name"]==img_filepath, "text"] = true_cap
    #     metadata.to_csv(csv_path)
    #     self.metadata = metadata


    def modify_cap_expert(self, img_filepath, modified_cap):
        """
        Expert can modify the incorrect captions and save them into metadata.
        img_filepath: A single image file path which has a wrong generated caption.
        false_cap: A string of the wrong caption.
        """
        csv_path = getPath("./folder/train/metadata.csv")
        metadata = pd.read_csv(csv_path, index_col=0)

        if img_filepath not in metadata["file_name"].values:
            metadata = metadata.append({"file_name": img_filepath, "text": modified_cap}, ignore_index=True)
        else:
            metadata.loc[metadata["file_name"]==img_filepath, "text"] = modified_cap
        metadata.to_csv(csv_path)
        self.metadata = metadata


    def retrain(self):
        """Retrain the model after adding or modifying metadata."""
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(device)

        dataset = load_dataset("imagefolder", data_dir=getPath("./folder"), split="train")

        processor = self.processor
        model = self.model

        train_dataset = ImageCaptioningDataset(dataset, processor)
        train_dataloader = DataLoader(train_dataset, shuffle=True, batch_size=8)

        optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5)
        model.to(device)
        model.train()

        loss_records = []
        start = time.time()

        for epoch in range(1):
            for idx, batch in enumerate(train_dataloader):
                input_ids = batch.pop("input_ids").to(device)
                pixel_values = batch.pop("pixel_values").to(device)

                outputs = model(input_ids=input_ids,
                                pixel_values=pixel_values,
                                labels=input_ids)

                loss = outputs.loss

                print("Loss:", loss.item())
                loss_records.append(loss.item())
                loss.backward()

                optimizer.step()
                optimizer.zero_grad()
        print("Time for retraining is:", time.time() - start)

        torch.save(model, getPath("./model_retrained.pth"))
        print("Retrained model is saved.")

        self.model = model
        self.processor = processor

        plt.plot(loss_records)
        plt.savefig(getPath("./loss.png"))
