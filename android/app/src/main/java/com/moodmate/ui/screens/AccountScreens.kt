package com.moodmate.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import com.moodmate.ui.components.CustomTopAppBar

@Composable
fun EditProfileScreen(navController: NavController) {
    CustomTopAppBar("Edit Profile")
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.Top,
        horizontalAlignment = Alignment.Start
    ) {
        Text(
            text = "Edit Profile Screen (TODO: add fields)",
            style = MaterialTheme.typography.bodyLarge
        )
    }
}

@Composable
fun ChangePasswordScreen(navController: NavController) {
    CustomTopAppBar("Change Password")
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.Top,
        horizontalAlignment = Alignment.Start
    ) {
        Text(
            text = "Change Password Screen (TODO: add fields)",
            style = MaterialTheme.typography.bodyLarge
        )
    }
}
