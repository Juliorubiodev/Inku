package com.juliorubio.inku.ui.screens.shell

import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.Add
import androidx.compose.material.icons.outlined.Home
import androidx.compose.material.icons.outlined.Person
import androidx.compose.material.icons.outlined.Search
import androidx.compose.material.icons.outlined.Settings
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.navigation.NavController
import com.juliorubio.inku.nav.Route
import com.juliorubio.inku.ui.screens.tabs.*

@Composable
fun HomeShell(onOpenSettings: () -> Unit, navController: NavController) {
    var selected by remember { mutableStateOf(Route.Home.path) }

    val items = listOf(
        Triple(Route.Home.path, "Home", Icons.Outlined.Home),
        Triple(Route.Explore.path, "Explore", Icons.Outlined.Search),
        Triple(Route.Upload.path, "Upload", Icons.Outlined.Add),
        Triple(Route.Profile.path, "Profile", Icons.Outlined.Person),
        Triple(Route.Settings.path, "Settings", Icons.Outlined.Settings)
    )

    Scaffold(
        bottomBar = {
            NavigationBar {
                items.forEach { (route, label, icon) ->
                    NavigationBarItem(
                        selected = selected == route,
                        onClick = { selected = route },
                        icon = { Icon(icon, contentDescription = label) },
                        label = { Text(label) }
                    )
                }
            }
        }
    ) { inner ->
        when (selected) {
            Route.Home.path -> HomeTab(Modifier.padding(inner))
            Route.Explore.path -> ExploreTab(Modifier.padding(inner))
            Route.Upload.path -> UploadTab(Modifier.padding(inner))
            Route.Profile.path -> ProfileTab(Modifier.padding(inner))
            Route.Settings.path -> SettingsTab(Modifier.padding(inner))
        }
    }
}
