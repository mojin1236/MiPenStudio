import PySimpleGUI as sg
import warnings
 
warnings.filterwarnings("ignore")
layout = [
    [sg.Text("Birelaod编译bom工具")],
    [sg.Text("请选择bom文件：", size=(15, 1)), sg.Input(key='file'), sg.FileBrowse(button_text='选择文件',file_types=(("bom文件", "*.bom")))],
    [sg.Button("编译")],
    [sg.ProgressBar(1000, orientation='h', size=(20, 20), key='progressbar')]
]
window = sg.Window("Birelaod编译bom工具", layout)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break 
    elif event == "编译":
        if values['file'] != '':
            sg.popup("开始编译bom")
            for i in range(1001):
                if i < 250:
                    window['progressbar'].UpdateBar(i+3)
                elif i < 600:
                    window['progressbar'].UpdateBar(i+2)
                else:
                    window['progressbar'].UpdateBar(i)
            sg.popup("bom编译成功")
            with open(values['file'][:-3]+'pbm', 'w+', encoding='utf-8') as f:
                f2 = open(values['file'], 'r', encoding='utf-8')
                for line in f2.read():
                    f.write(str(ord(line)))
                f2.close()
            sg.popup("pbm文件生成成功")

window.close()