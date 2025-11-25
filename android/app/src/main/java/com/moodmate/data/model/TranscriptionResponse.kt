package com.moodmate.data.model

data class TranscriptionResponse(
    val success: Boolean,
    val transcribed_text: String,
    val language: String? = null,
    val emotion: String? = null,  // Primary detected emotion
    val emotion_level: Int? = null,  // Emotion intensity level (1-10)
    val message: String? = null
)

