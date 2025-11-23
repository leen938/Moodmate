package com.moodmate

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.navigation.compose.rememberNavController
import com.moodmate.data.api.RetrofitClient
import com.moodmate.data.local.TokenManager
import com.moodmate.navigation.NavGraph
import com.moodmate.ui.theme.MoodMateTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        setContent {

            // ⭐ Global theme state (persists on rotation and UI recomposition)
            var isDarkTheme by rememberSaveable { mutableStateOf(false) }

            MoodMateTheme(darkTheme = isDarkTheme) {

                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    val navController = rememberNavController()
                    val tokenManager = TokenManager(this@MainActivity)

                    // Initialize retrofit — behavior unchanged
                    RetrofitClient.setAuthToken(null)

                    // ⭐ Pass theme state to NavGraph
                    NavGraph(
                        navController = navController,
                        isDarkTheme = isDarkTheme,
                        onDarkThemeChange = { isDarkTheme = it }
                    )
                }
            }
        }
    }
}
