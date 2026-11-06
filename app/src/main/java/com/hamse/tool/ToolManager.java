package com.hamse.tool;

import android.util.Log;
import java.io.*;
import java.nio.file.*;
import java.util.*;
import java.util.regex.*;
import java.util.zip.*;

public class ToolManager {

    private static final String TAG = "HamseToolManager";

    // ── XOR decode ────────────────────────────────────────────────────────────
    public String decodeXorScript(String filePath, int baseKey) {
        try {
            byte[] raw = Files.readAllBytes(Paths.get(filePath));
            byte[] dec = new byte[raw.length];
            for (int i = 0; i < raw.length; i++)
                dec[i] = (byte)(raw[i] ^ ((baseKey + i) & 0xFF));
            return new String(dec, "UTF-8");
        } catch (IOException e) {
            Log.e(TAG, "decodeXorScript: " + e.getMessage());
            return "ERROR: " + e.getMessage();
        }
    }

    // ── XOR encode ────────────────────────────────────────────────────────────
    public byte[] encodeXorScript(String plaintext, int baseKey) {
        try {
            byte[] raw = plaintext.getBytes("UTF-8");
            byte[] out = new byte[raw.length];
            for (int i = 0; i < raw.length; i++)
                out[i] = (byte)(raw[i] ^ ((baseKey + i) & 0xFF));
            return out;
        } catch (UnsupportedEncodingException e) { return new byte[0]; }
    }

    // ── URL pattern ───────────────────────────────────────────────────────────
    private static final Pattern URL_PAT = Pattern.compile(
        "https?://[\\w\\-._~:/?#\\[\\]@!$&'()*+,;=%]+",
        Pattern.CASE_INSENSITIVE);

    public List<String> scanUrlsFromApk(String apkPath) {
        Set<String> found = new LinkedHashSet<>();
        try (ZipFile zip = new ZipFile(apkPath)) {
            Enumeration<? extends ZipEntry> entries = zip.entries();
            while (entries.hasMoreElements()) {
                ZipEntry e = entries.nextElement();
                if (e.isDirectory()) continue;
                String n = e.getName().toLowerCase();
                if (n.endsWith(".xml") || n.endsWith(".json") || n.endsWith(".js")
                    || n.endsWith(".html") || n.endsWith(".txt") || n.endsWith(".dex")
                    || n.startsWith("assets/")) {
                    try (InputStream is = zip.getInputStream(e)) {
                        extractUrls(readStream(is), found);
                    } catch (Exception ignored) {}
                }
            }
        } catch (IOException e) { Log.e(TAG, "scanApk: " + e.getMessage()); }
        return new ArrayList<>(found);
    }

    public List<String> scanUrlsFromFile(String filePath) {
        Set<String> found = new LinkedHashSet<>();
        try {
            extractUrls(new String(Files.readAllBytes(Paths.get(filePath)), "UTF-8"), found);
        } catch (IOException e) { Log.e(TAG, "scanFile: " + e.getMessage()); }
        return new ArrayList<>(found);
    }

    private void extractUrls(String text, Set<String> out) {
        Matcher m = URL_PAT.matcher(text);
        while (m.find()) out.add(m.group());
    }

    private String readStream(InputStream is) throws IOException {
        ByteArrayOutputStream buf = new ByteArrayOutputStream();
        byte[] chunk = new byte[4096]; int n;
        while ((n = is.read(chunk)) != -1) buf.write(chunk, 0, n);
        return buf.toString("ISO-8859-1");
    }

    // ── PAK unpack ────────────────────────────────────────────────────────────
    public boolean unpackPak(String pakPath, String outputDir) {
        try {
            new File(outputDir).mkdirs();
            try (ZipInputStream zis = new ZipInputStream(new FileInputStream(pakPath))) {
                ZipEntry entry;
                while ((entry = zis.getNextEntry()) != null) {
                    File target = new File(outputDir, entry.getName());
                    if (entry.isDirectory()) { target.mkdirs(); }
                    else {
                        target.getParentFile().mkdirs();
                        try (FileOutputStream fos = new FileOutputStream(target)) {
                            byte[] buf = new byte[8192]; int n;
                            while ((n = zis.read(buf)) != -1) fos.write(buf, 0, n);
                        }
                    }
                    zis.closeEntry();
                }
            }
            return true;
        } catch (IOException e) { Log.e(TAG, "unpack: " + e.getMessage()); return false; }
    }

    // ── PAK repack ────────────────────────────────────────────────────────────
    public boolean repackPak(String sourceDir, String outputPakPath) {
        try (ZipOutputStream zos = new ZipOutputStream(new FileOutputStream(outputPakPath))) {
            zipDir(new File(sourceDir), new File(sourceDir), zos);
            return true;
        } catch (IOException e) { Log.e(TAG, "repack: " + e.getMessage()); return false; }
    }

    private void zipDir(File base, File cur, ZipOutputStream zos) throws IOException {
        File[] files = cur.listFiles();
        if (files == null) return;
        for (File f : files) {
            if (f.isDirectory()) { zipDir(base, f, zos); }
            else {
                String rel = base.toURI().relativize(f.toURI()).getPath();
                zos.putNextEntry(new ZipEntry(rel));
                try (FileInputStream fis = new FileInputStream(f)) {
                    byte[] buf = new byte[8192]; int n;
                    while ((n = fis.read(buf)) != -1) zos.write(buf, 0, n);
                }
                zos.closeEntry();
            }
        }
    }
}
