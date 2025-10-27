package com.juliorubio.inku.ui.screens.tabs

import androidx.compose.foundation.layout.*
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

@Composable
fun ProfileTab(modifier: Modifier = Modifier) {
    Column(
        modifier = modifier
            .fillMaxSize()
            .padding(horizontal = 16.dp)
            .statusBarsPadding()
    ) {
        Text("Profile", style = MaterialTheme.typography.headlineMedium)
        Spacer(Modifier.height(16.dp))

        Surface(tonalElevation = 2.dp, modifier = Modifier.fillMaxWidth(), shape = MaterialTheme.shapes.large) {
            Column(Modifier.padding(16.dp)) {
                Text("Your Name", style = MaterialTheme.typography.titleLarge)
                Text("@yourname", color = MaterialTheme.colorScheme.onSurface)
                Spacer(Modifier.height(12.dp))
                // Works/Favorites tabs mock
                Text("Works", style = MaterialTheme.typography.titleLarge)
            }
        }

        Spacer(Modifier.height(16.dp))
        Surface(tonalElevation = 1.dp, shape = MaterialTheme.shapes.large, modifier = Modifier.fillMaxWidth()) {
            Column(Modifier.padding(16.dp)) {
                Text("Create new work")
            }
        }
    }
}
