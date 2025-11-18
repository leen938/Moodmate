package com.moodmate.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import com.moodmate.ui.components.CustomTopAppBar
import com.moodmate.ui.theme.PurplePrimary
import com.moodmate.ui.theme.White

@Composable
fun AddTaskScreen(navController: NavController) {
    var title by remember { mutableStateOf("") }
    var description by remember { mutableStateOf("") }
    var selectedPriority by remember { mutableStateOf("MEDIUM") }
    
    val priorities = listOf("LOW", "MEDIUM", "HIGH", "URGENT")
    
    Column(modifier = Modifier.fillMaxSize()) {
        CustomTopAppBar(
            title = "Add Task",
            onBackClick = { navController.popBackStack() }
        )
        
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(24.dp),
            verticalArrangement = Arrangement.spacedBy(20.dp)
        ) {
            OutlinedTextField(
                value = title,
                onValueChange = { title = it },
                label = { Text("Task Title") },
                modifier = Modifier.fillMaxWidth(),
                singleLine = true
            )
            
            OutlinedTextField(
                value = description,
                onValueChange = { description = it },
                label = { Text("Description (optional)") },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(120.dp),
                maxLines = 5
            )
            
            Text(
                "Priority",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.SemiBold
            )
            
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                priorities.forEach { priority ->
                    val isSelected = selectedPriority == priority
                    Button(
                        onClick = { selectedPriority = priority },
                        modifier = Modifier.weight(1f),
                        colors = ButtonDefaults.buttonColors(
                            containerColor = if (isSelected) PurplePrimary else MaterialTheme.colorScheme.surface,
                            contentColor = if (isSelected) White else MaterialTheme.colorScheme.onSurface
                        ),
                        shape = RoundedCornerShape(12.dp)
                    ) {
                        Text(
                            priority,
                            style = MaterialTheme.typography.labelMedium
                        )
                    }
                }
            }
            
            Spacer(modifier = Modifier.weight(1f))
            
            Button(
                onClick = {
                    // TODO: Save task
                    navController.popBackStack()
                },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(56.dp),
                enabled = title.isNotBlank(),
                colors = ButtonDefaults.buttonColors(
                    containerColor = PurplePrimary,
                    contentColor = White
                ),
                shape = RoundedCornerShape(16.dp)
            ) {
                Text("Save Task", fontWeight = FontWeight.SemiBold)
            }
        }
    }
}

