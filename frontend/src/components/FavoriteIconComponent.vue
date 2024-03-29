<template>
  <button
    class="favorite-button"
    :class="{ 'is-favorite': isFavorite }"
    @click.stop="toggleFavorite"
  >
    <FontAwesomeIcon class="favorite-icon" :icon="isFavorite ? faHeart : faHeartEmpty" />
  </button>
</template>

<script setup>
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { faHeart } from "@fortawesome/free-solid-svg-icons";
import { faHeart as faHeartEmpty } from "@fortawesome/free-regular-svg-icons";
import { defineProps, defineEmits } from "vue";

const props = defineProps({
  trackId: Number,
  isFavorite: Boolean,
});

const emit = defineEmits(["toggleIsFavorite"]);

function toggleFavorite() {
  emit("toggleIsFavorite");
}
</script>

<style scoped>
.favorite-button {
  background: none;
  border: none;
  cursor: pointer;
  transition: opacity 0.3s ease;
  padding: 0 15px 0 15px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.favorite-icon {
  color: #db4c4c;
}

.favorite-button,
.favorite-icon {
  height: 20px; /* Adjust as needed */
  line-height: 20px; /* Adjust to match the height for vertical centering */
}
.favorite-icon {
  align-self: center; /* Ensures the icon itself is centered within the flex container */
}
</style>
