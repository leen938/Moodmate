# Troubleshooting Guide

## SDK XML Version Error

If you're still seeing "SDK XML versions up to 3 but an SDK XML file of version 4 was encountered":

1. **Install Android SDK Command-line Tools:**
   - Tools → SDK Manager → SDK Tools tab
   - Check "Android SDK Command-line Tools (latest)"
   - Click Apply

2. **Sync Project:**
   - File → Sync Project with Gradle Files
   - Or click the "Sync Now" banner

3. **Invalidate Caches:**
   - File → Invalidate Caches → Invalidate and Restart

## App Not Opening on Emulator

If the app doesn't appear or crashes:

1. **Check Build Output:**
   - View → Tool Windows → Build
   - Look for errors in red

2. **Check Logcat:**
   - View → Tool Windows → Logcat
   - Filter by "MoodMate" or look for errors

3. **Rebuild:**
   - Build → Clean Project
   - Build → Rebuild Project

4. **Check Backend:**
   - Make sure FastAPI backend is running
   - For emulator: use `http://10.0.2.2:8000`
   - Check `RetrofitClient.kt` for correct URL

5. **Reinstall App:**
   - Right-click app in emulator → Uninstall
   - Run again from Android Studio

## Common Issues

- **"App keeps stopping":** Check Logcat for crash logs
- **"Network error":** Verify backend URL and that backend is running
- **"Build failed":** Check Build output for specific errors

