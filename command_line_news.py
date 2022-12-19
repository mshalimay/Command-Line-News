# Moises Andrade

import requests
import re
import myNumbers
from dateutil import parser
from colorama import Fore

class CommandLineNews:
    """ An app that searchs for news in the web and display on the console
    Attributes:
     choice_options(dict) = the allowed type of news that might be searched
     category_options(dict) = the allowed type of categories of Top headlines that might be searched
     choice_input(str) = user input indicating the type of news desired in a specific each call of the app
     category_input(str) =  user input indicating the category of Top headlines desired in each call of the app. Only used if choice_input='1'
     keyword_input(str) = user input indicating the string to search for news in the web. Only used if choice_input = '2'
     y_n_input(str) = user input indicating if the user wants to keep retrieving news with the app. 
     out_string(str) = the top headlines to be displayed at the console
    """
    choice_options = {1: "Top headlines", 2: "Search"}
    category_options = {1:'business', 2:'entertainment', 3:'general', 4:'health',
                        5:'science', 6:'sports', 7:'technology'}

    def __init__(self, API_key, country='us'):
        self.API_key = API_key
        self.country = country
        
 #============================================================
 # News methods
 #============================================================

    def generate_top_results(self, top=10):
        """ Generates a list of top news results based on the type of news chosen by the user"""

        # define the source of news in line with the type of news chosen by the user
        if self.choice_input=='1':
            url = f"https://newsapi.org/v2/top-headlines?country={self.country}&category={self.category}&apiKey={self.API_key}"
        elif self.choice_input =='2':
            url = f"https://newsapi.org/v2/everything?q={self.keyword_input}&apiKey={self.API_key}"

        # make a request to the NewsAPI and transform the JSON result into a dictionary
        r = requests.get(url)
        json_dict = r.json()

        # generates the list of top news results
        self.generate_out_string(json_dict, top=10)             

    def generate_out_string(self, json_dict, top=10):
        """ From a dictionary constructed from a JSON, retrieves the 'title', 'description', 'author' and 
        'date' of the top news articles and outputs a summary string 

        Args:
            json_dict (dict): A dictionary created from a JSON object from NewsAPI
            top (int, optional): the maximum number of news to display. Defaults to 10.
        """
        # maximum lenght of iterations not to exceed the ammount of news
        max_iteration = min(top, len(json_dict['articles']))

        # placeholder string with the top news
        out_string = ""

        # loops through the articles, retrieves the 'title', 'description', 'date' and adds to the top news string
        for article in json_dict['articles'][0:max_iteration]:
            title = article['title']
            description = article['description']
            author = article['author']

            # parse the ISO date 
            ISO_date = article['publishedAt']
            day, month, year = self.parse_ISOdate(ISO_date)

            # checks if the author or description is empty; if yes, will fill the field with blank 
            str_author = f". Author: {author}" if self.not_null(author) else ""
            str_description = description.rjust(len(description)+8, " ") if self.not_null(description) else ""

            # adds the news to the top news list: first the title in cyan color; followed by the author and lastly the description
            # EXTRA CREDIT:
            out_string += f"\n* \033[96m {title} ({month} {day}, {year}) \033[00m" + str_author + "\n"
            out_string += str_description + "\n"*2
        self.out_string = out_string
        
    def parse_ISOdate(self, ISO_date:str):
        """ Parse a date in the ISO 8601 and returns (day, month-string, year)
        Examples:           
        parse("2022-07-30T20:52:53Z") -> (30, July, 2022)
        """
        date = parser.parse(ISO_date)
        day = date.day
        month = date.strftime("%B")
        year = date.year
        return day, month, year
            
    def not_null(self, json_result):
        """ Check if a JSON field has any values and returns a boolean
        """
        if json_result is not None:
                if len(json_result)>0:
                    return True
        return False
        
        
 #============================================================
 # Print methods
 #============================================================
    def print_welcome(self):
        """ Welcoming message for the application. Prints only at the start of each round.
        """
        print("Welcome to Command Line News!")

    def print_results(self):
        """ Print the top results. Prints only at the end of each round.
        """
        print(self.out_string)

    
 #============================================================
 # Require input methods
 #============================================================

    # asks for [1] Top headlines [2] Search 
    def ask_choice(self):
        """ Asks for the type of news to be displayed
        """
        str_choices= ""
        for option_num, option_str in self.choice_options.items():
            str_choices += f"[{option_num}] {option_str}\n"           
        self.choice_input = input(f"Please make a choice:\n{str_choices}")

    def try_again_choice(self):
        """ If the choice_input representing the type of news is not valid, ask the user for a new input
        """
        print("\nI couldn't understand. Please be sure to enter one of the below digits.\n")
        self.ask_choice()

    # asks for a category of headlines
    def ask_category(self):
        """ Asks for a category of top headlines. Activated only if choice_input = '1' = 'Top headlines'
        """
        str_categories = ""
        for option_num, option_str in self.category_options.items():
            str_categories += f"[{option_num}] {option_str}\n"           
        self.category_input = input(f"Select which category would you like headlines for:\n{str_categories}")

    def try_again_category(self):
        """ if the category input of headlines to be searched is not valid, asks for another input. 
        Activated only if choice_input = '1' = 'Top headlines'
        """
        print("\nI couldn't understand. Please be sure to enter one of the below digits.\n")
        self.ask_category()

    # asks for search term
    def ask_keword(self):
        """ asks for a keyword to search news. Activated only if choice_input = '2' = 'Search'
        """
        
        str_categories = ""     
        self.keyword_input = input(f"\nEnter your search term:\n")

    def try_again_keyword(self):
        """ if the keyword to search news is not valid, asks for another input. 
        Activated only if choice_input = '2' = 'Search'
        """
        print("\nPlease enter a input with at least 1 charachter.\n")
        self.ask_keword()

    # asks for 'y' or 'n'
    def ask_more_news(self):
        """ Ask the user for an input indicating if they want to play again
        """
        self.y_n_input = input("\nWould you like to find more news articles? [y/n]?")

    def try_again_y_n_input(self):
        """ If the input in the play_again questin is not valid, Ask the user for a new input indicating if they want to play again
        """
        self.y_n_input = input(f"I couldn't understand.\nPlease input 'y' for more news articles or 'n' to exit.\n")
        
    
 #============================================================
 # Validate user inputs
 #============================================================
    def check_choice_input(self):
        """ Checks if the choice of the type of news to be displayed is valid
        """
        # clean the string of whitespaces and update the attribute before validation
        self.choice_input = re.sub(r'\s', "", self.choice_input)
        
        if myNumbers.str_is_integer(self.choice_input):
            choice_num =  int(myNumbers.str_to_number(self.choice_input))
            if choice_num in self.choice_options:
                self.choice = choice_num
                return True
        return False
            
    def check_category_input(self):
        """ Checks if the category of headlines to be searched is valid. Activated only if choice_input = '1' = 'Top headlines'
        """
        # clean the string of whitespaces and update the attribute before validation
        self.category_input = re.sub(r'\s', "", self.category_input)

        if myNumbers.str_is_integer(self.category_input):
            category_num =  int(myNumbers.str_to_number(self.category_input))
            if category_num in self.category_options:
                self.category = self.category_options[category_num]
                return True
        return False

    def check_keyword_input(self):
        """ Checks if the keyword to be searched is valid. Activated only if choice_input = '2' = 'Search'
        """
        # clean the string of whitespaces, remove capitalization and update the attribute before validation
        self.keyword_input = re.sub(r'\s', "", self.keyword_input).lower()

        if len(self.keyword_input)>0:
            return True
        return False

    def check_y_n_input(self):
        """ Checks if the 'y' 'n' input indicating continuation of the CommandLineNews is valid
        """
        # clean the string of whitespaces, remove capitalization and update the attribute before validation
        self.y_n_input = re.sub(r'\s', "", self.y_n_input).lower()

        if self.y_n_input == "y" or self.y_n_input == "n":
            return True
        return False



 #============================================================
 # App flow control
 #============================================================
    def deploy_CommandLineNews(self):
        """ Deploy a new round of command line news 
        """
        # erase the attribute values
        self.choice_input = None
        self.category_input = None
        self.keyword_input = None
        self.y_n_input = None
        self.out_string = None

        # print welcome and asks for top headlines or search
        self.print_welcome()
        self.ask_choice()

        # check if user input is valid; in case not, ask for new inputs until one is valid
        valid_input = self.check_choice_input()
        while not valid_input:
            self.try_again_choice()
            valid_input = self.check_choice_input()

        # if user chose Top Headlines, 
        if self.choice_input=='1':
            # asks for a category and check if user input is valid; in case not, ask for new inputs until one is valid
            self.ask_category()
            valid_input = self.check_category_input()
            while not valid_input:
                self.try_again_category()
                valid_input = self.check_category_input()

        # if user chose Search 
        elif self.choice_input=='2':
            # asks for a keyword to search and check if user input is valid; in case not, ask for new inputs until one is valid
            self.ask_keword()
            valid_input = self.check_keyword_input()
            while not valid_input:
                self.try_again_keyword()
                valid_input = self.check_keyword_input()

        # generate the top 10 results and print to the console
        self.generate_top_results(top=10)
        self.print_results()

        # asks if wants to find more news and check if user input is valid; in case not, ask for new inputs until one is valid
        self.ask_more_news()
        valid_input = self.check_y_n_input()
        while not valid_input:
            self.try_again_y_n_input()
            valid_input = self.check_y_n_input()

    def continue_news(self):
        """ Test if the user wants to keep displaying news 
        Obs.: Useful to communicate outside of the class
        Returns:
            bool: A boolean indicating if the user wants to keep displaying news. 
        """
        if self.y_n_input == "y":
            return True
        else:
            return False








