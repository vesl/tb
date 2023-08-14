from tbmods.darwin.genom import Genom
from tbmods.darwin.id import Id
import random

class Darwin:
    
    def __init__(self, dataset_type, model_type, symbol, _map):
        self.dataset_type = dataset_type
        self.model_type = model_type
        self.nb_ids = _map["nb_ids"]
        self.nb_generations = _map["nb_generations"]
        self.current_generation = 1
        self.symbol = symbol
        self.genom = Genom(self.dataset_type, self.model_type)
        self.ids = []

    def evolve(self):
        self.populate_ids()
        while self.current_generation <= self.nb_generations:
            print("GENERATION {}".format(self.current_generation))
            self.train_ids()
            print("Train finished")
            self.rank_ids()
            print("RESULT : {} ".format([_id.model.perfs['f1_score'] for _id in self.ids]))
            self.ids.append(Id(self.cross_over(self.ids[0],self.ids[1]),self.dataset_type,self.model_type,self.symbol))
            self.ids.append(Id(self.cross_over(self.ids[0],self.ids[2]),self.dataset_type,self.model_type,self.symbol))
            self.ids.append(Id(self.cross_over(self.ids[1],self.ids[3]),self.dataset_type,self.model_type,self.symbol))
            self.ids = self.ids[10:]
            self.populate_ids()
            self.current_generation += 1
    
    def populate_ids(self):
        while len(self.ids) <= self.nb_ids:
            self.ids.append(Id(self.genom.get_random(),self.dataset_type,self.model_type,self.symbol))
            
    def train_ids(self):
        for _id in self.ids:
            _id.train()
            
    def rank_ids(self):
        self.ids = sorted(self.ids, key=lambda x: x.model.perfs['f1_score'],reverse=True)
        
    def cross_over(self,id1,id2):
        gid1 = id1.genom
        gid2 = id2.genom
        gid3 = gid1
        for gene in gid1['model_map'].keys():
            gid3['model_map'][gene] = random.choice([gid1['model_map'],gid2['model_map']])[gene]
        for features_map in gid1['features_maps'].keys():
            for gene in gid1['features_maps'][features_map]['features'].keys():
                gid3['features_maps'][features_map]['features'][gene] = random.choice([gid1,gid2])['features_maps'][features_map]['features'][gene]
        return gid3
        