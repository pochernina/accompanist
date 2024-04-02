<template>
  <div class="karaoke-player">
    <!--TODO: use AudioComponent here?-->
    <audio
      ref="audioPlayer"
      :src="mp3Url"
      @loadedmetadata="setupPlayer"
      controls
      class="audio-player"
    ></audio>
    <div class="controls">
      <button @click="recordTimecode" class="btn">Следующая строка</button>
      <button @click="recordInterludeEnd" class="btn">Конец проигрыша</button>
    </div>
    <div class="lyrics">
      <p class="current-line">
        {{ lyricsLines[currentLineIndex] }}
      </p>
      <p class="next-line">{{ lyricsLines?.[currentLineIndex + 1] }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, defineProps, defineEmits } from "vue";

const props = defineProps({
  mp3Url: String,
  lyricsText: String,
});
const emit = defineEmits(["sendRecordedKaraokeLyrics"]);

const audioPlayer = ref(null);
const lyricsLines = props.lyricsText
  .split("\n")
  .filter((line) => line.trim() && !line.trim().startsWith("["));
const lyricsWithTimecodes = reactive([]);
let currentLineIndex = ref(0);
let startTime = 0;

const setupPlayer = () => {
  if (audioPlayer.value) {
    audioPlayer.value.addEventListener("play", () => {
      startTime = audioPlayer.value.currentTime;
    });
    audioPlayer.value.play();
  }
};

const recordTimecode = () => {
  const endTime = audioPlayer.value.currentTime;
  lyricsWithTimecodes.push({
    line: lyricsLines[currentLineIndex.value],
    end_ts: endTime - startTime,
  });
  if (currentLineIndex.value == lyricsLines.length - 1) {
    emit("sendRecordedKaraokeLyrics", lyricsWithTimecodes);
    return;
  }
  currentLineIndex.value++;
};

const recordInterludeEnd = () => {
  let interludeText = "[Проигрыш]";
  let end_ts = audioPlayer.value.currentTime - startTime;
  if (
    lyricsWithTimecodes[lyricsWithTimecodes.length - 1]?.line !== interludeText
  ) {
    lyricsWithTimecodes.push({
      line: interludeText,
      end_ts: end_ts,
    });
  } else {
    // extend existing interlude
    lyricsWithTimecodes[lyricsWithTimecodes.length - 1].end_ts = end_ts;
  }
};
</script>

<style scoped>
.karaoke-player {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  font-family: "Arial", sans-serif;
}

.audio-player {
  max-width: 600px;
  width: 100%;
}

.controls {
  display: flex;
  gap: 10px;
}

.btn {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  border-radius: 5px;
  transition: background-color 0.2s;
}

.btn:hover {
  background-color: #1f77be;
}

.btn:active {
  background-color: #2196f3;
}

.lyrics {
  position: relative;
  white-space: pre-wrap;
  font-size: 25px;
  /* margin-top: 20px; */
  line-height: 1.5;
  padding: 30px; /* Добавлен внутренний отступ */
  text-align: center; /* Выравнивание текста по центру */
  /* background-color: #0093e9; */
  /* color: white; */
  /* background-image: linear-gradient(160deg, #0093e9 0%, #80d0c7 100%); */
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
