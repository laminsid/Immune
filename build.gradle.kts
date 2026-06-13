// Root plugin-version anchor for the multi-project build.
//
// Keep plugin versions here only. Subprojects must apply plugins without versions.
// This prevents the Kotlin Gradle plugin from being loaded independently in
// :app and :claimguard-core, and keeps Android/JVM modules on one toolchain.
plugins {
    id("com.android.application") version "8.8.2" apply false
    id("org.jetbrains.kotlin.android") version "1.9.24" apply false
    id("org.jetbrains.kotlin.jvm") version "1.9.24" apply false
    id("io.gitlab.arturbosch.detekt") version "1.23.7" apply false
}
