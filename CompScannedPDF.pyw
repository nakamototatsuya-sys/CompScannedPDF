"""
スキャンPDF 圧縮アプリ（モダンUI版）
=====================================
起動: python compress_app.py

必要なライブラリ:
  pip install pdf2image Pillow pypdf reportlab
  + poppler:
    Mac:   brew install poppler
    Win:   https://github.com/oschwartz10612/poppler-windows
    Linux: sudo apt install poppler-utils
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import tempfile
from pathlib import Path


# ── プリセット ────────────────────────────────────────────
PRESETS = {
    "low":    {"dpi": 200, "quality": 85, "label": "品質重視",    "sub": "品質重視・軽め圧縮"},
    "medium": {"dpi": 150, "quality": 72, "label": "バランス", "sub": "画質とサイズのバランス"},
    "high":   {"dpi": 100, "quality": 55, "label": "サイズ優先",  "sub": "サイズ優先・最大圧縮"},
}

C = {
    "bg":       "#F4F6F8",
    "surface":  "#FFFFFF",
    "surface2": "#EEF1F5",
    "border":   "#D8DDE5",
    "border_hi":"#A0AABB",
    "accent":   "#2563EB",
    "text":     "#1A202C",
    "text2":    "#4A5568",
    "text3":    "#9AA5B4",
    "green":    "#16A34A",
    "selected": "#EBF2FF",
    "sel_bdr":  "#2563EB",
    "btn_dis":  "#A0AABB",
}


def format_bytes(b):
    if b < 1024:       return f"{b} B"
    elif b < 1024**2:  return f"{b/1024:.1f} KB"
    else:              return f"{b/1024**2:.2f} MB"


def estimate_size(original_bytes, mode):
    ratios = {"low": 0.55, "medium": 0.25, "high": 0.12}
    return int(original_bytes * ratios.get(mode, 0.25))


def compress_pdf(input_path, output_path, dpi, quality, progress_cb, log_cb):
    import img2pdf
    from pdf2image import convert_from_path

    log_cb("PDFを読み込んでいます...")
    pages = convert_from_path(str(input_path), dpi=dpi)
    total = len(pages)
    log_cb(f"{total}ページを検出")

    tmp_jpgs = []
    try:
        for i, page_img in enumerate(pages):
            log_cb(f"ページ {i+1} / {total} を処理中...")
            progress_cb(int((i / total) * 85))

            if page_img.mode not in ("RGB", "L"):
                page_img = page_img.convert("RGB")

            fd, tmp_jpg = tempfile.mkstemp(suffix=".jpg")
            os.close(fd)
            tmp_jpgs.append(tmp_jpg)
            page_img.save(tmp_jpg, format="JPEG", quality=quality, optimize=True)

        log_cb("PDFに結合しています...")
        progress_cb(90)

        # img2pdfはJPEGをそのまま無劣化でPDFに埋め込む
        with open(output_path, "wb") as f:
            f.write(img2pdf.convert(tmp_jpgs))

        progress_cb(100)
        log_cb("完了")
    finally:
        for f in tmp_jpgs:
            try:
                if os.path.exists(f):
                    os.unlink(f)
            except Exception:
                pass


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CompScannedPDF")
        self.resizable(False, False)
        self.configure(bg=C["bg"])

        self.pdf_path = None
        self.mode_var = tk.StringVar(value="medium")
        self._mode_frames = {}

        self._setup_styles()
        self._build()
        self._update_estimate()

    def _setup_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure(
            "Dark.Horizontal.TProgressbar",
            troughcolor=C["border"],
            background=C["accent"],
            bordercolor=C["surface2"],
            lightcolor=C["accent"],
            darkcolor=C["accent"],
            thickness=6,
        )

    def _build(self):
        W   = 500
        PAD = 24

        # ── ヘッダー ──
        hdr = tk.Frame(self, bg=C["bg"])
        hdr.pack(fill="x", padx=PAD, pady=(PAD, 0))
        tk.Label(hdr, text="CompScanned", font=("Yu Gothic UI", 22, "bold"),
                 bg=C["bg"], fg=C["accent"]).pack(side="left")
        tk.Label(hdr, text="PDF", font=("Yu Gothic UI", 22, "bold"),
                 bg=C["bg"], fg=C["text"]).pack(side="left")
        tk.Label(hdr, text="ローカル処理 · 完全プライベート",
                 font=("Yu Gothic UI", 9), bg=C["bg"], fg=C["text3"]).pack(side="right", pady=6)

        tk.Frame(self, bg=C["border"], height=1).pack(fill="x", padx=PAD, pady=(12, 0))

        # ── ドロップゾーン ──
        self.drop_zone = tk.Frame(self, bg=C["surface"],
                                   highlightthickness=1,
                                   highlightbackground=C["border"])
        self.drop_zone.pack(fill="x", padx=PAD, pady=16)
        self.drop_zone.bind("<Button-1>", lambda e: self._pick_file())

        dz_inner = tk.Frame(self.drop_zone, bg=C["surface"], cursor="hand2")
        dz_inner.pack(pady=28)
        dz_inner.bind("<Button-1>", lambda e: self._pick_file())

        self.dz_icon = tk.Label(dz_inner, text="⊕", font=("Yu Gothic UI", 28),
                                 bg=C["surface"], fg=C["border_hi"], cursor="hand2")
        self.dz_icon.pack()
        self.dz_icon.bind("<Button-1>", lambda e: self._pick_file())

        self.dz_main = tk.Label(dz_inner, text="クリックしてPDFを選択",
                                 font=("Yu Gothic UI", 12, "bold"),
                                 bg=C["surface"], fg=C["text"], cursor="hand2")
        self.dz_main.pack(pady=(8, 2))
        self.dz_main.bind("<Button-1>", lambda e: self._pick_file())

        self.dz_sub = tk.Label(dz_inner, text="スキャンPDFに最適化された圧縮",
                                font=("Yu Gothic UI", 9),
                                bg=C["surface"], fg=C["text3"], cursor="hand2")
        self.dz_sub.pack()
        self.dz_sub.bind("<Button-1>", lambda e: self._pick_file())

        for w in [self.drop_zone, dz_inner, self.dz_icon, self.dz_main, self.dz_sub]:
            w.bind("<Enter>", lambda e: self.drop_zone.configure(highlightbackground=C["accent"]))
            w.bind("<Leave>", lambda e: self.drop_zone.configure(highlightbackground=C["border"]))

        # ── ファイル情報バー ──
        self.file_bar = tk.Frame(self, bg=C["surface2"],
                                  highlightthickness=1,
                                  highlightbackground=C["border"])
        fb = tk.Frame(self.file_bar, bg=C["surface2"])
        fb.pack(fill="x", padx=16, pady=10)
        tk.Label(fb, text="📄", font=("Yu Gothic UI", 14),
                 bg=C["surface2"], fg=C["text"]).pack(side="left", padx=(0, 10))
        fb_txt = tk.Frame(fb, bg=C["surface2"])
        fb_txt.pack(side="left", fill="x", expand=True)
        self.fb_name = tk.Label(fb_txt, text="", font=("Yu Gothic UI", 10, "bold"),
                                 bg=C["surface2"], fg=C["text"], anchor="w")
        self.fb_name.pack(fill="x")
        self.fb_meta = tk.Label(fb_txt, text="", font=("Yu Gothic UI", 9),
                                 bg=C["surface2"], fg=C["text2"], anchor="w")
        self.fb_meta.pack(fill="x")
        tk.Button(fb, text="変更", font=("Yu Gothic UI", 9),
                  bg=C["surface2"], fg=C["text2"], relief="flat", bd=0,
                  activebackground=C["border"], activeforeground=C["text"],
                  cursor="hand2", command=self._pick_file).pack(side="right")

        # ── モード選択 ──
        sec = tk.Frame(self, bg=C["bg"])
        sec.pack(fill="x", padx=PAD, pady=(0, 14))
        tk.Label(sec, text="COMPRESSION MODE", font=("Yu Gothic UI", 8, "bold"),
                 bg=C["bg"], fg=C["text3"]).pack(anchor="w", pady=(0, 8))

        row = tk.Frame(sec, bg=C["bg"])
        row.pack(fill="x")
        for key, p in PRESETS.items():
            f = tk.Frame(row, bg=C["surface"],
                         highlightthickness=1,
                         highlightbackground=C["border"],
                         cursor="hand2")
            f.pack(side="left", expand=True, fill="both",
                   padx=(0, 6 if key != "high" else 0))
            lbl = tk.Label(f, text=p["label"], font=("Yu Gothic UI", 10, "bold"),
                           bg=C["surface"], fg=C["accent"])
            lbl.pack(pady=(14, 2), padx=14)
            sub = tk.Label(f, text=p["sub"], font=("Yu Gothic UI", 8),
                           bg=C["surface"], fg=C["text3"], wraplength=120)
            sub.pack(pady=(0, 14), padx=14)
            for w in [f, lbl, sub]:
                w.bind("<Button-1>", lambda e, k=key: self._set_mode(k))
            self._mode_frames[key] = {"frame": f, "labels": [lbl, sub]}

        self._set_mode("medium", redraw=False)

        # ── 予想サイズ ──
        est_wrap = tk.Frame(self, bg=C["surface"],
                             highlightthickness=1, highlightbackground=C["border"])
        est_wrap.pack(fill="x", padx=PAD, pady=(0, 16))
        est_row = tk.Frame(est_wrap, bg=C["surface"])
        est_row.pack(fill="x", padx=16, pady=12)
        tk.Label(est_row, text="予想サイズ", font=("Yu Gothic UI", 9),
                 bg=C["surface"], fg=C["text3"]).pack(side="left")
        self.est_lbl = tk.Label(est_row, text="ファイルを選択してください",
                                 font=("Yu Gothic UI", 10, "bold"),
                                 bg=C["surface"], fg=C["text2"])
        self.est_lbl.pack(side="right")

        # ── 進捗エリア ──
        self.prog_area = tk.Frame(self, bg=C["bg"])
        self.prog_var = tk.IntVar(value=0)
        self.prog_bar = ttk.Progressbar(
            self.prog_area,
            variable=self.prog_var,
            maximum=100,
            style="Dark.Horizontal.TProgressbar",
        )
        self.prog_bar.pack(fill="x", padx=PAD)
        self.prog_lbl = tk.Label(self.prog_area, text="",
                                  font=("Yu Gothic UI", 9),
                                  bg=C["bg"], fg=C["text3"])
        self.prog_lbl.pack(anchor="w", padx=PAD, pady=(4, 0))

        # ── 実行ボタン ──
        self.run_btn = tk.Button(
            self,
            text="圧縮を開始  →",
            font=("Yu Gothic UI", 12, "bold"),
            bg=C["accent"], fg=C["bg"],
            relief="flat", bd=0,
            activebackground="#7BA7F7",
            activeforeground=C["bg"],
            cursor="hand2",
            pady=14,
            command=self._run,
        )
        self.run_btn.pack(fill="x", padx=PAD, pady=(0, PAD))

        self.geometry(f"{W}x670")

    def _pick_file(self):
        path = filedialog.askopenfilename(
            title="PDFを選択",
            filetypes=[("PDF ファイル", "*.pdf"), ("すべてのファイル", "*.*")]
        )
        if path:
            self._load_file(path)

    def _load_file(self, path):
        self.pdf_path = path
        size = os.path.getsize(path)
        name = Path(path).name
        pages_str = ""
        try:
            from pypdf import PdfReader
            pages_str = f"  ·  {len(PdfReader(path).pages)} ページ"
        except Exception:
            pass

        self.dz_icon.configure(text="✓", fg=C["green"])
        self.dz_main.configure(text=name)
        self.dz_sub.configure(text=f"{format_bytes(size)}{pages_str}", fg=C["text2"])
        self.fb_name.configure(text=name)
        self.fb_meta.configure(text=f"{format_bytes(size)}{pages_str}")
        self.file_bar.pack(fill="x", padx=PAD, pady=(0, 14))
        self._set_mode(self.mode_var.get(), redraw=False)
        self._update_estimate()

    def _set_mode(self, key, redraw=True):
        self.mode_var.set(key)
        for k, d in self._mode_frames.items():
            if k == key:
                d["frame"].configure(bg=C["selected"], highlightbackground=C["sel_bdr"])
                for lbl in d["labels"]:
                    lbl.configure(bg=C["selected"])
            else:
                d["frame"].configure(bg=C["surface"], highlightbackground=C["border"])
                for lbl in d["labels"]:
                    lbl.configure(bg=C["surface"])
        if redraw:
            self._update_estimate()

    def _update_estimate(self):
        if not self.pdf_path or not os.path.exists(self.pdf_path):
            self.est_lbl.configure(text="ファイルを選択してください", fg=C["text2"])
            return
        orig  = os.path.getsize(self.pdf_path)
        est   = estimate_size(orig, self.mode_var.get())
        ratio = (1 - est / orig) * 100
        self.est_lbl.configure(
            text=f"{format_bytes(orig)}  →  約 {format_bytes(est)}  ( -{ratio:.0f}% )",
            fg=C["green"]
        )

    def _run(self):
        if not self.pdf_path:
            messagebox.showwarning("ファイル未選択", "PDFファイルを選択してください。")
            return

        out_path = filedialog.asksaveasfilename(
            title="保存先を選択",
            initialfile=Path(self.pdf_path).stem + "_compressed.pdf",
            defaultextension=".pdf",
            filetypes=[("PDF ファイル", "*.pdf")]
        )
        if not out_path:
            return

        preset = PRESETS[self.mode_var.get()]
        self.run_btn.configure(state="disabled", text="処理中...", bg=C["btn_dis"])
        self.prog_area.pack(fill="x", pady=(0, 8))
        self.prog_var.set(0)

        def worker():
            try:
                compress_pdf(
                    self.pdf_path, out_path,
                    dpi=preset["dpi"], quality=preset["quality"],
                    progress_cb=lambda v: self.after(0, self.prog_var.set, v),
                    log_cb=lambda m: self.after(0, self.prog_lbl.configure, {"text": m})
                )
                orig  = os.path.getsize(self.pdf_path)
                comp  = os.path.getsize(out_path)
                ratio = (1 - comp / orig) * 100
                msg = (f"圧縮完了！\n\n"
                       f"元のサイズ   : {format_bytes(orig)}\n"
                       f"圧縮後サイズ : {format_bytes(comp)}\n"
                       f"削減率       : -{ratio:.1f}%")
                self.after(0, lambda: messagebox.showinfo("完了", msg))
            except Exception as e:
                err = str(e)
                self.after(0, lambda m=err: messagebox.showerror("エラー", m))
            finally:
                self.after(0, self._reset)

        threading.Thread(target=worker, daemon=True).start()

    def _reset(self):
        self.run_btn.configure(state="normal", text="圧縮を開始  →", bg=C["accent"])
        self._set_mode(self.mode_var.get(), redraw=False)


if __name__ == "__main__":
    import sys
    app = App()
    # 右クリックからファイルパスが渡された場合は自動でロード
    if len(sys.argv) > 1:
        import os
        path = sys.argv[1]
        if os.path.exists(path) and path.lower().endswith(".pdf"):
            app.after(200, lambda: app._load_file(path))
    app.mainloop()
