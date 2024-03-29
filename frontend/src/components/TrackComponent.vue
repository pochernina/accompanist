<template>
  <div class="track-details" v-if="track && album">
    <div @click="$emit('goToTrackChoosing')" class="go-back-button clickable">
      ← <slot>Назад</slot>
    </div>
    <h2>
      <FavoriteIconComponent
        :trackId="track.id"
        :isFavorite="track.is_favorite"
        class="favorite-component"
        @toggleIsFavorite="handleToggleIsFavorite"
      />
      {{ track.name }} by {{ album.artist.name }}
    </h2>
    <img :src="getStaticUrl(album.cover_path)" alt="Обложка альбома" class="album-cover" />
    <div class="songs-list">
      <div v-if="pageState === TrackPageStates.ShowSpinnerInsteadOfLyrics" class="marged-spinner">
        <SpinnerComponent size="70px" />
      </div>
      <div v-else>
        <div class="switch-outer-container">
          <div class="switch-container">
            <input
              id="karaoke-switch"
              type="checkbox"
              v-model="switchIsInKaraokeMode"
              @change="handleToggleLyricsMode"
            />
            <label for="karaoke-switch" class="switch-label">
              <span class="switch-label-text" v-if="switchIsInKaraokeMode">Режим караоке</span>
              <span class="switch-label-text" v-else>Полный текст</span>
            </label>
          </div>
        </div>
        <div class="navigation-buttons" v-if="!isSingle">
          <button v-if="!isFirstTrack" @click="goToPreviousTrack">Предыдущий трек</button>
          <button v-if="!isLastTrack" @click="goToNextTrack">Следующий трек</button>
        </div>

        <div v-if="switchIsInKaraokeMode">
          <button
            v-if="isKaraokeInRecordingMode"
            @click="toggleKaraokeRecordingMode"
            class="karaoke-toggle"
          >
            Назад
          </button>
          <button
            v-if="!karaokeModeIsAvaiable && !isKaraokeInRecordingMode"
            @click="toggleKaraokeRecordingMode"
            class="karaoke-toggle"
          >
            Разметить караоке-текст
          </button>
          <div v-if="isKaraokeInRecordingMode">
            <RecordTimecodesComponent
              :mp3Url="getStaticUrl(track.filename_original)"
              :lyricsText="track.lyrics"
              @sendRecordedKaraokeLyrics="handleUpdatedLyricsKaraoke"
            />
          </div>
          <div v-else>
            <div v-if="karaokeModeIsAvaiable">
              <KaraokeLyricsComponent :track="track" />
              <button @click="toggleKaraokeRecordingMode" class="karaoke-toggle">
                Переразметить караоке-текст
              </button>
              <button @click="removeLyricsKaraoke" class="karaoke-toggle">
                Удалить караоке-текст
              </button>
            </div>
          </div>
        </div>
        <div class="multiline-text" v-else>
          <AudioComponent
            :src="getStaticUrl(track.filename_instrumental)"
            :autoplay="userSettings.isAutoplayEnabled"
            :autocontinue="userSettings.isAutoplayEnabled"
            @finishAudio="
              () => {
                if (!isLastTrack) {
                  goToNextTrack();
                }
              }
            "
          />
          <AudioComponent :src="getStaticUrl(track.filename_vocals)" :autoplay="false" />
          <AudioComponent :src="getStaticUrl(track.filename_original)" :autoplay="false" />

          {{ track.lyrics }}
          <div class="updateLyricsButtonDiv">
            <div v-if="updateLyricsButtonIsLoading">
              <SpinnerComponent size="20px" />
            </div>
            <button v-else @click="updateLyrics" class="updateLyricsButton">Обновить текст</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { defineEmits, defineProps, inject, computed, ref, watch } from "vue";
import SpinnerComponent from "./SpinnerComponent.vue";
import KaraokeLyricsComponent from "./KaraokeLyricsComponent.vue";
import RecordTimecodesComponent from "./RecordTimecodesComponent.vue";
import AudioComponent from "./AudioComponent.vue";
import FavoriteIconComponent from "./FavoriteIconComponent.vue";

const backendAddress = inject("backendAddress");
const getStaticUrl = inject("getStaticUrl");
const updateLyricsButtonIsLoading = ref(false);
const TrackPageStates = {
  ShowSpinnerInsteadOfLyrics: 0,
  ShowPlainLyrics: 1,
  ShowKaraokeLyrics: 2,
  RecordKaraokeLyrics: 3,
};
const userSettings = inject("userSettings");

const pageState = ref(TrackPageStates.ShowSpinnerInsteadOfLyrics);

const props = defineProps({
  selectedTrackId: Number,
  selectedAlbumId: Number,
});

const emit = defineEmits(["goToTrackChoosing", "goToTrackById"]);

const track = ref(null);
const album = ref(null);

const switchIsInKaraokeMode = computed(() => {
  return pageState.value !== TrackPageStates.ShowPlainLyrics;
});

const karaokeModeIsAvaiable = computed(() => {
  return track.value?.lyrics_karaoke;
});

const isKaraokeInRecordingMode = ref(false);

const isFirstTrack = computed(() => track.value.number_in_album == 1);
const isLastTrack = computed(() => track.value.number_in_album == album.value.tracks.length);
const isSingle = computed(() => album.value.tracks.length == 1);

function toggleKaraokeRecordingMode() {
  isKaraokeInRecordingMode.value = !isKaraokeInRecordingMode.value;
}

function handleToggleLyricsMode() {
  if (pageState.value === TrackPageStates.ShowPlainLyrics) {
    pageState.value = TrackPageStates.ShowKaraokeLyrics;
  } else {
    pageState.value = TrackPageStates.ShowPlainLyrics;
  }
}

async function removeLyricsKaraoke() {
  if (window.confirm("Вы уверены, что хотите удалить эту разметку?")) {
    await handleUpdatedLyricsKaraoke(null);
  }
}

async function handleUpdatedLyricsKaraoke(lyrics_karaoke) {
  try {
    pageState.value = TrackPageStates.ShowSpinnerInsteadOfLyrics;
    const response = await fetch(`${backendAddress}/track/${track.value.id}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        lyrics_karaoke: lyrics_karaoke,
      }),
    });
    if (!response.ok) {
      throw new Error("Failed to update karaoke lyrics");
    }
    track.value = await response.json();
    chooseDefaultLyricsPage();
  } catch (error) {
    console.error(error);
    alert("Failed to update karaoke lyrics");
  }
}

async function handleToggleIsFavorite() {
  try {
    const response = await fetch(`${backendAddress}/track/${track.value.id}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        is_favorite: !track.value.is_favorite,
      }),
    });
    track.value = await response.json();
    if (!response.ok) {
      throw new Error("Failed to update is_favorite");
    }
  } catch (error) {
    console.error(error);
    alert("Failed to update is_favorite");
  }
}

async function updateLyrics() {
  try {
    updateLyricsButtonIsLoading.value = true;
    const response = await fetch(`${backendAddress}/tracks/${track.value.id}/lyrics`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });
    if (!response.ok) {
      throw new Error("Failed to update lyrics");
    }
    track.value = await response.json();
  } catch (error) {
    console.error(error);
    alert("Failed to update lyrics");
  } finally {
    updateLyricsButtonIsLoading.value = false;
  }
}

function goToNextTrack() {
  // `number_in_album` is indexed from 1
  let nextTrackId = album.value.tracks[track.value.number_in_album + 1 - 1].id;
  emit("goToTrackById", nextTrackId);
}

function goToPreviousTrack() {
  // `number_in_album` is indexed from 1
  let nextTrackId = album.value.tracks[track.value.number_in_album - 1 - 1].id;
  emit("goToTrackById", nextTrackId);
}

function chooseDefaultLyricsPage() {
  if (karaokeModeIsAvaiable.value) {
    pageState.value = TrackPageStates.ShowKaraokeLyrics;
    isKaraokeInRecordingMode.value = false;
  } else {
    pageState.value = TrackPageStates.ShowPlainLyrics;
  }
}
const fetchAlbum = async () => {
  try {
    const response = await fetch(`${backendAddress}/album/${props.selectedAlbumId}`);
    if (!response.ok) throw new Error("Failed to fetch");
    album.value = await response.json();
  } catch (error) {
    console.error("Error fetching album:", error);
  }
};

const fetchTrack = async () => {
  try {
    const response = await fetch(`${backendAddress}/track/${props.selectedTrackId}`);
    if (!response.ok) throw new Error("Failed to fetch");
    track.value = await response.json();
  } catch (error) {
    console.error("Error fetching album:", error);
  }
};

watch(
  () => props.selectedTrackId,
  async () => {
    await fetchTrack();
    chooseDefaultLyricsPage();
  },
  { immediate: true }
);

watch(
  () => props.selectedAlbumId,
  async () => {
    await fetchAlbum();
  },
  { immediate: true }
);
</script>

<style scoped>
.album-cover {
  display: block;
  margin-left: auto;
  margin-right: auto;
  /* margin-bottom: 40px; */
  max-width: 300px;
}

.track-details {
  max-width: 800px;
  margin: 10px auto;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
  background-color: white;
}

.track-details h2 {
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
  padding: 10px;
  background-color: #ffffff;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.song-title {
  font-weight: bold;
  color: #495057;
  margin-bottom: 5px;
}

.song-duration {
  font-style: italic;
  color: #6c757d;
  margin-bottom: 10px;
}

.song-info {
  display: flex;
  align-items: center;
  /* This will vertically center align the items if they have different heights */
  justify-content: space-between;
  /* Adjusts the space between the child elements */
}

.multiline-text {
  white-space: pre-wrap;
  font-size: 20px;
}

.navigation-buttons {
  display: flex;
  justify-content: center;
  gap: 10px; /* Adjust the gap between buttons as needed */
  margin: 20px 0; /* Adjust spacing as needed */
}

.navigation-buttons button {
  cursor: pointer;
  padding: 10px 15px;
  border: 1px solid #ccc;
  background-color: #f8f9fa;
  border-radius: 5px;
  transition: background-color 0.2s;
}

.updateLyricsButtonDiv {
  margin: 20px 0;
}
.updateLyricsButton {
  cursor: pointer;
  padding: 10px 15px;
  border: 1px solid #ccc;
  background-color: #f8f9fa;
  border-radius: 5px;
  transition: background-color 0.2s;
}
.switch-outer-container {
  display: flex;
  justify-content: center;
  margin: 20px 0;
}
.switch-container {
  position: relative;
  display: inline-block;
  width: 200px;
  height: 34px;
}

.switch-label {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: 0.6s;
  border-radius: 34px;
  /* padding: 0 10px; */
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: white;
  font-weight: bold;
}

#karaoke-switch:checked + .switch-label {
  background-color: #2196f3;
}

#karaoke-switch {
  opacity: 0;
  width: 0;
  height: 0;
}

.switch-label-text {
  margin: 0 auto;
}

.marged-spinner {
  margin-top: 50px;
}

.karaoke-toggle {
  padding: 10px 20px;
  margin: 10px 10px 10px 0;
  border: 1px solid #ccc;
  background-color: #f8f9fa;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s, color 0.3s;
  font-weight: bold;
}

.karaoke-toggle:hover {
  background-color: #e2e6ea;
}

.karaoke-toggle:focus {
  outline: none;
  box-shadow: 0 0 0 2px rgba(33, 150, 243, 0.5);
}

.favorite-component {
  position: relative;
  top: 0.1em;
  padding: 0 5px;
}

.track-heading {
  font-family: "Roboto", sans-serif;
  font-weight: 700; /* Bold */
  font-size: 24px; /* This is a common h2 size, adjust as needed */
  line-height: 1.2; /* Adjust based on your design */
}
</style>
