# BBC_News_Article_Scraper

PROJECT GOAL :
- To write an application in Python to crawl an online news website (https://bbc.com) using a crawler framework (Scrapy)
- The application should cleanse the articles to obtain only information relevant to the news story. eg. article body, title, author, article url, date of publication.
- Store the data in a hosted mongo database (MongoDB Atlas) for subsequent search and retrieval. Ensure the URL of the article is included to enable comparison t the original.
- Write an API that provides access to the content in the mongo database. The user should be able to search for articles by keyword.


STEPS to implement the project on your terminal

1. Creat a virtual environment (new project if using Pycharm). Lets call it BBCnews_article
2. We install the following necessary packages for our project:
  - Scrapy
  - Pymongo
  - fastapi
  - dnspython
  - regex
  - uvicorn
3. Type in your terminal :  scrapy startproject bbcscraper
4. Then type : cd bbcscraper
5. Now go to the spider folder that gets autocreated when u execute step 3 and right click on it and click on new python file. lets name it bbc_newsarticle_scraper
6. Please refer to the bbc_newsarticle_scraper.py file for contents. This file scrapes the urls of the various articles on BBC homepage and then visits each page to 
   scrape information relevant to the news story, cleanses the data and finally pipelines the data to the hosted MongoDB. 
   * Few things to make note of
   - In the items.py file, make sure u define the various fields
   - In the settings.py file make sure you uncomment the three lines of code to configure the pipeline. the number 300 there basically gives the priority to the task
   - In the pipelines.py file, specify the Mongo URI and the mongo database and table to created in the database. Refer to the contents of  my pipelines.py and comments 
     for details
7. We can now execute our spider, by typing the following in our terminal: scrapy crawl bbccrawl 
   (- Note that bbccrawl was the name given to our spider and thats the way scrapy initates a crawl on the start_url mentioned)

8. You can now verify if the data has been uploaded to your database by going to the hosted MongoDB Cluster and checking the collections tab. You should see an Articledatabase
   database created and it will contain a Article_tb table which contains our scraped data.
   (Please note you can also create a JSON file by typing in the terminal : scrapy crawl bbccrawl -o Articledata.json)

9. Now finally we can run our API to extract data based on a keyword. In the terminal change the directory back to the original directory i.e BBCnews_article
   (you can type dir and see the list of files in your directory. Verify that main.py is there)

10. We can now execute our main.py file (please go through the contents of file and read comments for detailed explanation of how it extracts data based on keyword)

11. In our terminal type: uvicorn main:app --reload

12. On Executing this, a connection will be made to the local host. You can now visit http://127.0.0.1:8000/docs for the SWAGGER UI and enter keyword to obtain 
    the extracted News article data.
    (If you don't want to run the SWAGGER UI, then do not enter any parameter in the def findbykeyword() function a define a variable keyword with whatever word 
     you want to search. On executing the API in terminal and once connection is made. Go to http://127.0.0.1:8000/findbykeyword )

Created by Mr. Enrich Braz
