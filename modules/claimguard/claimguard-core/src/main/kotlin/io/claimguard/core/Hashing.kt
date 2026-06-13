package io.claimguard.core

import org.json.JSONArray
import java.security.MessageDigest

/**
 * Shared, domain-free hashing utilities.
 *
 * Extracted from the original HypothesisProvenanceContractV30392 so that every
 * contract in the chain hashes identically. Pure JVM + org.json; no Android.
 */
object Hashing {

    /** Lowercase hex SHA-256 of the UTF-8 bytes of [text]. */
    fun sha256(text: String): String {
        val bytes = MessageDigest.getInstance("SHA-256").digest(text.toByteArray(Charsets.UTF_8))
        return bytes.joinToString("") { "%02x".format(it) }
    }

    /**
     * Order-independent canonical string for a set of tokens: trimmed, de-blanked,
     * sorted, pipe-joined. This is what makes the gene/covariate hash stable
     * regardless of declaration order but sensitive to membership changes.
     */
    fun canonicalArray(arr: JSONArray): String {
        val values = mutableListOf<String>()
        for (i in 0 until arr.length()) values += arr.optString(i).trim()
        return values.filter { it.isNotBlank() }.sorted().joinToString("|")
    }

    fun unique(arr: JSONArray): JSONArray {
        val seen = linkedSetOf<String>()
        for (i in 0 until arr.length()) {
            val v = arr.optString(i).trim()
            if (v.isNotBlank()) seen += v
        }
        return JSONArray(seen.toList())
    }
}
