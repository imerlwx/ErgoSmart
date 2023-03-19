# import sys, os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model.__src.ErgoSolCap import ErgoSolCap


class TrainingModel():
    def __init__(self) -> None:
        Ergo = ErgoSolCap()
        Ergo.load_model()
        self.Ergo = Ergo
        self.isRetraining = False


    def get_caption(self, img):
        return self.Ergo.gen_cap_worker(img)


    def modify_cap_expert(self, filename, caption):
        self.Ergo.modify_cap_expert(filename,caption)


    def retrain(self):
        self.isRetraining= True
        self.Ergo.retrain()
        self.isRetraining = False
