
package com.obsidian.clipper.ui

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.obsidian.clipper.ui.screens.library.LibraryScreen
import com.obsidian.clipper.ui.screens.settings.SettingsScreen
import com.obsidian.clipper.ui.screens.templates.TemplatesScreen
import com.obsidian.clipper.ui.theme.ObsidianClipperTheme
import dagger.hilt.android.AndroidEntryPoint

@AndroidEntryPoint
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()

        setContent {
            ObsidianClipperTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    ClipperApp()
                }
            }
        }
    }
}

@Composable
fun ClipperApp() {
    val navController = rememberNavController()

    NavHost(
        navController = navController,
        startDestination = "library"
    ) {
        composable("library") {
            LibraryScreen(
                onNavigateToSettings = { navController.navigate("settings") },
                onNavigateToTemplates = { navController.navigate("templates") }
            )
        }
        composable("settings") {
            SettingsScreen(
                onNavigateBack = { navController.popBackStack() }
            )
        }
        composable("templates") {
            TemplatesScreen(
                onNavigateBack = { navController.popBackStack() }
            )
        }
    }
}
