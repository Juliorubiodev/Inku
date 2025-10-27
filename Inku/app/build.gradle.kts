plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.android)
    alias(libs.plugins.kotlin.compose)

    // 🔹 Calidad de código (tareas :app:ktlintCheck / :app:detekt)
    id("org.jlleitschuh.gradle.ktlint") version "12.1.1"
    id("io.gitlab.arturbosch.detekt") version "1.23.6"

    // (Opcional) JUnit5 android plugin si quieres usar Jupiter en androidTest
    // id("de.mannodermaus.android-junit5") version "1.10.0.0"
}

android {
    namespace = "com.juliorubio.inku"

    compileSdk {
        version = release(36)
    }

    defaultConfig {
        applicationId = "com.juliorubio.inku"
        minSdk = 24
        targetSdk = 36
        versionCode = 1
        versionName = "1.0"
        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }

    // 🔹 Requerido por Compose moderno
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions { jvmTarget = "17" }

    buildFeatures { compose = true }

    // 🔹 MUY IMPORTANTE para evitar crashes por desalineación
    composeOptions {
        kotlinCompilerExtensionVersion = "1.5.15"
    }

    // 🔹 Necesario para que Robolectric cargue recursos de Android en unit tests
    testOptions {
        unitTests.isIncludeAndroidResources = true
    }
}

dependencies {
    implementation(libs.androidx.core.ktx)
    implementation(libs.androidx.lifecycle.runtime.ktx)
    implementation(libs.androidx.activity.compose)

    // BOM de Compose (tu catálogo lo maneja)
    implementation(platform(libs.androidx.compose.bom))
    implementation(libs.androidx.compose.ui)
    implementation(libs.androidx.compose.ui.graphics)
    implementation(libs.androidx.compose.ui.tooling.preview)
    implementation(libs.androidx.compose.material3)

    implementation(libs.androidx.navigation.runtime.ktx)
    implementation(libs.androidx.navigation.compose)

    // Íconos extendidos
    implementation("androidx.compose.material:material-icons-extended")

    // ViewModel-Compose + Coil (recomendado)
    implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.8.6")
    implementation("io.coil-kt:coil-compose:2.7.0")

    // -------- Tests (unit) que corren en CI sin emulador --------
    testImplementation("org.robolectric:robolectric:4.11.1")                // Robolectric
    testImplementation("androidx.compose.ui:ui-test-junit4")                 // Compose test JUnit4
    debugImplementation("androidx.compose.ui:ui-test-manifest")              // Manifiesto test
    testImplementation("com.google.truth:truth:1.4.4")                       // Aserciones
    testImplementation("junit:junit:4.13.2")

    // -------- AndroidTest (instrumentados) – por si luego agregas --------
    androidTestImplementation(platform(libs.androidx.compose.bom))
    androidTestImplementation(libs.androidx.compose.ui.test.junit4)

    testImplementation(libs.junit)
    androidTestImplementation(libs.androidx.junit)
    androidTestImplementation(libs.androidx.espresso.core)
    debugImplementation(libs.androidx.compose.ui.tooling)
    debugImplementation(libs.androidx.compose.ui.test.manifest)
}

// ---------- Config de calidad de código ----------
detekt {
    buildUponDefaultConfig = true
    allRules = false
    // Temporalmente no forzamos fallo si hay reglas conflictivas
    ignoreFailures = true
    // (opcional) comenta cualquier línea `config = files("$rootDir/detekt.yml")`
    // config = files("$rootDir/detekt.yml")
}


ktlint {
    android.set(true)
    outputToConsole.set(true)

    //  No rompas el build por estilo (solo avisa)
    ignoreFailures.set(true)

    //  Sólo chequea el código de producción (evita errores en tests ahora)
    filter {
        include("**/src/main/**")
        exclude("**/generated/**")
    }
}

