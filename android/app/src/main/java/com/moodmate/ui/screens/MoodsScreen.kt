package com.moodmate.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Favorite
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import com.moodmate.navigation.Screen
import com.moodmate.ui.components.BottomNavBar
import com.moodmate.ui.components.CustomTopAppBar
import com.moodmate.ui.theme.PurplePrimary
import com.moodmate.ui.theme.White

@Composable
fun MoodsScreen(navController: NavController) {
    Column(modifier = Modifier.fillMaxSize()) {
        CustomTopAppBar(title = "My Moods")
        
        Scaffold(
            bottomBar = { BottomNavBar(navController) },
            floatingActionButton = {
                FloatingActionButton(
                    onClick = { navController.navigate(Screen.AddMood.route) },
                    containerColor = PurplePrimary,
                    contentColor = White
                ) {
                    Icon(Icons.Default.Add, contentDescription = "Add Mood")
                }
            }
        ) { padding ->
            LazyColumn(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(padding)
                    .padding(16.dp),
                verticalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                item {
                    Text(
                        "Your mood history",
                        style = MaterialTheme.typography.titleMedium,
                        modifier = Modifier.padding(bottom = 8.dp)
                    )
                }
                
                // Placeholder for mood entries
                items(5) { index ->
                    MoodCard(
                        date = "2024-01-${15 + index}",
                        moodLevel = (1..5).random(),
                        notes = "Had a good day"
                    )
                }
            }
        }
    }
}

@Composable
fun MoodCard(date: String, moodLevel: Int, notes: String?) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(16.dp),
        colors = CardDefaults.cardColors(
            containerColor = White
        ),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            horizontalArrangement = Arrangement.spacedBy(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            // Mood Icon
            Icon(
                Icons.Default.Favorite,
                contentDescription = null,
                tint = when (moodLevel) {
                    5 -> MaterialTheme.colorScheme.primary
                    4 -> MaterialTheme.colorScheme.secondary
                    3 -> MaterialTheme.colorScheme.tertiary
                    else -> MaterialTheme.colorScheme.error
                },
                modifier = Modifier.size(48.dp)
            )
            
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    date,
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.SemiBold
                )
                Text(
                    "Mood: $moodLevel/5",
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.7f)
                )
                notes?.let {
                    Text(
                        it,
                        style = MaterialTheme.typography.bodySmall,
                        modifier = Modifier.padding(top = 4.dp)
                    )
                }
            }
        }
    }
}

