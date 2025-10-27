package com.juliorubio.inku.ui.screens.auth

import androidx.compose.ui.test.assertIsDisplayed
import androidx.compose.ui.test.junit4.createComposeRule
import androidx.compose.ui.test.onNodeWithText
import androidx.compose.ui.test.performClick
import com.juliorubio.inku.ui.theme.InkuTheme
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.annotation.Config
import org.robolectric.annotation.LooperMode
import java.util.concurrent.atomic.AtomicBoolean

@RunWith(RobolectricTestRunner::class)
@Config(sdk = [34])
@LooperMode(LooperMode.Mode.PAUSED)
class LoginScreenTest {

    @get:Rule
    val compose = createComposeRule()

    @Test
    fun loginScreen_showsBasicElements_andButtonsWork() {
        val signIn = AtomicBoolean(false)
        val signUp = AtomicBoolean(false)
        val forgot = AtomicBoolean(false)
        val google = AtomicBoolean(false)
        val github = AtomicBoolean(false)

        compose.setContent {
            InkuTheme(darkTheme = true) {
                LoginScreen(
                    onSignIn = { signIn.set(true) },
                    onGotoRegister = { signUp.set(true) },
                    onForgot = { forgot.set(true) },
                    onGoogle = { google.set(true) },
                    onGithub = { github.set(true) }
                )
            }
        }

        // Interacciones
        compose.onNodeWithText("Inku").assertIsDisplayed()
        compose.onNodeWithText("Email").assertIsDisplayed()
        compose.onNodeWithText("Password").assertIsDisplayed()
        compose.onNodeWithText("Sign In").performClick()
        compose.onNodeWithText("Forgot password?").performClick()
        compose.onNodeWithText("Google").performClick()
        compose.onNodeWithText("GitHub").performClick()
        compose.onNodeWithText("Sign up").performClick()

        assert(signIn.get())
        assert(forgot.get())
        assert(google.get())
        assert(github.get())
        assert(signUp.get())
    }
}
