package com.hamse.tool.ui;

import android.os.Bundle;
import android.view.*;
import android.widget.*;
import androidx.annotation.*;
import androidx.fragment.app.Fragment;
import com.hamse.tool.R;
import com.hamse.tool.ToolManager;

public class PakToolFragment extends Fragment {
    @Nullable @Override
    public View onCreateView(@NonNull LayoutInflater inf, @Nullable ViewGroup c, @Nullable Bundle s) {
        View v = inf.inflate(R.layout.fragment_pak, c, false);
        ToolManager tm = new ToolManager();
        EditText etPak = v.findViewById(R.id.et_pak_path);
        EditText etOut = v.findViewById(R.id.et_out_path);
        TextView tv    = v.findViewById(R.id.tv_pak_output);
        v.findViewById(R.id.btn_unpack).setOnClickListener(x -> {
            boolean ok = tm.unpackPak(etPak.getText().toString().trim(),
                                      etOut.getText().toString().trim());
            tv.setText(ok ? "Unpacked to: " + etOut.getText() : "Failed — check logcat");
        });
        v.findViewById(R.id.btn_repack).setOnClickListener(x -> {
            boolean ok = tm.repackPak(etPak.getText().toString().trim(),
                                      etOut.getText().toString().trim());
            tv.setText(ok ? "Repacked to: " + etOut.getText() : "Failed — check logcat");
        });
        return v;
    }
}
