import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

# keeps track of program state
user = None

####### CHOICE FUNCTIONS #######

def handle_question(tbody, question):
    if question in {"b", "c", "d", "e"}:
        data = parse_table(tbody, question)
        plot_graph(data, question)
    else:
        year, row, special_case = find_year()
        if special_case:
            return
        tds = tbody.find_all("tr")[row].find_all("td")
        winner, loser = get_winner_loser(tds)
        print(f'In {year}, the {winner} won the World Series against the {loser}.')

        if question == "f":
            team, manager = find_manager(tds, winner, loser)
            print(f'The manager of the {year} {team} was {manager}.')

####### SCRAPING FUNCTIONS #######

# function that finds the winner and loser of a world series matchup
def get_winner_loser(tds):
    # index 0 is american league team, index 3 is national league team
    # winner is bolded on the html
    if tds[0].find("strong") is not None:
        winner = tds[0].find("strong").text
        loser = tds[3].text
    else:
        winner = tds[3].find("strong").text
        loser = tds[0].text
    return winner, loser

# function that parses the data table based on user choice
def parse_table(tbody, question):
    trs = tbody.find_all("tr")
    data = {}
    for tr in trs:
        tds = tr.find_all("td")
        if len(tds) >= 4:
            winner, loser = get_winner_loser(tds)
            if question == "b":
                update_counts(data, winner)
            elif question == "c":
                update_counts(data, loser)
            elif question == "d":
                update_counts(data, winner)
                update_counts(data, loser)
            elif question == "e":
                update_counts(data, "American League" if winner in tds[0].text else "National League")
    return data

# function that updates dictionary passed as an argument
def update_counts(dictionary, key):
    if key in dictionary:
        dictionary[key] += 1
    else:
        dictionary[key] = 1

# finds manager based on user input
def find_manager(tds, winner, loser):
    print(f'Do you want to find the manager for the {winner} or the {loser}?')
    print(f'   a) {winner}')
    print(f'   b) {loser}')
    choice = getUserChoice({"a": "a", "b": "b"})

    if choice == "a":
        team, link = (winner, get_manager_link(tds, 0 if tds[0].find("strong") else 3))
    else:
        team, link = (loser, get_manager_link(tds, 3 if tds[0].find("strong") else 0))

    manager = scrape_manager(link)
    return team, manager

# gets link to find manager
def get_manager_link(tds, index):
    link = tds[index].find("a")['href']
    return "https://www.baseball-reference.com" + link

# scrapes link to find manager
def scrape_manager(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')
    body = soup.find("body")
    div1 = body.find("div", class_="teams")
    div2 = div1.find("div")
    div2s = div2.find_all("div")
    div3 = div2s[1]
    ps = div3.find_all("p")
    p = ps[2]
    a = p.find("a")
    return a.text

####### GRAPHING FUNCTIONS #######

# plots graphs based on question
def plot_graph(data, question):
    titles = {
        "b": "World Series Wins by Team",
        "c": "World Series Losses by Team",
        "d": "World Series Appearances by Team",
        "e": "World Series Wins by League"
    }
    xlabels = {
        "b": "Wins",
        "c": "Losses",
        "d": "Appearances"
    }
    if question == "e":
        plt.title(titles[question])
        plt.pie(data.values(), labels=data.keys(), autopct='%.0f%%', pctdistance=1.15, labeldistance=.25)
        print("I have produced a pie chart that highlights World Series' wins by league.")
        print("The American League has won more World Series' than the National League.")
        plt.show()
    else:
        print_statements(question)
        plot_bargraph(data, titles[question], xlabels[question])

# prints statements related to graphs
def print_statements(question):
    if question == 'b':
        print("I have produced a bar graph that highlights the number of World Series' wins by team.")
        print("The New York Yankees have won the most World Series' with 27 wins.")
    elif question == 'c':
        print("I have produced a bar graph that highlights the number of World Series' losses by team.")
        print("The New York Yankees have lost the most World Series' with 13 losses.")
    else:
        print("I have produced a bar graph that highlights the number of World Series' appearances by team.")
        print("The New York Yankees have the most World Series' apperarances with 40.")

# prints bargraph based on question
def plot_bargraph(data, title, xlabel):
    keys = list(data.keys())
    values = list(data.values())
    fig, ax = plt.subplots()
    hbars = ax.barh(keys, values, align='center')
    ax.set_yticks(keys, labels=keys, fontsize=6)
    ax.invert_yaxis()
    ax.set_xlabel(xlabel)
    ax.set_title(title)
    ax.bar_label(hbars)
    plt.show()

####### USER INTERACTION FUNCTIONS #######

# lists choices and prompts user to enter choice
def options():
    print("What would you like to find?:")
    print("   a) World Series Matchups by Year")
    print("   b) World Series Wins by Team")
    print("   c) World Series Losses by Team")
    print("   d) World Series Appearances by Team")
    print("   e) World Series Wins by League")
    print("   f) Manager of A World Series Team")
    return getUserChoice()

# prompts user to enter choice, will continue until choice is valid
def getUserChoice(options = None):
    if not options:
        options = {"a", "b", "c", "d", "e", "f"}
    choice = None
    while choice not in options:
        choice = input("Please enter the letter of your choice: ").lower()
        if choice not in options:
            print("That is not one of the letters available.")
    return choice

# gets row that has data for corresponding year
def find_year():
    # ensures that a valid year is inputted
    while True:
        year = input("Please enter a year (i.e: 1977) between 1903 and 2023 (no spaces!): ")
        if year.isdigit() and 1903 <= int(year) <= 2023:
            year = int(year)
            break
        print("That is not a valid year.")
    special_case = check_year(year)
    #formula for finding the row that corresponds to each year
    row = 124 - (year - 1899)
    return year, row, special_case

# checks if the year is a special case where there was no world series that year
def check_year(year):
    if year == 1994:
        print("There was no World Series held in 1994 due to The Players' Strike")
        return True
    elif year == 1904:
        print("There was no World Series held in 1904 due to the boycott by the New York Giants")
        return True
    else:
        return False

# asks user if they want to find something else
def another_question(user):
    answer = input(user + ", would you like to find something else? ")
    answer = answer.lower()
    affirmative = ['yes','yeah','sure','y','ye','yup','ok','ya','yea']
    negative = ['no','n','nope','nop','nah','na','never']
    if answer in affirmative:
        main()
    elif answer in negative:
        print("Ok! I hope you learned something new. Thanks for chatting with me!")
    else:
        print("I don't understand...")
        another_question(user)

# chatbot introduction and grabs user name
def intro():
    user = input("Hello! Please enter your name: ")
    print(f'Nice to meet you {user}. My name is BaseballBot, and I scrape Baseball Reference for World Series Data.')
    return user

####### MAIN FUNCTION #######
def main():
    global user
    page = requests.get("https://www.baseball-reference.com/postseason/world-series.shtml")
    soup = BeautifulSoup(page.content, 'html.parser')
    body = soup.find("body")
    div = body.find("div", class_="index")
    div1 = div.find("div", class_="table_wrapper")
    div2 = div1.find("div", class_="table_container")
    table = div2.find("table", class_="sortable stats_table")
    tbody = table.find("tbody")
    
    #introduction - only if user hasnt been created yet (initial start up)
    if not user:
        user = intro()

    #list choices for scraping and carry out user choice
    choice = options()
    handle_question(tbody, choice)
    another_question(user)
    return
    
if __name__ == "__main__":
    main()