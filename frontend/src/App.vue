<template>
  <div id="app">
    <HeaderComponent @goToAlbumChoosing="handleGoToAlbumChoosing" />
    <AddAlbumComponent
      v-if="appState === AppStates.UploadingNewAlbum"
      @confirmUploadNewAlbum="handleConfirmUploadNewAlbum"
      @goToAlbumChoosing="handleGoToAlbumChoosing"
    />
    <AlbumListComponent
      v-if="appState === AppStates.ChoosingAlbum"
      @selectAlbum="handleSelectAlbum"
      @uploadNewAlbum="handleUploadNewAlbum"
    />
    <AlbumComponent
      v-if="appState === AppStates.ChoosingTrack"
      :selectedAlbumId="selectedAlbumId"
      @goToAlbumChoosing="handleGoToAlbumChoosing"
      @selectTrack="handleSelectTrack"
      @deleteAlbum="handleDeleteAlbum"
    />
    <TrackComponent
      v-if="appState === AppStates.ListeningToTrack"
      :selectedAlbumId="selectedAlbumId"
      :selectedTrackId="selectedTrackId"
      @goToTrackChoosing="handleGoToTrackChoosing"
      @goToTrackById="handleGoToTrackById"
    />
  </div>
</template>

<script setup>
import AddAlbumComponent from "./components/AddAlbumComponent.vue";
import AlbumComponent from "./components/AlbumComponent.vue";
import AlbumListComponent from "./components/AlbumListComponent.vue";
import TrackComponent from "./components/TrackComponent.vue";
import HeaderComponent from "./components/HeaderComponent.vue";
import SpinnerComponent from "./components/SpinnerComponent.vue";

import { onMounted, provide, ref, computed, reactive } from "vue";

const _backendHost = process.env.VUE_APP_DEPLOYMENT_HOST || "localhost";
const _backendPort = process.env.VUE_APP_BACKEND_PORT || 8090;
const backendAddress = `http://${_backendHost}:${_backendPort}`;

provide("backendAddress", backendAddress);
const getStaticUrl = (filename) => {
  return `${backendAddress}/static/${filename}`;
};

// TODO: wrap with `useLocalStorage` from useVue
const userSettings = reactive({
  isAutoplayEnabled: false,
});

provide("getStaticUrl", getStaticUrl);
provide("userSettings", userSettings);

const appState = ref(1);

const AppStates = {
  UploadingNewAlbum: 0,
  ChoosingAlbum: 1,
  ChoosingTrack: 2,
  ListeningToTrack: 3,
};

const selectedAlbumId = ref(null);
const selectedTrackId = ref(null);

function scrollToTop() {
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function handleSelectAlbum(albumId) {
  selectedAlbumId.value = albumId;
  appState.value = AppStates.ChoosingTrack;
  scrollToTop();
}

function handleSelectTrack(trackId) {
  selectedTrackId.value = trackId;
  appState.value = AppStates.ListeningToTrack;
  scrollToTop();
}

function handleGoToAlbumChoosing() {
  appState.value = AppStates.ChoosingAlbum;
  scrollToTop();
}

function handleGoToTrackChoosing() {
  appState.value = AppStates.ChoosingTrack;
  scrollToTop();
}

function handleUploadNewAlbum() {
  appState.value = AppStates.UploadingNewAlbum;
  scrollToTop();
}

function handleConfirmUploadNewAlbum() {
  appState.value = AppStates.ChoosingAlbum;
  scrollToTop();
}

function handleGoToTrackById(newTrackId) {
  selectedTrackId.value = newTrackId;
  scrollToTop();
}

const handleDeleteAlbum = async () => {
  handleGoToAlbumChoosing();
};
</script>

<style>
@import url("https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap");

body {
  font-family: "Roboto", sans-serif;
  background-color: #fafafa;
}

h1,
h2,
h3,
h4,
h5,
h6 {
  font-family: "Roboto", sans-serif;
}

.clickable {
  cursor: pointer;
}

.spinner-container {
  margin-top: 200px;
}

/* Safari */
@-webkit-keyframes spin {
  0% {
    -webkit-transform: rotate(0deg);
  }

  100% {
    -webkit-transform: rotate(360deg);
  }
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}
</style>
