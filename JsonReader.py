import simplejson as json
import glob

class JsonReader:
    data = {}

    def parse_all_files(self, path):
        """Parse All Json files on the path and return a dictionary with keys been only the filename without the extention """
        files = glob.glob(path + "*.json")
        for file in files:
            with open(file) as f: 
                self.data[file[file.rfind("/") + 1:file.rfind(".")]] = json.load(f)
        return self.data


