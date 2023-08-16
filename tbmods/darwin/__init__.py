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
            self.train_ids()
            self.rank_ids()
            print("GENERATION {}".format(self.current_generation))
            print("BETTER : {}".format(self.ids[0].model.perfs['f1_score']))
            print("GENOM : {}".format(self.ids[0].genom))
            self.new_gen_ids = []
            while len(self.new_gen_ids) >= len(self.ids)/2:
                self.new_gen_ids.append(Id(self.cross_over(self.ids[0],random.choice(self.ids[1:])),self.dataset_type,self.model_type,self.symbol))
                self.new_gen_ids.append(Id(self.cross_over(self.ids[1],random.choice(self.ids[2:])),self.dataset_type,self.model_type,self.symbol))
            self.ids = self.new_gen_ids
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
        gid3['vertical'] = random.choice([gid1,gid2])['vertical']
        return gid3
        