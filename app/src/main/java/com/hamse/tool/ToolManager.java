package com.hamse.tool;

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
