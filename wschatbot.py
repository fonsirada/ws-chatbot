import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

def main():
    page = requests.get("https://www.baseball-reference.com/postseason/world-series.shtml")
    soup = BeautifulSoup(page.content, 'html.parser')
    body = soup.find("body")
    div = body.find("div", class_="index")
    div1 = div.find("div", class_="table_wrapper")
    div2 = div1.find("div", class_="table_container")
    table = div2.find("table", class_="sortable stats_table")
    tbody = table.find("tbody")

    ## THINGS I WANT TO DO IN THE PROJECT
    ## SCRAPING BASEBALL-REFERENCE
    ##a. World Series Matchups by year and who won
    ##b. Graph which teams have won the most world series'
    ##c. most losses
    ##d. most appearances
    ##e. american league wins vs. national league wins (which wins more?)
    ##f. manager of world series winning teams
    
    
    user = intro()
    print("What would you like to find?:")
    print("   a) World Series Matchups by Year")
    print("   b) World Series Wins by Team")
    print("   c) World Series Losses by Team")
    print("   d) World Series Appearances by Team")
    print("   e) World Series Wins by League")
    print("   f) Manager of A World Series Team")
    question = input("Please enter the letter of your choice. ")
    if (question.lower() == "a"):
        year = int(input("Please enter a year (i.e: 1977) between 1903 and 2023 (no spaces!): "))
        qA(tbody,year)
        another_question(user)
        return
    if (question.lower() == "b"):
        qB(tbody)
        another_question(user)
        return
    if (question.lower() == "c"):
        qC(tbody)
        another_question(user)
        return
    if (question.lower() == "d"):
        qD(tbody)
        another_question(user)
        return
    if (question.lower() == "e"):
        qE(tbody)
        another_question(user)
        return
    if (question.lower() == "f"):
        year = int(input("Please enter a year (i.e: 1977) between 1903 and 2023 (no spaces!) to find the World Series' teams: "))
        winner, loser, row = qA(tbody,year)
        if winner != None:
            print(f'Do you want to find the manager for the {winner} or the {loser}?')
            print(f'   a) {winner}')
            print(f'   b) {loser}')
            answer = input("Please enter the letter of your choice. ")
            if (answer.lower() == "a"):
                qF(tbody,row,"w",winner,year)
                another_question(user)
                return
            if (answer.lower() == "b"):
                qF(tbody,row,"l",loser,year)
                another_question(user)
                return
            else:
                ##restarts code if user doesnt input a valid answer
                print("I don't think that's one of the letters available.")
                print("Restarting program...")
                main()
        another_question(user)
        return
    else:
        ##restarts code if user doesnt input a valid answer
        print("I don't think that's one of the letters available.")
        print("Restarting program...")
        main()
        
def qA(tbody,year):
    ##formula for finding the row that corresponds to each year
    row = 124 - (year - 1899)
    winner = None
    loser = None
    ##user entered a year that is before 1903
    if row > 120:
        print("I am afraid I cannot find information before 1903.")
        return winner, loser, row
    ##user entered a year that has not happened yet
    elif row < 0:
        print("I am afraid I cannot predict the future.")
        return winner, loser, row
    ##years where there was no world series
    elif row == 30:
        print("No World Series held in 1994 due to players' strike")
        return winner, loser, row
    elif row == 123:
        print("No World Series heeld in 1904 due to boycott by the New York Giants")
        return winner, loser, row

    trs = tbody.find_all("tr")
    tds = trs[row].find_all("td")
    
    #index 0 is american league winner index 3 is national league winner
    #the world series winner is bolded on the website
    if tds[0].find("strong") != None:
        winner = tds[0].find("strong").text
        loser = tds[3].text
    elif tds[3].find("strong") != None:
        winner = tds[3].find("strong").text
        loser = tds[0].text
    
    print(f'In {year}, the {winner} won the World Series against the {loser}.')
    
    return winner, loser, row
        
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
    
def qF(tbody,row,w_l,team,year):
    trs = tbody.find_all("tr")
    tds = trs[row].find_all("td")
    
    if w_l == "w":
        #index 0 is american league winner index 3 is national league winner
        #the world series winner is bolded on the website
        if tds[0].find("strong") != None:
            team = tds[0].find("strong").text
            a = tds[0].find("a")
            link = a['href']
        elif tds[3].find("strong") != None:
            team = tds[3].find("strong").text
            a = tds[3].find("a")
            link = a['href']
    else:
        if tds[0].find("strong") != None:
            team = tds[3].text
            a = tds[3].find("a")
            link = a['href']
        elif tds[3].find("strong") != None:
            team = tds[0].text
            a = tds[0].find("a")
            link = a['href']
            
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
    manager = a.text
    print(f'The manager of the {year} {team} was {manager}.')
    
    ##really cool function that I wanted to add, and that I believe is correct,
    ##but doesn't work because the website blocks me from accessing the website
    ##too many times
# def qG(tbody):
#     trs = tbody.find_all("tr")
#     managerwins = {}
#     for index in range(len(trs)): 
#         #individual tds within each tr
#         indiv_tds = trs[index].find_all("td")
#         ##only accounts for rows with world series info
#         if len(indiv_tds) >= 4:
#             #index 0 is american league winner index 3 is national league winner
#             #the world series winner is bolded on the website
#             if indiv_tds[0].find("strong") != None:
#                 a = indiv_tds[0].find("a")
#                 link = a['href']
#             elif indiv_tds[3].find("strong") != None:
#                 a = indiv_tds[3].find("a")
#                 link = a['href']
#         link = "https://www.baseball-reference.com" + link
#         HEADERS = {"User-Agent": """Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
#         AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"""}
#         page = requests.get(link, headers=HEADERS).text
#         soup = BeautifulSoup(page, 'html.parser')
#         body = soup.find("body")
#         div1 = body.find("div", class_="teams")
#         div2 = div1.find("div")
#         div2s = div2.find_all("div")
#         div3 = div2s[1]
#         ps = div3.find_all("p")
#         p = ps[2]
#         a = p.find("a")
#         manager = a.text
#     
#         if manager in managerwins:
#             managerwins[manager] += 1
#         else:
#             managerwins[manager] = 1
#                 
#     plt.title("World Series' Wins by Manager")
#     plt.xlabel("Manager")
#     plt.ylabel("World Series Wins")
#     ##figure out how to vertically shift values on x axis
#     plt.bar(managerwins.keys(),managerwins.values())
#     print("I have produced a bar graph that highlights the number of World Series' wins by manager.")
#     plt.show()
    
def intro():
    print("Hello! Nice to meet you, my name is BaseballBot.")
    user = input("What is your name? ")
    print(user + ", I see that you are interested in scraping the Baseball Reference website.")
    print("I love baseball!")
    return user

def another_question(user):
    answer = input(user + ", would you like to find something else? ")
    answer = answer.lower()
    affirmative = ['yes','yeah','sure','y','ye','yup','ok','ya','yea']
    negative = ['no','n','nope','nop','nah','na','never']
    if answer in affirmative:
        print("Ok! Restarting program...")
        main()
    if answer in negative:
        print("Alright. Thanks for chatting with me!")
    
if __name__ == "__main__":
    main()