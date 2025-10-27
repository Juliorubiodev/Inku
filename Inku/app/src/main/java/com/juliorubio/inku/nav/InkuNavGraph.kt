package com.juliorubio.inku.nav

import androidx.compose.runtime.Composable
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import com.juliorubio.inku.ui.screens.auth.LoginScreen
import com.juliorubio.inku.ui.screens.auth.RegisterScreen
import com.juliorubio.inku.ui.screens.shell.HomeShell


@Composable
fun InkuNavGraph(navController: NavHostController) {
    NavHost(navController, startDestination = Route.Login.path) {
        composable(Route.Login.path) {
            LoginScreen(
                onSignIn = { navController.navigate(Route.HomeShell.path) { popUpTo(Route.Login.path) { inclusive = true } } },
                onGotoRegister = { navController.navigate(Route.Register.path) },
                onForgot = { /* TODO */ },
                onGoogle = { /* TODO */ },
                onGithub = { /* TODO */ }
            )
        }
        composable(Route.Register.path) {
            RegisterScreen(
                onBackToLogin = { navController.popBackStack() },
                onRegistered = { navController.navigate(Route.HomeShell.path) { popUpTo(Route.Login.path) { inclusive = true } } }
            )
        }
        composable(Route.HomeShell.path) {
            HomeShell(
                onOpenSettings = { /* Navegar dentro del shell */ },
                navController = navController
            )
        }
    }
}
