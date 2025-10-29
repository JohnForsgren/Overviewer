from __future__ import annotations
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

from .scanner import scan_project
from .renderer import render_markdown, MODE_DEVELOPER, MODE_AI
from .config import load_config, save_config

class OverviewerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Overviewer')
        self.project_path_var = tk.StringVar()
        self.mode_var = tk.StringVar(value=MODE_DEVELOPER)
        self.filetype_vars = {}  # dynamically populated after first scan
        self.cache_var = tk.BooleanVar(value=True)
        self.status_var = tk.StringVar(value='Idle')
        self.count_var = tk.StringVar(value='Files: 0 | Folders: 0')
        self.colorized = True  # colorization enabled by default
        self._build()
        self.scanned_once = False

    def _build(self):
        top = tk.Frame(self.root)
        top.pack(fill=tk.X, padx=5, pady=5)
        tk.Label(top, text='Project Root:').pack(side=tk.LEFT)
        tk.Entry(top, textvariable=self.project_path_var, width=50).pack(side=tk.LEFT, padx=5)
        tk.Button(top, text='Browse', command=self._browse).pack(side=tk.LEFT)
        tk.Label(top, text='Mode:').pack(side=tk.LEFT, padx=10)
        tk.OptionMenu(top, self.mode_var, MODE_DEVELOPER, MODE_AI).pack(side=tk.LEFT)
        tk.Button(top, text='Scan', command=self._scan).pack(side=tk.LEFT, padx=10)
        tk.Button(top, text='Save Markdown', command=self._save).pack(side=tk.LEFT)
        # Numbering now always on (removed toggle)
        tk.Button(top, text='Colorize', command=self._toggle_colors).pack(side=tk.LEFT, padx=5)

        options_frame = tk.Frame(self.root)
        options_frame.pack(fill=tk.X, padx=5)
        tk.Label(options_frame, text='File Types (discovered):').pack(anchor='w')
        self.types_container = tk.Frame(options_frame)
        self.types_container.pack(fill=tk.X)

        bottom = tk.Frame(self.root)
        bottom.pack(fill=tk.X, padx=5, pady=2)
        tk.Checkbutton(bottom, text='Use Cache', variable=self.cache_var).pack(side=tk.LEFT)
        tk.Label(bottom, textvariable=self.count_var).pack(side=tk.LEFT, padx=10)
        tk.Label(bottom, textvariable=self.status_var, fg='gray').pack(side=tk.RIGHT)

        # Scrollable text output
        text_frame = tk.Frame(self.root)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.output_text = tk.Text(text_frame, width=100, height=40, wrap='none')
        yscroll = tk.Scrollbar(text_frame, orient='vertical', command=self.output_text.yview)
        self.output_text.configure(yscrollcommand=yscroll.set)
        yscroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def _browse(self):
        chosen = filedialog.askdirectory()
        if chosen:
            self.project_path_var.set(chosen)

    def _scan(self):
        import threading
        path_str = self.project_path_var.get().strip()
        if not path_str:
            messagebox.showerror('Error', 'Please select a project root path.')
            return
        root_path = Path(path_str)
        if not root_path.exists():
            messagebox.showerror('Error', 'Path does not exist.')
            return

        # Load config if first time scanning this root
        config = load_config(root_path)
        if not self.scanned_once and 'extensions' in config:
            # Pre-populate extensions after initial scan populates them
            pass

        use_cache = self.cache_var.get()
        include_exts = None
        if self.scanned_once:
            include_exts = [ext for ext, var in self.filetype_vars.items() if var.get()]

        self.status_var.set('Scanning...')
        self.root.config(cursor='watch')

        progress_win = tk.Toplevel(self.root)
        progress_win.title('Scanning')
        tk.Label(progress_win, text='Scanning project, please wait...').pack(padx=20, pady=10)
        progress_win.transient(self.root)
        progress_win.grab_set()
        progress_win.update()

        def task():
            try:
                # First scan without metadata if first time
                tree = scan_project(root_path, include_exts=include_exts, use_cache=use_cache, parse_metadata=self.scanned_once)
                # Populate extensions dynamically after first scan
                if not self.scanned_once:
                    exts = sorted({f.ext for f in _iter_files(tree) if f.ext})
                    # Count files per extension (baseline counts from initial full scan)
                    ext_counts = {}
                    for f in _iter_files(tree):
                        if f.ext:
                            ext_counts[f.ext] = ext_counts.get(f.ext, 0) + 1
                    for child in self.types_container.winfo_children():
                        child.destroy()
                    for ext in exts:
                        var = tk.BooleanVar(value=True)
                        self.filetype_vars[ext] = var
                        ext_frame = tk.Frame(self.types_container)
                        ext_frame.pack(side=tk.LEFT, padx=4, pady=2)
                        tk.Checkbutton(ext_frame, text=ext, variable=var, command=self._rescan_after_toggle).pack(anchor='w')
                        count = ext_counts.get(ext, 0)
                        tk.Label(ext_frame, text=f"{count} {ext}", fg='gray').pack(anchor='w')
                    self.scanned_once = True
                    # Save config after initial detection
                    save_config(root_path, {'extensions': {e: True for e in self.filetype_vars}})
                    # After populating extensions, trigger second pass with metadata for selected ones
                    selected_exts = [e for e, v in self.filetype_vars.items() if v.get()]
                    tree = scan_project(root_path, include_exts=selected_exts, use_cache=use_cache, parse_metadata=True)
                else:
                    # Save current toggles
                    save_config(root_path, {'extensions': {e: v.get() for e, v in self.filetype_vars.items()}})
                md = render_markdown(tree, mode=self.mode_var.get())
                def update_ui():
                    self.output_text.delete('1.0', tk.END)
                    self.output_text.insert(tk.END, md)
                    files_count, folders_count = _count_objects(tree)
                    self.count_var.set(f'Files: {files_count} | Folders: {folders_count}')
                    self.status_var.set('Done')
                    self.root.config(cursor='')
                    progress_win.destroy()
                    if self.colorized:
                        self._apply_colors()
                    if self.colorized:
                        self._apply_colors()
                self.root.after(0, update_ui)
            except Exception as e:
                def show_err():
                    self.status_var.set('Error')
                    self.root.config(cursor='')
                    progress_win.destroy()
                    messagebox.showerror('Error', str(e))
                self.root.after(0, show_err)

        threading.Thread(target=task, daemon=True).start()

    def _rescan_after_toggle(self):
        # Only rescan metadata with selected extensions (fast path) but keep using cache
        if not self.scanned_once:
            return
        self._scan()

    def _toggle_colors(self):
        self.colorized = not self.colorized
        if self.colorized:
            self._apply_colors()
        else:
            # Remove color tags
            for tag in self.output_text.tag_names():
                if tag.startswith('ext_'):
                    self.output_text.tag_delete(tag)

    def _apply_colors(self):
        # Assign consistent colors per extension
        extensions = list(self.filetype_vars.keys())
        if not extensions:
            return
        # High-contrast palette (WCAG-inspired hues)
        palette = [
            "#0D47A1",  # deep blue
            "#B71C1C",  # deep red
            "#1B5E20",  # deep green
            "#4A148C",  # deep purple
            "#E65100",  # strong orange
            "#004D40",  # teal dark
            "#827717",  # olive
            "#263238",  # blue gray
            "#880E4F",  # magenta dark
            "#3E2723",  # brown dark
        ]
        ext_colors = {ext: palette[i % len(palette)] for i, ext in enumerate(extensions)}
        # Clear old tags first
        for tag in self.output_text.tag_names():
            if tag.startswith('ext_'):
                self.output_text.tag_delete(tag)
        lines = self.output_text.get('1.0', tk.END).splitlines()
        for idx, raw in enumerate(lines, start=1):
            line = raw.rstrip('\n')
            stripped = line.strip()
            if not stripped:
                continue
            # Skip folder headings & description lines
            if '📁' in stripped or stripped.startswith(('=', '#')) or stripped.startswith('📄'):
                continue
            display = stripped
            if display.startswith('⭐️ '):
                display = display[3:]
            # The filename is the last token (after indentation & star)
            parts = display.split()
            if not parts:
                continue
            filename = parts[-1]
            if '.' in filename:
                ext = '.' + filename.split('.')[-1].lower()
                if ext in ext_colors:
                    tag = f'ext_{ext[1:]}'
                    self.output_text.tag_configure(tag, foreground=ext_colors[ext])
                    self.output_text.tag_add(tag, f"{idx}.0", f"{idx}.end")

    def _save(self):
        md = self.output_text.get('1.0', tk.END).strip()
        if not md:
            messagebox.showerror('Error', 'Nothing to save.')
            return
        file_path = filedialog.asksaveasfilename(defaultextension='.md', filetypes=[('Markdown', '*.md')])
        if file_path:
            Path(file_path).write_text(md, encoding='utf-8')
            messagebox.showinfo('Saved', f'Saved to {file_path}')

    def run(self):
        self.root.mainloop()


def launch_gui():
    OverviewerGUI().run()


def _iter_files(folder_node):
    for f in folder_node.files:
        yield f
    for sub in folder_node.subfolders.values():
        yield from _iter_files(sub)

def _count_objects(folder_node):
    files = 0
    folders = 0
    def walk(node):
        nonlocal files, folders
        folders += 1
        files += len(node.files)
        for child in node.subfolders.values():
            walk(child)
    walk(folder_node)
    return files, folders
