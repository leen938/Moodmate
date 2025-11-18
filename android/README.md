# MoodMate Android App

Minimal Android app to test the MoodMate FastAPI backend.

## Setup Instructions

### 1. Open in Android Studio

1. Open Android Studio
2. Click "Open" and select the `android` folder
3. Wait for Gradle sync to complete

### 2. Configure Backend URL

The app is configured to connect to `http://10.0.2.2:8000` by default (Android Emulator).

**For Android Emulator:**
- No changes needed - `10.0.2.2` is the special IP that maps to `localhost` on your computer

**For Physical Device:**
- Find your computer's IP address (e.g., `192.168.1.100`)
- Update `RetrofitClient.kt`:
  ```kotlin
  private const val BASE_URL = "http://192.168.1.100:8000/"
  ```

### 3. Start Your Backend

Make sure your FastAPI backend is running:
```bash
cd ..
uvicorn app.main:app --reload
```

### 4. Run the App

1. Create an Android Virtual Device (AVD) or connect a physical device
2. Click the "Run" button in Android Studio
3. The app will install and launch

### 5. Test Login

1. Enter any username and password
2. Click "Login / Sign Up"
3. If the user doesn't exist, it will be created
4. If the user exists, it will log in
5. The token will be saved locally

## Project Structure

```
android/
├── app/
│   └── src/main/java/com/moodmate/
│       ├── MainActivity.kt          # Main login screen
│       ├── LoginViewModel.kt        # Login logic
│       ├── data/
│       │   ├── api/                 # Retrofit API client
│       │   ├── model/                # Data models
│       │   └── local/                # Token storage
│       └── ui/theme/                 # Material Design 3 theme
```

## Features

- ✅ Minimal login/signup screen
- ✅ Retrofit API client
- ✅ Token storage with DataStore
- ✅ Material Design 3 UI
- ✅ Error handling

## Next Steps

Once you confirm this works, you can add:
- Mood tracking screen
- Task management screen
- Profile settings
- Navigation between screens

## Troubleshooting

**Connection Error:**
- Make sure backend is running
- Check the BASE_URL in `RetrofitClient.kt`
- For emulator, use `10.0.2.2:8000`
- For physical device, use your computer's IP

**Build Errors:**
- Make sure you're using Android Studio Hedgehog or later
- Sync Gradle: File → Sync Project with Gradle Files
- Invalidate caches: File → Invalidate Caches → Invalidate and Restart

