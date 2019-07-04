from JsonReader import JsonReader
from RepeatingKeyDictionary import RepeatingKeyDictionary
import constants

class DataIndexer:
    __data = RepeatingKeyDictionary() 
    __keys = set() 
    __entities = set()
 
    def index_all(self, source):
        """This method will read the incomming data structure from the json files and will create an optimized data structure that will support an O(1) time retrival algorithem"""
        jsonReader = JsonReader() 
        jsonData = jsonReader.parse_all_files(source)
        for filename, jsonvalue in jsonData.items():
            for dictionary in jsonvalue:
                for key, value in dictionary.items(): 
                    self.__data[filename + constants.KEY_DELIMETER + key + constants.KEY_DELIMETER + unicode(value)] = dictionary 
                    self.__keys.add(filename + constants.KEY_DELIMETER + key) 
                    self.__entities.add(filename)
        return self.__data 
 
    def get_all_keys(self):
        """This method will return a set of keys, where each key contains the pattern x-y, x been the json file name without extention and y been a key of a dictionary in that file"""
        return self.__keys       

    def get_all_entities(self):
        """This method will return a set of keys, where each key will be the name of a json file that was indexed"""
        return self.__entities
    
    @staticmethod 
    def as_list(data):
        if data is None:
            return []
        if isinstance(data,list):
            return data
        else:
            temp = []
            temp.append(data)
            return temp
 
    def search_by_organization(self,entity,key,value):
        """Specialized method to handle links to other entities"""
        results = DataIndexer.as_list(self.__data.get(entity + constants.KEY_DELIMETER + key + constants.KEY_DELIMETER + unicode(value), None))
        for result in results: 
            users = DataIndexer.as_list(self.__data.get("users" + constants.KEY_DELIMETER + "organization_id" + constants.KEY_DELIMETER + str(result["_id"]), None))
            count = 0
            for user in users:
                result["User_" + str(count)] = user.get("name")
                count = count + 1
            tickets = DataIndexer.as_list(self.__data.get("tickets" + constants.KEY_DELIMETER + "organization_id" + constants.KEY_DELIMETER + str(result["_id"]), None))
            count = 0
            for ticket in tickets:
                result["Ticket_" + str(count)] = ticket.get("subject")
                count = count + 1
        return results
    
    def search_by_users(self,entity,key,value):
        """Specialized method to handle links to other entities"""
        results = DataIndexer.as_list(self.__data.get(entity + constants.KEY_DELIMETER + key + constants.KEY_DELIMETER + unicode(value), None))
        for result in results:
            submittedtickets = DataIndexer.as_list(self.__data.get("tickets" + constants.KEY_DELIMETER + "submitter_id" + constants.KEY_DELIMETER + str(result["_id"]), None))
            count = 0
            for submittedticket in submittedtickets:
                result["SubmitttedTicket_" + str(count)] = submittedticket.get("subject")
                count = count + 1
            assignedtickets = DataIndexer.as_list(self.__data.get("tickets" + constants.KEY_DELIMETER + "assignee_id" + constants.KEY_DELIMETER + str(result["_id"]), None))
            count = 0
            for assignedticket in assignedtickets:
                result["AssignedTicket_" + str(count)] = assignedticket.get("subject")
                count = count + 1
            organizations = DataIndexer.as_list(self.__data.get("organizations" + constants.KEY_DELIMETER + "_id" + constants.KEY_DELIMETER + str(result.get("organization_id")), None)) 
            if len(organizations) > 0:
                result["organization"] = organizations[0].get("name") # There will only be one organization per user
        return results
 
    def search_by_tickets(self,entity,key,value):
        """Specialized method to handle links to other entities"""
        results = DataIndexer.as_list(self.__data.get(entity + constants.KEY_DELIMETER + key + constants.KEY_DELIMETER + unicode(value), None))
        for result in results:
            organizations = DataIndexer.as_list(self.__data.get("organizations" + constants.KEY_DELIMETER + "_id" + constants.KEY_DELIMETER + str(result.get("organization_id")), None))
            if len(organizations) > 0: 
                result["organization"] = organizations[0].get("name")              # There will only be one organization per ticket
 
            submitters = DataIndexer.as_list(self.__data.get("users" + constants.KEY_DELIMETER + "_id" + constants.KEY_DELIMETER + str(result.get("submitter_id")), None))
            if len(submitters) > 0:
                result["submitter"] = submitters[0].get("name")                    # There will only be one submitter per ticket
            
            assignees = DataIndexer.as_list(self.__data.get("users" + constants.KEY_DELIMETER + "_id" + constants.KEY_DELIMETER + str(result.get("assignee_id")), None))
            if len(assignees) > 0:
                result["assignee"] = assignees[0].get("name")                      # There will only be one assignee per ticket 
        return results
 
    def search_by_key(self,entity,key,value):
        """This method will return either a dictionary OR a list of dictionaries for which the key matches"""
        if entity == "organizations":
            return self.search_by_organization(entity,key,value)
        if entity == "users":
            return self.search_by_users(entity,key,value)
        if entity == "tickets":
            return self.search_by_tickets(entity,key,value)
        return self.__data.get(entity + constants.KEY_DELIMETER + key + constants.KEY_DELIMETER + value, None)

