# Fix SDK XML Version Error

The error "SDK XML versions up to 3 but an SDK XML file of version 4 was encountered" means your Android Studio and command-line tools are out of sync.

## Solution:

1. **Update SDK Command-Line Tools in Android Studio:**
   - Open Android Studio
   - Go to: **Tools → SDK Manager**
   - Click on the **SDK Tools** tab
   - Check **Android SDK Command-line Tools (latest)**
   - Click **Apply** and let it install

2. **Or update via terminal:**
   ```bash
   sdkmanager --update
   sdkmanager "cmdline-tools;latest"
   ```

3. **Sync the project again:**
   - File → Sync Project with Gradle Files

The Android Gradle Plugin has been updated to 8.3.0 which supports SDK XML v4.

