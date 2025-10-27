package com.juliorubio.inku.nav

sealed class Route(val path: String) {
    data object Login : Route("login")
    data object Register : Route("register")
    data object HomeShell : Route("home_shell")        // Contiene bottom bar
    // Tabs
    data object Home : Route("home")
    data object Explore : Route("explore")
    data object Upload : Route("upload")
    data object Profile : Route("profile")
    data object Settings : Route("settings")
}
