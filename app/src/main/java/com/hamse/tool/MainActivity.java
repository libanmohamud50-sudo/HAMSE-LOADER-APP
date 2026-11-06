package com.hamse.tool;

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
