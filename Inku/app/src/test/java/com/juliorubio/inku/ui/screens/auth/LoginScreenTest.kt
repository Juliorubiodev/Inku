package com.juliorubio.inku.ui.screens.auth

import androidx.compose.ui.test.assertIsDisplayed
import androidx.compose.ui.test.junit4.createComposeRule
import androidx.compose.ui.test.onNodeWithText
import androidx.compose.ui.test.performClick
import com.google.common.truth.Truth
import com.juliorubio.inku.ui.theme.InkuTheme
import org.junit.Rule
import org.junit.Test
import java.util.concurrent.atomic.AtomicBoolean

class LoginScreenTest {

    @get:Rule
    val compose = createComposeRule()

    @Test
    fun loginScreen_showsBasicElements_andButtonsWork() {
        val signInClicked = AtomicBoolean(false)
        val signUpClicked = AtomicBoolean(false)
        val forgotClicked = AtomicBoolean(false)
        val googleClicked = AtomicBoolean(false)
        val githubClicked = AtomicBoolean(false)

        compose.setContent {
            InkuTheme(darkTheme = true) {
                LoginScreen(
                    onSignIn = { signInClicked.set(true) },
                    onGotoRegister = { signUpClicked.set(true) },
                    onForgot = { forgotClicked.set(true) },
                    onGoogle = { googleClicked.set(true) },
                    onGithub = { githubClicked.set(true) }
                )
            }
        }

        // Verifica título y campos visibles
        compose.onNodeWithText("Inku").assertIsDisplayed()
        compose.onNodeWithText("Email").assertExists()
        compose.onNodeWithText("Password").assertExists()
        compose.onNodeWithText("Sign In").assertIsDisplayed()

        // Click en "Sign In"
        compose.onNodeWithText("Sign In").performClick()
        Truth.assertThat(signInClicked.get()).isTrue()

        // Click en "Forgot password?"
        compose.onNodeWithText("Forgot password?").performClick()
        Truth.assertThat(forgotClicked.get()).isTrue()

        // Botones sociales
        compose.onNodeWithText("Google").performClick()
        compose.onNodeWithText("GitHub").performClick()
        Truth.assertThat(googleClicked.get()).isTrue()
        Truth.assertThat(githubClicked.get()).isTrue()

        // Enlace "Sign up"
        compose.onNodeWithText("Sign up").performClick()
        Truth.assertThat(signUpClicked.get()).isTrue()
    }
}