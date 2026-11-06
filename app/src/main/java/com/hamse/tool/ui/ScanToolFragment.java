package com.hamse.tool.ui;

import android.os.Bundle;
import android.view.*;
import android.widget.*;
import androidx.annotation.*;
import androidx.fragment.app.Fragment;
import com.hamse.tool.R;
import com.hamse.tool.ToolManager;
import java.util.List;

public class ScanToolFragment extends Fragment {
    @Nullable @Override
    public View onCreateView(@NonNull LayoutInflater inf, @Nullable ViewGroup c, @Nullable Bundle s) {
        View v = inf.inflate(R.layout.fragment_scan, c, false);
        ToolManager tm = new ToolManager();
        EditText etPath = v.findViewById(R.id.et_scan_path);
        TextView tv     = v.findViewById(R.id.tv_scan_output);
        v.findViewById(R.id.btn_scan).setOnClickListener(x -> {
            String path = etPath.getText().toString().trim();
            List<String> urls = path.endsWith(".apk")
                ? tm.scanUrlsFromApk(path) : tm.scanUrlsFromFile(path);
            if (urls.isEmpty()) { tv.setText("No URLs found."); return; }
            StringBuilder sb = new StringBuilder("Found " + urls.size() + " URLs:\n\n");
            for (String u : urls) sb.append("→ ").append(u).append("\n");
            tv.setText(sb.toString());
        });
        return v;
    }
}
