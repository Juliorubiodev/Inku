package com.juliorubio.inku.ui.screens.tabs

import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.*
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.juliorubio.inku.ui.components.Pill
import com.juliorubio.inku.ui.components.PrimaryButton

@OptIn(ExperimentalLayoutApi::class)
@Composable
fun UploadTab(modifier: Modifier = Modifier) {
    var title by remember { mutableStateOf("") }
    var desc by remember { mutableStateOf("") }
    val tags = listOf("Action", "Romance", "Fantasy", "Horror", "Sci-Fi", "Comedy")
    var selected by remember { mutableStateOf(setOf<String>()) }

    Column(
        modifier = modifier
            .fillMaxSize()
            .padding(horizontal = 16.dp)
            .statusBarsPadding(),
    ) {
        Text("Upload Manga", style = MaterialTheme.typography.headlineMedium)
        Spacer(Modifier.height(16.dp))

        Text("Title"); Spacer(Modifier.height(4.dp))
        OutlinedTextField(title, { title = it }, modifier = Modifier.fillMaxWidth(), singleLine = true)
        Spacer(Modifier.height(12.dp))
        Text("Description"); Spacer(Modifier.height(4.dp))
        OutlinedTextField(desc, { desc = it }, modifier = Modifier.fillMaxWidth(), minLines = 3)

        Spacer(Modifier.height(12.dp))
        Text("Genre"); Spacer(Modifier.height(8.dp))
        FlowRow(horizontalArrangement = Arrangement.spacedBy(8.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
            tags.forEach { t ->
                Pill(text = t, selected = t in selected, onClick = {
                    selected = if (t in selected) selected - t else selected + t
                })
            }
        }

        Spacer(Modifier.height(16.dp))
        PrimaryButton(
            text = "Select PDF & Upload",
            onClick = { /* TODO: picker */ }
        )

    }
}
