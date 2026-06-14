from flask import Blueprint, request
from flask_restful import Api,Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Playlist, PlaylistSong
from app import db
from app.schema import PlaylistCreateSchema, PlaylistResponseSchema, PlaylistSongCreateSchema, PlaylistSongResponseSchema
import logging
from flasgger import swag_from

playlist=Blueprint("playlist",__name__, url_prefix="/api")
api=Api(playlist)

class CreatePlaylistResource(Resource):
    @swag_from({
        "tags": ["Playlist"],
        "summary": "Create a new playlist",
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
                    "required": ["name"],
                    "properties": {
                        "name": {
                            "type": "string",
                            "example": "My Chill Playlist"
                        }
                    }
                }
            }
        ],
        "responses": {
            201: {
                "description": "Playlist created successfully",
                "examples": {
                    "application/json": {
                        "status": "success",
                        "message": "Playlist Created successfully!"
                    }
                }
            },
            400: {
                "description": "Validation error in request body",
                "examples": {
                    "application/json": {
                        "status": "fail",
                        "error": "{'name': ['Missing data for required field.']}"
                    }
                }
            },
            401: {
                "description": "Missing or invalid JWT token",
                "examples": {
                    "application/json": {
                        "msg": "Missing Authorization Header"
                    }
                }
            },
            409: {
                "description": "Playlist with that name already exists for this user",
                "examples": {
                    "application/json": {
                        "status": "fail",
                        "message": "Playlist already exists!"
                    }
                }
            }
        }
    })
    @jwt_required()
    def post(self):
        user_id=int(get_jwt_identity())
        data=request.get_json()
        schema=PlaylistCreateSchema()
        validated_data=schema.load(data)
        existing=Playlist.query.filter_by(user_id=user_id,name=validated_data["name"]).first()
        if existing :
            logging.info(f"Playlist {validated_data['name']} already exist for {user_id}")
            return {
                "status":"fail",
                "message":"Playlist already exists!"
            },409
        playlist=Playlist(user_id=user_id,**validated_data)
        db.session.add(playlist)
        db.session.commit()
        return {
            "status":"success",
            "message" : "Playlist Created successfully!"
        },201
    
class ViewPlaylistResource(Resource):
    @swag_from({
        "tags": ["Playlist"],
        "summary": "Get all playlists for the authenticated user",
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
                "description": "List of playlists returned successfully",
                "examples": {
                    "application/json": {
                        "status": "success",
                        "data": [
                            {"id": 1, "name": "My Chill Playlist", "user_id": 42},
                            {"id": 2, "name": "Workout Bangers", "user_id": 42}
                        ]
                    }
                }
            },
            401: {
                "description": "Missing or invalid JWT token",
                "examples": {
                    "application/json": {
                        "msg": "Missing Authorization Header"
                    }
                }
            },
            404: {
                "description": "No playlists found for this user",
                "examples": {
                    "application/json": {
                        "status": "fail",
                        "message": "No existing playlist!"
                    }
                }
            }
        }
    })
    @jwt_required()
    def get(self):
        #checking ownership {use query filter with userid to filter the playlists}
        user_id=int(get_jwt_identity())
        playlists=Playlist.query.filter_by(user_id=user_id).all()
        if not playlists :
            logging.info(f"No playlist found for user {user_id} !")
            return {
                "status" : "fail",
                "message" : "No existing playlist!"
            },404
        schema=PlaylistResponseSchema(many=True)
        return {
            "status" : "success",
            "data" : schema.dump(playlists)
        },200

class DeletePlaylistResource(Resource):
    @swag_from({
        "tags": ["Playlist"],
        "summary": "Delete a playlist by ID",
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
                "name": "playlist_id",
                "in": "path",
                "required": True,
                "type": "integer",
                "description": "ID of the playlist to delete",
                "example": 1
            }
        ],
        "responses": {
            200: {
                "description": "Playlist deleted successfully",
                "examples": {
                    "application/json": {
                        "status": "success",
                        "message": "playlist deleted successfully!"
                    }
                }
            },
            401: {
                "description": "Missing or invalid JWT token",
                "examples": {
                    "application/json": {
                        "msg": "Missing Authorization Header"
                    }
                }
            },
            404: {
                "description": "Playlist not found or does not belong to the user",
                "examples": {
                    "application/json": {
                        "status": "fail",
                        "message": "Playlist not found or unauthorised!"
                    }
                }
            }
        }
    })
    @jwt_required()
    def delete(self,playlist_id):
        user_id=int(get_jwt_identity())
        playlist=Playlist.query.filter_by(user_id=user_id,id=playlist_id).first()
        if not playlist:
            logging.info(f"User {user_id} tried deleting unauthorized playlist {playlist_id}")
            return {
                "status" : "fail",
                "message" : "Playlist not found or unauthorised!"
            },404
        db.sesion.delete(playlist)
        db.session.commit()
        logging.info(f"Playlist {playlist_id} deleted by user {user_id}")
        return {
            "status" : "success",
            "message" : "playlist deleted successfully!"
        },200
    

class AddPlaylistSongResource(Resource):
    @swag_from({
        "tags": ["Playlist"],
        "summary": "Add a song to a playlist",
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
                "name": "playlist_id",
                "in": "path",
                "required": True,
                "type": "integer",
                "description": "ID of the playlist to add the song to",
                "example": 1
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
                        }
                    }
                }
            }
        ],
        "responses": {
            201: {
                "description": "Song added to playlist successfully",
                "examples": {
                    "application/json": {
                        "status": "success",
                        "message": "song added to playlist!"
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
                        "msg": "Missing Authorization Header"
                    }
                }
            },
            404: {
                "description": "Playlist not found or does not belong to the user",
                "examples": {
                    "application/json": {
                        "status": "fail",
                        "message": "Playlist not found or unauthorized!"
                    }
                }
            },
            409: {
                "description": "Song already exists in the playlist",
                "examples": {
                    "application/json": {
                        "status": "fail",
                        "message": "Song already added to playlist!"
                    }
                }
            }
        }
    })
    @jwt_required()
    def post(self,playlist_id):
        #step1 check ownership (the user access its own playlist only)
        user_id=int(get_jwt_identity())
        playlist=Playlist.query.filter_by(id=playlist_id,user_id=user_id).first()
        if not playlist:
            return{
                "status":"fail",
                "message":"Playlist not found or unauthorized!"
            },404
        #step2 validate data
        data=request.get_json()
        schema=PlaylistSongCreateSchema()
        validated_data=schema.load(data)
        #step3 check for duplicates
        existing=PlaylistSong.query.filter_by(playlist_id=playlist_id,song_id=validated_data["song_id"]).first()
        if existing:
            logging.info(f"Song {validated_data['song_id']} already exist in playlist {playlist_id}")
            return {
                "status" : "fail",
                "message" : "Song already added to playlist!"
            },409
        #step 4 add song to db
        song = PlaylistSong(playlist_id=playlist_id, **validated_data)
        db.session.add(song)
        db.session.commit()
        logging.info(f"Song {validated_data['song_id']} added to playlist {playlist_id} for user {user_id} !")
        return{
            "status":"success",
            "message":"song added to playlist!"
        },201

class ViewPlaylistSongResource(Resource):
    @swag_from({
        "tags": ["Playlist"],
        "summary": "View all songs in a playlist (paginated)",
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
                "name": "playlist_id",
                "in": "path",
                "required": True,
                "type": "integer",
                "description": "ID of the playlist to view songs from",
                "example": 1
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
                "description": "Songs retrieved successfully (empty list if none found)",
                "examples": {
                    "application/json": {
                        "status": "success",
                        "data": [
                            {"id": 1, "playlist_id": 1, "song_id": "spotify:track:3n3Ppam7vgaVa1iaRUIOKE"},
                            {"id": 2, "playlist_id": 1, "song_id": "spotify:track:0VjIjW4GlUZAMYd2vXMi3b"}
                        ],
                        "pagination": {
                            "page": 1,
                            "total": 2
                        }
                    }
                }
            },
            401: {
                "description": "Missing or invalid JWT token",
                "examples": {
                    "application/json": {
                        "msg": "Missing Authorization Header"
                    }
                }
            },
            404: {
                "description": "Playlist not found or does not belong to the user",
                "examples": {
                    "application/json": {
                        "status": "fail",
                        "message": "Playlist not found or unauthorized!"
                    }
                }
            }
        }
    })
    @jwt_required()
    def get(self,playlist_id):
        user_id=int(get_jwt_identity())
        playlist=Playlist.query.filter_by(id=playlist_id,user_id=user_id).first()
        if not playlist:
            return {
                "status" : "fail",
                "message":"Playlist not found or unauthorized!"
            },404
        page=request.args.get("page", type=int , default=1)
        limit=request.args.get("limit", type=int, default=10)
        songs_query=PlaylistSong.query.filter_by(playlist_id=playlist_id)
        songs=songs_query.paginate(page=page, per_page=limit, error_out=False)
        if not songs.items:
            return {
                "status": "success",
                "data": [],
                "pagination": {
                    "page": page,
                    "total": 0
                }
            },200
        schema=PlaylistSongResponseSchema(many=True)
        return {
            "status" : "success",
            "data" : schema.dump(songs.items),
            "pagination": {
                "page": page,
                "total": songs.total
            }
        },200

class RemovePlaylistSongResource(Resource):
    @swag_from({
        "tags": ["Playlist"],
        "summary": "Remove a song from a playlist",
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
                "name": "playlist_id",
                "in": "path",
                "required": True,
                "type": "integer",
                "description": "ID of the playlist",
                "example": 1
            },
            {
                "name": "song_id",
                "in": "path",
                "required": True,
                "type": "string",
                "description": "ID of the song to remove",
                "example": "spotify:track:3n3Ppam7vgaVa1iaRUIOKE"
            }
        ],
        "responses": {
            200: {
                "description": "Song removed from playlist successfully",
                "examples": {
                    "application/json": {
                        "status": "success",
                        "message": "song removed successfully!"
                    }
                }
            },
            401: {
                "description": "Missing or invalid JWT token",
                "examples": {
                    "application/json": {
                        "msg": "Missing Authorization Header"
                    }
                }
            },
            404: {
                "description": "Playlist or song not found, or unauthorized access",
                "examples": {
                    "application/json": {
                        "status": "fail",
                        "message": "Playlist not found or unauthorized!"
                    }
                }
            }
        }
    })
    @jwt_required()
    def delete(self,playlist_id,song_id):
        user_id=int(get_jwt_identity())
        playlist=Playlist.query.filter_by(id=playlist_id,user_id=user_id).first()
        if not playlist:
            logging.info(f"User {user_id} tried deleting song from unauthorized playlist {playlist_id}")
            return {
                "status" : "fail",
                "message" : "Playlist not found or unauthorized!"
            },404
        song=PlaylistSong.query.filter_by(playlist_id=playlist_id,song_id=song_id).first()
        if not song:
            logging.info(f"User {user_id} tried deleting unauthorized song {song_id}")
            return {
                "status" : "fail",
                "message" : "Song not found or unauthorized!"
            },404
        db.session.delete(song)
        db.session.commit()
        logging.info(f"song {song_id} removed from playlist {playlist_id} by user {user_id}")
        return{
            "status" : "success",
            "message" : "song removed successfully!"
        },200


api.add_resource(CreatePlaylistResource,"/playlists")
api.add_resource(ViewPlaylistResource,"/playlists")
api.add_resource(DeletePlaylistResource,"/playlists/<int:playlist_id>")

api.add_resource(AddPlaylistSongResource,"/playlists/<int:playlist_id>/songs")
api.add_resource(ViewPlaylistSongResource,"/playlists/<int:playlist_id>/songs")
api.add_resource(RemovePlaylistSongResource,"/playlists/<int:playlist_id>/songs/<string:song_id>")