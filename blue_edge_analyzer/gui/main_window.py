"""
主視窗GUI模組
使用tkinter建立使用者介面
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import pandas as pd
from typing import Optional
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.font_manager as fm

from ..core.excel_processor import ExcelProcessor
from ..core.blue_edge_calculator import BlueEdgeCalculator


class MainWindow:
    """主視窗類別"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Blue Edge Index Analyzer v1.0")
        self.root.geometry("800x600")
        
        # 核心處理器
        self.excel_processor = ExcelProcessor()
        self.calculator = BlueEdgeCalculator()
        
        # 結果變數
        self.result_text = tk.StringVar()
        self.file_path_text = tk.StringVar(value="尚未選擇檔案")
        
        # 為了向後相容，保持舊的threshold_var引用
        self.threshold_var = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """設定使用者介面"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 檔案選擇區域
        file_frame = ttk.LabelFrame(main_frame, text="檔案選擇", padding="5")
        file_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(file_frame, textvariable=self.file_path_text).grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        ttk.Button(file_frame, text="選擇檔案", command=self.select_file).grid(row=0, column=1)
        
        file_frame.columnconfigure(0, weight=1)
        
        # 參數設定區域
        param_frame = ttk.LabelFrame(main_frame, text="參數設定", padding="5")
        param_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 工作表選擇
        ttk.Label(param_frame, text="工作表:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.sheet_var = tk.StringVar()
        self.sheet_combobox = ttk.Combobox(param_frame, textvariable=self.sheet_var, state="readonly", width=20)
        self.sheet_combobox.grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        self.sheet_combobox.bind('<<ComboboxSelected>>', self.on_sheet_selected)
        
        # 資料開始行數
        ttk.Label(param_frame, text="資料開始行數:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(5, 0))
        self.start_row_var = tk.StringVar(value="0")
        start_row_spinbox = ttk.Spinbox(param_frame, from_=0, to=1000, textvariable=self.start_row_var, width=10)
        start_row_spinbox.grid(row=1, column=1, sticky=tk.W, padx=(0, 20), pady=(5, 0))
        
        # 自動偵測按鈕
        ttk.Button(param_frame, text="自動偵測", command=self.auto_detect_start_row).grid(row=1, column=2, pady=(5, 0))
        
        # 預覽數據按鈕
        ttk.Button(param_frame, text="預覽數據", command=self.preview_data).grid(row=1, column=3, padx=(10, 0), pady=(5, 0))
        
        # 資料結束行數
        ttk.Label(param_frame, text="資料結束行數:").grid(row=2, column=0, sticky=tk.W, padx=(0, 10), pady=(5, 0))
        self.end_row_var = tk.StringVar(value="")
        end_row_spinbox = ttk.Spinbox(param_frame, from_=1, to=10000, textvariable=self.end_row_var, width=10)
        end_row_spinbox.grid(row=2, column=1, sticky=tk.W, padx=(0, 20), pady=(5, 0))
        
        # 自動偵測結束行數按鈕
        ttk.Button(param_frame, text="自動偵測", command=self.auto_detect_end_row).grid(row=2, column=2, pady=(5, 0))
        
        # 預覽結束數據按鈕
        ttk.Button(param_frame, text="預覽結束數據", command=self.preview_end_data).grid(row=2, column=3, padx=(10, 0), pady=(5, 0))
        
        # TopSide 閾值設定
        ttk.Label(param_frame, text="TopSide N%閾值:").grid(row=3, column=0, sticky=tk.W, padx=(0, 10), pady=(5, 0))
        self.topside_threshold_var = tk.StringVar(value="10")
        topside_threshold_spinbox = ttk.Spinbox(param_frame, from_=1, to=50, textvariable=self.topside_threshold_var, width=10)
        topside_threshold_spinbox.grid(row=3, column=1, sticky=tk.W, padx=(0, 20), pady=(5, 0))
        ttk.Label(param_frame, text="%").grid(row=3, column=2, sticky=tk.W, pady=(5, 0))
        
        # BottomSide 閾值設定
        ttk.Label(param_frame, text="BottomSide N%閾值:").grid(row=4, column=0, sticky=tk.W, padx=(0, 10), pady=(5, 0))
        self.bottomside_threshold_var = tk.StringVar(value="10")
        bottomside_threshold_spinbox = ttk.Spinbox(param_frame, from_=1, to=50, textvariable=self.bottomside_threshold_var, width=10)
        bottomside_threshold_spinbox.grid(row=4, column=1, sticky=tk.W, padx=(0, 20), pady=(5, 0))
        ttk.Label(param_frame, text="%").grid(row=4, column=2, sticky=tk.W, pady=(5, 0))
        
        # NG 閾值設定
        ttk.Label(param_frame, text="NG判斷閾值:").grid(row=5, column=0, sticky=tk.W, padx=(0, 10), pady=(5, 0))
        self.ng_threshold_var = tk.StringVar(value="10.0")
        ng_threshold_spinbox = ttk.Spinbox(param_frame, from_=0.0, to=1000.0, increment=0.1, textvariable=self.ng_threshold_var, width=10)
        ng_threshold_spinbox.grid(row=5, column=1, sticky=tk.W, padx=(0, 20), pady=(5, 0))
        ttk.Label(param_frame, text="(Index值 > 此數值 = NG)").grid(row=5, column=2, sticky=tk.W, pady=(5, 0))
        
        # 計算按鈕
        calc_frame = ttk.Frame(main_frame)
        calc_frame.grid(row=2, column=0, columnspan=2, pady=(0, 10))
        
        calc_button = ttk.Button(calc_frame, text="開始計算 Blue Edge Index", 
                               command=self.calculate_blue_edge, 
                               style="Accent.TButton")
        calc_button.pack(side=tk.LEFT, padx=(0, 10))
        
        chart_button = ttk.Button(calc_frame, text="顯示中間列曲線圖", 
                                command=self.show_middle_column_chart)
        chart_button.pack(side=tk.LEFT)
        
        # 結果顯示區域
        result_frame = ttk.LabelFrame(main_frame, text="計算結果", padding="5")
        result_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # 結果文字區域
        self.result_text_widget = tk.Text(result_frame, height=15, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.result_text_widget.yview)
        self.result_text_widget.configure(yscrollcommand=scrollbar.set)
        
        self.result_text_widget.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)
        
        # 複製按鈕
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2)
        
        ttk.Button(button_frame, text="複製結果", command=self.copy_result).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="清除結果", command=self.clear_result).pack(side=tk.LEFT)
        
        # 設定網格權重
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # 為了向後相容，設定threshold_var引用
        self.threshold_var = self.topside_threshold_var
        
        # 設定matplotlib中文字體
        self.setup_matplotlib_fonts()
    
    def setup_matplotlib_fonts(self):
        """設定matplotlib字體支援"""
        try:
            # 為了確保兼容性，暫時使用英文顯示
            # 未來可以根據需要啟用中文字體支援
            self.use_chinese = False
            
            # 如果用戶想要嘗試中文字體，可以取消註釋以下代碼
            """
            # 嘗試找到系統中的中文字體
            chinese_fonts = []
            
            # macOS 常見中文字體
            macos_fonts = ['PingFang SC', 'Arial Unicode MS', 'STHeiti']
            # Windows 常見中文字體
            windows_fonts = ['Microsoft YaHei', 'SimHei', 'SimSun']
            
            all_fonts = macos_fonts + windows_fonts
            available_fonts = [f.name for f in fm.fontManager.ttflist]
            
            for font in all_fonts:
                if font in available_fonts:
                    chinese_fonts.append(font)
            
            if chinese_fonts:
                plt.rcParams['font.sans-serif'] = [chinese_fonts[0]] + plt.rcParams['font.sans-serif']
                plt.rcParams['axes.unicode_minus'] = False
                self.use_chinese = True
                print(f"使用中文字體: {chinese_fonts[0]}")
            else:
                self.use_chinese = False
            """
            
            print("使用英文顯示圖表文字")
            print("如需啟用中文顯示，請調用 enable_chinese_fonts() 方法")
                
        except Exception as e:
            print(f"字體設定失敗，使用英文顯示: {e}")
            self.use_chinese = False
    
    def enable_chinese_fonts(self):
        """手動啟用中文字體支援（實驗性功能）"""
        try:
            # 嘗試找到系統中的中文字體
            chinese_fonts = []
            
            # macOS 常見中文字體（按優先級排序）
            macos_fonts = ['PingFang SC', 'Arial Unicode MS', 'STHeiti']
            # Windows 常見中文字體
            windows_fonts = ['Microsoft YaHei', 'SimHei', 'SimSun']
            
            all_fonts = macos_fonts + windows_fonts
            available_fonts = [f.name for f in fm.fontManager.ttflist]
            
            for font in all_fonts:
                if font in available_fonts:
                    chinese_fonts.append(font)
            
            if chinese_fonts:
                plt.rcParams['font.sans-serif'] = [chinese_fonts[0]] + plt.rcParams['font.sans-serif']
                plt.rcParams['axes.unicode_minus'] = False
                self.use_chinese = True
                print(f"✓ 已啟用中文字體: {chinese_fonts[0]}")
                messagebox.showinfo("字體設定", f"已啟用中文字體顯示：{chinese_fonts[0]}\\n重新生成圖表將使用中文標籤")
                return True
            else:
                self.use_chinese = False
                messagebox.showwarning("字體設定", "系統中未找到支援的中文字體\\n將繼續使用英文顯示")
                return False
                
        except Exception as e:
            print(f"中文字體啟用失敗: {e}")
            messagebox.showerror("字體設定", f"啟用中文字體失敗：{e}")
            self.use_chinese = False
            return False
    
    def get_chart_text(self, chinese_text, english_text):
        """根據字體支援情況返回對應的文字"""
        return chinese_text if self.use_chinese else english_text
    
    def select_file(self):
        """選擇Excel或CSV檔案"""
        file_path = filedialog.askopenfilename(
            title="選擇Excel或CSV檔案",
            filetypes=[
                ("支援的檔案", "*.xlsx *.xls *.csv"),
                ("Excel files", "*.xlsx *.xls"), 
                ("CSV files", "*.csv"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            if self.excel_processor.load_file(file_path):
                self.file_path_text.set(os.path.basename(file_path))
                self.update_sheet_list()
                self.show_file_info()
            else:
                messagebox.showerror("錯誤", "無法載入檔案")
    
    def update_sheet_list(self):
        """更新工作表選擇清單"""
        sheets = self.excel_processor.get_available_sheets()
        self.sheet_combobox['values'] = sheets
        if sheets:
            self.sheet_var.set(sheets[0])  # 預設選擇第一個工作表
    
    def on_sheet_selected(self, event):
        """當選擇工作表時的回調函數"""
        selected_sheet = self.sheet_var.get()
        if selected_sheet and self.excel_processor.file_path:
            # 重新載入選擇的工作表
            file_type = self.excel_processor.get_file_type()
            if file_type == 'excel':
                if self.excel_processor.load_file(self.excel_processor.file_path, selected_sheet):
                    self.show_file_info()
                    # 重新偵測資料開始行數
                    start_pandas_index = self.excel_processor.detect_data_start_row()
                    start_excel_row = start_pandas_index + 1
                    self.start_row_var.set(str(start_excel_row))
                    
                    # 重新偵測資料結束行數
                    end_pandas_index = self.excel_processor.detect_data_end_row(start_pandas_index)
                    end_excel_row = end_pandas_index
                    self.end_row_var.set(str(end_excel_row))
                else:
                    messagebox.showerror("錯誤", f"無法載入工作表: {selected_sheet}")
    
    def auto_detect_start_row(self):
        """自動偵測資料開始行數"""
        if self.excel_processor.data is None:
            messagebox.showwarning("警告", "請先選擇檔案")
            return
        
        pandas_row_index = self.excel_processor.detect_data_start_row()
        excel_row_number = pandas_row_index + 1  # 轉換為Excel行號顯示
        self.start_row_var.set(str(excel_row_number))
        messagebox.showinfo("資訊", f"偵測到資料開始行數: Excel第{excel_row_number}行")
    
    def auto_detect_end_row(self):
        """自動偵測資料結束行數"""
        if self.excel_processor.data is None:
            messagebox.showwarning("警告", "請先選擇檔案")
            return
        
        # 取得開始行數
        try:
            start_excel_row = int(self.start_row_var.get()) if self.start_row_var.get() else 1
            start_pandas_index = start_excel_row - 1
        except ValueError:
            start_pandas_index = 0
        
        end_pandas_index = self.excel_processor.detect_data_end_row(start_pandas_index)
        end_excel_row = end_pandas_index  # 結束行數已經是實際的行號
        self.end_row_var.set(str(end_excel_row))
        messagebox.showinfo("資訊", f"偵測到資料結束行數: Excel第{end_excel_row}行")
    
    def preview_end_data(self):
        """預覽結束數據"""
        if self.excel_processor.data is None:
            messagebox.showwarning("警告", "請先選擇檔案")
            return
        
        try:
            end_excel_row = int(self.end_row_var.get())
            end_pandas_index = end_excel_row  # 結束行數直接對應pandas索引
            
            # 取得預覽數據
            preview_info = self.excel_processor.get_end_preview_data(end_row=end_pandas_index)
            
            if not preview_info:
                messagebox.showerror("錯誤", "無法取得預覽數據")
                return
            
            # 建立預覽視窗
            self.show_end_preview_window(preview_info)
            
        except ValueError as e:
            messagebox.showerror("錯誤", f"參數輸入錯誤: {e}")
        except Exception as e:
            messagebox.showerror("錯誤", f"預覽數據時發生錯誤: {e}")
    
    def preview_data(self):
        """預覽選取的數據"""
        if self.excel_processor.data is None:
            messagebox.showwarning("警告", "請先選擇檔案")
            return
        
        try:
            excel_row_number = int(self.start_row_var.get())
            pandas_row_index = excel_row_number - 1  # 轉換為pandas索引
            
            # 取得預覽數據
            preview_info = self.excel_processor.get_preview_data(start_row=pandas_row_index)
            
            if not preview_info:
                messagebox.showerror("錯誤", "無法取得預覽數據")
                return
            
            # 建立預覽視窗
            self.show_preview_window(preview_info)
            
        except ValueError as e:
            messagebox.showerror("錯誤", f"參數輸入錯誤: {e}")
        except Exception as e:
            messagebox.showerror("錯誤", f"預覽數據時發生錯誤: {e}")
    
    def show_preview_window(self, preview_info: dict):
        """顯示數據預覽視窗"""
        preview_window = tk.Toplevel(self.root)
        preview_window.title("數據預覽")
        preview_window.geometry("1000x700")
        preview_window.transient(self.root)
        preview_window.grab_set()
        
        # 建立筆記本控件（分頁）
        notebook = ttk.Notebook(preview_window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 第一個分頁：原始數據預覽
        raw_frame = ttk.Frame(notebook)
        notebook.add(raw_frame, text="原始數據預覽")
        
        # 資訊標籤
        info_frame = ttk.Frame(raw_frame)
        info_frame.pack(fill=tk.X, padx=5, pady=5)
        
        info_text = f"""數據範圍: 第 {preview_info['start_row']} 行到第 {preview_info['end_row']} 行 (總共 {preview_info['total_rows']} 行)
矩陣形狀: {preview_info['matrix_shape']}
中間列索引: {preview_info['middle_column_index']}"""
        
        if preview_info['truncated_cols']:
            info_text += f"\n注意: 只顯示前10列，實際共有 {preview_info['actual_cols']} 列"
        
        ttk.Label(info_frame, text=info_text, font=('Arial', 10)).pack(anchor=tk.W)
        
        # 數據表格
        tree_frame = ttk.Frame(raw_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 建立Treeview
        columns = list(preview_info['preview_dataframe'].columns)
        tree = ttk.Treeview(tree_frame, columns=columns, show='tree headings')
        
        # 設定列標題
        tree.heading('#0', text='行號')
        tree.column('#0', width=60, minwidth=60)
        
        for col in columns:
            tree.heading(col, text=str(col))
            tree.column(col, width=100, minwidth=80)
        
        # 插入數據
        df = preview_info['preview_dataframe']
        for idx, row in df.iterrows():
            values = [str(val) if not pd.isna(val) else '' for val in row.values]
            tree.insert('', 'end', text=str(idx + 1), values=values)  # 顯示Excel行號
        
        # 滾動條
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=tree.xview)
        tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # 第二個分頁：中間列數據
        middle_frame = ttk.Frame(notebook)
        notebook.add(middle_frame, text="中間列數據 (用於計算)")
        
        # 中間列資訊
        middle_info_frame = ttk.Frame(middle_frame)
        middle_info_frame.pack(fill=tk.X, padx=5, pady=5)
        
        if preview_info['middle_column_data'] is not None:
            middle_info_text = f"""中間列索引: {preview_info['middle_column_index']}
數據點數: {len(preview_info['middle_column_data'])}
這些數據將用於Blue Edge Index計算"""
            
            ttk.Label(middle_info_frame, text=middle_info_text, font=('Arial', 10)).pack(anchor=tk.W)
            
            # 中間列數據表格
            middle_tree_frame = ttk.Frame(middle_frame)
            middle_tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            middle_tree = ttk.Treeview(middle_tree_frame, columns=['value'], show='tree headings')
            middle_tree.heading('#0', text='行號')
            middle_tree.heading('value', text='數值')
            middle_tree.column('#0', width=100, minwidth=100)
            middle_tree.column('value', width=150, minwidth=150)
            
            # 插入中間列數據
            for i, val in enumerate(preview_info['middle_column_data']):
                display_val = str(val) if not pd.isna(val) else 'NaN'
                middle_tree.insert('', 'end', text=str(preview_info['start_row'] + i + 1), values=[display_val])  # 顯示Excel行號
            
            # 中間列滾動條
            middle_v_scrollbar = ttk.Scrollbar(middle_tree_frame, orient=tk.VERTICAL, command=middle_tree.yview)
            middle_tree.configure(yscrollcommand=middle_v_scrollbar.set)
            
            middle_tree.grid(row=0, column=0, sticky='nsew')
            middle_v_scrollbar.grid(row=0, column=1, sticky='ns')
            
            middle_tree_frame.grid_rowconfigure(0, weight=1)
            middle_tree_frame.grid_columnconfigure(0, weight=1)
        else:
            ttk.Label(middle_info_frame, text="無法取得中間列數據", font=('Arial', 10)).pack(anchor=tk.W)
        
        # 關閉按鈕
        button_frame = ttk.Frame(preview_window)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(button_frame, text="關閉", command=preview_window.destroy).pack(side=tk.RIGHT)
    
    def show_end_preview_window(self, preview_info: dict):
        """顯示結束數據預覽視窗"""
        preview_window = tk.Toplevel(self.root)
        preview_window.title("結束數據預覽")
        preview_window.geometry("1000x700")
        preview_window.transient(self.root)
        preview_window.grab_set()
        
        # 建立筆記本控件（分頁）
        notebook = ttk.Notebook(preview_window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 第一個分頁：原始數據預覽
        raw_frame = ttk.Frame(notebook)
        notebook.add(raw_frame, text="原始數據預覽")
        
        # 資訊標籤
        info_frame = ttk.Frame(raw_frame)
        info_frame.pack(fill=tk.X, padx=5, pady=5)
        
        info_text = f"""結束數據預覽 (最後10行)
數據範圍: Excel第{preview_info['preview_start_row'] + 1}行到第{preview_info['preview_end_row']}行
結束行數: Excel第{preview_info['end_row']}行
矩陣形狀: {preview_info['matrix_shape']}
中間列索引: {preview_info['middle_column_index']}"""
        
        if preview_info['truncated_cols']:
            info_text += f"\n注意: 只顯示前10列，實際共有 {preview_info['actual_cols']} 列"
        
        ttk.Label(info_frame, text=info_text, font=('Arial', 10)).pack(anchor=tk.W)
        
        # 數據表格
        tree_frame = ttk.Frame(raw_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 建立Treeview
        columns = list(preview_info['preview_dataframe'].columns)
        tree = ttk.Treeview(tree_frame, columns=columns, show='tree headings')
        
        # 設定列標題
        tree.heading('#0', text='Excel行號')
        tree.column('#0', width=60, minwidth=60)
        
        for col in columns:
            tree.heading(col, text=str(col))
            tree.column(col, width=100, minwidth=80)
        
        # 插入數據
        df = preview_info['preview_dataframe']
        for idx, row in df.iterrows():
            values = [str(val) if not pd.isna(val) else '' for val in row.values]
            tree.insert('', 'end', text=str(idx + 1), values=values)  # 顯示Excel行號
        
        # 滾動條
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=tree.xview)
        tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # 第二個分頁：中間列數據
        middle_frame = ttk.Frame(notebook)
        notebook.add(middle_frame, text="中間列數據 (用於計算)")
        
        # 中間列資訊
        middle_info_frame = ttk.Frame(middle_frame)
        middle_info_frame.pack(fill=tk.X, padx=5, pady=5)
        
        if preview_info['middle_column_data'] is not None:
            middle_info_text = f"""中間列索引: {preview_info['middle_column_index']}
數據點數: {len(preview_info['middle_column_data'])}
這些數據將用於Blue Edge Index計算"""
            
            ttk.Label(middle_info_frame, text=middle_info_text, font=('Arial', 10)).pack(anchor=tk.W)
            
            # 中間列數據表格
            middle_tree_frame = ttk.Frame(middle_frame)
            middle_tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            middle_tree = ttk.Treeview(middle_tree_frame, columns=['value'], show='tree headings')
            middle_tree.heading('#0', text='Excel行號')
            middle_tree.heading('value', text='數值')
            middle_tree.column('#0', width=100, minwidth=100)
            middle_tree.column('value', width=150, minwidth=150)
            
            # 插入中間列數據
            for i, val in enumerate(preview_info['middle_column_data']):
                display_val = str(val) if not pd.isna(val) else 'NaN'
                middle_tree.insert('', 'end', text=str(preview_info['preview_start_row'] + i + 1), values=[display_val])  # 顯示Excel行號
            
            # 中間列滾動條
            middle_v_scrollbar = ttk.Scrollbar(middle_tree_frame, orient=tk.VERTICAL, command=middle_tree.yview)
            middle_tree.configure(yscrollcommand=middle_v_scrollbar.set)
            
            middle_tree.grid(row=0, column=0, sticky='nsew')
            middle_v_scrollbar.grid(row=0, column=1, sticky='ns')
            
            middle_tree_frame.grid_rowconfigure(0, weight=1)
            middle_tree_frame.grid_columnconfigure(0, weight=1)
        else:
            ttk.Label(middle_info_frame, text="無法取得中間列數據", font=('Arial', 10)).pack(anchor=tk.W)
        
        # 關閉按鈕
        button_frame = ttk.Frame(preview_window)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(button_frame, text="關閉", command=preview_window.destroy).pack(side=tk.RIGHT)
    
    def show_file_info(self):
        """顯示檔案資訊"""
        info = self.excel_processor.get_data_info()
        file_type_text = "Excel檔案" if info.get('file_type') == 'excel' else "CSV檔案"
        sheets_info = f"- 可用工作表: {', '.join(info.get('available_sheets', []))}\n" if info.get('available_sheets') else ""
        
        info_text = f"""
檔案資訊:
- 檔案路徑: {info.get('file_path', 'N/A')}
- 檔案類型: {file_type_text}
{sheets_info}- 資料形狀: {info.get('shape', 'N/A')}
- 欄位數量: {len(info.get('columns', []))}
- 是否有空值: {'是' if info.get('has_null', False) else '否'}
"""
        self.result_text_widget.delete(1.0, tk.END)
        self.result_text_widget.insert(tk.END, info_text)
    
    def calculate_blue_edge(self):
        """計算Blue Edge Index"""
        if self.excel_processor.data is None:
            messagebox.showwarning("警告", "請先選擇檔案")
            return
        
        try:
            # 取得參數
            start_excel_row = int(self.start_row_var.get())
            start_pandas_index = start_excel_row - 1  # 轉換為pandas索引
            
            # 取得結束行數
            end_pandas_index = None
            if self.end_row_var.get().strip():
                end_excel_row = int(self.end_row_var.get())
                end_pandas_index = end_excel_row  # 結束行數直接對應pandas索引
            
            topside_threshold_percent = float(self.topside_threshold_var.get()) / 100.0
            bottomside_threshold_percent = float(self.bottomside_threshold_var.get()) / 100.0
            ng_threshold = float(self.ng_threshold_var.get())
            
            # 設定計算器參數
            self.calculator.set_topside_threshold_percentage(topside_threshold_percent)
            self.calculator.set_bottomside_threshold_percentage(bottomside_threshold_percent)
            self.calculator.set_ng_threshold(ng_threshold)
            
            # 取得矩陣資料
            matrix_data = self.excel_processor.get_matrix_data(start_row=start_pandas_index, end_row=end_pandas_index)
            
            if matrix_data.size == 0:
                messagebox.showerror("錯誤", "無法取得有效資料")
                return
            
            # 取得中間列資料
            middle_column_data = self.excel_processor.get_middle_column_data(matrix_data)
            
            # 計算TopSide Blue Edge Index
            topside_result, topside_judgment = self.calculator.calculate_blue_edge_index(middle_column_data)
            topside_details = self.calculator.get_calculation_details(middle_column_data)
            
            # 計算BottomSide Blue Edge Index
            bottomside_result, bottomside_judgment = self.calculator.calculate_bottomside_blue_edge_index(middle_column_data)
            bottomside_details = self.calculator.get_bottomside_calculation_details(middle_column_data)
            
            # 顯示結果
            topside_threshold_percent = int(float(self.topside_threshold_var.get()))
            bottomside_threshold_percent = int(float(self.bottomside_threshold_var.get()))
            
            # 隱藏詳細計算過程 - 使用者不需要這些資訊
            topside_calculation_details_text = ""
            bottomside_calculation_details_text = ""
            
            result_text = f"""
=== Blue Edge Index 計算結果 ===

【TopSide 結果】
最大值: {topside_result:.4f}
最大值位置: 第{topside_details.get('max_position', 'N/A')}個數據
判斷結果: {topside_judgment}

【BottomSide 結果】
最大值: {bottomside_result:.4f}
最大值位置: 倒數第{bottomside_details.get('max_position', 'N/A')}個數據
判斷結果: {bottomside_judgment}

=== 計算參數 ===
總資料點數: {topside_details.get('total_data_points', 'N/A')}
TopSide {topside_threshold_percent}%資料點數: {topside_details.get('threshold_points', 'N/A')}
TopSide 基準值 (第{topside_details.get('baseline_position', 'N/A')}個): {topside_details.get('baseline_value', 'N/A'):.4f}
BottomSide {bottomside_threshold_percent}%資料點數: {bottomside_details.get('threshold_points', 'N/A')}
BottomSide 基準值 (倒數第{bottomside_details.get('baseline_position', 'N/A')}個): {bottomside_details.get('baseline_value', 'N/A'):.4f}
NG判斷閾值: {ng_threshold}
資料範圍: {topside_details.get('data_range', 'N/A')}

=== 矩陣資訊 ===
矩陣形狀: {matrix_data.shape}
中間列索引: {matrix_data.shape[1] // 2}
使用的開始行數: Excel第{start_excel_row}行
使用的結束行數: {f'Excel第{end_excel_row}行' if end_pandas_index is not None else '到檔案結尾'}
{topside_calculation_details_text}
=== TopSide 所有計算結果 ===
"""
            
            # 添加TopSide所有計算值 - 反向顯示順序
            if 'calculated_values' in topside_details and topside_details['calculated_values']:
                calculated_values = topside_details['calculated_values']
                max_position = topside_details.get('max_position', 0)
                
                # 反向顯示：從最後一個到第一個
                for i in range(len(calculated_values) - 1, -1, -1):
                    value = calculated_values[i]
                    original_position = i + 1  # 原始位置（從1開始）
                    display_position = len(calculated_values) - i  # 顯示位置（反向）
                    is_max = original_position == max_position
                    result_text += f"第{display_position:2d}個結果: {value:10.4f}{'  ← 最大值' if is_max else ''}\n"
            
            result_text += f"{bottomside_calculation_details_text}\n=== BottomSide 所有計算結果 ===\n"
            
            # 添加BottomSide所有計算值
            if 'calculated_values' in bottomside_details and bottomside_details['calculated_values']:
                for i, value in enumerate(bottomside_details['calculated_values']):
                    result_text += f"倒數第{i+1:2d}個結果: {value:10.4f}{'  ← 最大值' if i+1 == bottomside_details.get('max_position', 0) else ''}\n"
            
            self.result_text_widget.delete(1.0, tk.END)
            self.result_text_widget.insert(tk.END, result_text)
            
            # 顯示結果對話框
            messagebox.showinfo("計算完成", f"TopSide 最大值: {topside_result:.4f} ({topside_judgment})\nBottomSide 最大值: {bottomside_result:.4f} ({bottomside_judgment})")
            
        except ValueError as e:
            messagebox.showerror("錯誤", f"參數輸入錯誤: {e}")
        except Exception as e:
            messagebox.showerror("錯誤", f"計算過程發生錯誤: {e}")
    
    def show_middle_column_chart(self):
        """顯示中間列數據曲線圖"""
        if self.excel_processor.data is None:
            messagebox.showwarning("警告", "請先選擇檔案")
            return
        
        try:
            # 取得參數
            start_excel_row = int(self.start_row_var.get())
            start_pandas_index = start_excel_row - 1
            
            # 取得結束行數
            end_pandas_index = None
            if self.end_row_var.get().strip():
                end_excel_row = int(self.end_row_var.get())
                end_pandas_index = end_excel_row
            
            # 取得矩陣資料
            matrix_data = self.excel_processor.get_matrix_data(start_row=start_pandas_index, end_row=end_pandas_index)
            
            if matrix_data.size == 0:
                messagebox.showerror("錯誤", "無法取得有效資料")
                return
            
            # 取得中間列資料
            middle_column_data = self.excel_processor.get_middle_column_data(matrix_data)
            
            # 建立曲線圖視窗
            self.show_chart_window(middle_column_data, start_excel_row, end_pandas_index)
            
        except ValueError as e:
            messagebox.showerror("錯誤", f"參數輸入錯誤: {e}")
        except Exception as e:
            messagebox.showerror("錯誤", f"顯示曲線圖時發生錯誤: {e}")
    
    def show_chart_window(self, middle_column_data, start_excel_row, end_pandas_index):
        """顯示曲線圖視窗"""
        chart_window = tk.Toplevel(self.root)
        chart_window.title("中間列數據曲線圖")
        chart_window.geometry("1200x800")
        chart_window.transient(self.root)
        chart_window.grab_set()
        
        # 計算中間列索引（避免重複計算）
        start_pandas_index = start_excel_row - 1
        matrix_data = self.excel_processor.get_matrix_data(start_pandas_index, end_pandas_index)
        middle_col_index = matrix_data.shape[1] // 2 if matrix_data.size > 0 else 0
        
        # 建立筆記本控件（分頁）
        notebook = ttk.Notebook(chart_window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 第一個分頁：完整曲線圖
        full_chart_frame = ttk.Frame(notebook)
        notebook.add(full_chart_frame, text="完整數據曲線")
        
        # 建立matplotlib圖形
        fig1 = Figure(figsize=(12, 6), dpi=100)
        ax1 = fig1.add_subplot(111)
        
        # 準備數據 - 重新定義X軸從1開始
        x_values = list(range(1, len(middle_column_data) + 1))  # 從1開始的連續數值
        y_values = middle_column_data
        excel_row_mapping = list(range(start_excel_row, start_excel_row + len(middle_column_data)))  # 保存Excel行號對應
        
        # 繪製曲線
        ax1.plot(x_values, y_values, 'b-', linewidth=1.5, marker='o', markersize=2)
        ax1.set_xlabel(self.get_chart_text('數據序號', 'Data Index'))
        ax1.set_ylabel(self.get_chart_text('數值', 'Value'))
        
        title_zh = f'中間列數據趨勢圖 (共{len(middle_column_data)}個數據點, Excel第{start_excel_row}行到第{start_excel_row + len(middle_column_data) - 1}行)'
        title_en = f'Middle Column Data Trend ({len(middle_column_data)} data points, Excel Row {start_excel_row} to {start_excel_row + len(middle_column_data) - 1})'
        ax1.set_title(self.get_chart_text(title_zh, title_en))
        ax1.grid(True, alpha=0.3)
        
        # 添加統計信息
        mean_val = float(middle_column_data.mean())
        max_val = float(middle_column_data.max())
        min_val = float(middle_column_data.min())
        
        mean_label = self.get_chart_text(f'平均值: {mean_val:.2f}', f'Mean: {mean_val:.2f}')
        max_label = self.get_chart_text(f'最大值: {max_val:.2f}', f'Max: {max_val:.2f}')
        min_label = self.get_chart_text(f'最小值: {min_val:.2f}', f'Min: {min_val:.2f}')
        
        ax1.axhline(y=mean_val, color='r', linestyle='--', alpha=0.7, label=mean_label)
        ax1.axhline(y=max_val, color='g', linestyle='--', alpha=0.7, label=max_label)
        ax1.axhline(y=min_val, color='orange', linestyle='--', alpha=0.7, label=min_label)
        
        # 取得閾值設定
        topside_threshold = float(self.topside_threshold_var.get()) / 100.0
        bottomside_threshold = float(self.bottomside_threshold_var.get()) / 100.0
        
        # 計算閾值位置
        total_points = len(middle_column_data)
        topside_points = int(total_points * topside_threshold)
        bottomside_points = int(total_points * bottomside_threshold)
        
        if topside_points == 0:
            topside_points = 1
        if bottomside_points == 0:
            bottomside_points = 1
        
        # 添加閾值分界線
        topside_position = topside_points + 0.5  # 在閾值後面畫線
        bottomside_position = total_points - bottomside_points + 0.5  # 在閾值前面畫線
        
        topside_label = self.get_chart_text(f'TopSide {int(topside_threshold*100)}%界線', f'TopSide {int(topside_threshold*100)}% Line')
        bottomside_label = self.get_chart_text(f'BottomSide {int(bottomside_threshold*100)}%界線', f'BottomSide {int(bottomside_threshold*100)}% Line')
        
        ax1.axvline(x=topside_position, color='gray', linestyle='--', alpha=0.8, linewidth=1, label=topside_label)
        ax1.axvline(x=bottomside_position, color='gray', linestyle='--', alpha=0.8, linewidth=1, label=bottomside_label)
        
        ax1.legend()
        
        # 新增互動功能：滑鼠懸停顯示座標
        self.add_hover_functionality(fig1, ax1, x_values, y_values, excel_row_mapping)
        
        fig1.tight_layout()
        
        # 嵌入tkinter
        canvas1 = FigureCanvasTkAgg(fig1, full_chart_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # 第二個分頁：TopSide和BottomSide數據對比
        comparison_frame = ttk.Frame(notebook)
        notebook.add(comparison_frame, text="TopSide vs BottomSide")
        
        # 建立對比圖形
        fig2 = Figure(figsize=(12, 8), dpi=100)
        
        # 取得閾值（重複使用之前計算的值）
        topside_threshold = float(self.topside_threshold_var.get()) / 100.0
        bottomside_threshold = float(self.bottomside_threshold_var.get()) / 100.0
        
        # 計算TopSide和BottomSide數據範圍（重複使用之前計算的值）
        total_points = len(middle_column_data)
        topside_points = int(total_points * topside_threshold)
        bottomside_points = int(total_points * bottomside_threshold)
        
        if topside_points == 0:
            topside_points = 1
        if bottomside_points == 0:
            bottomside_points = 1
        
        # TopSide數據 - 使用重新定義的X軸
        topside_data = middle_column_data[:topside_points]
        topside_x = x_values[:topside_points]  # 從1開始
        topside_excel_mapping = excel_row_mapping[:topside_points]
        
        # BottomSide數據 - 使用重新定義的X軸
        bottomside_data = middle_column_data[-bottomside_points:]
        bottomside_x = list(range(len(middle_column_data) - bottomside_points + 1, len(middle_column_data) + 1))  # 保持連續性
        bottomside_excel_mapping = excel_row_mapping[-bottomside_points:]
        
        # 上半部分：TopSide
        ax2_top = fig2.add_subplot(211)
        topside_label = self.get_chart_text('TopSide數據', 'TopSide Data')
        ax2_top.plot(topside_x, topside_data, 'b-', linewidth=2, marker='o', markersize=3, label=topside_label)
        ax2_top.set_xlabel(self.get_chart_text('數據序號', 'Data Index'))
        ax2_top.set_ylabel(self.get_chart_text('數值', 'Value'))
        
        topside_title_zh = f'TopSide 數據 (前{int(topside_threshold*100)}%，共{topside_points}個數據點)'
        topside_title_en = f'TopSide Data (Top {int(topside_threshold*100)}%, {topside_points} data points)'
        ax2_top.set_title(self.get_chart_text(topside_title_zh, topside_title_en))
        ax2_top.grid(True, alpha=0.3)
        
        # 在TopSide圖中添加閾值線
        topside_position = topside_points + 0.5
        topside_line_label = self.get_chart_text(f'TopSide {int(topside_threshold*100)}%界線', f'TopSide {int(topside_threshold*100)}% Line')
        ax2_top.axvline(x=topside_position, color='gray', linestyle='--', alpha=0.8, linewidth=1, label=topside_line_label)
        
        ax2_top.legend()
        
        # 為TopSide添加互動功能
        self.add_hover_functionality(fig2, ax2_top, topside_x, topside_data, topside_excel_mapping)
        
        # 下半部分：BottomSide
        ax2_bottom = fig2.add_subplot(212)
        bottomside_label = self.get_chart_text('BottomSide數據', 'BottomSide Data')
        ax2_bottom.plot(bottomside_x, bottomside_data, 'r-', linewidth=2, marker='s', markersize=3, label=bottomside_label)
        ax2_bottom.set_xlabel(self.get_chart_text('數據序號', 'Data Index'))
        ax2_bottom.set_ylabel(self.get_chart_text('數值', 'Value'))
        
        bottomside_title_zh = f'BottomSide 數據 (後{int(bottomside_threshold*100)}%，共{bottomside_points}個數據點)'
        bottomside_title_en = f'BottomSide Data (Bottom {int(bottomside_threshold*100)}%, {bottomside_points} data points)'
        ax2_bottom.set_title(self.get_chart_text(bottomside_title_zh, bottomside_title_en))
        ax2_bottom.grid(True, alpha=0.3)
        
        # 在BottomSide圖中添加閾值線
        bottomside_position = len(middle_column_data) - bottomside_points + 0.5
        bottomside_line_label = self.get_chart_text(f'BottomSide {int(bottomside_threshold*100)}%界線', f'BottomSide {int(bottomside_threshold*100)}% Line')
        ax2_bottom.axvline(x=bottomside_position, color='gray', linestyle='--', alpha=0.8, linewidth=1, label=bottomside_line_label)
        
        ax2_bottom.legend()
        
        # 為BottomSide添加互動功能
        self.add_hover_functionality(fig2, ax2_bottom, bottomside_x, bottomside_data, bottomside_excel_mapping)
        
        fig2.tight_layout()
        
        # 嵌入tkinter
        canvas2 = FigureCanvasTkAgg(fig2, comparison_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # 第三個分頁：統計資訊
        stats_frame = ttk.Frame(notebook)
        notebook.add(stats_frame, text="統計資訊")
        
        # 統計資訊文字
        stats_text = tk.Text(stats_frame, font=('Courier', 10))
        stats_scrollbar = ttk.Scrollbar(stats_frame, orient=tk.VERTICAL, command=stats_text.yview)
        stats_text.configure(yscrollcommand=stats_scrollbar.set)
        
        # 計算統計資訊
        if self.use_chinese:
            stats_info = f"""
=== 中間列數據統計資訊 ===

數據範圍: 數據1到數據{len(middle_column_data)} (對應Excel第{start_excel_row}行到第{start_excel_row + len(middle_column_data) - 1}行)
總數據點數: {len(middle_column_data)}
數據列索引: {middle_col_index}

=== 基本統計 ===
平均值: {mean_val:.4f}
最大值: {max_val:.4f}
最小值: {min_val:.4f}
標準差: {float(middle_column_data.std()):.4f}
變異數: {float(middle_column_data.var()):.4f}

=== TopSide 統計 (前{int(topside_threshold*100)}%) ===
數據點數: {topside_points}
平均值: {float(topside_data.mean()):.4f}
最大值: {float(topside_data.max()):.4f}
最小值: {float(topside_data.min()):.4f}

=== BottomSide 統計 (後{int(bottomside_threshold*100)}%) ===
數據點數: {bottomside_points}
平均值: {float(bottomside_data.mean()):.4f}
最大值: {float(bottomside_data.max()):.4f}
最小值: {float(bottomside_data.min()):.4f}

=== 趨勢分析 ===
整體趨勢: {'上升' if y_values[-1] > y_values[0] else '下降' if y_values[-1] < y_values[0] else '平穩'}
TopSide vs BottomSide 平均值比較: {float(topside_data.mean()) / float(bottomside_data.mean()):.4f}
"""
        else:
            trend = 'Rising' if y_values[-1] > y_values[0] else 'Falling' if y_values[-1] < y_values[0] else 'Stable'
            stats_info = f"""
=== Middle Column Data Statistics ===

Data Range: Data 1 to Data {len(middle_column_data)} (Excel Row {start_excel_row} to {start_excel_row + len(middle_column_data) - 1})
Total Data Points: {len(middle_column_data)}
Data Column Index: {middle_col_index}

=== Basic Statistics ===
Mean: {mean_val:.4f}
Maximum: {max_val:.4f}
Minimum: {min_val:.4f}
Standard Deviation: {float(middle_column_data.std()):.4f}
Variance: {float(middle_column_data.var()):.4f}

=== TopSide Statistics (Top {int(topside_threshold*100)}%) ===
Data Points: {topside_points}
Mean: {float(topside_data.mean()):.4f}
Maximum: {float(topside_data.max()):.4f}
Minimum: {float(topside_data.min()):.4f}

=== BottomSide Statistics (Bottom {int(bottomside_threshold*100)}%) ===
Data Points: {bottomside_points}
Mean: {float(bottomside_data.mean()):.4f}
Maximum: {float(bottomside_data.max()):.4f}
Minimum: {float(bottomside_data.min()):.4f}

=== Trend Analysis ===
Overall Trend: {trend}
TopSide vs BottomSide Mean Ratio: {float(topside_data.mean()) / float(bottomside_data.mean()):.4f}
"""
        
        stats_text.insert(tk.END, stats_info)
        stats_text.config(state=tk.DISABLED)
        
        stats_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        stats_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 關閉按鈕
        button_frame = ttk.Frame(chart_window)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(button_frame, text="關閉", command=chart_window.destroy).pack(side=tk.RIGHT)
    
    def add_hover_functionality(self, fig, ax, x_values, y_values, excel_row_mapping):
        """為圖表添加滑鼠懸停顯示座標功能"""
        # 創建文字標註
        annotation = ax.annotate('', xy=(0, 0), xytext=(20, 20), 
                               textcoords="offset points",
                               bbox=dict(boxstyle="round", fc="w", alpha=0.9, edgecolor="gray"),
                               arrowprops=dict(arrowstyle="->", color="gray"))
        annotation.set_visible(False)
        
        def on_hover(event):
            if event.inaxes == ax:
                # 找到最接近滑鼠位置的數據點
                if len(x_values) > 0 and len(y_values) > 0:
                    # 計算距離最近的點
                    distances = [(abs(x - event.xdata), abs(y - event.ydata), i) 
                               for i, (x, y) in enumerate(zip(x_values, y_values))]
                    distances.sort(key=lambda x: x[0]**2 + x[1]**2)
                    
                    if distances and len(distances) > 0:
                        closest_idx = distances[0][2]
                        x_val = x_values[closest_idx]
                        y_val = y_values[closest_idx]
                        excel_row = excel_row_mapping[closest_idx]
                        
                        # 設定顯示文字
                        if self.use_chinese:
                            text = f'數據序號: {x_val}\n數值: {y_val:.4f}\nX軸座標: {x_val}\n(Excel行號: {excel_row})'
                        else:
                            text = f'Data Index: {x_val}\nValue: {y_val:.4f}\nX-axis: {x_val}\n(Excel Row: {excel_row})'
                        
                        # 智能定位：根據數據點位置調整資訊框位置
                        x_range = ax.get_xlim()
                        y_range = ax.get_ylim()
                        
                        # 計算數據點在圖表中的相對位置
                        x_ratio = (x_val - x_range[0]) / (x_range[1] - x_range[0])
                        y_ratio = (y_val - y_range[0]) / (y_range[1] - y_range[0])
                        
                        # 智能選擇資訊框位置
                        if x_ratio > 0.7:  # 右側
                            if y_ratio > 0.7:  # 右上角
                                offset_x, offset_y = -120, -80
                            elif y_ratio < 0.3:  # 右下角
                                offset_x, offset_y = -120, 30
                            else:  # 右側中間
                                offset_x, offset_y = -120, -20
                        elif x_ratio < 0.3:  # 左側
                            if y_ratio > 0.7:  # 左上角
                                offset_x, offset_y = 20, -80
                            elif y_ratio < 0.3:  # 左下角
                                offset_x, offset_y = 20, 30
                            else:  # 左側中間
                                offset_x, offset_y = 20, -20
                        else:  # 中間
                            if y_ratio > 0.7:  # 上方
                                offset_x, offset_y = 20, -80
                            elif y_ratio < 0.3:  # 下方
                                offset_x, offset_y = 20, 30
                            else:  # 中央
                                offset_x, offset_y = 20, 20
                        
                        # 更新標註位置和文字
                        annotation.xy = (x_val, y_val)
                        annotation.xytext = (offset_x, offset_y)
                        annotation.set_text(text)
                        annotation.set_visible(True)
                        fig.canvas.draw_idle()
            else:
                annotation.set_visible(False)
                fig.canvas.draw_idle()
        
        def on_leave(event):
            annotation.set_visible(False)
            fig.canvas.draw_idle()
        
        # 綁定事件
        fig.canvas.mpl_connect('motion_notify_event', on_hover)
        fig.canvas.mpl_connect('axes_leave_event', on_leave)
    
    def copy_result(self):
        """複製結果到剪貼簿"""
        result_content = self.result_text_widget.get(1.0, tk.END).strip()
        if result_content:
            self.root.clipboard_clear()
            self.root.clipboard_append(result_content)
            messagebox.showinfo("成功", "結果已複製到剪貼簿")
        else:
            messagebox.showwarning("警告", "沒有結果可複製")
    
    def clear_result(self):
        """清除結果"""
        self.result_text_widget.delete(1.0, tk.END)


def run_application():
    """執行應用程式"""
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    run_application()
