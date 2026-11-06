from pathlib import Path

files = {}

files["settings.gradle"] = r'''pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}

dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}

rootProject.name = "HamseTool"
include(":app")
'''

files["build.gradle"] = r'''plugins {
    id 'com.android.application' version '8.1.1' apply false
}
'''

files["gradle.properties"] = r'''org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
android.useAndroidX=true
android.nonTransitiveRClass=true
'''

files["app/build.gradle"] = r'''plugins {
    id 'com.android.application'
}

android {
    namespace 'com.hamse.tool'
    compileSdk 34

    defaultConfig {
        applicationId 'com.hamse.tool'
        minSdk 23
        targetSdk 34
        versionCode 1
        versionName "1.0"
    }

    buildTypes {
        release {
            minifyEnabled false
            shrinkResources false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'),
                    'proguard-rules.pro'
        }
    }

    compileOptions {
        sourceCompatibility JavaVersion.VERSION_17
        targetCompatibility JavaVersion.VERSION_17
    }
}

dependencies {
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.11.0'
    implementation 'androidx.activity:activity:1.8.2'
}
'''

files["app/proguard-rules.pro"] = r'''# Hamse Tool
'''

files["app/src/main/AndroidManifest.xml"] = r'''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

    <uses-permission android:name="android.permission.INTERNET"/>

    <application
        android:allowBackup="true"
        android:label="Hamse Tool"
        android:theme="@style/Theme.HamseTool"
        android:resizeableActivity="true">

        <activity
            android:name=".MainActivity"
            android:exported="true">

            <intent-filter>
                <action android:name="android.intent.action.MAIN"/>
                <category android:name="android.intent.category.LAUNCHER"/>
            </intent-filter>

        </activity>
    </application>
</manifest>
'''

files["app/src/main/res/values/themes.xml"] = r'''<?xml version="1.0" encoding="utf-8"?>
<resources>

    <style name="Theme.HamseTool"
        parent="Theme.Material3.Dark.NoActionBar">

        <item name="android:fontFamily">sans</item>
        <item name="android:windowLightStatusBar">false</item>
        <item name="android:statusBarColor">#090B12</item>
        <item name="android:navigationBarColor">#090B12</item>
        <item name="android:windowActionModeOverlay">true</item>

        <item name="colorPrimary">#7C5CFF</item>
        <item name="colorSecondary">#00D4FF</item>

    </style>

</resources>
'''

files["app/src/main/res/values/colors.xml"] = r'''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="bg">#090B12</color>
    <color name="card">#151824</color>
    <color name="card2">#1B1F2D</color>
    <color name="white">#FFFFFF</color>
    <color name="muted">#9BA1B2</color>
    <color name="purple">#7C5CFF</color>
    <color name="cyan">#00D4FF</color>
    <color name="green">#35D07F</color>
    <color name="red">#FF5570</color>
</resources>
'''

files["app/src/main/res/drawable/bg.xml"] = r'''<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android">
    <solid android:color="#090B12"/>
</shape>
'''

files["app/src/main/res/drawable/card.xml"] = r'''<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android">
    <solid android:color="#151824"/>
    <corners android:radius="24dp"/>
    <padding
        android:left="18dp"
        android:top="18dp"
        android:right="18dp"
        android:bottom="18dp"/>
</shape>
'''

files["app/src/main/res/drawable/button.xml"] = r'''<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android">
    <solid android:color="#7C5CFF"/>
    <corners android:radius="18dp"/>
    <padding
        android:left="16dp"
        android:top="13dp"
        android:right="16dp"
        android:bottom="13dp"/>
</shape>
'''

files["app/src/main/res/drawable/button_dark.xml"] = r'''<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android">
    <solid android:color="#202432"/>
    <corners android:radius="18dp"/>
    <stroke
        android:width="1dp"
        android:color="#303548"/>
    <padding
        android:left="16dp"
        android:top="13dp"
        android:right="16dp"
        android:bottom="13dp"/>
</shape>
'''

files["app/src/main/res/layout/activity_main.xml"] = r'''<?xml version="1.0" encoding="utf-8"?>
<ScrollView xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="@drawable/bg"
    android:fillViewport="true">

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="vertical"
        android:padding="20dp">

        <TextView
            android:id="@+id/title"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="Hamse Tool"
            android:textColor="#FFFFFF"
            android:textSize="32sp"
            android:textStyle="bold"/>

        <TextView
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:layout_marginTop="5dp"
            android:text="Developer File Utility"
            android:textColor="#9BA1B2"
            android:textSize="15sp"/>

        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginTop="24dp"
            android:orientation="vertical"
            android:background="@drawable/card">

            <TextView
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:text="FILE TOOLS"
                android:textColor="#9BA1B2"
                android:textSize="12sp"
                android:textStyle="bold"/>

            <Button
                android:id="@+id/btnPick"
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:layout_marginTop="12dp"
                android:text="Select File"
                android:textColor="#FFFFFF"
                android:background="@drawable/button"/>

            <TextView
                android:id="@+id/fileName"
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:layout_marginTop="10dp"
                android:text="No file selected"
                android:textColor="#9BA1B2"
                android:textSize="13sp"/>

        </LinearLayout>

        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginTop="16dp"
            android:orientation="vertical"
            android:background="@drawable/card">

            <TextView
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:text="ARCHIVE TOOLS"
                android:textColor="#9BA1B2"
                android:textSize="12sp"
                android:textStyle="bold"/>

            <Button
                android:id="@+id/btnUnpack"
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:layout_marginTop="12dp"
                android:text="Unpack ZIP / PAK Archive"
                android:textColor="#FFFFFF"
                android:background="@drawable/button_dark"/>

            <Button
                android:id="@+id/btnRepack"
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:layout_marginTop="8dp"
                android:text="Repack Folder to ZIP"
                android:textColor="#FFFFFF"
                android:background="@drawable/button_dark"/>

        </LinearLayout>

        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginTop="16dp"
            android:orientation="vertical"
            android:background="@drawable/card">

            <TextView
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:text="PROCESSING"
                android:textColor="#9BA1B2"
                android:textSize="12sp"
                android:textStyle="bold"/>

            <Button
                android:id="@+id/btnXor"
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:layout_marginTop="12dp"
                android:text="XOR Process File"
                android:textColor="#FFFFFF"
                android:background="@drawable/button_dark"/>

            <Button
                android:id="@+id/btnUrl"
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:layout_marginTop="8dp"
                android:text="Scan URLs"
                android:textColor="#FFFFFF"
                android:background="@drawable/button_dark"/>

            <Button
                android:id="@+id/btnView"
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:layout_marginTop="8dp"
                android:text="View Text File"
                android:textColor="#FFFFFF"
                android:background="@drawable/button_dark"/>

        </LinearLayout>

        <TextView
            android:id="@+id/status"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginTop="18dp"
            android:padding="16dp"
            android:background="@drawable/card"
            android:text="Ready"
            android:textColor="#35D07F"
            android:textSize="14sp"/>

    </LinearLayout>
</ScrollView>
'''

files["app/src/main/java/com/hamse/tool/ToolManager.java"] = r'''package com.hamse.tool;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;
import java.util.zip.ZipOutputStream;

public final class ToolManager {

    private ToolManager() {}

    public static byte[] xor(byte[] data, String key) {
        if (data == null) {
            throw new IllegalArgumentException("Data is empty");
        }

        if (key == null || key.isEmpty()) {
            throw new IllegalArgumentException("XOR key is empty");
        }

        byte[] k = key.getBytes(StandardCharsets.UTF_8);
        byte[] out = new byte[data.length];

        for (int i = 0; i < data.length; i++) {
            out[i] = (byte) (data[i] ^ k[i % k.length]);
        }

        return out;
    }

    public static List<String> scanUrls(File file) throws IOException {
        byte[] bytes = Files.readAllBytes(file.toPath());

        String text = new String(bytes, StandardCharsets.UTF_8);

        Pattern p = Pattern.compile(
                "https?://[^\\s\"'<>]+",
                Pattern.CASE_INSENSITIVE
        );

        Matcher m = p.matcher(text);

        Set<String> unique = new HashSet<>();
        List<String> result = new ArrayList<>();

        while (m.find()) {
            String url = m.group();

            while (url.endsWith(".") ||
                    url.endsWith(",") ||
                    url.endsWith(")") ||
                    url.endsWith("]")) {
                url = url.substring(0, url.length() - 1);
            }

            if (unique.add(url)) {
                result.add(url);
            }
        }

        return result;
    }

    public static int unpackZip(File zip, File outputDir)
            throws IOException {

        if (!outputDir.exists() && !outputDir.mkdirs()) {
            throw new IOException("Cannot create output directory");
        }

        int count = 0;

        try (ZipInputStream zis =
                     new ZipInputStream(
                             new BufferedInputStream(
                                     new FileInputStream(zip)))) {

            ZipEntry entry;

            byte[] buffer = new byte[8192];

            while ((entry = zis.getNextEntry()) != null) {

                File target = new File(outputDir, entry.getName());

                String root = outputDir.getCanonicalPath();
                String targetPath = target.getCanonicalPath();

                if (!targetPath.startsWith(root + File.separator)) {
                    throw new IOException("Unsafe archive entry");
                }

                if (entry.isDirectory()) {
                    if (!target.exists()) {
                        target.mkdirs();
                    }
                    continue;
                }

                File parent = target.getParentFile();

                if (parent != null && !parent.exists()) {
                    parent.mkdirs();
                }

                try (BufferedOutputStream bos =
                             new BufferedOutputStream(
                                     new FileOutputStream(target))) {

                    int read;

                    while ((read = zis.read(buffer)) != -1) {
                        bos.write(buffer, 0, read);
                    }
                }

                count++;
            }
        }

        return count;
    }

    public static int zipFolder(File folder, File output)
            throws IOException {

        if (!folder.isDirectory()) {
            throw new IOException("Folder not found");
        }

        try (ZipOutputStream zos =
                     new ZipOutputStream(
                             new BufferedOutputStream(
                                     new FileOutputStream(output)))) {

            return addFolder(folder, folder, zos);
        }
    }

    private static int addFolder(
            File root,
            File current,
            ZipOutputStream zos) throws IOException {

        int count = 0;

        File[] children = current.listFiles();

        if (children == null) {
            return 0;
        }

        for (File child : children) {

            if (child.isDirectory()) {
                count += addFolder(root, child, zos);
                continue;
            }

            String relative =
                    root.toURI()
                            .relativize(child.toURI())
                            .getPath();

            ZipEntry entry = new ZipEntry(relative);
            zos.putNextEntry(entry);

            try (BufferedInputStream bis =
                         new BufferedInputStream(
                                 new FileInputStream(child))) {

                byte[] buffer = new byte[8192];

                int read;

                while ((read = bis.read(buffer)) != -1) {
                    zos.write(buffer, 0, read);
                }
            }

            zos.closeEntry();

            count++;
        }

        return count;
    }
}
'''

files["app/src/main/java/com/hamse/tool/MainActivity.java"] = r'''package com.hamse.tool;

import android.app.Activity;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.util.List;

public class MainActivity extends Activity {

    private static final int PICK_FILE = 100;
    private static final int PICK_FOLDER = 101;

    private TextView fileName;
    private TextView status;

    private Uri selectedUri;
    private String selectedName = "";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        fileName = findViewById(R.id.fileName);
        status = findViewById(R.id.status);

        findViewById(R.id.btnPick).setOnClickListener(v ->
                pickFile());

        findViewById(R.id.btnUnpack).setOnClickListener(v ->
                unpackSelected());

        findViewById(R.id.btnRepack).setOnClickListener(v ->
                pickFolder());

        findViewById(R.id.btnXor).setOnClickListener(v ->
                xorSelected());

        findViewById(R.id.btnUrl).setOnClickListener(v ->
                scanSelected());

        findViewById(R.id.btnView).setOnClickListener(v ->
                viewSelected());
    }

    private void pickFile() {
        Intent intent = new Intent(Intent.ACTION_OPEN_DOCUMENT);
        intent.setType("*/*");
        intent.addCategory(Intent.CATEGORY_OPENABLE);
        startActivityForResult(intent, PICK_FILE);
    }

    private void pickFolder() {
        Intent intent = new Intent(Intent.ACTION_OPEN_DOCUMENT_TREE);
        startActivityForResult(intent, PICK_FOLDER);
    }

    @Override
    protected void onActivityResult(
            int requestCode,
            int resultCode,
            Intent data) {

        super.onActivityResult(
                requestCode,
                resultCode,
                data);

        if (resultCode != RESULT_OK || data == null) {
            return;
        }

        Uri uri = data.getData();

        if (requestCode == PICK_FILE) {
            selectedUri = uri;
            selectedName = getFileName(uri);

            fileName.setText(
                    selectedName == null
                            ? "Selected file"
                            : selectedName);

            setStatus("File selected", false);
        }

        if (requestCode == PICK_FOLDER) {
            repackFolder(uri);
        }
    }

    private String getFileName(Uri uri) {
        String result = "Selected file";

        if (uri == null) {
            return result;
        }

        String path = uri.getPath();

        if (path != null) {
            int slash = path.lastIndexOf('/');

            if (slash >= 0 && slash + 1 < path.length()) {
                result = path.substring(slash + 1);
            }
        }

        return result;
    }

    private File copySelectedToCache() throws Exception {

        if (selectedUri == null) {
            throw new Exception("No file selected");
        }

        File input = new File(
                getCacheDir(),
                "input_" + System.currentTimeMillis());

        try (InputStream in =
                     getContentResolver()
                             .openInputStream(selectedUri);
             FileOutputStream out =
                     new FileOutputStream(input)) {

            if (in == null) {
                throw new Exception("Cannot open selected file");
            }

            byte[] buffer = new byte[8192];

            int read;

            while ((read = in.read(buffer)) != -1) {
                out.write(buffer, 0, read);
            }
        }

        return input;
    }

    private void unpackSelected() {
        new Thread(() -> {

            try {
                File input = copySelectedToCache();

                File output = new File(
                        getExternalFilesDir(null),
                        "HamseTool/Unpacked_" +
                                System.currentTimeMillis());

                int count =
                        ToolManager.unpackZip(input, output);

                runOnUiThread(() ->
                        setStatus(
                                "Unpacked " +
                                        count +
                                        " files to " +
                                        output.getAbsolutePath(),
                                false));

            } catch (Exception e) {
                runOnUiThread(() ->
                        showError(
                                "Unpack failed: " +
                                        safeMessage(e)));
            }

        }).start();
    }

    private void repackFolder(Uri folderUri) {

        new Thread(() -> {

            try {

                File source =
                        new File(
                                getCacheDir(),
                                "repack_" +
                                        System.currentTimeMillis());

                if (!source.mkdirs()) {
                    throw new Exception(
                            "Cannot create temporary folder");
                }

                copyTreeFromUri(folderUri, source);

                File output =
                        new File(
                                getExternalFilesDir(null),
                                "HamseTool/Repacked_" +
                                        System.currentTimeMillis() +
                                        ".zip");

                File parent = output.getParentFile();

                if (parent != null && !parent.exists()) {
                    parent.mkdirs();
                }

                int count =
                        ToolManager.zipFolder(
                                source,
                                output);

                runOnUiThread(() ->
                        setStatus(
                                "Repacked " +
                                        count +
                                        " files: " +
                                        output.getAbsolutePath(),
                                false));

            } catch (Exception e) {
                runOnUiThread(() ->
                        showError(
                                "Repack failed: " +
                                        safeMessage(e)));
            }

        }).start();
    }

    private void copyTreeFromUri(
            Uri tree,
            File destination) throws Exception {

        android.database.Cursor cursor =
                getContentResolver()
                        .query(
                                tree,
                                new String[]{
                                        android.provider.DocumentsContract.Document.COLUMN_DOCUMENT_ID
                                },
                                null,
                                null,
                                null);

        if (cursor == null) {
            throw new Exception("Cannot read folder");
        }

        cursor.close();

        copyDocumentTree(
                android.provider.DocumentsContract
                        .buildChildDocumentsUriUsingTree(
                                tree,
                                android.provider.DocumentsContract
                                        .getTreeDocumentId(tree)),
                destination);
    }

    private void copyDocumentTree(
            Uri childrenUri,
            File destination) throws Exception {

        android.database.Cursor cursor =
                getContentResolver()
                        .query(
                                childrenUri,
                                new String[]{
                                        android.provider.DocumentsContract.Document.COLUMN_DOCUMENT_ID,
                                        android.provider.DocumentsContract.Document.COLUMN_DISPLAY_NAME,
                                        android.provider.DocumentsContract.Document.COLUMN_MIME_TYPE
                                },
                                null,
                                null,
                                null);

        if (cursor == null) {
            throw new Exception("Cannot read folder contents");
        }

        while (cursor.moveToNext()) {

            String id = cursor.getString(0);
            String name = cursor.getString(1);
            String mime = cursor.getString(2);

            Uri documentUri =
                    android.provider.DocumentsContract
                            .buildDocumentUriUsingTree(
                                    childrenUri,
                                    id);

            File target = new File(destination, name);

            if ("vnd.android.document/directory".equals(mime)) {

                if (!target.exists()) {
                    target.mkdirs();
                }

                Uri childUri =
                        android.provider.DocumentsContract
                                .buildChildDocumentsUriUsingTree(
                                        childrenUri,
                                        id);

                copyDocumentTree(
                        childUri,
                        target);

            } else {

                try (InputStream in =
                             getContentResolver()
                                     .openInputStream(documentUri);
                     FileOutputStream out =
                             new FileOutputStream(target)) {

                    if (in == null) {
                        throw new Exception(
                                "Cannot read " + name);
                    }

                    byte[] buffer = new byte[8192];

                    int read;

                    while ((read =
                            in.read(buffer)) != -1) {

                        out.write(buffer, 0, read);
                    }
                }
            }
        }

        cursor.close();
    }

    private void xorSelected() {

        if (selectedUri == null) {
            showError("Select a file first");
            return;
        }

        EditText keyInput = new EditText(this);
        keyInput.setHint("XOR key");

        new androidx.appcompat.app.AlertDialog.Builder(this)
                .setTitle("XOR Processor")
                .setMessage(
                        "Enter the key used for processing.")
                .setView(keyInput)
                .setNegativeButton("Cancel", null)
                .setPositiveButton(
                        "Process",
                        (dialog, which) -> {

                            String key =
                                    keyInput.getText()
                                            .toString();

                            if (key.isEmpty()) {
                                showError(
                                        "XOR key cannot be empty");
                                return;
                            }

                            new Thread(() -> {

                                try {

                                    File input =
                                            copySelectedToCache();

                                    byte[] data =
                                            java.nio.file.Files
                                                    .readAllBytes(
                                                            input.toPath());

                                    byte[] outputData =
                                            ToolManager.xor(
                                                    data,
                                                    key);

                                    File output =
                                            new File(
                                                    getExternalFilesDir(null),
                                                    "HamseTool/XOR_" +
                                                            System.currentTimeMillis() +
                                                            ".bin");

                                    File parent =
                                            output.getParentFile();

                                    if (parent != null &&
                                            !parent.exists()) {
                                        parent.mkdirs();
                                    }

                                    java.nio.file.Files.write(
                                            output.toPath(),
                                            outputData);

                                    runOnUiThread(() ->
                                            setStatus(
                                                    "XOR output: " +
                                                            output.getAbsolutePath(),
                                                    false));

                                } catch (Exception e) {

                                    runOnUiThread(() ->
                                            showError(
                                                    "XOR failed: " +
                                                            safeMessage(e)));
                                }

                            }).start();
                        })
                .show();
    }

    private void scanSelected() {

        if (selectedUri == null) {
            showError("Select a file first");
            return;
        }

        new Thread(() -> {

            try {

                File input =
                        copySelectedToCache();

                List<String> urls =
                        ToolManager.scanUrls(input);

                StringBuilder result =
                        new StringBuilder();

                result.append("Found ")
                        .append(urls.size())
                        .append(" URL(s)\n\n");

                for (String url : urls) {
                    result.append(url)
                            .append("\n");
                }

                runOnUiThread(() ->
                        showResult(
                                "URL Scanner",
                                result.toString()));

            } catch (Exception e) {

                runOnUiThread(() ->
                        showError(
                                "URL scan failed: " +
                                        safeMessage(e)));
            }

        }).start();
    }

    private void viewSelected() {

        if (selectedUri == null) {
            showError("Select a file first");
            return;
        }

        new Thread(() -> {

            try {

                File input =
                        copySelectedToCache();

                long size =
                        input.length();

                if (size > 1024 * 1024) {
                    throw new Exception(
                            "File is larger than 1 MB");
                }

                String text =
                        new String(
                                java.nio.file.Files
                                        .readAllBytes(
                                                input.toPath()),
                                StandardCharsets.UTF_8);

                runOnUiThread(() ->
                        showResult(
                                selectedName,
                                text));

            } catch (Exception e) {

                runOnUiThread(() ->
                        showError(
                                "Cannot view file: " +
                                        safeMessage(e)));
            }

        }).start();
    }

    private void showResult(
            String title,
            String message) {

        new androidx.appcompat.app.AlertDialog.Builder(this)
                .setTitle(title)
                .setMessage(message)
                .setPositiveButton("Close", null)
                .show();
    }

    private void showError(String message) {
        Toast.makeText(
                this,
                message,
                Toast.LENGTH_LONG).show();

        setStatus(message, true);
    }

    private void setStatus(
            String message,
            boolean error) {

        status.setText(message);

        status.setTextColor(
                getColor(
                        error
                                ? R.color.red
                                : R.color.green));
    }

    private String safeMessage(Exception e) {

        String message = e.getMessage();

        if (message == null ||
                message.trim().isEmpty()) {
            return "Unknown error";
        }

        return message;
    }
}
'''

files[".github/workflows/apk.yml"] = r'''name: Hamse Tool APK

on:
  push:
    branches:
      - main
  workflow_dispatch:

concurrency:
  group: hamse-tool-build-${{ github.ref }}
  cancel-in-progress: true

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Java 17
        uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: '17'

      - name: Setup Gradle
        uses: gradle/actions/setup-gradle@v4

      - name: Create Gradle Wrapper
        run: gradle wrapper --gradle-version 8.0

      - name: Make wrapper executable
        run: chmod +x gradlew

      - name: Build Debug APK
        run: ./gradlew clean assembleDebug --stacktrace

      - name: Upload APK
        uses: actions/upload-artifact@v4
        with:
          name: Hamse-Tool-debug
          path: app/build/outputs/apk/debug/app-debug.apk
          if-no-files-found: error
'''

for path, content in files.items():
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")

print("================================")
print("HAMSE TOOL PROJECT CREATED")
print("================================")
print("Files:", len(files))
print("Location:", Path.cwd())
print("")
print("Next:")
print("1. git init")
print("2. git add .")
print("3. git commit -m 'Create Hamse Tool'")
print("4. Add your new GitHub repository as origin")
print("5. git push -u origin main")
