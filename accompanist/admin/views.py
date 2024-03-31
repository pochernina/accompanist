from sqladmin import ModelView

from accompanist.collection.models import Album, Artist, Track


class AlbumAdmin(ModelView, model=Album):
    column_list = ["id", "artist", "name"]
    column_searchable_list = ["name", "artist"]
    name = "Альбом"
    name_plural = "Альбомы"
    icon = "fa-solid fa-record-vinyl"


class TrackAdmin(ModelView, model=Track):
    column_list = ["id", "artist", "name", "number_in_album", "is_favorite"]
    column_searchable_list = ["name", "artist"]
    name = "Трек"
    name_plural = "Треки"
    icon = "fa-solid fa-music"


class ArtistAdmin(ModelView, model=Artist):
    column_list = ["id", "name"]
    name = "Исполнитель"
    name_plural = "Исполнители"
    icon = "fa-solid fa-microphone"
