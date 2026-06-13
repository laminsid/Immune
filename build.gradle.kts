# Runtime hardening v1.10.1
# Keep JSON-reflected model names stable for report export.
-keep class com.immunesignal.app.** { *; }
-dontwarn org.json.**
