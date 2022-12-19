# Moises Andrade
# Problem 4 - main loop to run the Command Line News app


from CommandLineNews import CommandLineNews

def main():
    # inputs
    API_key = "ac54555cc34d49c69cf7b068f9ec6c2e"
   
    command_line_news = CommandLineNews(API_key, country="us")

    # loop to play the game until the player input 'n'
    while True:
        command_line_news.deploy_CommandLineNews()
        cont = command_line_news.continue_news()
        if not cont:
            exit()

if __name__ == "__main__":
    main()
