from DataIndexer import DataIndexer
from os import system, name
import constants

print("      Starting indexing of content...")

dataIndexer = DataIndexer()
dataIndexer.index_all(constants.DATA_DIR)

print("      Indexing complete")

def clear():
    if name == 'nt':
        system("cls")
    else:
        system("clear")

def main_screen():
    clear()
     
    print("Type 'quit' to exit at any time, Press 'Enter' to continue")
    print("      Select search options:         ")
    print("           " + u"\u2022" + " Press 1 to search Zendesk")
    print("           " + u"\u2022" + " Press 2 to view a list of searchable fields")
    print("           " + u"\u2022" + " Type 'quit' to exit")

    text = raw_input("")

    if text == "quit":
        quit()
    if text == "1":
        print("Select one of the below")
        count = 1
        optionsList = []
        for value in dataIndexer.get_all_entities():
            print("                  {}) {}".format(count, value))
            optionsList.append(value)  
            count = count + 1
        try:
            option = raw_input("")
            term = raw_input("Enter search term \n")
            value = raw_input("Enter search value \n")
            result = dataIndexer.search_by_key(optionsList[int(option) - 1],term,value)
            if len(result) == 0:
                print("Searching {} for {} with a value of {}. \n No results found.".format(optionsList[int(option) - 1], term, value))
                raw_input("\n\nPress Enter to continue")
            else:
                print_dictionary_or_list(result)
        except ValueError:
            print("\n\nPlease enter valid data above. Press Enter to continue")  
            raw_input("") 
        main_screen()
    if text == "2":
        print_keys(dataIndexer.get_all_keys(),dataIndexer.get_all_entities())
        main_screen()

def print_keys(keys,entities):
    clear() 
    for entity in entities:
        print("----------------------------------------------------------------------------------------------------------------------------------------------------------------")
        print("Search {} with".format(entity))
        for key in keys:
            if key.startswith(entity):
                print(key.split("-")[1]) #split a key with user-_id and show only the _id part
    raw_input("\n\nPress Enter to continue")

def print_dictionary_or_list(data):
    clear()
    if isinstance(data,dict):
        for key, value in sorted(data.items()):
            print("%-45s %-100s" % (key,value))
        raw_input("\n\nPress Enter to continue")
    if isinstance(data,list):
        for value in data:
            if isinstance(value,dict):
                print_dictionary_or_list(value)

main_screen() 
