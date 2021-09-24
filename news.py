import requests
import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 170)
engine.setProperty('volume', 0.8)

def speak(text):
  engine.say(text)
  engine.runAndWait()

def NewsFromBBC():
     
    # BBC news api
    # following query parameters are used
    # source, sortBy and apiKey
    print("business")
    print("entertainment")
    print("general")
    print("health")
    print("science")
    print("technology")
    category_input =  input("Which category?: ")
    query_params = {
        "source": "bbc-news",
        "language": "en",
        "sortBy": "latest",
        "apiKey": "14566905717a4e8e8697766ce4a9e48d",
        "category": category_input
    }
    main_url = " https://newsapi.org/v2/top-headlines"
 
    # fetching data in json format
    res = requests.get(main_url, params=query_params)
    open_bbc_page = res.json()
 
    # getting all articles in a string article
    article = open_bbc_page["articles"]
 
    # empty list which will
    # contain all trending news
    results = []
     
    for ar in article:
        results.append(ar["title"])
         
    results_int = int(len(results))
    result_length = int(results_int / 2)
    for i in range(result_length):
         
        # printing all trending news
        result_obo = (i + 1, results[i])
        print(result_obo)	
 
    #to read the news out loud for us
             
 
# Driver Code
if __name__ == '__main__':
     
    # function call
    NewsFromBBC()