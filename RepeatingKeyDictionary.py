class RepeatingKeyDictionary(dict):
    def __setitem__(self, key, value):
        """This method sets a value to a key if the key has no value or if it does then it sets a list to that key with both the old and the new value"""  
        try:
            self[key].append(value)
        except AttributeError:
            super(RepeatingKeyDictionary, self).__setitem__(key, [self[key], value])
        except KeyError:
            super(RepeatingKeyDictionary, self).__setitem__(key, value) 
