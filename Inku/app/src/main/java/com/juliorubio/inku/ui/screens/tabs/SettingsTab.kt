package com.juliorubio.inku.ui.screens.tabs

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

@Composable
fun SettingsTab(modifier: Modifier = Modifier) {
    var push by remember { mutableStateOf(true) }
    var chapters by remember { mutableStateOf(true) }
    var creator by remember { mutableStateOf(false) }

    Column(
        modifier = modifier
            .fillMaxSize()
            .padding(horizontal = 16.dp)
            .statusBarsPadding()
    ) {
        Text("Settings", style = MaterialTheme.typography.headlineMedium)
        Spacer(Modifier.height(16.dp))

        Card(Modifier.fillMaxWidth(), colors = CardDefaults.cardColors()) {
            ListItem(
                headlineContent = { Text("Dark Mode") },
                supportingContent = { Text("Always enabled") },
                trailingContent = { Switch(checked = true, onCheckedChange = {}) }
            )
        }

        Spacer(Modifier.height(12.dp))
        Text("Notifications", style = MaterialTheme.typography.titleLarge)
        Spacer(Modifier.height(8.dp))
        Card(Modifier.fillMaxWidth()) {
            Column {
                ListItem(headlineContent = { Text("Push Notifications") }, trailingContent = {
                    Switch(checked = push, onCheckedChange = { push = it })
                })
                Divider()
                ListItem(headlineContent = { Text("New Chapter Alerts") }, trailingContent = {
                    Switch(checked = chapters, onCheckedChange = { chapters = it })
                })
                Divider()
                ListItem(headlineContent = { Text("Creator Updates") }, trailingContent = {
                    Switch(checked = creator, onCheckedChange = { creator = it })
                })
            }
        }
    }
}

