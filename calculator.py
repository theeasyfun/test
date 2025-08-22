import tkinter as tk
from tkinter import ttk, messagebox
import math

class Shape:
    """形状基类"""
    def __init__(self, unit):
        self.unit = unit  # 单位：'cm' 或 'inch'
    
    def calculate_area(self):
        """计算面积（需要在子类中实现）"""
        raise NotImplementedError("子类必须实现calculate_area方法")
    
    def get_inputs(self):
        """获取输入参数（需要在子类中实现）"""
        raise NotImplementedError("子类必须实现get_inputs方法")
    
    def convert_to_cm(self, value):
        """将输入值转换为厘米"""
        if self.unit == 'inch':
            return value * 2.54  # 1英寸 = 2.54厘米
        return value
    
    def format_value(self, value):
        """格式化数值，保留3位小数"""
        return f"{value:.3f}"

class Square(Shape):
    """正方形类"""
    def get_inputs(self):
        # 创建输入窗口
        input_window = tk.Toplevel()
        input_window.title("正方形参数输入")
        input_window.geometry("400x200")
        input_window.grab_set()  # 设置为模态窗口
        
        # 主框架
        main_frame = ttk.Frame(input_window, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 边长输入
        ttk.Label(main_frame, text=f"请输入边长 ({self.unit}):", font=('Arial', 11)).pack(pady=10)
        side_entry = ttk.Entry(main_frame, font=('Arial', 11), width=15)
        side_entry.pack(pady=5)
        side_entry.focus()  # 聚焦到输入框
        
        result = [False]  # 用于存储结果状态
        
        # 确认按钮
        def on_confirm():
            try:
                self.side = float(side_entry.get())
                if self.side <= 0:
                    raise ValueError("边长必须大于0")
                result[0] = True
                input_window.destroy()
            except ValueError as e:
                messagebox.showerror("输入错误", f"请输入有效的数字: {e}")
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=15)
        
        ttk.Button(button_frame, text="确认", command=on_confirm, width=10).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="取消", command=input_window.destroy, width=10).pack(side=tk.LEFT, padx=10)
        
        # 绑定回车键
        input_window.bind('<Return>', lambda event: on_confirm())
        
        # 等待窗口关闭
        input_window.wait_window()
        return result[0]
    
    def calculate_area(self):
        side_cm = self.convert_to_cm(self.side)
        area = side_cm ** 2
        return area, {"边长": self.format_value(self.side) + f" {self.unit}", 
                     "边长(厘米)": self.format_value(side_cm) + " cm"}

class Rectangle(Shape):
    """长方形类"""
    def get_inputs(self):
        input_window = tk.Toplevel()
        input_window.title("长方形参数输入")
        input_window.geometry("400x250")
        input_window.grab_set()
        
        main_frame = ttk.Frame(input_window, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 长输入
        ttk.Label(main_frame, text=f"请输入长 ({self.unit}):", font=('Arial', 11)).pack(pady=5)
        length_entry = ttk.Entry(main_frame, font=('Arial', 11), width=15)
        length_entry.pack(pady=5)
        
        # 宽输入
        ttk.Label(main_frame, text=f"请输入宽 ({self.unit}):", font=('Arial', 11)).pack(pady=5)
        width_entry = ttk.Entry(main_frame, font=('Arial', 11), width=15)
        width_entry.pack(pady=5)
        
        result = [False]
        
        def on_confirm():
            try:
                self.length = float(length_entry.get())
                self.width = float(width_entry.get())
                if self.length <= 0 or self.width <= 0:
                    raise ValueError("长和宽必须大于0")
                result[0] = True
                input_window.destroy()
            except ValueError as e:
                messagebox.showerror("输入错误", f"请输入有效的数字: {e}")
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=15)
        
        ttk.Button(button_frame, text="确认", command=on_confirm, width=10).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="取消", command=input_window.destroy, width=10).pack(side=tk.LEFT, padx=10)
        
        input_window.wait_window()
        return result[0]
    
    def calculate_area(self):
        length_cm = self.convert_to_cm(self.length)
        width_cm = self.convert_to_cm(self.width)
        area = length_cm * width_cm
        return area, {"长": self.format_value(self.length) + f" {self.unit}", 
                     "宽": self.format_value(self.width) + f" {self.unit}",
                     "长(厘米)": self.format_value(length_cm) + " cm",
                     "宽(厘米)": self.format_value(width_cm) + " cm"}

class Triangle(Shape):
    """三角形类（使用海伦公式）"""
    def get_inputs(self):
        input_window = tk.Toplevel()
        input_window.title("三角形参数输入")
        input_window.geometry("400x300")
        input_window.grab_set()
        
        main_frame = ttk.Frame(input_window, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 三边输入
        ttk.Label(main_frame, text=f"请输入边a ({self.unit}):", font=('Arial', 11)).pack(pady=3)
        side_a_entry = ttk.Entry(main_frame, font=('Arial', 11), width=15)
        side_a_entry.pack(pady=3)
        
        ttk.Label(main_frame, text=f"请输入边b ({self.unit}):", font=('Arial', 11)).pack(pady=3)
        side_b_entry = ttk.Entry(main_frame, font=('Arial', 11), width=15)
        side_b_entry.pack(pady=3)
        
        ttk.Label(main_frame, text=f"请输入边c ({self.unit}):", font=('Arial', 11)).pack(pady=3)
        side_c_entry = ttk.Entry(main_frame, font=('Arial', 11), width=15)
        side_c_entry.pack(pady=3)
        
        result = [False]
        
        def on_confirm():
            try:
                self.side_a = float(side_a_entry.get())
                self.side_b = float(side_b_entry.get())
                self.side_c = float(side_c_entry.get())
                
                if self.side_a <= 0 or self.side_b <= 0 or self.side_c <= 0:
                    raise ValueError("三边长度必须大于0")
                
                # 检查三角形不等式
                if (self.side_a + self.side_b <= self.side_c or 
                    self.side_a + self.side_c <= self.side_b or 
                    self.side_b + self.side_c <= self.side_a):
                    raise ValueError("输入的三边不能构成三角形（不满足三角形不等式）")
                
                result[0] = True
                input_window.destroy()
            except ValueError as e:
                messagebox.showerror("输入错误", f"请输入有效的数字: {e}")
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=15)
        
        ttk.Button(button_frame, text="确认", command=on_confirm, width=10).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="取消", command=input_window.destroy, width=10).pack(side=tk.LEFT, padx=10)
        
        input_window.wait_window()
        return result[0]
    
    def calculate_area(self):
        # 转换为厘米
        a_cm = self.convert_to_cm(self.side_a)
        b_cm = self.convert_to_cm(self.side_b)
        c_cm = self.convert_to_cm(self.side_c)
        
        # 使用海伦公式计算面积
        s = (a_cm + b_cm + c_cm) / 2  # 半周长
        area = math.sqrt(s * (s - a_cm) * (s - b_cm) * (s - c_cm))
        
        return area, {
            "边a": self.format_value(self.side_a) + f" {self.unit}",
            "边b": self.format_value(self.side_b) + f" {self.unit}",
            "边c": self.format_value(self.side_c) + f" {self.unit}",
            "边a(厘米)": self.format_value(a_cm) + " cm",
            "边b(厘米)": self.format_value(b_cm) + " cm",
            "边c(厘米)": self.format_value(c_cm) + " cm",
            "半周长": self.format_value(s) + " cm"
        }

class Circle(Shape):
    """圆形类"""
    def get_inputs(self):
        input_window = tk.Toplevel()
        input_window.title("圆形参数输入")
        input_window.geometry("400x200")
        input_window.grab_set()
        
        main_frame = ttk.Frame(input_window, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 直径输入
        ttk.Label(main_frame, text=f"请输入直径 ({self.unit}):", font=('Arial', 11)).pack(pady=10)
        diameter_entry = ttk.Entry(main_frame, font=('Arial', 11), width=15)
        diameter_entry.pack(pady=5)
        
        result = [False]
        
        def on_confirm():
            try:
                self.diameter = float(diameter_entry.get())
                if self.diameter <= 0:
                    raise ValueError("直径必须大于0")
                result[0] = True
                input_window.destroy()
            except ValueError as e:
                messagebox.showerror("输入错误", f"请输入有效的数字: {e}")
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=15)
        
        ttk.Button(button_frame, text="确认", command=on_confirm, width=10).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="取消", command=input_window.destroy, width=10).pack(side=tk.LEFT, padx=10)
        
        input_window.wait_window()
        return result[0]
    
    def calculate_area(self):
        radius_cm = self.convert_to_cm(self.diameter / 2)
        area = math.pi * (radius_cm ** 2)
        return area, {"直径": self.format_value(self.diameter) + f" {self.unit}", 
                     "半径(厘米)": self.format_value(radius_cm) + " cm"}

import tkinter as tk
from tkinter import ttk

class AreaCalculator:
    """面积计算器主类"""
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("通用面积计算器")
        self.root.geometry("700x1000")  # 增大主窗口尺寸
        self.root.resizable(True, True)

        # 定义皮肤
        self.skins = {
            "默认": {
                "bg": "#f8f9fa",
                "fg": "#2c3e50",
                "result_bg": "#ffffff"
            },
            "深色": {
                "bg": "#2e2e2e",
                "fg": "#ecf0f1",
                "result_bg": "#1e1e1e"
            },
            "米色": {
                "bg": "#f5f5dc",
                "fg": "#333333",
                "result_bg": "#fff8dc"
            }
        }
        self.current_skin = "默认"

        # 主框架
        self.main_frame = ttk.Frame(self.root, padding=25)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # 设置样式
        self.setup_style()
        
        # 创建界面
        self.create_widgets()
        
    def setup_style(self):
        """设置界面样式"""
        style = ttk.Style()
        style.theme_use('clam')  # 使用更现代的主题

        # 当前皮肤
        skin = self.skins[self.current_skin]
        
        # 设置 ttk 样式
        style.configure('TFrame', background='#f8f9fa')
        style.configure('Title.TLabel', font=('Arial', 18, 'bold'), background='#f8f9fa', foreground='#2c3e50')
        style.configure('TButton', font=('Arial', 11), padding=8)
        style.configure('TLabel', background='#f8f9fa', font=('Arial', 10))
        style.configure('TLabelframe', background='#f8f9fa', font=('Arial', 11, 'bold'))
        style.configure('TLabelframe.Label', background='#f8f9fa', font=('Arial', 11, 'bold'))
        
        # 如果 result_text 已经存在，修改颜色
        if hasattr(self, "result_text"):
            self.result_text.configure(bg=skin["result_bg"], fg=skin["fg"])

        # 改变根窗口颜色
        self.root.configure(bg=skin["bg"])

    def create_widgets(self):
        """创建界面组件"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding=25)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = ttk.Label(main_frame, text="📐 通用面积计算器", style='Title.TLabel')
        title_label.pack(pady=25)

        # 新增皮肤选择下拉框
        skin_frame = ttk.Frame(main_frame)
        skin_frame.pack(pady=10)
        ttk.Label(skin_frame, text="🎨 选择皮肤:").pack(side=tk.LEFT, padx=5)
        self.skin_combo = ttk.Combobox(skin_frame, values=list(self.skins.keys()), state="readonly", width=10)
        self.skin_combo.set(self.current_skin)
        self.skin_combo.pack(side=tk.LEFT)
        self.skin_combo.bind("<<ComboboxSelected>>", self.change_skin)
        
        # 形状选择框架
        shape_frame = ttk.LabelFrame(main_frame, text="选择形状", padding=15)
        shape_frame.pack(fill=tk.X, pady=15, padx=10)
        
        self.shape_var = tk.StringVar(value="square")
        shapes = [("🔲 正方形", "square"), ("⬜ 长方形", "rectangle"), 
                 ("🔺 三角形", "triangle"), ("🔵 圆形", "circle")]
        
        shape_container = ttk.Frame(shape_frame)
        shape_container.pack(fill=tk.X)
        
        for i, (text, value) in enumerate(shapes):
            rb = ttk.Radiobutton(shape_container, text=text, value=value, 
                               variable=self.shape_var, style='Toolbutton')
            rb.grid(row=0, column=i, padx=15, pady=5, sticky='ew')
            shape_container.columnconfigure(i, weight=1)
        
        # 单位选择框架
        unit_frame = ttk.LabelFrame(main_frame, text="选择单位", padding=15)
        unit_frame.pack(fill=tk.X, pady=15, padx=10)
        
        self.unit_var = tk.StringVar(value="cm")
        unit_container = ttk.Frame(unit_frame)
        unit_container.pack()
        
        ttk.Radiobutton(unit_container, text="📏 厘米 (cm)", value="cm", 
                       variable=self.unit_var, style='Toolbutton').pack(side=tk.LEFT, padx=30)
        ttk.Radiobutton(unit_container, text="📐 英寸 (inch)", value="inch", 
                       variable=self.unit_var, style='Toolbutton').pack(side=tk.LEFT, padx=30)
        
        # 计算按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        calc_button = ttk.Button(button_frame, text="🧮 计算面积", command=self.calculate_area, width=15)
        calc_button.pack(side=tk.LEFT, padx=10)
        
        history_button = ttk.Button(button_frame, text="📋 查看历史记录", command=self.show_history, width=15)
        history_button.pack(side=tk.LEFT, padx=10)
        
        clear_button = ttk.Button(button_frame, text="🗑️ 清除结果", command=self.clear_results, width=15)
        clear_button.pack(side=tk.LEFT, padx=10)
        
        # 结果显示区域
        result_frame = ttk.LabelFrame(main_frame, text="计算结果", padding=15)
        result_frame.pack(fill=tk.BOTH, expand=True, pady=15, padx=10)
        
        # 使用Text控件显示结果，带有更好的格式
        self.result_text = tk.Text(result_frame, height=12, width=70, font=('Consolas', 11), 
                                 wrap=tk.WORD, bg='#ffffff', relief=tk.FLAT, padx=10, pady=10)
        
        # 创建滚动条
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        # 布局
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 初始化历史记录
        self.history = []
        
        # 显示欢迎信息
        self.show_welcome_message()

    def change_skin(self, event=None):
        """切换皮肤"""
        self.current_skin = self.skin_combo.get()
        self.setup_style()    
        
    def show_welcome_message(self):
        """显示欢迎信息"""
        welcome_text = """欢迎使用通用面积计算器！

使用方法：
1. 选择要计算的形状类型
2. 选择输入单位（厘米或英寸）
3. 点击"计算面积"按钮
4. 在弹出的窗口中输入所需参数
5. 查看计算结果

支持的形状：
• 正方形 - 输入边长
• 长方形 - 输入长和宽
• 三角形 - 输入三边长度（使用海伦公式）
• 圆形 - 输入直径

所有结果都将转换为平方厘米显示。
"""
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, welcome_text)
        
    def clear_results(self):
        """清除结果"""
        self.result_text.delete(1.0, tk.END)
        self.show_welcome_message()
        
    def calculate_area(self):
        """计算面积"""
        shape_type = self.shape_var.get()
        unit = self.unit_var.get()
        
        # 创建对应的形状对象
        if shape_type == "square":
            shape = Square(unit)
        elif shape_type == "rectangle":
            shape = Rectangle(unit)
        elif shape_type == "triangle":
            shape = Triangle(unit)
        else:  # circle
            shape = Circle(unit)
        
        # 获取输入参数
        if not shape.get_inputs():
            return  # 用户取消输入或输入无效
        
        # 计算面积
        try:
            area, params = shape.calculate_area()
            
            # 准备结果显示
            shape_names = {
                "square": "正方形",
                "rectangle": "长方形",
                "triangle": "三角形",
                "circle": "圆形"
            }
            
            result = "=" * 60 + "\n"
            result += f"📊 计算结果\n"
            result += "=" * 60 + "\n\n"
            result += f"📐 图形类型: {shape_names[shape_type]}\n"
            result += f"📏 输入单位: {unit}\n\n"
            result += "📋 输入参数:\n"
            
            for key, value in params.items():
                result += f"   • {key}: {value}\n"
            
            result += f"\n✅ 面积结果: {area:.3f} 平方厘米\n"
            result += "=" * 60
            
            # 显示结果
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, result)
            
            # 添加到历史记录
            self.history.append(result)
            
        except Exception as e:
            messagebox.showerror("计算错误", f"计算过程中出现错误: {e}")
        
    def show_history(self):
        """显示历史记录"""
        if not self.history:
            messagebox.showinfo("历史记录", "暂无历史记录")
            return
            
        history_window = tk.Toplevel(self.root)
        history_window.title("计算历史记录")
        history_window.geometry("800x500")
        history_window.minsize(600, 400)
        
        # 主框架
        main_frame = ttk.Frame(history_window, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = ttk.Label(main_frame, text="📋 计算历史记录", font=('Arial', 14, 'bold'))
        title_label.pack(pady=10)
        
        # 创建文本框显示历史记录
        history_text = tk.Text(main_frame, font=('Consolas', 10), wrap=tk.WORD, padx=10, pady=10)
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=history_text.yview)
        history_text.configure(yscrollcommand=scrollbar.set)
        
        # 布局
        history_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 插入历史记录
        for i, record in enumerate(self.history, 1):
            history_text.insert(tk.END, f"记录 {i}:\n")
            history_text.insert(tk.END, record)
            history_text.insert(tk.END, "\n" + "="*80 + "\n\n")
        
        history_text.config(state=tk.DISABLED)  # 设置为只读
        
        # 添加关闭按钮
        close_button = ttk.Button(main_frame, text="关闭", command=history_window.destroy)
        close_button.pack(pady=10)
        
    def run(self):
        """运行应用程序"""
        self.root.mainloop()

# 创建并运行应用程序
if __name__ == "__main__":
    app = AreaCalculator()
    app.run()