package com.juliorubio.inku.ui.screens.tabs

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

@Composable
fun HomeTab(modifier: Modifier = Modifier) {
    LazyColumn(
        modifier = modifier
            .fillMaxSize()
            .padding(horizontal = 16.dp)
            .statusBarsPadding(),
        contentPadding = PaddingValues(bottom = 84.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        item {
            Text("Inku", style = MaterialTheme.typography.headlineMedium)
            Text("Welcome back", color = MaterialTheme.colorScheme.onSurface)
            Spacer(Modifier.height(8.dp))
        }

        // Continue Reading (mock)
        items(listOf("Crimson Chronicles" to 65, "Shadow Realm" to 40)) { (title, progress) ->
            Surface(shape = MaterialTheme.shapes.large, tonalElevation = 1.dp, modifier = Modifier.fillParentMaxWidth()) {
                Column(Modifier.padding(16.dp)) {
                    Text(title, style = MaterialTheme.typography.titleLarge)
                    Spacer(Modifier.height(8.dp))
                    androidx.compose.material3.LinearProgressIndicator(progress / 100f)
                    Spacer(Modifier.height(4.dp))
                    Text("${progress}%", color = MaterialTheme.colorScheme.onSurface)
                }
            }
        }

        // Trending Now header
        item { Text("Trending Now", style = MaterialTheme.typography.titleLarge) }
        // TODO: Grid de cards con Coil para portadas
    }
}

