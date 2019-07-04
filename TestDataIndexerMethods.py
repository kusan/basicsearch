import unittest
from DataIndexer import DataIndexer
from JsonReader import JsonReader
import constants

class TestDataIndexerMethods(unittest.TestCase):
 
    def setUp(self):
        self.dataIndexer = DataIndexer()
        self.data = self.dataIndexer.index_all(constants.DATA_DIR)
        jsonReader = JsonReader()
        self.raw_data = jsonReader.parse_all_files(constants.DATA_DIR)

    def test_index_all(self):
        for key,value in self.raw_data.items():
            for row in value:
                for dictkey,dictvalue in row.items():         
                    for dictionary in DataIndexer.as_list(self.data.get(key + constants.KEY_DELIMETER + dictkey + constants.KEY_DELIMETER + unicode(dictvalue))):
                        self.assertEqual(dictionary.get(dictkey),dictvalue)

    def test_get_all_keys(self):
        keys = self.dataIndexer.get_all_keys()
        for key,value in self.raw_data.items():
            for row in value:
                for dictkey in row:
                    self.assertTrue((key + constants.KEY_DELIMETER + dictkey) in keys)


    def test_get_all_entities(self):
        entities = self.dataIndexer.get_all_entities()
        for key,value in self.raw_data.items():
            self.assertTrue(key in entities)

    def test_search_by_organization(self):
        for organization in self.raw_data.get("organizations"):
            for key, value in organization.items(): 
                indexedOrganizations = DataIndexer.as_list(self.dataIndexer.search_by_organization("organizations",key,value))
                for indexedOrganization in indexedOrganizations:
                    #check if the value matches for each key
                    self.assertEqual(indexedOrganization.get(key),value)

                    #check if the subject of the ticket appears on the organization dictionary returned by the search if the ticket belongs to org 
                    for ticket in self.raw_data.get("tickets"): 
                        if ticket.get("organization_id") == indexedOrganization.get("_id"):
                            self.assertTrue(ticket.get("subject") in indexedOrganization.values())

                    #check if the name of the user apears on the organization dictionary returned by the search if the user belongs to org
                    for user in self.raw_data.get("users"):
                        if user.get("organization_id") == indexedOrganization.get("_id"):
                            self.assertTrue(user.get("name") in indexedOrganization.values()) 
 
    def test_search_by_users(self):
        for user in self.raw_data.get("users"):
            for key, value in user.items():
                indexedUsers = DataIndexer.as_list(self.dataIndexer.search_by_users("users",key,value))
                for indexedUser in indexedUsers:
                    #check if the value matches for each key
                    self.assertEqual(indexedUser.get(key),value)

                    #check if the subject of the ticket appears on the user dictionary returned by the search if the ticket is submitted by the user 
                    for ticket in self.raw_data.get("tickets"):
                        if ticket.get("submitter_id") == indexedUser.get("_id"):
                            self.assertTrue(ticket.get("subject") in indexedUser.values())

                    #check if the subject of the ticket appears on the user dictionary returned by the search if the ticket is assigned to the user
                    for ticket in self.raw_data.get("tickets"):
                        if ticket.get("assignee_id") == indexedUser.get("_id"):
                            self.assertTrue(ticket.get("subject") in indexedUser.values())

                    #check if the name of the user apears on the organization dictionary returned by the search if the user belongs to org
                    for organization in self.raw_data.get("organizations"):
                        if organization.get("_id") == indexedUser.get("oragnization_id"):
                            self.assertTrue(organization.get("name") in indexedUser.values())
        
    def test_search_by_tickets(self):
        for ticket in self.raw_data.get("tickets"):
            for key, value in ticket.items():
                indexedTickets = DataIndexer.as_list(self.dataIndexer.search_by_tickets("tickets",key,value))
                for indexedTicket in indexedTickets:
                    #check if the value matches for each key
                    self.assertEqual(indexedTicket.get(key),value)

                    #check if the submitter an assignee are correct 
                    for user in self.raw_data.get("users"):
                        if indexedTicket.get("submitter_id") == user.get("_id"):
                            self.assertEquals(indexedTicket.get("submitter"), user.get("name"))
                        if indexedTicket.get("assignee_id") == user.get("_id"):
                            self.assertEquals(indexedTicket.get("assignee"), user.get("name"))

                    #check if the organization is correct 
                    for organization in self.raw_data.get("organizations"):
                        if organization.get("_id") == indexedTicket.get("oragnization_id"):
                            self.assertEquals(organization.get("name"), indexedTicket.get("organization"))

    def suite():
        tests = ['test_index_all','test_get_all_keys','test_get_all_entities','test_search_by_organization','test_search_by_users', 'test_search_by_tickets']
        return unittest.TestSuite(map(TestDataIndexerMethods, tests))

if __name__ == '__main__':
    unittest.main()
