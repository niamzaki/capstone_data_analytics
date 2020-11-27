from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.imdb.com/search/title/?release_date=2019-01-01,2019-12-31')
soup = BeautifulSoup(url_get.content,"html.parser")

tbody = soup.find('div',attrs={'class':'lister-list'})
total_film = tbody.find_all('div',attrs={'class':"lister-item mode-advanced"})
judul=tbody.find_all('h3',attrs={'class':"lister-item-header"})
voting=tbody.find_all('p',attrs={'class':"sort-num_votes-visible"})
imdb=tbody.find_all('div',attrs={'class':"inline-block ratings-imdb-rating"})
metascore=tbody.find_all('div',attrs={'class':"inline-block ratings-metascore"})
 #initiating a tuple
storage_metascore=[]
for i in range(0,len(metascore)):
    metascore=tbody.find_all('div',attrs={'class':"inline-block ratings-metascore"})
    metascore=metascore[i].text.split('\n')[1].strip()
    storage_metascore.append(metascore)

storage=[]
for i in range(0, len(total_film)):
    if "inline-block ratings-metascore" in str(total_film[i]):
        storage.append(i)
    else:
        pass
    
list_besar=[None]*len(total_film)    

for c in range(0,len(storage_metascore)):
    list_besar[storage[c]]=storage_metascore[c]

#insert the scrapping process here    
judul_film=[]
jumlah_voting=[]
rating_imdb=[]
for i in range(0, len(total_film)):
    judul=tbody.find_all('h3',attrs={'class':"lister-item-header"})
    judul=judul[i].text.split('\n')[2]
    judul_film.append(judul)
    
    voting=tbody.find_all('p',attrs={'class':"sort-num_votes-visible"})
    voting=voting[i].text.split('\n')[2]
    jumlah_voting.append(voting)
    
    imdb=tbody.find_all('div',attrs={'class':"inline-block ratings-imdb-rating"})
    imdb=imdb[i].text.split('\n')[2]
    rating_imdb.append(imdb)
    
   

#change into dataframe

data = pd.DataFrame(list(zip( jumlah_voting, rating_imdb, list_besar)), 
               columns =[ 'jumlah_voting', 'rating_imdb','metascore'],
                 index=judul_film)

#insert data wrangling here
data['rating_imdb']=data['rating_imdb'].astype(float)
data['jumlah_voting']=data['jumlah_voting'].str.replace(',', '').astype(int)
data['metascore']=data['metascore'].astype(float)

#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'USD {data["jumlah_voting"].mean()}'

	# generate plot
	ax = data.plot(figsize = (20,9))
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]


	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)
