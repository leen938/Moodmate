package com.moodmate.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.navigation.NavController
import com.moodmate.ui.components.CustomTopAppBar

@Composable
fun SettingsScreen(navController: NavController) {
    CustomTopAppBar("Settings")
    Box(
        modifier = Modifier.fillMaxSize(),
        contentAlignment = Alignment.Center
    ) {
        Text("Settings page")
    }
}
