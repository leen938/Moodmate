package com.moodmate.navigation

import androidx.compose.runtime.Composable
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import com.moodmate.ui.screens.*

sealed class Screen(val route: String) {
    object Login : Screen("login")
    object Home : Screen("home")
    object Moods : Screen("moods")
    object AddMood : Screen("add_mood")
    object Tasks : Screen("tasks")
    object AddTask : Screen("add_task")
    object Hacks : Screen("hacks")
    object Profile : Screen("profile")
}

@Composable
fun NavGraph(navController: NavHostController) {
    NavHost(
        navController = navController,
        startDestination = Screen.Login.route
    ) {
        composable(Screen.Login.route) {
            LoginScreen(navController = navController)
        }
        composable(Screen.Home.route) {
            HomeScreen(navController = navController)
        }
        composable(Screen.Moods.route) {
            MoodsScreen(navController = navController)
        }
        composable(Screen.AddMood.route) {
            AddMoodScreen(navController = navController)
        }
        composable(Screen.Tasks.route) {
            TasksScreen(navController = navController)
        }
        composable(Screen.AddTask.route) {
            AddTaskScreen(navController = navController)
        }
        composable(Screen.Hacks.route) {
            HacksScreen(navController = navController)
        }
        composable(Screen.Profile.route) {
            ProfileScreen(navController = navController)
        }
    }
}

