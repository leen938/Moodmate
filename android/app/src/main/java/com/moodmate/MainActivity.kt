package com.moodmate

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
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
            MoodMateTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    val navController = rememberNavController()
                    val tokenManager = TokenManager(this@MainActivity)
                    
                    // Initialize Retrofit with token manager
                    RetrofitClient.setAuthToken(null) // Will be set after login
                    
                    NavGraph(navController = navController)
                }
            }
        }
    }
}

