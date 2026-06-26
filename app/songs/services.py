import random
import requests
import logging
from sqlalchemy import or_
from app.models import LikedSongs, Song
from app.extensions import cache

ITUNES_URL= "https://itunes.apple.com/search"


#song searching logic
@cache.memoize(timeout=300)
def search_songs(query,entity,attribute):
    params={
        "term" : query,
        "entity" : entity,
        "attribute" : attribute,
        "limit" : 15,
        "timeout" : 5
    }
    try :
        response=requests.get(ITUNES_URL,params=params)
        response.raise_for_status()
    except requests.RequestException as e :
        logging.error(f"Song Api Error: {str(e)}")
        return None
    data=response.json()
    songs=[]
    for item in data.get("results",[]):
        songs.append({
            "song_id" : item.get("trackId"),
            "title" : item.get("trackName"),
            "artist" : item.get("artistName"),
            "album" : item.get("collectionName"),
            "preview" : item.get("previewUrl"),
            "image" : item.get("artworkUrl60")
        })
    return songs


#recommendation logic
def get_recommendation(user_id):
    liked_songs=LikedSongs.query.filter_by(user_id=user_id).all()
    if not liked_songs :
        all_songs=Song.query.all()
        random.shuffle(all_songs)
        return all_songs[:10]
    
    artists=[s.song.artist for s in liked_songs]
    albums=[s.song.album for s in liked_songs]
    if not artists and not albums:
        all_songs=Song.query.all()
        random.shuffle(all_songs)
        return all_songs[:10]
    
    liked_ids={s.song_id for s in liked_songs}

    songs=Song.query.filter(
        or_(Song.artist.in_(artists),
            Song.album.in_(albums)
            )
        ).all()
    
    unique={}

    for s in songs :
        if s.id not in liked_ids:
            unique[s.id]=s

    result=list(unique.values())
    
    #used list for artists since we just want a collection of items 
    #used a set for liked_ids since we are checking membership and TC for this operation in sets is O(1) while in list it would be O(n)
    #used dictionary for unique since we want unique songs only secondly we can easily acces the values while constructing the result
    if not result :
        all_songs=Song.query.all()
        random.shuffle(all_songs)
        return all_songs[:10]

    random.shuffle(result)
    return result[:10]