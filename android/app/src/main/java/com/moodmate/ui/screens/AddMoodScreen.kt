package com.moodmate.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import com.moodmate.ui.components.CustomTopAppBar
import com.moodmate.ui.theme.PurplePrimary
import com.moodmate.ui.theme.White

@Composable
fun AddMoodScreen(navController: NavController) {
    var selectedMood by remember { mutableStateOf(0) }
    var notes by remember { mutableStateOf("") }
    
    Column(modifier = Modifier.fillMaxSize()) {
        CustomTopAppBar(
            title = "Add Mood",
            onBackClick = { navController.popBackStack() }
        )
        
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(24.dp),
            verticalArrangement = Arrangement.spacedBy(24.dp)
        ) {
            Text(
                "How are you feeling?",
                style = MaterialTheme.typography.headlineMedium,
                fontWeight = FontWeight.Bold
            )
            
            // Mood Selector
            // Mood Selector: 2 rows of 5
            Column(
                modifier = Modifier.fillMaxWidth(),
                verticalArrangement = Arrangement.spacedBy(12.dp),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceEvenly
                ) {
                    (1..5).forEach { level ->
                        MoodButton(
                            level = level,
                            isSelected = selectedMood == level,
                            onClick = { selectedMood = level }
                        )
                    }
                }

                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceEvenly
                ) {
                    (6..10).forEach { level ->
                        MoodButton(
                            level = level,
                            isSelected = selectedMood == level,
                            onClick = { selectedMood = level }
                        )
                    }
                }
            }

            // Notes
            OutlinedTextField(
                value = notes,
                onValueChange = { notes = it },
                label = { Text("Notes (optional)") },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(120.dp),
                maxLines = 5
            )
            
            // Save Button
            Button(
                onClick = {
                    // TODO: Save mood
                    navController.popBackStack()
                },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(56.dp),
                enabled = selectedMood > 0,
                colors = ButtonDefaults.buttonColors(
                    containerColor = PurplePrimary,
                    contentColor = White
                ),
                shape = RoundedCornerShape(16.dp)
            ) {
                Text("Save Mood", fontWeight = FontWeight.SemiBold)
            }
        }
    }
}

@Composable
fun MoodButton(level: Int, isSelected: Boolean, onClick: () -> Unit) {
    val emoji = when (level) {
        1 -> "😢"
        2 -> "😣"
        3 -> "😥"
        4 -> "😕"
        5 -> "😐"
        6 -> "🙂"
        7 -> "😎"
        8 -> "🤭"
        9 -> "☺️"
        10 -> "😄"
        else -> "😐"
    }

    Surface(
        onClick = onClick,
        modifier = Modifier.size(64.dp),
        shape = RoundedCornerShape(16.dp),
        color = if (isSelected) PurplePrimary else MaterialTheme.colorScheme.surface,
        border = if (!isSelected) {
            androidx.compose.foundation.BorderStroke(1.dp, MaterialTheme.colorScheme.outline)
        } else null
    ) {
        Box(
            modifier = Modifier.fillMaxSize(),
            contentAlignment = Alignment.Center
        ) {
            Text(emoji, style = MaterialTheme.typography.headlineMedium)
        }
    }
}

