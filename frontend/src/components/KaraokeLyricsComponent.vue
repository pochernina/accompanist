<template>
  <div class="karaoke-lyrics">
    <AudioComponent
      :timeupdate="updateCurrentLine"
      :src="getStaticUrl(track.filename_instrumental)"
      @goToNextTrack="$emit('goToNextTrack')"
      :autoplay="props.autoplay"
      :autocontinue="props.autocontinue"
    />
    <div class="lyrics">
      <div v-if="currentLineIndex % 2 == 0">
        <p class="current-line">{{ currentLineText }}</p>
        <p class="next-line">{{ nextLineText }}</p>
      </div>
      <div v-else>
        <p class="next-line">{{ nextLineText }}</p>
        <p class="current-line">{{ currentLineText }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps, inject, computed, defineEmits } from "vue";
import AudioComponent from "./AudioComponent.vue";

const emit = defineEmits(["goToNextTrack"]);

const props = defineProps({
  track: Object,
  autoplay: Boolean,
  autocontinue: Boolean,
});

const currentLineIndex = ref(0);
const linesNumber = computed(() => props.track.lyrics_karaoke.length);
const currentLineText = computed(() => {
  if (currentLineIndex.value >= linesNumber.value) {
    return "";
  } else {
    return props.track.lyrics_karaoke[currentLineIndex.value].line;
  }
});
const nextLineText = computed(() => {
  if (currentLineIndex.value + 1 >= linesNumber.value) {
    return "";
  } else {
    return props.track.lyrics_karaoke[currentLineIndex.value + 1].line;
  }
});
const getStaticUrl = inject("getStaticUrl");

const updateCurrentLine = (currentTime) => {
  // sustainable for track rewinding

  let low = 0;
  let high = linesNumber.value - 1;
  let mid;
  if (currentTime < props.track.lyrics_karaoke[0].end_ts) {
    currentLineIndex.value = 0;
    return;
  }
  if (currentTime >= props.track.lyrics_karaoke[high].end_ts) {
    currentLineIndex.value = high + 1;
    return;
  }
  while (low <= high) {
    mid = Math.floor((low + high) / 2);
    const midValEndTs = props.track.lyrics_karaoke[mid].end_ts;
    if (midValEndTs === currentTime) {
      currentLineIndex.value = mid;
      return;
    } else if (midValEndTs < currentTime) {
      low = mid + 1;
    } else {
      high = mid - 1;
    }
  }
  currentLineIndex.value = Math.max(0, low);
};
</script>

<style scoped>
.karaoke-lyrics .lyrics {
  position: relative;
  white-space: pre-wrap;
  font-size: 25px;
  margin-top: 20px;
  line-height: 1.5;
  padding: 15px; /* Добавлен внутренний отступ */
  text-align: center; /* Выравнивание текста по центру */
  background-color: #0093e9;
  color: white;
  background-image: linear-gradient(160deg, #0093e9 0%, #80d0c7 100%);
}

.current-line,
.next-line {
  width: 100%; /* Обеспечивает полную ширину для выравнивания текста */
  font-weight: bold;
}

.next-line {
  font-weight: normal; /* Устанавливаем обычное начертание для следующей строки */
}
</style>
