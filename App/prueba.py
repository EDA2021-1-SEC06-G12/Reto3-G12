import config as cf
import csv
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import map as mp
from DISClib.ADT import list as lt


events2file=cf.data_dir+'user_track_hashtag_timestamp-small.csv'
input2_file = csv.DictReader(open(events2file, encoding="utf-8"),delimiter=",")
mapa=mp.newMap()
for event in input2_file:
    llave=(event['track_id'],event['user_id'],event['created_at'])
    if mp.contains(mapa,llave):
        pareja=mp.get(mapa,llave)
        lista=me.getValue(pareja)
        lt.addLast(lista,event['hashtag'])
    else:
        lista=lt.newList()
        lt.addLast(lista,event['hashtag'])
        mp.put(mapa,llave,lista)

eventsfile=cf.data_dir + 'context_content_features-small.csv'
input_file = csv.DictReader(open(eventsfile, encoding="utf-8"),delimiter=",")
i=1
for event in input_file:
    llave=(event['track_id'],event['user_id'],event['created_at'])
    if mp.contains(mapa,llave):
        pareja=mp.get(mapa,llave)
        hashtags=me.getValue(pareja)
        event['hashtags']=hashtags
    else:
        event['hashtags']=None


file3=cf.data_dir+'sentiment_values.csv'
input_file3=csv.DictReader(open(file3, encoding="utf-8"),delimiter=",")
i=1
for hashtag in input_file3:
    while i<2:
        x=(hashtag[' ss_avg'])
        if x=='':
            print('miau')
        else:
            print('guau')
        i+=1