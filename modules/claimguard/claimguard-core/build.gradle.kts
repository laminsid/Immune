plugins {
    kotlin("jvm")
    `java-library`
}

dependencies {
    compileOnly("org.json:json:20231013")
    testImplementation("junit:junit:4.13.2")
    testImplementation("org.json:json:20231013")
}

java {
    toolchain {
        languageVersion.set(JavaLanguageVersion.of(11))
    }
    sourceCompatibility = JavaVersion.VERSION_11
    targetCompatibility = JavaVersion.VERSION_11
}

kotlin {
    jvmToolchain(11)
}

tasks.withType<org.jetbrains.kotlin.gradle.tasks.KotlinCompile>().configureEach {
    kotlinOptions.jvmTarget = "11"
}
