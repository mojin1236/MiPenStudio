import PySimpleGUI as sg

layout = [
    [sg.Text("Birelaod刷入固件工具")],
    [sg.Text("请选择固件文件：", size=(15, 1)), sg.Input(), sg.FileBrowse(button_text='选择文件',file_types=(("bin文件", "*.bin"),))],
    [sg.B('连接设备'), sg.B('断开连接'), sg.Text("状态：未连接", key='status', size=(15, 1))],
    [sg.Button("开始刷入")],
    [sg.ProgressBar(1000, orientation='h', size=(20, 20), key='progressbar')]
]
window = sg.Window("Birelaod刷入固件工具", layout)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break 
    elif event == "连接设备":
        sg.popup("连接设备成功")
        window['status'].update("状态：已连接")
    elif event == "断开连接":
        sg.popup("断开连接成功")
        window['status'].update("状态：未连接")
    elif event == "开始刷入":
        sg.popup("开始刷入固件")
        for i in range(1001):
            if i < 250:
                window['progressbar'].UpdateBar(i+3)
            elif i < 600:
                window['progressbar'].UpdateBar(i+2)
            else:
                window['progressbar'].UpdateBar(i)
        sg.popup("固件刷入成功")
    