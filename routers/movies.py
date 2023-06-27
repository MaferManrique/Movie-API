from fastapi import APIRouter
from fastapi import  Path, Query, Depends
from fastapi.responses import JSONResponse
from typing import List
from config.database import Session
from models.movie import Movie_model
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService
from schemas.movie import Movie

movie_router = APIRouter()


@movie_router.get('/movies', tags=["movies"], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movies()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.get('/movies/{id}', tags=["movies"], response_model =Movie) #get movie by id
def get_movie(id: int = Path(ge=1, le=1000)) -> Movie: #path param
    db = Session()
    result = MovieService(db).get_movies(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': "Not found"})
    return JSONResponse(status_code=200,content=jsonable_encoder(result))


@movie_router.get('/movies/', tags=["movies"], response_model=List[Movie]) #filter movie by category
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> Movie: #query param
    db = Session()
    result = MovieService(db).get_movies_by_category(category)
    if not result:
        return JSONResponse(status_code=404, content={'message': "Not found"})
    return JSONResponse(status_code=200,content=jsonable_encoder(result))
    

@movie_router.post('/movies', tags=["movies"], response_model=dict, status_code=201) #create movie
def create_movies(movie: Movie) -> dict:
    db = Session()
    MovieService(db).create_movie(movie)
    return JSONResponse(status_code=201,content={"message": "Se ha registrado la pelicula"})


@movie_router.put('/movies/{id}', tags=["movies"], response_model=dict,status_code=200) #update movies
def update_movie(id: int, movie: Movie)-> dict:
    db = Session()
    result = MovieService(db).get_movies_by_id(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': "Not found"})
    MovieService(db).update_movie(id, movie)
    return JSONResponse(status_code=200, content={"message": "Se ha modificado la pelicula"})

@movie_router.delete('/movies/{id}', tags=["movies"], response_model=dict,status_code=200) #delete movie by id
def delete_movies(id: int) -> dict:
    db = Session()
    result = db.query(Movie_model).filter(Movie_model.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message': "Not found"})
    MovieService(db).delete_movie(id)
    return JSONResponse(status_code=200,content={"message": "Se ha eliminado la pelicula"})