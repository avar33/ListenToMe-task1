import json

class DataLoader:
    @staticmethod
    def write_json(file, key, new_data):
        with open(file, "r") as f:
            data = json.load(f)
        
        if isinstance(data, dict):
            data[key] = new_data
        else:
            data = {key: new_data}

        with open(file, "w") as f:
            json.dump(data, f, indent=2)

    @staticmethod
    def read_json(file, key): 
        with open (file, "r") as f:
            data = json.load(f)
        if isinstance(data, dict) and key in data:
            return data[key]
        else: 
            return None