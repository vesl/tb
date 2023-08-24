from tbmods.mongodb import MongoDB
import random

class Genom:
    
    def __init__(self, dataset_type, model_type):
        self.dataset_type = dataset_type
        self.model_type = model_type

    def get_random(self):
        self.get_stumps()
        model_map = { parameter_name:self.randomise_model_parameter(parameter_name) for parameter_name in self.stumps['model_map'] }
        features_maps = { features_map_name:self.randomise_features_map(features_map_name) for features_map_name in self.stumps['features_maps'] }
        return {
            "model_map": self.model_constraints(model_map),
            "features_maps": features_maps,
            "vertical": self.randomise_int(9)
        }

    def get_stumps(self):
        mongodb = MongoDB()
        features_maps_names = mongodb.find('TB','datasets_maps',{"name":self.dataset_type})[0]['features_maps']
        self.stumps = {
            "model_map": mongodb.find('TB','models_maps',{"name":self.model_type})[0]['parameters'],
            "features_maps": { features_maps_name:mongodb.find('TB','features_maps',{"name":features_maps_name})[0] for features_maps_name in features_maps_names }
        }
        mongodb.close()

    def randomise_int(self,i):
        max_ = (int(i)+1)*5
        return random.randint(1,max_)

    def randomise_model_parameter(self, parameter_name):
        parameter = self.stumps['model_map'][parameter_name]
        if parameter['type'] == 'list': parameter['value'] = random.choice(parameter['values'])
        elif parameter['type'] == 'bool': parameter['value'] = bool(random.getrandbits(1))
        elif parameter['type'] == 'int' or parameter['type'] == 'float':
            if parameter['value'] == 'None':
                if random.random() > 0.3: parameter['value'] == None
                elif 'min' in parameter: parameter['value'] = random.uniform(parameter['min'],parameter['max'])
                else: parameter['value'] = self.randomise_int(100)
            elif 'min' in parameter: parameter['value'] = random.uniform(parameter['min'],parameter['max'])
            else: parameter['value'] = self.randomise_int(parameter['value'])
        return parameter

    def randomise_features_map(self, features_map_name):
        features_map = {"features": {}, "source": self.stumps['features_maps'][features_map_name]["source"] }
        features_map_stump = self.stumps['features_maps'][features_map_name]["features"]
        for feature_name in features_map_stump:
            feature = features_map_stump[feature_name].copy()
            if random.random() < 0.5: feature['lag'] = random.randint(1,8)
            if 'args' in feature and random.random() > 0.1: feature['args'] = {arg:self.randomise_int(value) for arg, value in feature['args'].items()}
            features_map["features"][feature_name] = feature
        return features_map
        
    def model_constraints(self,model_map):
        if self.model_type == 'random_forest':
            if model_map['max_samples']['value'] != 'None': model_map['bootstrap']['value'] = True
            if model_map['class_weight']['value'] == 'balanced' or model_map['class_weight']['value'] == 'balanced_subsample':
                model_map['warm_start']['value'] = False
            if model_map['max_leaf_nodes']['value'] != 'None' and model_map['max_leaf_nodes']['value'] < 2:
                model_map['max_leaf_nodes']['value'] = 2
            if model_map['oob_score']['value'] == True: model_map['bootstrap']['value'] = True
        return model_map