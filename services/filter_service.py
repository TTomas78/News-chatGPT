import re

class FilterService():
    def  __init__(self, pattern):
        self.pattern = pattern
        
    def remove_by_regex(self,link):
        #TODO cambiar el nombre del metodo, deberia ser simplemente un nombre como "match with regex"
        if re.search(self.pattern, link):
            return False
        return True