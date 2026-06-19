from flask import Blueprint, request
from app.songs.services import search_songs, get_recommendation
from flask_restful import Api,Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import LikedSongs, Song
from app import db
from app.schema import LikeSongSchema, SongSchema
import logging
from flasgger import swag_from

songs=Blueprint("songs",__name__, url_prefix="/api/songs")
api=Api(songs)

class SearchSongResource(Resource):
    @swag_from({
        "tags": ["Songs"],
        "summary": "Search for songs by query",
        "parameters": [
            {
                "name": "q",
                "in": "query",
                "required": True,
                "type": "string",
                "description": "Search query string",
                "example": "Blinding Lights"
            }
        ],
        "responses": {
            200: {
                "description": "Songs fetched and returned successfully",
                "examples": {
                    "application/json": {
                        "status": "success",
                        "data": [
                            {
                                "song_id": "spotify:track:3n3Ppam7vgaVa1iaRUIOKE",
                                "title": "Blinding Lights",
                                "artist": "The Weeknd",
                                "album": "After Hours"
                            }
                        ]
                    }
                }
            },
            400: {
                "description": "Missing query parameter 'q'",
                "examples": {
                    "application/json": {
                        "status": "fail",
                        "message": "query parameter 'q' is required"
                    }
                }
            },
            500: {
                "description": "Failed to fetch songs from external service",
                "examples": {
                    "application/json": {
                        "status": "fail",
                        "message": "Failed to fetch songs"
                    }
                }
            }
        }
    })
    def get(self):
        query=request.args.get("q")
        if not query :
            logging.warning(f"missing query parameter")
            return {
                "status" : "fail",
                "message" : " query parameter 'q' is required"
            }, 400
        
        songs=search_songs(query)
        if songs is None :
            return {
                "status" : "fail",
                "message" : "Failed to fetch songs"
            },500
        
        for s in songs:
            existing=Song.query.filter_by(song_id=s["song_id"]).first()
            if not existing :
                song=Song(**s)
                db.session.add(song)
        db.session.commit()

        logging.info(f"Search song with query parameter: {query}")
        return {
            "status" : "success",
            "data" : songs
        },200

class LikeSongResource(Resource):
    @swag_from({
        "tags": ["Songs"],
        "summary": "Like a song",
        "security": [{"Bearer": []}],
        "parameters": [
            {
                "name": "Authorization",
                "in": "header",
                "required": True,
                "type": "string",
                "description": "Bearer <JWT token>"
            },
            {
                "name": "body",
                "in": "body",
                "required": True,
                "schema": {
                    "type": "object",
                    "required": ["song_id"],
                    "properties": {
                        "song_id": {
                            "type": "string",
                            "example": "spotify:track:3n3Ppam7vgaVa1iaRUIOKE"
                        },
                        "title": {
                            "type": "string",
                            "example": "Blinding Lights"
                        },
                        "artist": {
                            "type": "string",
                            "example": "The Weeknd"
                        },
                        "album": {
                            "type": "string",
                            "example": "After Hours"
                        }
                    }
                }
            }
        ],
        "responses": {
            201: {
                "description": "Song liked successfully",
                "examples": {
                    "application/json": {
                        "status": "success",
                        "message": "Song added to LikedSongs!"
                    }
                }
            },
            400: {
                "description": "Validation error in request body",
                "examples": {
                    "application/json": {
                        "status": "fail",
                        "error": "{'song_id': ['Missing data for required field.']}"
                    }
                }
            },
            401: {
                "description": "Missing or invalid JWT token",
                "examples": {
                    "application/json": {
                        "msg": "Missing or Invalid Authorization Header"
                    }
                }
            },
            409: {
                "description": "Song already liked by the user",
                "examples": {
                    "application/json": {
                        "status": "fail",
                        "message": "Already Liked!"
                    }
                }
            }
        }
    })
    @jwt_required()
    def post(self):
        user_id=int(get_jwt_identity())
        data=request.get_json()
        schema=SongSchema()
        validated_data=schema.load(data)

        song=Song.query.filter_by(song_id=validated_data["song_id"]).first()
        if song not in Song:
            song=Song(**validated_data)
            db.session.add(song)
            db.session.commit()

        existing=LikedSongs.query.filter_by(
            user_id=user_id,song_id=validated_data["song_id"]
        ).first()
        if existing :
            logging.warning(f"User {user_id} tried to like already liked song {validated_data['song_id']}")
            return {
                "status" :"fail",
                "message" : "Already Liked!"
            },409
        
        liked_song=LikedSongs(user_id=user_id,song_id=song.id)
        db.session.add(liked_song)
        db.session.commit()
        logging.info(f"User {user_id} liked song {validated_data['song_id']}")
        return {
            "status" : "success",
            "message" : "Song added to LikedSongs!"
        },201


class GetLikedSongResource(Resource):
    @swag_from({
        "tags": ["Songs"],
        "summary": "Get all liked songs for the authenticated user (paginated)",
        "security": [{"Bearer": []}],
        "parameters": [
            {
                "name": "Authorization",
                "in": "header",
                "required": True,
                "type": "string",
                "description": "Bearer <JWT token>"
            },
            {
                "name": "page",
                "in": "query",
                "required": False,
                "type": "integer",
                "default": 1,
                "description": "Page number for pagination"
            },
            {
                "name": "limit",
                "in": "query",
                "required": False,
                "type": "integer",
                "default": 10,
                "description": "Number of songs per page"
            }
        ],
        "responses": {
            200: {
                "description": "Liked songs returned successfully (empty list if none found)",
                "examples": {
                    "application/json": {
                        "status": "success",
                        "data": [
                            {
                                "song_id": "spotify:track:3n3Ppam7vgaVa1iaRUIOKE",
                                "title": "Blinding Lights",
                                "artist": "The Weeknd",
                                "album": "After Hours"
                            }
                        ],
                        "pagination": {
                            "page": 1,
                            "total": 1
                        }
                    }
                }
            },
            401: {
                "description": "Missing or invalid JWT token",
                "examples": {
                    "application/json": {
                        "msg": "Missing or Invalid Authorization Header"
                    }
                }
            }
        }
    })
    @jwt_required()
    def get(self):
        user_id=get_jwt_identity()
        page=request.args.get("page",type=int, default=1)
        limit=request.args.get("limit", type=int, default=10)
        results_query=LikedSongs.query.filter_by(user_id=user_id)
        results=results_query.paginate(page=page,per_page=limit, error_out=False)
        if not results.items:
            return {
                "status": "success",
                "data": [],
                "pagination": {
                    "page": page,
                    "total": 0
                }
            },200

        songs= [like.song for like in results.items if like.song]

        ''' the above line is a query that creates a songs list for each LikedSongs object
        like is a single LikedSong object and like.song relates the song to song model
        results.items store LikedSongs object that only have song_id and user_id '''

        schema=SongSchema(many=True)
        logging.info(f"Fetched liked songs for user {user_id}")
        return {
            "status" : "success",
            "data" : schema.dump(songs),
            "pagination": {
                "page": page,
                "total": results.total
            }
        },200
    
class DeleteLikedSongResource(Resource):
    @swag_from({
        "tags": ["Songs"],
        "summary": "Unlike a song",
        "security": [{"Bearer": []}],
        "parameters": [
            {
                "name": "Authorization",
                "in": "header",
                "required": True,
                "type": "string",
                "description": "Bearer <JWT token>"
            },
            {
                "name": "song_id",
                "in": "path",
                "required": True,
                "type": "string",
                "description": "Internal DB song_id of the liked song to remove",
                "example": "spotify:track:3n3Ppam7vgaVa1iaRUIOKE"
            }
        ],
        "responses": {
            200: {
                "description": "Song unliked successfully",
                "examples": {
                    "application/json": {
                        "status": "success",
                        "message": "Song unliked successfully!"
                    }
                }
            },
            401: {
                "description": "Missing or invalid JWT token",
                "examples": {
                    "application/json": {
                        "msg": "Missing or Invalid Authorization Header"
                    }
                }
            },
            404: {
                "description": "Song not found in liked songs for this user",
                "examples": {
                    "application/json": {
                        "status": "fail",
                        "message": "Song not found!"
                    }
                }
            }
        }
    })
    @jwt_required()
    def delete(self,song_id):
        # song_id sent here is not the trackid from itunes app
        user_id=int(get_jwt_identity())
        song=LikedSongs.query.filter_by(song_id=song_id,user_id=user_id).first()
        if not song :
            return {
                "status" : "fail",
                "message" : "Song not found!"
            },404
        db.session.delete(song)
        db.session.commit()
        return {
            "status" : "success",
            "message" : "Song unliked successfully!"
        },200
    
class RecommendationResource(Resource):
    @swag_from({
        "tags": ["Songs"],
        "summary": "Get song recommendations for the authenticated user",
        "security": [{"Bearer": []}],
        "parameters": [
            {
                "name": "Authorization",
                "in": "header",
                "required": True,
                "type": "string",
                "description": "Bearer <JWT token>"
            }
        ],
        "responses": {
            200: {
                "description": "Recommendations fetched successfully",
                "examples": {
                    "application/json": {
                        "status": "success",
                        "data": [
                            {
                                "song_id": "spotify:track:0VjIjW4GlUZAMYd2vXMi3b",
                                "title": "Save Your Tears",
                                "artist": "The Weeknd",
                                "album": "After Hours"
                            }
                        ]
                    }
                }
            },
            401: {
                "description": "Missing or invalid JWT token",
                "examples": {
                    "application/json": {
                        "msg": "Missing or Invalid Authorization Header"
                    }
                }
            },
            500: {
                "description": "Failed to fetch recommendations from external service",
                "examples": {
                    "application/json": {
                        "status": "fail",
                        "message": "Failed to fetch songs"
                    }
                }
            }
        }
    })
    @jwt_required()
    def get(self):
        user_id=int(get_jwt_identity())
        recommendations=get_recommendation(user_id)
        if recommendations is None :
            return {
                "status" : "fail",
                "message" : "Failed to fetch songs"
            },500
        schema=SongSchema(many=True)
        logging.info(f"Fetched recommndations for user {user_id}")
        return {
            "status" : "success",
            "data":schema.dump(recommendations)
        },200
    

api.add_resource(SearchSongResource,"")
api.add_resource(LikeSongResource,"/like-song")
api.add_resource(GetLikedSongResource,"/liked-songs")
api.add_resource(DeleteLikedSongResource,"/liked-songs/<string:song_id>")
api.add_resource(RecommendationResource,"/recommendations")