package com.juliorubio.inku.ui.screens.auth

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.AlternateEmail
import androidx.compose.material.icons.filled.Lock
import androidx.compose.material.icons.filled.Person
import androidx.compose.material3.Checkbox
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.juliorubio.inku.ui.components.LabeledInput
import com.juliorubio.inku.ui.components.PrimaryButton

@Composable
fun RegisterScreen(
    onBackToLogin: () -> Unit,
    onRegistered: () -> Unit
) {
    var username by remember { mutableStateOf("") }
    var email by remember { mutableStateOf("") }
    var pass by remember { mutableStateOf("") }
    var pass2 by remember { mutableStateOf("") }
    var agree by remember { mutableStateOf(false) }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .systemBarsPadding()
            .padding(horizontal = 24.dp)
            .verticalScroll(rememberScrollState()),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Spacer(Modifier.height(48.dp))
        Text("Create Account", style = MaterialTheme.typography.headlineLarge)
        Text("Join the Inku community", color = MaterialTheme.colorScheme.onSurface)

        Spacer(Modifier.height(24.dp))
        LabeledInput(username, { username = it }, "Username", leading = Icons.Filled.Person)
        Spacer(Modifier.height(12.dp))
        LabeledInput(email, { email = it }, "Email", leading = Icons.Filled.AlternateEmail)
        Spacer(Modifier.height(12.dp))
        LabeledInput(pass, { pass = it }, "Password", leading = Icons.Filled.Lock, password = true)
        Spacer(Modifier.height(12.dp))
        LabeledInput(pass2, { pass2 = it }, "Confirm Password", leading = Icons.Filled.Lock, password = true)

        Spacer(Modifier.height(12.dp))
        Row(verticalAlignment = Alignment.CenterVertically) {
            Checkbox(checked = agree, onCheckedChange = { agree = it })
            Text("I agree to the Terms of Service and Privacy Policy")
        }

        Spacer(Modifier.height(12.dp))
        PrimaryButton(text = "Create Account", onClick = onRegistered, enabled = agree)

        Spacer(Modifier.height(16.dp))
        Row {
            Text("Already have an account? ")
            Text("Sign in", color = MaterialTheme.colorScheme.primary)
            // Añade clickable { onBackToLogin() } si quieres
        }
        Spacer(Modifier.height(24.dp))
    }
}


