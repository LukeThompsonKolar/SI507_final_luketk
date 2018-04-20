import requests
import json
from bs4 import BeautifulSoup
import sqlite3

def get_cache():
    try:
        t=open("pokemon_cache.json",'r')
        cache_dict = json.loads(t.read())
        t.close()
    except:
        cache_dict={}

        baseurl = "https://pokemondb.net/pokedex/all"
        resp = requests.get(baseurl).text
        soup = BeautifulSoup(resp,"html.parser")

        names=soup.findAll('a',class_="ent-name")
        name_list,url_list=[],[]
        cache_dict = {}
        for n in names:
            name_list.append(n["href"])
        for u in name_list:
            if u not in url_list:
                url_list.append(u)

        for url_ending in url_list:
            url2 = "https://pokemondb.net"+url_ending
            resp2 = requests.get(url2).text
            soup2 = BeautifulSoup(resp2,"html.parser")

            bodies = soup2.findAll("tbody")
            data_dict = {}
            info_list = []
            name = soup2.find('article',class_="main-content grid-wrapper").find("h1").getText()
            if "\u2640" in name:
                name=name.replace("\u2640"," f")
            elif '\u2642' in name:
            	name=name.replace("\u2642"," m")
            info_list.append(name)

            for b in bodies[0].findAll("tr"):
                x = b.find("td").getText()
                if "\u00e9" in x:
                	x=x.replace("\u00e9","e")
                if "′" in x:
                    x=x.replace("′","'")
                if "″" in x:
                    x=x.replace('″','"')
                info_list.append(x)
	        
            if len(info_list)==8:
            	info_list.append(None)

            data_dict["info"] = [info_list[0],info_list[1],info_list[2][1:-1],info_list[3],info_list[4].split("(")[1][:-2],
            	info_list[5].split("(")[1][:-4],info_list[8]]

            stats_list = []
            stat_table = soup2.find("div",class_="col desk-span-8 lap-span-12").find("tbody")
            stats = stat_table.findAll("td",class_="num")

            for i in [0,3,6,9,12,15]:
                stats_list.append(int(stats[i].getText()))
            stats_list.append(int(soup2.find("td",class_="num-total").find("b").getText()))
            data_dict["stats"] = stats_list

            cache_dict[url_ending]=data_dict

        t=open("pokemon_cache.json",'w')
        t.write(json.dumps(cache_dict,sort_keys=True,indent=2))
        t.close()
    return(cache_dict)

def make_db():
    conn = sqlite3.connect('pokemon.db')
    cur = conn.cursor()

    statement = "DROP TABLE IF EXISTS 'Pokemon';"
    cur.execute(statement)
    statement = "DROP TABLE IF EXISTS 'Stats';"
    cur.execute(statement)
    conn.commit()

    statement = '''CREATE TABLE 'Pokemon' (
            'Id' INTEGER PRIMARY KEY,
            'Name' TEXT NOT NULL,
            'Type1' TEXT NOT NULL,
            'Type2' TEXT,
            'Species' TEXT NOT NULL,
            'Height' REAL NOT NULL,
            'Weight' REAL NOT NULL,
            'Japanese' TEXT
            );
    '''
    cur.execute(statement)
    statement = '''CREATE TABLE 'Stats' (
                'PokemonName' TEXT,
                'Total' INTEGER NOT NULL,
                'HP' INTEGER NOT NULL,
                'Attack' INTEGER NOT NULL,
                'Defense' INTEGER NOT NULL,
                'SpecialAttack' INTEGER NOT NULL,
                'SpecialDefense' INTEGER NOT NULL,
                'Speed' INTEGER NOT NULL,
                FOREIGN KEY (PokemonName) REFERENCES Pokemon(Name)
                );
    '''
    cur.execute(statement)
    conn.commit()
    conn.close()

def fill_db():
    conn = sqlite3.connect('pokemon.db')
    cur = conn.cursor()
    cache_dict = get_cache()
    for poke in cache_dict.keys():
        p = cache_dict[poke]["info"]
        types = p[2].split(" ")
        type1 = types[0]
        type2 = "None"
        if len(types)>1:
            type2 = types[1]
        j = p[6]
        if j is None:
            j = "N/A"
        insertion = (int(p[1]),p[0],type1,type2,p[3],float(p[4]),float(p[5]),j)
        statement = 'INSERT INTO "Pokemon" VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
        cur.execute(statement, insertion)

        p2 = cache_dict[poke]["stats"]
        insertion = (p[0],int(p2[6]),int(p2[0]),int(p2[1]),int(p2[2]),int(p2[3]),int(p2[4]),int(p2[5]))
        statement = 'INSERT INTO "Stats" VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
        cur.execute(statement, insertion)
    conn.commit()
    conn.close()

get_cache()
make_db()
fill_db()