package com.moodmate.data.model
data class Emotion(
    val label: String,
    val confidence: Float
)

data class TranscriptionResponse(
    val success: Boolean,
    val transcribed_text: String,
    val language: String? = null,
    val emotion: Emotion? = null,  // Now expects an object
    val emotion_level: Int? = null,
    val message: String? = null
)
