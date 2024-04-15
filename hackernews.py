import requests
from bs4 import BeautifulSoup as bss
import pprint 

# Beautiful Soup is a Python package for parsing HTML and XML documents. We could also scrapy- another web scraping tool for proffessionals
#pprint - pretty print used for better printing and formatting
#PARSING = the process of analyzing an HTML document and extracting its structural components,
#such as tags, attributes, and content, to create a structured representation of the document.

res = requests.get('https://news.ycombinator.com/news') # Getting the websites data
soup = bss(res.text, 'html.parser') #Have to mention the html.parser cuz beautiful soup also uses XML
#soup.body; soup.find_all('<a> tags or div); soup.find('a'); soup.contents; soup.title; soup.find(id="score_20203030") for getting upvotes no. are all valid arguments
res2 = requests.get('https://news.ycombinator.com/news?p=2') #The same thing for page 2 "?p=2"
soup2 = bss(res.text, 'html.parser') #parser it again

links = soup.select('.titleline') #We use selectors - allows us to grab a piece of data[html] by a CSS selector. To get score_id and .score to get class score
subtext = soup.select('.subtext') #grabs the upvotes of a headline in hackernews; we can even use upvotes.get()

links2 = soup2.select('.titleline') #same thing- also it used to be .storylink but now it changed to .titleline
subtext2 = soup2.select('.subtext') #same blah blah

merge_links = links + links2 #Merging links 1 and 2 to print out both pages at once
merge_subtext = subtext + subtext2 #subtext is actually the class above the upvotes class [see html page] 

def sort_stories_votes(hnlist): #This function is going to sort the stories in the page according to the no. of votes 
    return sorted(hnlist, key = lambda k:k['votes'], reverse=True) #The more number of votes to less number of votes and its reverse=True, passing 3 arguments
#We do have to get familiar to this argument above key = lamda k:k['votes'] to access items in a dictionary

def custom_hacker_news(links, subtext): #This is the essential function which is going to print out things we want on the terminal 
    hn = [] #And we are only returning the text and not the html code, hence we use a for loop to iterate through the links and text 
    for index, item in enumerate(links): 
        #We are using enumerate becuz both links and subtext are lists, if we dint enumerate we cant grab both of them
        #The enumerate() method adds a counter to an iterable and returns it in the form of an enumerating object

        title = item.getText() #getText() is a beautiful soup function that gets text instead of html code
        href = item.get('href', None) #A link in html is defined with an href and if there is no link for the story it returns a NONE object
        vote = subtext[index].select('.score') #score is a subclass of subtext. if we dont use subtext and use score instead, we get an IndexError
        if len(vote): #If the votes have no length then execute the below line of code
            points = int(vote[0].getText().replace(' points', '')) #Points intially is a string so we convert into a integer and we replace the space points to an empty string
            if points > 99: #And if the votes are less than 100 we dont wanna print it out 
                hn.append({'title': title , 'link' : href, 'votes' : points}) #Using a dict to combine  and print the title, links and votes of the story
    return sort_stories_votes(hn) #We are going to return the sort the stories according to votes in descending order after grabbing the hn list

pprint.pprint(custom_hacker_news(merge_links, merge_subtext)) #pprint is used to print better. and we're passing arguments for both pages [mege_links and merge_subtext]

