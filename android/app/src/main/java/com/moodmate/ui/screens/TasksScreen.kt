package com.moodmate.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.CheckCircle
import androidx.compose.material.icons.filled.Circle
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import com.moodmate.navigation.Screen
import com.moodmate.ui.components.BottomNavBar
import com.moodmate.ui.components.CustomTopAppBar
import com.moodmate.ui.theme.PurplePrimary

@Composable
fun TasksScreen(navController: NavController) {
    Column(modifier = Modifier.fillMaxSize()) {
        CustomTopAppBar(title = "My Tasks")

        Scaffold(
            bottomBar = { BottomNavBar(navController) },
            floatingActionButton = {
                FloatingActionButton(
                    onClick = { navController.navigate(Screen.AddTask.route) },
                    containerColor = PurplePrimary,
                    contentColor = MaterialTheme.colorScheme.onPrimary
                ) {
                    Icon(Icons.Default.Add, contentDescription = "Add Task")
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
                        text = "Your tasks",
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.SemiBold,
                        color = MaterialTheme.colorScheme.onBackground,
                        modifier = Modifier.padding(bottom = 8.dp)
                    )
                }

                // Placeholder tasks
                items((0 until 5).toList()) { index ->
                    TaskCard(
                        title = "Task ${index + 1}",
                        description = "Task description",
                        isCompleted = index % 2 == 0,
                        priority = when (index % 4) {
                            0 -> "URGENT"
                            1 -> "HIGH"
                            2 -> "MEDIUM"
                            else -> "LOW"
                        }
                    )
                }
            }
        }
    }
}

@Composable
fun TaskCard(
    title: String,
    description: String?,
    isCompleted: Boolean,
    priority: String
) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(16.dp),
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.surface
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
            IconButton(onClick = { /* TODO: Toggle */ }) {
                Icon(
                    if (isCompleted) Icons.Default.CheckCircle else Icons.Default.Circle,
                    contentDescription = if (isCompleted) "Completed" else "Not completed",
                    tint = if (isCompleted)
                        PurplePrimary
                    else
                        MaterialTheme.colorScheme.onSurfaceVariant
                )
            }

            Column(modifier = Modifier.weight(1f)) {
                // Title
                Text(
                    text = title,
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.SemiBold,
                    color = if (isCompleted)
                        MaterialTheme.colorScheme.onSurface.copy(alpha = 0.6f)
                    else
                        MaterialTheme.colorScheme.onSurface
                )

                // Description
                description?.let {
                    Text(
                        text = it,
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        modifier = Modifier.padding(top = 4.dp)
                    )
                }

                // Priority label
                Text(
                    text = priority,
                    style = MaterialTheme.typography.labelSmall,
                    color = PurplePrimary,
                    modifier = Modifier.padding(top = 4.dp)
                )
            }
        }
    }
}
