# -*- coding: utf-8 -*-
"""
Legal Retrieval Relevance Labeler
----------------------------------
GUI tool to manually annotate retrieved chunks as Relevant / Not Relevant.

Controls:
  y  or  [Relevant]     -> mark as Relevant (1)
  n  or  [Not Relevant] -> mark as Not Relevant (0)
  s  or  [Skip]         -> skip (leave blank)
  b  or  [<< Back]      -> go to previous item
  Right/Left arrows     -> next/previous

Input:  data/experiments/master_evaluation_sheet.csv
Output: data/experiments/completed_labels.csv
"""
from pathlib import Path
import pandas as pd
import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

PROJECT_ROOT = Path(r"E:\Legal Finale")
INPUT_FILE   = PROJECT_ROOT / "data" / "experiments" / "master_evaluation_sheet.csv"
OUTPUT_FILE  = PROJECT_ROOT / "data" / "experiments" / "completed_labels.csv"


class EvaluationApp:
    def __init__(self):
        # Load or init dataframe
        if OUTPUT_FILE.exists():
            self.df = pd.read_csv(OUTPUT_FILE)
        elif INPUT_FILE.exists():
            self.df = pd.read_csv(INPUT_FILE)
        else:
            raise FileNotFoundError(f"Neither {OUTPUT_FILE} nor {INPUT_FILE} found.")

        # Ensure required columns
        if "Relevant" not in self.df.columns:
            self.df["Relevant"] = ""
        for col in ["Case_ID","Court","Case_Title","Chunk_Text"]:
            if col not in self.df.columns:
                self.df[col] = ""

        # Find first unlabelled row
        self.i = 0
        for idx in range(len(self.df)):
            v = str(self.df.loc[idx, "Relevant"]).strip().lower()
            if v in ("", "nan"):
                self.i = idx
                break
        else:
            self.i = len(self.df)  # all done

        # Stats
        self.total    = len(self.df)
        self.labelled = int(self.df["Relevant"].apply(
            lambda v: str(v).strip().lower() not in ("","nan")).sum())

        # Build UI
        self.root = ctk.CTk()
        self.root.title("Legal Retrieval Evaluation Tool")
        self.root.geometry("1350x900")
        self.root.configure(fg_color="#1a1a2e")

        # Progress bar + stats
        top = ctk.CTkFrame(self.root, fg_color="#16213e"); top.pack(fill="x", padx=10, pady=6)
        self.pb  = ctk.CTkProgressBar(top, width=900, height=16); self.pb.pack(side="left", padx=10, pady=8)
        self.stat_lbl = ctk.CTkLabel(top, font=("Segoe UI", 13), text=""); self.stat_lbl.pack(side="left", padx=10)

        # Query label
        self.query_lbl = ctk.CTkLabel(self.root, font=("Segoe UI", 20, "bold"),
                                       text_color="#e94560"); self.query_lbl.pack(pady=(4,0))

        # Metadata
        self.info = ctk.CTkTextbox(self.root, width=1280, height=80,
                                    font=("Segoe UI", 12), fg_color="#0f3460",
                                    text_color="#a8dadc"); self.info.pack(padx=10, pady=4)

        # Chunk text
        self.txt = ctk.CTkTextbox(self.root, width=1280, height=520,
                                   font=("Segoe UI", 12), fg_color="#16213e",
                                   text_color="#e0e0e0"); self.txt.pack(padx=10, pady=4)

        # Buttons
        btn_frame = ctk.CTkFrame(self.root, fg_color="#1a1a2e"); btn_frame.pack(pady=8)

        ctk.CTkButton(btn_frame, text="<< Back (b)", width=120, fg_color="#444",
                      command=self.go_back).grid(row=0, column=0, padx=8)
        ctk.CTkButton(btn_frame, text="Relevant (y)", width=160, fg_color="#1a7a4a",
                      font=("Segoe UI", 14, "bold"),
                      command=lambda: self.mark(1)).grid(row=0, column=1, padx=8)
        ctk.CTkButton(btn_frame, text="Not Relevant (n)", width=160, fg_color="#a83232",
                      font=("Segoe UI", 14, "bold"),
                      command=lambda: self.mark(0)).grid(row=0, column=2, padx=8)
        ctk.CTkButton(btn_frame, text="Skip (s)", width=120, fg_color="#8a6a00",
                      command=lambda: self.mark("")).grid(row=0, column=3, padx=8)
        ctk.CTkButton(btn_frame, text="Save & Quit", width=120, fg_color="#333",
                      command=self.save_quit).grid(row=0, column=4, padx=8)

        # Current label indicator
        self.cur_label_lbl = ctk.CTkLabel(self.root, font=("Segoe UI", 13), text="")
        self.cur_label_lbl.pack()

        # Keyboard bindings
        self.root.bind("y", lambda e: self.mark(1))
        self.root.bind("Y", lambda e: self.mark(1))
        self.root.bind("n", lambda e: self.mark(0))
        self.root.bind("N", lambda e: self.mark(0))
        self.root.bind("s", lambda e: self.mark(""))
        self.root.bind("S", lambda e: self.mark(""))
        self.root.bind("b", lambda e: self.go_back())
        self.root.bind("B", lambda e: self.go_back())
        self.root.bind("<Right>", lambda e: self.mark(""))
        self.root.bind("<Left>",  lambda e: self.go_back())

        self.refresh()

    def save(self):
        self.df.to_csv(OUTPUT_FILE, index=False)

    def save_quit(self):
        self.save()
        self.root.destroy()

    def refresh(self):
        labelled = int(self.df["Relevant"].apply(
            lambda v: str(v).strip().lower() not in ("", "nan")).sum())
        pct = labelled / max(1, self.total)

        self.pb.set(pct)
        self.stat_lbl.configure(text=f"{labelled}/{self.total} labelled  ({100*pct:.1f}%)")

        if self.i >= self.total:
            self.query_lbl.configure(text="All chunks evaluated!")
            self.info.delete("1.0", "end")
            self.info.insert("end", "Evaluation complete. Close the window or save & quit.")
            self.txt.delete("1.0", "end")
            self.save()
            messagebox.showinfo("Done", "All chunks labelled! File saved.")
            return

        r = self.df.iloc[self.i]
        self.query_lbl.configure(text=f"[{self.i+1}/{self.total}]  Query: {r.get('Query','')}")

        self.info.configure(state="normal")
        self.info.delete("1.0", "end")
        self.info.insert("end",
            f"Case ID : {r.get('Case_ID','')}\n"
            f"Court   : {r.get('Court','')}\n"
            f"Title   : {r.get('Case_Title','')}")
        self.info.configure(state="disabled")

        self.txt.configure(state="normal")
        self.txt.delete("1.0", "end")
        self.txt.insert("end", str(r.get("Chunk_Text","")))
        self.txt.configure(state="disabled")

        cur_rel = str(self.df.loc[self.i, "Relevant"]).strip()
        if cur_rel in ("1", "1.0"):
            cur_str = "Current label: RELEVANT"
            col = "#1a7a4a"
        elif cur_rel in ("0", "0.0"):
            cur_str = "Current label: NOT RELEVANT"
            col = "#a83232"
        else:
            cur_str = "Current label: (unlabelled)"
            col = "#888"
        self.cur_label_lbl.configure(text=cur_str, text_color=col)

    def mark(self, v):
        if self.i >= self.total:
            return
        self.df.loc[self.i, "Relevant"] = v
        self.save()
        self.i += 1
        # Skip already-labelled rows going forward (find next unlabelled)
        # (Actually, advance normally so user can review all)
        self.refresh()

    def go_back(self):
        if self.i > 0:
            self.i -= 1
            self.refresh()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    EvaluationApp().run()