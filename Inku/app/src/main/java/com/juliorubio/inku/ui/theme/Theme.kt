package com.juliorubio.inku.ui.theme

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.runtime.Composable

private val DarkScheme = darkColorScheme(
    primary = RedPrimary,
    onPrimary = OnPrimary,
    background = Bg,
    onBackground = OnBg,
    surface = SurfaceDark,
    onSurface = OnSurface,
    outline = OutlineDark,
    error = Error
)

@Composable
fun InkuTheme(
    darkTheme: Boolean = true,
    content: @Composable () -> Unit
) {
    MaterialTheme(
        colorScheme = DarkScheme,
        typography = InkuTypography,
        content = content
    )
}