package com.moodmate.data.model

data class Emotion(
    val primary_emotion: String?,
    val confidence: Float?
)

data class TranscriptionResponse(
    val success: Boolean,
    val transcribed_text: String,
    val language: String? = null,
    val emotion: Emotion? = null,
    val emotion_level: Int? = null,
    val message: String? = null
)