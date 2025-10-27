package com.juliorubio.inku

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.core.view.WindowCompat
import androidx.compose.material3.Surface
import androidx.compose.runtime.Composable
import androidx.navigation.compose.rememberNavController
import com.juliorubio.inku.nav.InkuNavGraph
import com.juliorubio.inku.ui.theme.InkuTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // Pantalla edge-to-edge (opcional)
        WindowCompat.setDecorFitsSystemWindows(window, false)

        setContent {
            InkuTheme(darkTheme = true) {
                Surface {
                    App()
                }
            }
        }
    }
}

@Composable
private fun App() {
    // Usa el rememberNavController de Navigation-Compose (NO definas uno propio)
    val nav = rememberNavController()
    InkuNavGraph(navController = nav)
}

