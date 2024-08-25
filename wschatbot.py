import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

user = None

def find_year():
    year = ""
    while not year.isdigit():
        user_input = input("Please enter a year (i.e: 1977) between 1903 and 2023 (no spaces!): ")
        if user_input.isdigit():
            year = int(user_input)
            break
        else:
            print("That is not a valid year.")
    special_case = check_year(year)
    #formula for finding the row that corresponds to each year
    row = 124 - (year - 1899)
    return year, row, special_case
        
def check_year(year):
    #special cases
    if (year > 2023 or year < 1903 or year == 1994 or year == 1904):
        #user entered a year that has not happened yet
        if year > 2023:
            print("I am afraid I cannot predict the future.")
        #user entered a year that is before 1903
        elif year < 1903:
            print("I am afraid I cannot find information before 1903.")
        #years where there was no world series
        elif year == 1994:
            print("There was no World Series held in 1994 due to The Players' Strike")
        elif year == 1904:
            print("There was no World Series held in 1904 due to the boycott by the New York Giants")
        return True
    else:
        return False

def qA(tbody):
    year, row, special_case = find_year()
    if special_case:
        return
    trs = tbody.find_all("tr")
    tds = trs[row].find_all("td")
    
    #index 0 is american league winner index 3 is national league winner
    #the winner is bolded on the html
    if tds[0].find("strong") != None:
        winner = tds[0].find("strong").text
        loser = tds[3].text
    elif tds[3].find("strong") != None:
        winner = tds[3].find("strong").text
        loser = tds[0].text
    
    print(f'In {year}, the {winner} won the World Series against the {loser}.')
        
def qB(tbody):
    trs = tbody.find_all("tr")
    winners = {}
    for index in range(len(trs)): 
        #individual tds within each tr
        indiv_tds = trs[index].find_all("td")
        ##only accounts for rows with world series info
        if len(indiv_tds) >= 4:
            #index 0 is american league winner index 3 is national league winner
            #the world series winner is bolded on the website
            if indiv_tds[0].find("strong") != None:
                winner = indiv_tds[0].find("strong").text
                if winner in winners:
                    winners[winner] += 1
                else:
                    winners[winner] = 1
            else:
                winner = indiv_tds[3].find("strong").text
                if winner in winners:
                    winners[winner] += 1
                else:
                    winners[winner] = 1
    keys = list(winners.keys())
    values = list(winners.values())
    fig, ax = plt.subplots()
    hbars = ax.barh(keys, values, align='center')
    ax.set_yticks(keys, labels=keys, fontsize=6)
    ax.invert_yaxis()
    ax.set_xlabel('World Series Wins')
    ax.set_title('World Series Wins by Team')
    ax.bar_label(hbars)
    ax.set_xlim(right=30)
    print("I have produced a bar graph that highlights the number of World Series' wins by team.")
    print("The New York Yankees have won the most World Series' with 27 wins.")
    plt.show()
    
def qC(tbody):
    trs = tbody.find_all("tr")
    losers = {}
    for index in range(len(trs)): 
        #individual tds within each tr
        indiv_tds = trs[index].find_all("td")
        ##only accounts for rows with world series info
        if len(indiv_tds) >= 4:
            #index 0 is american league winner index 3 is national league winner
            #the world series winner is bolded on the website
            if indiv_tds[0].find("strong") != None:
                loser = indiv_tds[3].text
                if loser in losers:
                    losers[loser] += 1
                else:
                    losers[loser] = 1
            else:
                loser = indiv_tds[0].text
                if loser in losers:
                    losers[loser] += 1
                else:
                    losers[loser] = 1
    keys = list(losers.keys())
    values = list(losers.values())
    fig, ax = plt.subplots()
    hbars = ax.barh(keys, values, align='center')
    ax.set_yticks(keys, labels=keys, fontsize=6)
    ax.invert_yaxis()
    ax.set_xlabel('World Series Losses')
    ax.set_title('World Series Losses by Team')
    ax.bar_label(hbars)
    ax.set_xlim(right=15)
    print("I have produced a bar graph that highlights the number of World Series' losses by team.")
    print("The New York Yankees have lost the most World Series' with 13 losses.")
    plt.show()

def qD(tbody):
    trs = tbody.find_all("tr")
    appearances = {}
    for index in range(len(trs)): 
        #individual tds within each tr
        indiv_tds = trs[index].find_all("td")
        ##only accounts for rows with world series info
        if len(indiv_tds) >= 4:
            #index 0 is american league winner index 3 is national league winner
            #the world series winner is bolded on the website
            if indiv_tds[0].find("strong") != None:
                team = indiv_tds[0].find("strong").text
                if team in appearances:
                    appearances[team] += 1
                else:
                    appearances[team] = 1
                team = indiv_tds[3].text
                if team in appearances:
                    appearances[team] += 1
                else:
                    appearances[team] = 1
            else:
                team = indiv_tds[3].find("strong").text
                if team in appearances:
                    appearances[team] += 1
                else:
                    appearances[team] = 1
                team = indiv_tds[0].text
                if team in appearances:
                    appearances[team] += 1
                else:
                    appearances[team] = 1
    keys = list(appearances.keys())
    values = list(appearances.values())
    fig, ax = plt.subplots()
    hbars = ax.barh(keys, values, align='center')
    ax.set_yticks(keys, labels=keys, fontsize=6)
    ax.invert_yaxis()
    ax.set_xlabel('World Series Appearances')
    ax.set_title('World Series Appearances by Team')
    ax.bar_label(hbars)
    ax.set_xlim(right=42)
    print("I have produced a bar graph that highlights the number of World Series' appearances by team.")
    print("The New York Yankees have the most World Series' apperarances with 40.")
    plt.show()
    
def qE(tbody):
    trs = tbody.find_all("tr")
    wins = {}
    for index in range(len(trs)): 
        #individual tds within each tr
        indiv_tds = trs[index].find_all("td")
        ##only accounts for rows with world series info
        if len(indiv_tds) >= 4:
            #index 0 is american league winner index 3 is national league winner
            #the world series winner is bolded on the website
            if indiv_tds[0].find("strong") != None:
                american = "American League"
                if american in wins:
                    wins[american] += 1
                else:
                    wins[american] = 1
            else:
                national = "National League"
                if national in wins:
                    wins[national] += 1
                else:
                    wins[national] = 1
    plt.title("World Series Wins by League")
    plt.pie(wins.values(), labels=wins.keys(), autopct='%.0f%%', pctdistance=1.15, labeldistance=.25)
    print("I have produced a pie chart that highlights World Series' wins by league.")
    print("The American League has won more World Series' than the National League.")
    plt.show()

# choice F - manager of a world series team
def qF(tbody):
    year, row, special_case = find_year()
    if special_case:
        return
    trs = tbody.find_all("tr")
    tds = trs[row].find_all("td")
    
    #index 0 is american league winner index 3 is national league winner
    #the winner is bolded on the html
    if tds[0].find("strong") != None:
        winner = tds[0].find("strong").text
        loser = tds[3].text
    elif tds[3].find("strong") != None:
        winner = tds[3].find("strong").text
        loser = tds[0].text
    
    print(f'In {year}, the {winner} won the World Series against the {loser}.')
    team, manager = find_manager(tds, winner, loser)
    print(f'The manager of the {year} {team} was {manager}.')

# choice F_a - manager of winning world series team
def qF_a(tds):
    #index 0 is american league winner index 3 is national league winner
    #the world series winner is bolded on the html
    if tds[0].find("strong") != None:
        team = tds[0].find("strong").text
        a = tds[0].find("a")
        link = a['href']
    else:
        team = tds[3].find("strong").text
        a = tds[3].find("a")
        link = a['href']
    return team, a, link

#choice F_b - manager of losing world series team
def qF_b(tds):
    #index 0 is american league winner index 3 is national league winner
    #the world series loser is not bolded on the html
    if tds[0].find("strong") != None:
        team = tds[3].text
        a = tds[3].find("a")
        link = a['href']
    else:
        team = tds[0].text
        a = tds[0].find("a")
        link = a['href']
    return team, a, link

#find manager function
def find_manager(tds, winner, loser):
    print(f'Do you want to find the manager for the {winner} or the {loser}?')
    print(f'   a) {winner}')
    print(f'   b) {loser}')
    options = {
        "a": qF_a,
        "b": qF_b
    }
    choice = getUserChoice(options)
    team, a, link = options[choice](tds)

    link = "https://www.baseball-reference.com" + link
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
    return team, a.text

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

# dictionary storing choices and functions that correspond to each choice
questions = {
    "a": qA,
    "b": qB,
    "c": qC,
    "d": qD,
    "e": qE,
    "f": qF
}

# prompts user to enter choice, will continue until choice is valid
def getUserChoice(options = questions):
    choice = None
    while choice not in options:
        choice = input("Please enter the letter of your choice: ").lower()
        if choice not in options:
            print("That is not one of the letters available.")
    return choice

# chatbot introduction and grabs user name
def intro():
    user = input("Hello! Please enter your name: ")
    print(f'Nice to meet you {user}, my name is BaseballBot, and I love baseball!')
    print("I see that you are interested in scraping Baseball Reference for World Series Data.")
    return user

# asks user if they want to find something else
def another_question(user):
    answer = input(user + ", would you like to find something else? ")
    answer = answer.lower()
    affirmative = ['yes','yeah','sure','y','ye','yup','ok','ya','yea']
    negative = ['no','n','nope','nop','nah','na','never']
    if answer in affirmative:
        main()
    elif answer in negative:
        print("Alright. Thanks for chatting with me!")
    else:
        print("I don't understand...")
        another_question(user)

# main function
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
    
    #introduction
    if not user:
        user = intro()

    #list choices for scraping and carry out functions
    choice = options()
    if choice in questions:
        questions[choice](tbody)
        another_question(user)
    return
    
if __name__ == "__main__":
    main()