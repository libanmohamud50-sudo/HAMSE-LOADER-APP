package com.hamse.tool.ui;

import android.os.Bundle;
import android.view.*;
import android.widget.*;
import androidx.annotation.*;
import androidx.fragment.app.Fragment;
import com.hamse.tool.R;
import com.hamse.tool.ToolManager;
import java.io.*;
import java.nio.file.*;

public class LuaToolFragment extends Fragment {
    @Nullable @Override
    public View onCreateView(@NonNull LayoutInflater inf, @Nullable ViewGroup c, @Nullable Bundle s) {
        View v = inf.inflate(R.layout.fragment_lua, c, false);
        ToolManager tm = new ToolManager();
        EditText etPath = v.findViewById(R.id.et_lua_path);
        EditText etKey  = v.findViewById(R.id.et_lua_key);
        TextView tv     = v.findViewById(R.id.tv_lua_output);
        v.findViewById(R.id.btn_decrypt).setOnClickListener(x ->
            tv.setText(tm.decodeXorScript(etPath.getText().toString().trim(), key(etKey))));
        v.findViewById(R.id.btn_encrypt).setOnClickListener(x -> {
            try {
                String path = etPath.getText().toString().trim();
                String plain = new String(Files.readAllBytes(Paths.get(path)));
                byte[] enc = tm.encodeXorScript(plain, key(etKey));
                String out = path + ".enc";
                Files.write(Paths.get(out), enc);
                tv.setText("Encrypted → " + out);
            } catch (IOException e) { tv.setText("Error: " + e.getMessage()); }
        });
        return v;
    }
    private int key(EditText et) {
        try { return Integer.parseInt(et.getText().toString().trim(), 16); }
        catch (NumberFormatException e) { return 0x5A; }
    }
}
