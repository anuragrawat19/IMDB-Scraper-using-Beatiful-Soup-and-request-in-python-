import requests #imported request moduel to do a request on a server with a particular URL
from bs4 import BeautifulSoup  #python library to parse data from html file
from pprint import pprint #pprint module provides a capability to “pretty-print” arbitrary Python data structures in a form which can be used as input to the interpreter.
import os.path,json,random,time


# task 1:- returns all  250 movies along with there details from IMDB.

def scrape_top_list():
	#checking whether a file exist in a system or not
	if os.path.isfile("movies_details.json"):
		with open("movies_details.json","r") as file1:
			read=file1.read()
			data=json.loads(read)
		return(data)

	# if file does not exist it will make a request to a server and store the data in a file (caching)
	a=random.randint(1,3)
	time.sleep(a)  #delaying  a request for random seconds between 1 and 3 so that our request is not consistent.
	url="https://www.imdb.com/india/top-rated-indian-movies/"
	data=requests.get(url)
	soup=BeautifulSoup(data.text,"html.parser")
	main_div=soup.find("div",class_="lister")
	tbody=main_div.find("tbody",class_="lister-list")
	trs=tbody.find_all("tr")

	movies_ranks=[]
	movie_name=[]
	year_of_release=[]
	movie_urls=[]
	movie_rating=[]
	for tr in trs:
		td=tr.find('td',class_="titleColumn").get_text().strip()
		rank=""
		for i in td:
			if "." not  in i:
				rank=rank+i
			else:
				break
		movies_ranks.append(rank)
		title=tr.find("td",class_="titleColumn").a.get_text()
		movie_name.append(title)
		year=tr.find("td",class_="titleColumn").span.get_text()
		year_of_release.append(year)
		rating=tr.find("td",class_="ratingColumn imdbRating").strong.get_text()
		movie_rating.append(rating)
		link=tr.find("td",class_="titleColumn").a["href"][:17]
		url="https://www.imdb.com"+link
		movie_urls.append(url)
	top_movies=[]
	dictionary={}
	for i in range(0,len(movies_ranks)):

	 	dictionary["name"]=str(movie_name[i])
	 	dictionary["rank"]=int(movies_ranks[i])
	 	year_of_release[i]=year_of_release[i][1:5]
	 	dictionary["year"]=int(year_of_release[i])
	 	dictionary["rating"]=float(movie_rating[i])
	 	dictionary["Url"]=movie_urls[i]
	 	top_movies.append(dictionary.copy())
	with open("movies_details.json","w") as file1:
		data=json.dump(top_movies,file1,indent=4)
	return(top_movies)

	
movies=(scrape_top_list())




# #------------------------------------------------------------------------------------------------------------------------
# # task 2 return the  details of all the movies that were released on the same year.


def group_by_year(movies):
	year=[]
	for i in movies:
		if i["year"] not in year:
			year.append(i["year"])
	movies_year_wise={}
	for year in year:
		a=[]
		for i in movies:
			if year==i["year"]:
				a.append(i)
		movies_year_wise[year]=a
	return (movies_year_wise)
group_by_year(movies)
dec_arg=group_by_year(movies)


# #---------------------------------------------------------------------------------------------------------------

# task3:- return the details of all the movies by grouping them in decades
def movies_by_decade(movies):
	movies_dec={}
	list1=[]
	for  index in movies:
		Mod=index%10
		decade=index-Mod
		if decade not in list1:
			list1.append(decade)
	list1.sort()
	for i in list1:
		movies_dec[i]=[]
	for i in movies_dec:
		dec10=i+9
		for x in movies:
		 	if x <=dec10 and x>=i:
		 		for v in movies[x]:
		 			movies_dec[i].append(v)
	return movies_dec
movies_by_decade(dec_arg)



#----------------------------------------------------------------------------------------------------------------------
#task 12
def scrape_movie_cast (movie_caste_url):
	url=movie_caste_url
	file_id=movie_caste_url[27:-31]
	file_name=file_id+"_cast.json"
	
	data=requests.get(url)
	soup=BeautifulSoup(data.text,"html.parser")
	
	movie_cast_details=[]
	dic={"imdb_id":"","name":""}

	main_table=soup.find("table",class_="cast_list")
	actors=main_table.find_all("td",class_="")

	for i in actors:
		imdb_id=i.find("a").get("href")[6:15]
		dic["imdb_id"]=imdb_id

		name=i.find("a").get_text().strip()
		dic["name"]=name
		movie_cast_details.append(dic.copy())

	
	return(movie_cast_details)


#----------------------------------------------------------------------------------------------------------

# task 4:- scrapping the details of an individual movies from its url
# task 8:- creating a json file for a particular movies
#task 9:-intereval of random  seconds bewtween 1sec-3sec at every request that we are doing
#task 13:- adding cast details in this function

def scrape_movie_details(movie_url):

	#task 9  
	
	file_name=movie_url[27:-1]
	movie_path=f"movies_details/{file_name}.json"
	if os.path.isfile(movie_path):
		with open(movie_path,"r") as file:
			read=file.read()
			data=json.loads(read)
		return(data)
	
	# a=random.randint(1,3)
	# time.sleep(a)

	movie_dic = {
				"name": "",
				"director":[],
				"country":"",
				"languages":[],
				"poster_image_url":"",
				"bio":"",
				"runtime":"",
				"genre":[]
				}
	url=movie_url
	data=requests.get(url)
	soup=BeautifulSoup(data.text,"html.parser") 

	Time = soup.find("div",class_= "subtext")
	runtime=Time.find("time").get_text().strip().split()
	_tm = ""
	if len(runtime) == 2:
		timeh = runtime[0][:-1]
		timem = runtime[1][:-3]
		tm = int(timeh)*60+int(timem)
		tm = str(tm)+"min"
		movie_dic["runtime"]=tm
	if len(runtime) == 1:
		timeh = runtime[0][:-1]
		tm = int(timeh*60)	
		tm = str(tm)+"min"
		movie_dic["runtime"]=tm

	main_div = soup.find("div",class_ = "heroic-overview")
	name = main_div.find("div",class_="title_wrapper").h1.get_text()[:-7]
	movie_dic["name"] = name

	post = soup.find("div",class_="poster").a.img["src"]
	movie_dic["poster_image_url"]=post

	bio=soup.find("div",class_="summary_text").get_text()
	movie_dic["bio"]=bio.strip()

	dir_div=soup.find("div",class_="credit_summary_item")
	directors=dir_div.find_all("a")
	for i in directors:
		movie_dic["director"].append(i.get_text())

	finding_genre=soup.find("div", id = "titleStoryLine")
	divs =finding_genre.find_all("div",class_ = "see-more inline canwrap")
	for i in divs:
		genre = i.find("h4", class_ = "inline").get_text()
		if "Genres:" == genre:
			genres=i.find_all("a")
			for i in genres:
				movie_dic["genre"].append(i.get_text())

	country_div=soup.find("div",id="titleDetails")
	country_sub_div=country_div.find_all("div",class_="txt-block")
	count=0
	for i in country_sub_div:
		data=i.find("h4")
		if count==2:
			break
		elif data.get_text()=="Country:":
			country=i.find("a").get_text()
			movie_dic["country"]=country
			count=count+1
		elif data.get_text()=="Language:":
			languages=i.find_all("a")
			count=count=count+1
			for i in languages:
				movie_dic["languages"].append(i.get_text())
	#task13: adding cast details
	cast=scrape_movie_cast(url)
	movie_dic["cast"]=cast

	# return(movie_dic)
	with open(movie_path,"w") as file:
		json.dump(movie_dic,file,indent=4)

	return (movie_dic)




#-----------------------------------------------------------------------------------------------------------------


# Task 5 scrapping the details of 10 movies from its url


def get_movie_list_details(movies_list):
	urls = []
	movies = []
	for dic in movies_list:
		link = dic["Url"]
		urls.append(link)
	for url in urls:
		movies.append(scrape_movie_details(url))
	return movies
get_movie_list_details(movies)
movies_list=get_movie_list_details(movies)






#---------------------------------------------------------------------------------------------------------------


#task 6 finding how many times movies  of  particular languges are there


def analyse_movies_language(movies_list):
	language_dic={}
	list1=[]
	for i in movies_list:
		for language in i["languages"]:
			list1.append(language)
	
	unique_lang=[]
	for language in list1:
		if language not in unique_lang:
			unique_lang.append(language)

	for lang in unique_lang:
		count=0
		for langu in list1:
			if lang==langu:
				count+=1
		language_dic[lang]=count
	return(language_dic)
analyse_movies_language(movies_list)


#--------------------------------------------------------------------------------------------------------------------


# #task 7 finding that a particualr directors name is repeating how many times as a director


def analyse_movies_directors(movies_list):
	directors={}
	list1=[]
	for i in movies_list:
		for direct in i["director"]:
			list1.append(direct)

	unique_director=[]
	for i in list1:
		if i not in unique_director:
			unique_director.append(i)


	for direct in  unique_director:
		count=0
		for director in list1:
			if direct==director:
				count+=1
		directors[direct]=count
	return(directors)



analyse_movies_directors(movies_list))


#----------------------------------------------------------------------------------------


#task 10  one directors has directed how many movies in hindi and how many in other languages



def analyse_language_and_directors(movies_list):
	dic={}

	for i in movies_list:
		for director in i["director"]:
			dic[director]={}
	for i in range(len(movies_list)):
		for director in dic:
			if director in movies_list[i]["director"]:
				for language in movies_list[i]["languages"]:
					dic[director][language]=0
	for i in range(len(movies_list)):
		for director in dic:
			if director in movies_list[i]["director"]:
				for language in movies_list[i]["languages"]:
					dic[director][language]+=1
	return(dic)

analyse_language_and_directors(movies_list)

#-----------------------------------------------------------------------------------------




#task 11 how many movies are their of particular Genre


def analyse_movies_genre(movies_list):
	genre_dic={}
	for i in movies_list:
		for genre in i["genre"]:
			genre_dic[genre]=0
	for i in range(len(movies_list)):
		for genre in genre_dic:
			if genre in movies_list[i]["genre"]:
				genre_dic[genre]+=1
	return(genre_dic)


(analyse_movies_genre(movies_list))

#-----------------------------------------------------------------------------------------


# Task 15:-  ONE ACTOR has workded in how  many movies.


def analyse_actors(movies_list):
	dic_actors={}
	for i in movies_list:
		for actor_id in i["cast"]:
			dic={"name":"","num_movies":0}
			for  i in movies_list:
	 			for id1 in i["cast"]:
	 				if actor_id["imdb_id"] == id1["imdb_id"]:
	 					dic["name"]=actor_id["name"]
	 					dic["num_movies"]+=1
			dic_actors[actor_id["imdb_id"]]=dic

	return(dic_actors)

analyse_actors(movies_list)


#---------------------------------------------------------------------------------------------------

