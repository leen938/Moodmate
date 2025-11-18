package com.moodmate.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Lightbulb
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
fun HacksScreen(navController: NavController) {
    Column(modifier = Modifier.fillMaxSize()) {
        CustomTopAppBar(title = "Tips & Hacks")
        
        Scaffold(
            bottomBar = { BottomNavBar(navController) }
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
                        "Wellness tips and tricks",
                        style = MaterialTheme.typography.titleMedium,
                        modifier = Modifier.padding(bottom = 8.dp)
                    )
                }
                
                // Placeholder hacks
                items(5) { index ->
                    HackCard(
                        title = "Tip ${index + 1}",
                        content = "This is a helpful tip for improving your mood and wellbeing.",
                        category = "Wellness"
                    )
                }
            }
        }
    }
}

@Composable
fun HackCard(title: String, content: String, category: String?) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(16.dp),
        colors = CardDefaults.cardColors(
            containerColor = White
        ),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    title,
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.SemiBold
                )
                Icon(
                    Icons.Default.Lightbulb,
                    contentDescription = null,
                    tint = PurplePrimary,
                    modifier = Modifier.size(24.dp)
                )
            }
            
            Text(
                content,
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.7f)
            )
            
            category?.let {
                Text(
                    it,
                    style = MaterialTheme.typography.labelSmall,
                    color = PurplePrimary,
                    modifier = Modifier.padding(top = 4.dp)
                )
            }
        }
    }
}

