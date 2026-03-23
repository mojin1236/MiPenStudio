import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext,filedialog,dialog
import random
import struct
import binascii
from datetime import datetime
import pygame

# 初始化Pygame
pygame.init()

# 设置窗口大小和无边框模式
screen = pygame.display.set_mode((400, 300), pygame.NOFRAME)

screen.blit(pygame.image.load(r'.\datas\mb.png'), (0, 0))
# 主循环
for i in range(15000):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 更新显示
    pygame.display.update()

# 退出Pygame
pygame.quit()
names = ['SMFW','DMFW','ZMFW','HWEN','HNEN','OQQO']

def saveFile(d):
    file_path = filedialog.asksaveasfilename(title=u'保存文件')
    print('保存文件：', file_path)
    file_text = d
    if file_path is not None:
        with open(file=file_path, mode='wb+') as file:
            file.write(file_text)
        dialog.Dialog(None, {'title': 'File Modified', 'text': '保存完成', 'bitmap': 'warning', 'default': 0,
                             'strings': ('OK', 'Cancle')})
        print('保存完成')


def openFile():
    file_path = filedialog.askopenfilename(title=u'打开文件')
    print('打开文件：', file_path)
    if file_path is not None:
        with open(file=file_path, mode='rb') as file:
            file_text = file.read()
            dialog.Dialog(None, {'title': 'File Modified', 'text': '打开完成', 'bitmap': 'warning', 'default': 0,
                                'strings': ('OK', 'Cancle')})
            print('打开完成')
            return file_text

class XiaomiFirmwareEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("MipenStudio v.2026R1.02a")
        self.root.geometry("1200x800")
        
        # 模拟固件数据 (1MB)
        self.firmware_data = self.generate_firmware_data(1024 * 1024)  # 1MB
        self.original_data = self.firmware_data.copy()
        self.current_offset = 0
        self.connected = False
        
        # 创建界面
        self.create_menu()
        self.create_toolbar()
        self.create_status_bar()
        self.create_editor_panel()
        self.create_info_panel()
        
        # 更新显示
        self.update_display()
    
    def generate_firmware_data(self, size):
        """生成随机的固件数据"""
        # 生成随机字节数据
        data = bytearray(random.getrandbits(8) for _ in range(size))
        
        # 添加一些特定的模式，使数据看起来更像真实的固件
        # 文件头
        self.a = random.choice(names)
        data[0:4] = self.a.encode('utf-8')
        
        data[16:32] = b'RecoveryMode\'s boot v2.3.1'
        
        # 添加一些字符串
        strings = [
            b"printf          static_cast",
            b"DO NOT MODIFY WITHOUT AUTHORIZATION",
            b"Secure Boot Enabled",
            b"Hardware ID: PW-2023-8872",
            b"Manufacturing Date: 2023-06-15",
            b"BLE MAC: 00:1A:7D:DA:71:13",
            b"Battery Capacity: 120mAh",
            b"Ink Level Sensor Calibration Data",
            b"Pressure Sensitivity Settings"
        ]
        
        # 在随机位置插入字符串
        for s in strings:
            pos = random.randint(256, len(data) - len(s) - 1)
            data[pos:pos+len(s)] = s
        
        return data
    
    def create_menu(self):
        """创建菜单栏"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # 文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="新建", command=self.new_file)
        file_menu.add_command(label="打开", command=self.open_file)
        file_menu.add_command(label="保存", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.root.quit)
        
        # 编辑菜单
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="编辑", menu=edit_menu)
        edit_menu.add_command(label="撤销", command=self.undo)
        edit_menu.add_command(label="重做", command=self.redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="查找", command=self.find)
        edit_menu.add_command(label="替换", command=self.replace)
        edit_menu.add_separator()
        edit_menu.add_command(label="转到偏移", command=self.goto_offset)
        
        # 工具菜单
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="工具", menu=tools_menu)
        tools_menu.add_command(label="连接设备", command=self.connect_device)
        tools_menu.add_command(label="断开连接", command=self.disconnect_device)
        tools_menu.add_separator()
        tools_menu.add_command(label="读取固件", command=self.read_firmware)
        tools_menu.add_command(label="写入固件", command=self.write_firmware)
        tools_menu.add_command(label="验证固件", command=self.verify_firmware)
        
        # 视图菜单
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="视图", menu=view_menu)
        view_menu.add_command(label="刷新", command=self.update_display)
        view_menu.add_separator()
        view_menu.add_command(label="16进制视图", command=self.hex_view)
        view_menu.add_command(label="文本视图", command=self.text_view)
        
        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="帮助", menu=help_menu)
        help_menu.add_command(label="关于", command=self.about)
    
    def create_toolbar(self):
        """创建工具栏"""
        toolbar = ttk.Frame(self.root, relief=tk.RAISED)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
        # 连接按钮
        self.connect_btn = ttk.Button(toolbar, text="连接设备", command=self.connect_device)
        self.connect_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        # 断开按钮
        self.disconnect_btn = ttk.Button(toolbar, text="断开连接", command=self.disconnect_device, state=tk.DISABLED)
        self.disconnect_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        # 分隔符
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=5, pady=2)
        
        # 读取按钮
        self.read_btn = ttk.Button(toolbar, text="读取固件", command=self.read_firmware, state=tk.DISABLED)
        self.read_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        # 写入按钮
        self.write_btn = ttk.Button(toolbar, text="写入固件", command=self.write_firmware, state=tk.DISABLED)
        self.write_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        # 验证按钮
        self.verify_btn = ttk.Button(toolbar, text="验证固件", command=self.verify_firmware, state=tk.DISABLED)
        self.verify_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        # 分隔符
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=5, pady=2)
        
        # 偏移量输入
        ttk.Label(toolbar, text="偏移量:").pack(side=tk.LEFT, padx=2, pady=2)
        self.offset_var = tk.StringVar()
        self.offset_entry = ttk.Entry(toolbar, textvariable=self.offset_var, width=10)
        self.offset_entry.pack(side=tk.LEFT, padx=2, pady=2)
        self.offset_entry.bind("<Return>", self.goto_offset)
        
        # 转到按钮
        self.goto_btn = ttk.Button(toolbar, text="转到", command=self.goto_offset)
        self.goto_btn.pack(side=tk.LEFT, padx=2, pady=2)
    
    def create_status_bar(self):
        """创建状态栏"""
        self.status_bar = ttk.Frame(self.root)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_left = ttk.Label(self.status_bar, text="就绪", relief=tk.SUNKEN, anchor=tk.W)
        self.status_left.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.status_right = ttk.Label(self.status_bar, text="偏移: 0x00000000", relief=tk.SUNKEN, anchor=tk.E)
        self.status_right.pack(side=tk.RIGHT)
    
    def create_editor_panel(self):
        """创建编辑器面板"""
        editor_frame = ttk.Frame(self.root)
        editor_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 创建16进制编辑器
        hex_frame = ttk.LabelFrame(editor_frame, text="16进制编辑器", padding=5)
        hex_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建文本框和滚动条
        self.text_frame = ttk.Frame(hex_frame)
        self.text_frame.pack(fill=tk.BOTH, expand=True)
        
        # 偏移量列
        self.offset_text = scrolledtext.ScrolledText(
            self.text_frame, width=10, height=30, 
            font=('Courier New', 10), state=tk.DISABLED
        )
        self.offset_text.pack(side=tk.LEFT, fill=tk.Y)
        
        # 16进制数据列
        self.hex_text = scrolledtext.ScrolledText(
            self.text_frame, width=50, height=30, 
            font=('Courier New', 10)
        )
        self.hex_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.hex_text.bind("<KeyRelease>", self.hex_text_changed)
        
        # ASCII列
        self.ascii_text = scrolledtext.ScrolledText(
            self.text_frame, width=20, height=30, 
            font=('Courier New', 10), state=tk.DISABLED
        )
        self.ascii_text.pack(side=tk.LEFT, fill=tk.Y)
        
        # 垂直滚动条同步
        def sync_scroll(*args):
            self.offset_text.yview(*args)
            self.hex_text.yview(*args)
            self.ascii_text.yview(*args)
        
        scrollbar = ttk.Scrollbar(hex_frame, orient=tk.VERTICAL, command=sync_scroll)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.offset_text.config(yscrollcommand=scrollbar.set)
        self.hex_text.config(yscrollcommand=scrollbar.set)
        self.ascii_text.config(yscrollcommand=scrollbar.set)
    
    def create_info_panel(self):
        """创建设备信息面板"""
        info_frame = ttk.LabelFrame(self.root, text="设备信息", width=300, padding=5)
        info_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        info_frame.pack_propagate(False)
        
        # 设备信息
        info_text = f"""
其他智能笔
型号: {self.a}
序列号: PW-{random.randint(2020,2025)}-{random.randint(1000,8720)}
固件版本: v0.0.1
硬件版本: {random.randint(2020,2025)}
生产日期: 2025-06-15
电池容量: {str(random.randint(9, 12)) + '0'}mAh
连接协议: BLE 3.0
"""
        
        device_info = scrolledtext.ScrolledText(
            info_frame, width=35, height=15, 
            font=('Segoe UI', 9), state=tk.DISABLED
        )
        device_info.pack(fill=tk.BOTH, expand=True)
        device_info.insert(tk.END, info_text)
        
        # 操作按钮
        btn_frame = ttk.Frame(info_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(btn_frame, text="备份固件", command=self.backup_firmware).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="恢复固件", command=self.restore_firmware).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="校验和", command=self.calculate_checksum).pack(side=tk.LEFT, padx=2)
        
        # 状态信息
        status_frame = ttk.LabelFrame(info_frame, text="操作状态", padding=5)
        status_frame.pack(fill=tk.X, pady=5)
        
        self.status_text = scrolledtext.ScrolledText(
            status_frame, width=35, height=8, 
            font=('Consolas', 8), state=tk.DISABLED
        )
        self.status_text.pack(fill=tk.BOTH, expand=True)
    
    def update_display(self):
        """更新显示内容"""
        # 清空文本框
        self.offset_text.config(state=tk.NORMAL)
        self.offset_text.delete(1.0, tk.END)
        self.hex_text.delete(1.0, tk.END)
        self.ascii_text.config(state=tk.NORMAL)
        self.ascii_text.delete(1.0, tk.END)
        
        # 每行显示16字节
        bytes_per_line = 16
        total_lines = len(self.firmware_data) // bytes_per_line
        
        for i in range(total_lines):
            offset = i * bytes_per_line
            # 显示偏移量
            self.offset_text.insert(tk.END, f"{offset:08X}\n")
            
            # 显示16进制数据
            hex_line = ""
            ascii_line = ""
            
            for j in range(bytes_per_line):
                pos = offset + j
                if pos < len(self.firmware_data):
                    byte = self.firmware_data[pos]
                    hex_line += f"{byte:02X} "
                    
                    # 显示可打印字符，不可打印字符显示为点
                    if 32 <= byte <= 126:
                        ascii_line += chr(byte)
                    else:
                        ascii_line += "."
                else:
                    hex_line += "   "
                    ascii_line += " "
            
            self.hex_text.insert(tk.END, hex_line + "\n")
            self.ascii_text.insert(tk.END, ascii_line + "\n")
        
        # 禁用偏移量和ASCII文本框的编辑
        self.offset_text.config(state=tk.DISABLED)
        self.ascii_text.config(state=tk.DISABLED)
        
        # 更新状态栏
        self.status_right.config(text=f"偏移: 0x{self.current_offset:08X}")
    
    def hex_text_changed(self, event):
        """16进制文本框内容改变事件"""
        # 获取当前光标位置
        cursor_pos = self.hex_text.index(tk.INSERT)
        line, col = map(int, cursor_pos.split('.'))
        
        # 计算字节偏移量
        byte_offset = (line - 1) * 16 + (col // 3)
        
        if byte_offset < len(self.firmware_data):
            # 获取当前行的文本
            line_text = self.hex_text.get(f"{line}.0", f"{line}.end")
            hex_bytes = line_text.split()
            
            # 更新数据
            for i, hex_byte in enumerate(hex_bytes):
                if len(hex_byte) == 2:
                    try:
                        byte_val = int(hex_byte, 16)
                        pos = (line - 1) * 16 + i
                        if pos < len(self.firmware_data):
                            self.firmware_data[pos] = byte_val
                    except ValueError:
                        pass
            
            # 更新ASCII显示
            self.update_ascii_line(line - 1)
    
    def update_ascii_line(self, line_index):
        """更新指定行的ASCII显示"""
        self.ascii_text.config(state=tk.NORMAL)
        
        # 计算偏移量
        offset = line_index * 16
        
        # 生成ASCII行
        ascii_line = ""
        for i in range(16):
            pos = offset + i
            if pos < len(self.firmware_data):
                byte = self.firmware_data[pos]
                if 32 <= byte <= 126:
                    ascii_line += chr(byte)
                else:
                    ascii_line += "."
            else:
                ascii_line += " "
        
        # 更新指定行
        self.ascii_text.delete(f"{line_index + 1}.0", f"{line_index + 1}.end")
        self.ascii_text.insert(f"{line_index + 1}.0", ascii_line)
        
        self.ascii_text.config(state=tk.DISABLED)
    
    def connect_device(self):
        """连接设备"""
        if not self.connected:
            # 模拟连接过程
            self.add_status_message("正在搜索设备...")
            self.root.after(1000, self.device_found)
    
    def device_found(self):
        """设备找到"""
        self.add_status_message("找到设备")
        self.add_status_message("正在建立连接...")
        self.root.after(1500, self.connection_established)
    
    def connection_established(self):
        """连接建立"""
        self.connected = True
        self.add_status_message("连接成功!")
        self.add_status_message("设备就绪")
        
        # 更新按钮状态
        self.connect_btn.config(state=tk.DISABLED)
        self.disconnect_btn.config(state=tk.NORMAL)
        self.read_btn.config(state=tk.NORMAL)
        self.write_btn.config(state=tk.NORMAL)
        self.verify_btn.config(state=tk.NORMAL)
        
        self.status_left.config(text="已连接")
    
    def disconnect_device(self):
        """断开设备连接"""
        if self.connected:
            self.connected = False
            self.add_status_message("断开连接")
            
            # 更新按钮状态
            self.connect_btn.config(state=tk.NORMAL)
            self.disconnect_btn.config(state=tk.DISABLED)
            self.read_btn.config(state=tk.DISABLED)
            self.write_btn.config(state=tk.DISABLED)
            self.verify_btn.config(state=tk.DISABLED)
            
            self.status_left.config(text="就绪")
    
    def read_firmware(self):
        """读取固件"""
        if self.connected:
            self.add_status_message("开始读取固件...")
            self.root.after(500, self.read_progress)
    
    def read_progress(self):
        """读取进度"""
        self.add_status_message("读取中... 50%")
        self.root.after(500, self.read_complete)
    
    def read_complete(self):
        """读取完成"""
        self.add_status_message("固件读取完成")
        self.add_status_message(f"固件大小: {len(self.firmware_data)} 字节")
        
        # 更新显示
        self.update_display()
    
    def write_firmware(self):
        """写入固件"""
        if self.connected:
            self.add_status_message("开始写入固件...")
            self.root.after(500, self.write_progress)
    
    def write_progress(self):
        """写入进度"""
        self.add_status_message("写入中... 50%")
        self.root.after(500, self.write_complete)
    
    def write_complete(self):
        """写入完成"""
        self.add_status_message("固件写入完成")
        self.add_status_message("设备重启中...")
        self.root.after(1000, lambda: self.add_status_message("设备重启完成"))
    
    def verify_firmware(self):
        """验证固件"""
        if self.connected:
            self.add_status_message("开始验证固件...")
            self.root.after(1000, self.verify_complete)
    
    def verify_complete(self):
        """验证完成"""
        # 模拟验证结果
        if random.random() > 0.2:
            self.add_status_message("固件验证成功")
        else:
            self.add_status_message("固件验证失败")
            self.add_status_message("校验和不匹配")
    
    def goto_offset(self, event=None):
        """转到指定偏移量"""
        try:
            offset_str = self.offset_var.get().strip()
            if offset_str.startswith("0x"):
                offset = int(offset_str[2:], 16)
            else:
                offset = int(offset_str)
            
            if 0 <= offset < len(self.firmware_data):
                self.current_offset = offset
                line = offset // 16 + 1
                self.hex_text.see(f"{line}.0")
                self.status_right.config(text=f"偏移: 0x{offset:08X}")
            else:
                messagebox.showerror("错误", "偏移量超出范围")
        except ValueError:
            messagebox.showerror("错误", "无效的偏移量")
    
    def add_status_message(self, message):
        """添加状态消息"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.status_text.config(state=tk.NORMAL)
        self.status_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.status_text.see(tk.END)
        self.status_text.config(state=tk.DISABLED)
    
    def backup_firmware(self):
        """备份固件"""
        saveFile(self.firmware_data)
        self.add_status_message("固件备份成功")
    
    def restore_firmware(self):
        """恢复固件"""
        self.add_status_message("固件恢复功能尚未实现")
    
    def calculate_checksum(self):
        """计算校验和"""
        # 计算简单的校验和
        checksum = sum(self.firmware_data) & 0xFFFFFFFF
        self.add_status_message(f"校验和: 0x{checksum:08X}")
    
    # 以下为菜单功能的空实现
    def new_file(self):
        messagebox.showinfo("信息", "新建文件功能尚未实现")
    
    def open_file(self):
        d = openFile()
        if d is not None:
            self.firmware_data = d
            self.update_display()
        messagebox.showinfo("信息", "打开文件成功")
    
    def save_file(self):
        saveFile(self.firmware_data)
        messagebox.showinfo("信息", "保存文件成功")
    
    def undo(self):
        messagebox.showinfo("信息", "撤销功能尚未实现")
    
    def redo(self):
        messagebox.showinfo("信息", "重做功能尚未实现")
    
    def find(self):
        messagebox.showinfo("信息", "查找功能尚未实现")
    
    def replace(self):
        messagebox.showinfo("信息", "替换功能尚未实现")
    
    def hex_view(self):
        messagebox.showinfo("信息", "已经是16进制视图")
    
    def text_view(self):
        messagebox.showinfo("信息", "文本视图功能尚未实现")
    
    def about(self):
        about_text = """
MipenStudio v.2026R1.02a

用于编辑巨能写智能笔的固件文件。
支持16进制查看和编辑，固件读取和写入功能。

注意: 这是一个模拟工具，仅供演示使用。
修改固件可能导致设备无法正常工作，请谨慎操作。
"""
        messagebox.showinfo("关于", about_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = XiaomiFirmwareEditor(root)
    root.mainloop()