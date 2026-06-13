package io.claimguard.core

import org.json.JSONObject

/**
 * Injectable engine identity, replacing the hard dependency on the Android app's
 * ResearchEngineV3ReleaseIdentity.
 *
 * Why this matters: the receipt deliberately separates the *app* runtime proof
 * (an Android build has no Docker digest) from the *CLI/CI* runtime proof
 * (container digest + pinned R/survival/package locks). Mixing them makes the
 * receipt dishonest. The library never hardcodes one host; the caller supplies it.
 */
data class EngineIdentity(
    val engineVersion: String = "claimguard-core-0.1.0",
    val schemaVersion: String = "claimguard-core-0.1.0",
    val versionCode: Int = 1,
    /** "android-app" | "cli" | "ci" | host of your choosing. */
    val host: RuntimeHost = RuntimeHost.UNSPECIFIED,
) {
    fun runtimeEnvironmentJson(): JSONObject = when (host) {
        RuntimeHost.ANDROID_APP -> JSONObject()
            .put("app_receipt", JSONObject()
                .put("engine_version", engineVersion)
                .put("schema_version", schemaVersion)
                .put("version_code", versionCode)
                .put("kotlin_android_runtime", "ANDROID_APP_RUNTIME_NO_DOCKER_DIGEST"))
        RuntimeHost.CLI, RuntimeHost.CI -> JSONObject()
            .put("cli_github_receipt", JSONObject()
                .put("engine_version", engineVersion)
                .put("schema_version", schemaVersion)
                .put("container_digest", "REQUIRED_FOR_CLI_TIER1_TIER2_REPLAY")
                .put("analysis_runtime_version", "REQUIRED_FOR_CLI_MODEL_REPLAY")
                .put("package_lock", "REQUIRED_FOR_CLI_REPRODUCIBILITY"))
        RuntimeHost.UNSPECIFIED -> JSONObject()
            .put("engine_version", engineVersion)
            .put("schema_version", schemaVersion)
            .put("version_code", versionCode)
            .put("note", "Runtime host unspecified; supply ANDROID_APP, CLI, or CI for an honest environment proof.")
    }

    companion object {
        val DEFAULT = EngineIdentity()
    }
}

enum class RuntimeHost { ANDROID_APP, CLI, CI, UNSPECIFIED }
