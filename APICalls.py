from tmdbv3api import TMDb
tmdb = TMDb()
tmdb.api_key = 'f53ed888427b55ea0dbb18cf5608d9d5'

import tmdbsimple as tmdb
tmdb.API_KEY = 'f53ed888427b55ea0dbb18cf5608d9d5'

tmdb.language = 'en'
tmdb.debug = True

from tmdbv3api import Movie

movie = Movie()


def getTitle(m_id):
    movie = tmdb.Movies(m_id)
    response = movie.info()
    return movie.title

def getPosterPath(m_id):
    movie = tmdb.Movies(m_id)
    response = movie.info()
    path="http://image.tmdb.org/t/p/w185/"+movie.poster_path
    return path

def getOverview(m_id):
    movie = tmdb.Movies(m_id)
    response = movie.info()
    return movie.overview

def getIdsfromQuery(title):
    ids=[]
    search = tmdb.Search()
    response = search.movie(query=title)
    for s in search.results:
        ids.append(s['id'])
    return ids

def getURL(m_id):
    title=getTitle(m_id)    
    title=title.replace(' ','-')
    path="https://www.themoviedb.org/movie/"+str(m_id)+"-"+title
    return path

def getRatings(m_id):
    movie = tmdb.Movies(m_id)
    response = movie.info()
    return movie.vote_average 

def getTrending():
    ids=[]
    popular = movie.popular()
    for p in popular:
        ids.append(p.id)
    return ids

def getRecommend(m_id=getTrending()[1]):
    ids=[]
    recommendations = movie.recommendations(movie_id=m_id)
    for recommendation in recommendations:
        ids.append(recommendation.id)
    return ids

def getUpcoming():
    ids=[]
    upcoming = movie.upcoming()
    for u in upcoming:
        ids.append(u.id)
    return ids




#print(str(getRatings(111)))

