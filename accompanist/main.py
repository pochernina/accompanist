from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin

from accompanist.admin.views import AlbumAdmin, ArtistAdmin, TrackAdmin
from accompanist.collection.router import router as collection_router
from accompanist.database import engine

app = FastAPI(
    title="Accompanist",
)

app.include_router(collection_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

admin = Admin(app, engine, base_url="/admin")
for admin_view in (AlbumAdmin, TrackAdmin, ArtistAdmin):
    admin.add_view(admin_view)
