package com.juliorubio.inku.ui.screens.auth

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.AlternateEmail
import androidx.compose.material.icons.filled.Lock
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.juliorubio.inku.ui.components.LabeledInput
import com.juliorubio.inku.ui.components.OutlineIconButton
import com.juliorubio.inku.ui.components.PrimaryButton

@Composable
fun LoginScreen(
    onSignIn: () -> Unit,
    onGotoRegister: () -> Unit,
    onForgot: () -> Unit,
    onGoogle: () -> Unit,
    onGithub: () -> Unit
) {
    var email by remember { mutableStateOf("") }
    var pass by remember { mutableStateOf("") }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .systemBarsPadding()
            .padding(horizontal = 24.dp)
            .verticalScroll(rememberScrollState()),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Spacer(modifier = Modifier.height(48.dp))

        // Logo placeholder (pon tu Image si tienes asset)
        Box(modifier = Modifier.size(72.dp))

        Spacer(modifier = Modifier.height(12.dp))
        Text("Inku", style = MaterialTheme.typography.headlineLarge)
        Text("読む、創る、共有する", style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurface)

        Spacer(modifier = Modifier.height(24.dp))
        LabeledInput(email, onValueChange = { email = it }, placeholder = "Email", leading = Icons.Filled.AlternateEmail)
        Spacer(modifier = Modifier.height(12.dp))
        LabeledInput(pass, onValueChange = { pass = it }, placeholder = "Password", leading = Icons.Filled.Lock, password = true)

        Spacer(modifier = Modifier.height(8.dp))
        Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.End) {
            Text(
                "Forgot password?",
                color = MaterialTheme.colorScheme.primary,
                modifier = Modifier.clickable { onForgot() }
            )
        }

        Spacer(modifier = Modifier.height(16.dp))
        PrimaryButton(text = "Sign In", onClick = onSignIn)

        Spacer(modifier = Modifier.height(24.dp))
        Row(Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
            Box(
                modifier = Modifier
                    .weight(1f)
                    .height(1.dp)
                    .background(MaterialTheme.colorScheme.outline)
            )
            Text("  or continue with  ", color = MaterialTheme.colorScheme.onSurface)
            Box(
                modifier = Modifier
                    .weight(1f)
                    .height(1.dp)
                    .background(MaterialTheme.colorScheme.outline)
            )
        }

        Spacer(modifier = Modifier.height(16.dp))
        Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            OutlineIconButton(text = "Google", onClick = onGoogle) {
                Box(Modifier.size(18.dp)) // reemplaza por tu icono
            }
            OutlineIconButton(text = "GitHub", onClick = onGithub) {
                Box(Modifier.size(18.dp)) // reemplaza por tu icono
            }
        }

        Spacer(modifier = Modifier.height(24.dp))
        Row {
            Text("Don't have an account? ")
            Text(
                "Sign up",
                color = MaterialTheme.colorScheme.primary,
                modifier = Modifier
                    .padding(start = 4.dp)
                    .clickable { onGotoRegister() }
            )
        }

        Spacer(modifier = Modifier.height(24.dp))
    }
}
