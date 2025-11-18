package com.moodmate.ui.theme

import android.os.Build
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.dynamicDarkColorScheme
import androidx.compose.material3.dynamicLightColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.platform.LocalContext
import com.moodmate.ui.theme.PurplePrimary
import com.moodmate.ui.theme.PurpleSecondary
import com.moodmate.ui.theme.PurpleLight
import com.moodmate.ui.theme.White
import com.moodmate.ui.theme.WhiteBackground
import com.moodmate.ui.theme.PurpleDark

private val DarkColorScheme = darkColorScheme(
    primary = PurplePrimary,
    secondary = PurpleSecondary,
    tertiary = PurpleLight,
    background = androidx.compose.ui.graphics.Color(0xFF1A1A1A),
    surface = androidx.compose.ui.graphics.Color(0xFF2D2D2D),
    onPrimary = White,
    onSecondary = White,
    onBackground = White,
    onSurface = White
)

private val LightColorScheme = lightColorScheme(
    primary = PurplePrimary,
    secondary = PurpleSecondary,
    tertiary = PurpleLight,
    background = WhiteBackground,
    surface = White,
    onPrimary = White,
    onSecondary = White,
    onBackground = PurpleDark,
    onSurface = PurpleDark
)

@Composable
fun MoodMateTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    dynamicColor: Boolean = true,
    content: @Composable () -> Unit
) {
    val colorScheme = when {
        dynamicColor && Build.VERSION.SDK_INT >= Build.VERSION_CODES.S -> {
            val context = LocalContext.current
            if (darkTheme) dynamicDarkColorScheme(context) else dynamicLightColorScheme(context)
        }
        darkTheme -> DarkColorScheme
        else -> LightColorScheme
    }

    MaterialTheme(
        colorScheme = colorScheme,
        typography = androidx.compose.material3.Typography(),
        content = content
    )
}

