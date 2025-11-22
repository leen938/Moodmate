package com.moodmate.ui.screens

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import com.moodmate.ui.components.CustomTopAppBar

@Composable
fun SettingsScreen(navController: NavController) {

    // Local UI states (you can later connect these to DataStore / ViewModel)
    var isDarkModeEnabled by remember { mutableStateOf(false) }
    var isNotificationsEnabled by remember { mutableStateOf(true) }
    var isEmailNotificationsEnabled by remember { mutableStateOf(false) }
    var isVibrationEnabled by remember { mutableStateOf(true) }

    Scaffold(
        topBar = {
            CustomTopAppBar("Settings")
        }
    ) { innerPadding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
                .verticalScroll(rememberScrollState())
                .padding(16.dp)
        ) {

            // GENERAL
            SettingsSectionTitle(title = "General")

            SettingsSwitchRow(
                title = "Dark mode",
                description = "Use dark theme throughout the app",
                checked = isDarkModeEnabled,
                onCheckedChange = { isDarkModeEnabled = it } // TODO: persist
            )

            SettingsClickableRow(
                title = "Language",
                description = "App language",
                onClick = {
                    // TODO: navController.navigate("language")
                }
            )

            Spacer(modifier = Modifier.height(16.dp))

            // NOTIFICATIONS
            SettingsSectionTitle(title = "Notifications")

            SettingsSwitchRow(
                title = "Push notifications",
                description = "Receive updates and reminders",
                checked = isNotificationsEnabled,
                onCheckedChange = { isNotificationsEnabled = it }
            )

            SettingsSwitchRow(
                title = "Email notifications",
                description = "Get summaries by email",
                checked = isEmailNotificationsEnabled,
                onCheckedChange = { isEmailNotificationsEnabled = it }
            )

            SettingsSwitchRow(
                title = "Vibration",
                description = "Vibrate on important alerts",
                checked = isVibrationEnabled,
                onCheckedChange = { isVibrationEnabled = it }
            )

            Spacer(modifier = Modifier.height(16.dp))

            // ACCOUNT
            SettingsSectionTitle(title = "Account")

            SettingsClickableRow(
                title = "Edit profile",
                description = "Name, photo, and bio",
                onClick = {
                    // TODO: navController.navigate("editProfile")
                }
            )

            SettingsClickableRow(
                title = "Change password",
                description = "Update your password",
                onClick = {
                    // TODO: navController.navigate("changePassword")
                }
            )

            SettingsClickableRow(
                title = "Privacy & security",
                description = "Blocked users, data & permissions",
                onClick = {
                    // TODO: navController.navigate("privacy")
                }
            )

            Spacer(modifier = Modifier.height(16.dp))

            // ABOUT
            SettingsSectionTitle(title = "About")

            SettingsClickableRow(
                title = "About MoodMate",
                description = "Version 1.0.0 • Learn more",
                onClick = {
                    // TODO: navController.navigate("about")
                }
            )

            SettingsClickableRow(
                title = "Terms of use",
                onClick = {
                    // TODO: navController.navigate("terms")
                }
            )

            SettingsClickableRow(
                title = "Privacy policy",
                onClick = {
                    // TODO: navController.navigate("privacyPolicy")
                }
            )

            Spacer(modifier = Modifier.height(24.dp))

            // DANGER / LOGOUT
            Divider()
            Spacer(modifier = Modifier.height(12.dp))

            Text(
                text = "Danger zone",
                style = MaterialTheme.typography.bodyMedium.copy(
                    color = MaterialTheme.colorScheme.error,
                    fontWeight = FontWeight.SemiBold
                )
            )

            Spacer(modifier = Modifier.height(8.dp))

            Text(
                text = "Delete account",
                style = MaterialTheme.typography.bodyMedium.copy(
                    color = MaterialTheme.colorScheme.error
                ),
                modifier = Modifier
                    .fillMaxWidth()
                    .clickable {
                        // TODO: open confirm delete dialog
                    }
                    .padding(vertical = 8.dp)
            )

            Spacer(modifier = Modifier.height(24.dp))

            Button(
                onClick = {
                    // TODO: clear token, navigate to login screen
                    // navController.navigate("login") {
                    //     popUpTo(0)
                    // }
                },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(48.dp)
            ) {
                Text("Log out")
            }

            Spacer(modifier = Modifier.height(16.dp))
        }
    }
}

@Composable
private fun SettingsSectionTitle(title: String) {
    Text(
        text = title,
        style = MaterialTheme.typography.titleSmall.copy(fontWeight = FontWeight.SemiBold),
        modifier = Modifier
            .fillMaxWidth()
            .padding(bottom = 8.dp)
    )
}

@Composable
private fun SettingsSwitchRow(
    title: String,
    description: String? = null,
    checked: Boolean,
    onCheckedChange: (Boolean) -> Unit
) {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 8.dp)
    ) {
        Row(
            verticalAlignment = Alignment.CenterVertically,
            modifier = Modifier.fillMaxWidth()
        ) {
            Column(
                modifier = Modifier.weight(1f)
            ) {
                Text(
                    text = title,
                    style = MaterialTheme.typography.bodyLarge
                )
                if (description != null) {
                    Spacer(modifier = Modifier.height(2.dp))
                    Text(
                        text = description,
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            }

            Switch(
                checked = checked,
                onCheckedChange = onCheckedChange
            )
        }
        Divider(modifier = Modifier.padding(top = 8.dp))
    }
}

@Composable
private fun SettingsClickableRow(
    title: String,
    description: String? = null,
    onClick: () -> Unit
) {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .clickable { onClick() }
            .padding(vertical = 8.dp)
    ) {
        Text(
            text = title,
            style = MaterialTheme.typography.bodyLarge
        )
        if (description != null) {
            Spacer(modifier = Modifier.height(2.dp))
            Text(
                text = description,
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
        Divider(modifier = Modifier.padding(top = 8.dp))
    }
}
