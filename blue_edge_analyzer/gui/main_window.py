"""
主視窗GUI模組
使用tkinter建立使用者介面
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from typing import Optional

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
        ttk.Button(file_frame, text="選擇Excel檔案", command=self.select_file).grid(row=0, column=1)
        
        file_frame.columnconfigure(0, weight=1)
        
        # 參數設定區域
        param_frame = ttk.LabelFrame(main_frame, text="參數設定", padding="5")
        param_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 資料開始行數
        ttk.Label(param_frame, text="資料開始行數:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.start_row_var = tk.StringVar(value="0")
        start_row_spinbox = ttk.Spinbox(param_frame, from_=0, to=1000, textvariable=self.start_row_var, width=10)
        start_row_spinbox.grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        
        # 自動偵測按鈕
        ttk.Button(param_frame, text="自動偵測", command=self.auto_detect_start_row).grid(row=0, column=2)
        
        # 閾值設定
        ttk.Label(param_frame, text="前N%閾值:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(5, 0))
        self.threshold_var = tk.StringVar(value="10")
        threshold_spinbox = ttk.Spinbox(param_frame, from_=1, to=50, textvariable=self.threshold_var, width=10)
        threshold_spinbox.grid(row=1, column=1, sticky=tk.W, padx=(0, 20), pady=(5, 0))
        ttk.Label(param_frame, text="%").grid(row=1, column=2, sticky=tk.W, pady=(5, 0))
        
        # 計算按鈕
        calc_frame = ttk.Frame(main_frame)
        calc_frame.grid(row=2, column=0, columnspan=2, pady=(0, 10))
        
        calc_button = ttk.Button(calc_frame, text="開始計算 Blue Edge Index", 
                               command=self.calculate_blue_edge, 
                               style="Accent.TButton")
        calc_button.pack()
        
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
    
    def select_file(self):
        """選擇Excel檔案"""
        file_path = filedialog.askopenfilename(
            title="選擇Excel檔案",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        
        if file_path:
            if self.excel_processor.load_excel(file_path):
                self.file_path_text.set(os.path.basename(file_path))
                self.show_file_info()
            else:
                messagebox.showerror("錯誤", "無法載入Excel檔案")
    
    def auto_detect_start_row(self):
        """自動偵測資料開始行數"""
        if self.excel_processor.data is None:
            messagebox.showwarning("警告", "請先選擇Excel檔案")
            return
        
        start_row = self.excel_processor.detect_data_start_row()
        self.start_row_var.set(str(start_row))
        messagebox.showinfo("資訊", f"偵測到資料開始行數: {start_row}")
    
    def show_file_info(self):
        """顯示檔案資訊"""
        info = self.excel_processor.get_data_info()
        info_text = f"""
檔案資訊:
- 檔案路徑: {info.get('file_path', 'N/A')}
- 資料形狀: {info.get('shape', 'N/A')}
- 欄位數量: {len(info.get('columns', []))}
- 是否有空值: {'是' if info.get('has_null', False) else '否'}
"""
        self.result_text_widget.delete(1.0, tk.END)
        self.result_text_widget.insert(tk.END, info_text)
    
    def calculate_blue_edge(self):
        """計算Blue Edge Index"""
        if self.excel_processor.data is None:
            messagebox.showwarning("警告", "請先選擇Excel檔案")
            return
        
        try:
            # 取得參數
            start_row = int(self.start_row_var.get())
            threshold_percent = float(self.threshold_var.get()) / 100.0
            
            # 設定計算器參數
            self.calculator.set_threshold_percentage(threshold_percent)
            
            # 取得矩陣資料
            matrix_data = self.excel_processor.get_matrix_data(start_row=start_row)
            
            if matrix_data.size == 0:
                messagebox.showerror("錯誤", "無法取得有效資料")
                return
            
            # 取得中間列資料
            middle_column_data = self.excel_processor.get_middle_column_data(matrix_data)
            
            # 計算Blue Edge Index
            result, judgment = self.calculator.calculate_blue_edge_index(middle_column_data)
            
            # 取得詳細資訊
            details = self.calculator.get_calculation_details(middle_column_data)
            
            # 顯示結果
            result_text = f"""
=== Blue Edge Index 計算結果 ===

計算結果: {result:.6f}
判斷結果: {judgment}

=== 詳細資訊 ===
總資料點數: {details.get('total_data_points', 'N/A')}
前{self.threshold_var.get()}%資料點數: {details.get('top_10_percent_points', 'N/A')}
前{self.threshold_var.get()}%平均值: {details.get('top_10_percent_avg', 'N/A'):.6f}
整體平均值: {details.get('overall_avg', 'N/A'):.6f}
資料範圍: {details.get('data_range', 'N/A')}

=== 矩陣資訊 ===
矩陣形狀: {matrix_data.shape}
中間列索引: {matrix_data.shape[1] // 2}
使用的開始行數: {start_row}
"""
            
            self.result_text_widget.delete(1.0, tk.END)
            self.result_text_widget.insert(tk.END, result_text)
            
            # 顯示結果對話框
            messagebox.showinfo("計算完成", f"Blue Edge Index: {result:.6f}\n判斷結果: {judgment}")
            
        except ValueError as e:
            messagebox.showerror("錯誤", f"參數輸入錯誤: {e}")
        except Exception as e:
            messagebox.showerror("錯誤", f"計算過程發生錯誤: {e}")
    
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
