<template>
  <div class="album-details" v-if="album">
    <div @click="$emit('goToAlbumChoosing')" class="go-back-button clickable">
      ← <slot>Назад</slot>
    </div>
    <h2>{{ album.name }} by {{ album.artist.name }}</h2>
    <img :src="getStaticUrl(album.cover_path)" alt="Обложка альбома" class="album-cover" />
    <div class="songs-list">
      <ul>
        <li
          v-for="track in album.tracks"
          :key="track.id"
          @click="$emit('selectTrack', track.id)"
          :class="{ 'has-karaoke-lyrics': track.has_lyrics_karaoke }"
        >
          <div class="song-info">
            <div class="song-title clickable">
              <FavoriteIconComponent
                :trackId="track.id"
                :isFavorite="track.is_favorite"
                class="favorite-component"
                @toggleIsFavorite="() => handleToggleIsFavorite(track)"
              />

              {{ track.name }}
            </div>
            <div class="song-duration">{{ track.duration }}</div>
          </div>
        </li>
      </ul>
    </div>
    <button @click="deleteAlbum" class="delete-album-button">Удалить альбом</button>
  </div>
</template>

<script setup>
import { defineProps, inject, defineEmits, onMounted, ref } from "vue";

import FavoriteIconComponent from "./FavoriteIconComponent.vue";

const backendAddress = inject("backendAddress");
const getStaticUrl = inject("getStaticUrl");

const props = defineProps({
  selectedAlbumId: Number,
});

const album = ref(null);

const emit = defineEmits(["selectTrack", "goToAlbumChoosing", "deleteAlbum"]);

const fetchAlbum = async () => {
  try {
    const response = await fetch(`${backendAddress}/album/${props.selectedAlbumId}`);
    if (!response.ok) throw new Error("Failed to fetch");
    album.value = await response.json();
  } catch (error) {
    console.error("Error fetching album:", error);
  }
};

onMounted(async () => {
  await fetchAlbum();
});

const deleteAlbum = async () => {
  if (window.confirm("Вы уверены, что хотите удалить этот альбом?")) {
    try {
      const response = await fetch(`${backendAddress}/album/${album.value.id}`, {
        method: "DELETE",
      });
      if (response.ok) {
        emit("deleteAlbum");
      } else {
        alert("Произошла ошибка при удалении альбома.");
      }
    } catch (error) {
      console.error("Ошибка при удалении альбома:", error);
      alert("Произошла ошибка при удалении альбома.");
    }
  }
};

async function handleToggleIsFavorite(track) {
  try {
    const response = await fetch(`${backendAddress}/track/${track.id}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        is_favorite: !track.is_favorite,
      }),
    });
    await fetchAlbum();
    if (!response.ok) {
      throw new Error("Failed to update is_favorite");
    }
  } catch (error) {
    console.error(error);
    alert("Failed to update is_favorite");
  }
}
</script>

<style scoped>
.album-cover {
  display: block;
  margin-left: auto;
  margin-right: auto;
  margin-bottom: 40px;
  max-width: 300px;
}

.album-details {
  max-width: 800px;
  margin: 10px auto;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
  background-color: white;
}

.album-details h2 {
  color: #343a40;
  margin-bottom: 16px;
  text-align: center;
}

.songs-list ul {
  list-style-type: none;
  padding: 0;
  margin-top: 0;
}

.songs-list li {
  margin-bottom: 20px;
  padding: 10px 30px 10px 10px;
  background-color: #ffffff;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.song-title {
  font-weight: bold;
  color: #495057;
  /* margin-bottom: 5px; */
  display: flex;
  align-items: center;
  justify-content: start; /* Ensures content is aligned to the start */
  width: 100%; /* Ensures the .song-title takes full width of its parent for better alignment */
}

.song-duration {
  font-style: italic;
  color: #6c757d;
}

.song-info {
  display: flex;
  align-items: center;
  /* This will vertically center align the items if they have different heights */
  justify-content: space-between;
  /* Adjusts the space between the child elements */
}

.has-karaoke-lyrics {
  background-color: #e9f5db; /* A light green background for karaoke tracks */
  border-left: 4px solid #2196f3; /* A green border on the left for emphasis */
  padding-left: 26px; /* Adjust padding to accommodate the border */
}

audio {
  width: 100%;
  margin-top: 10px;
}

.delete-album-button {
  background-color: #c0392b;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 20px;
  display: block;
  margin-left: auto;
  margin-right: auto;
}

.delete-album-button:hover {
  background-color: darkred;
}
.favorite-component {
  margin-top: -0.2em;
}
</style>
