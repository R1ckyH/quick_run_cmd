# -*- coding: utf-8 -*-
import json
import copy
import time
from utils.rtext import *


def rtext_cmd(txt, msg, cmd):
    return RText(txt).h(msg).c(RAction.run_command, cmd)


plugin = 'quick_run_cmd'
prefix = '!!qrcmd'
prefix1 = '!!qr'
json_path = 'config/' + plugin + '.json'

systemreturn = '''§b[§rquick_run_cmd§b] §r'''
error = systemreturn + '''§cError: '''

error_no_script = error + '''未知脚本§r
''' + rtext_cmd('输入 §7!!qrcmd show§r 以显示脚本列表', '点击我显示脚本列表', '!!qrcmd show')
error_cmd_exist = '''脚本已经存在§r
''' + rtext_cmd('输入 §7!!qrcmd show§r 以显示脚本列表', '点击我以显示脚本列表', '!!qrcmd show')
error_unknown_command = error + '''未知命令§r
''' + rtext_cmd('输入 §7!!qrcmd help§r 以获取更多资讯', '点击我显示帮助信息', '!!qrcmd help')
error_syntax = error + '''格式错误
''' + rtext_cmd('输入 §7!!qrcmd help§r 以获取更多资讯', '点击我显示帮助信息', '!!qrcmd help')
error_permission = error + '你没有权限使用此指令'
error_no_cmd = error + '这里没有任何脚本'
error_no_page = error + '404 此页面不存在'

pline = '§b=====================================§r'
help = '''§b============§fquick_run_cmd§b============§r
''' + rtext_cmd('!!qr §b[脚本名]§r §a快速运行脚本§r', '点击我运行脚本', '!!qrcmd help') + '''
''' + rtext_cmd('!!qrcmd help §a显示帮助信息§r', '点击我显示帮助信息', '!!qrcmd help') + '''
''' + rtext_cmd('!!qrcmd show §e(页数)§r §a显示脚本列表§r', '点击我显示脚本列表', '!!qrcmd show') + '''
''' + rtext_cmd('!!qrcmd showcmd §b[脚本名] §e(页数)§r §a显示脚本中详细信息§r', '点击我显示脚本详细信息', '!!qrcmd show') + '''
''' + rtext_cmd('!!qrcmd add §b[脚本名]§r §a加入一个新脚本§r', ' ', prefix) + '''
''' + rtext_cmd('!!qrcmd addcmd §b[脚本名] §d[command]§r §a在脚本中添加一个新指令§r', ' ', prefix)

help2 = '''§b============§fquick_run_cmd§b============§r
''' + rtext_cmd('!!qrcmd del/remove §b[脚本名]§r §a删除一个脚本§r', ' ', prefix) +  '''
''' + rtext_cmd('!!qrcmd delcmd/removecmd §b[脚本名] §e[number]§r §a在脚本中删除指令§r', ' ', prefix) +  '''
''' + rtext_cmd('!!qrcmd edit §b[脚本名] §d[新脚本名]§r §a编辑脚本名称§r', ' ', prefix) + '''
''' + rtext_cmd('!!qrcmd editdelay §b[脚本名] §d[新延迟]§r §a编辑脚本指令运行间隔§r', ' ', prefix) + '''
''' + rtext_cmd('!!qrcmd editcmd §b[脚本名] §e[指令编号] §d[新指令]§r §a在脚本中编辑指令§r', ' ', prefix) + '''
''' + rtext_cmd('!!qrcmd editinfo §b[脚本名] §d[新描述信息]§r §a编辑脚本描述信息§r', ' ', prefix)


def permission_check(server, info):
    if info.isPlayer:
        return server.get_permission_level(info.player)
    else:
        return 999


def not_num(server, player, num):
    try:
        float(num)
    except ValueError:
        server.tell(player, error_syntax)
        return True
    return False


def json_read():
    with open(json_path,"r") as f:
        data = json.load(f)
    return data


def json_search(name, data):
    for i in range(len(data["command_list"])):
        if data["command_list"][i]["name"] == name:
            return i
    return -1


def json_search_cmd(cmd, data, index):
    cmd_list = data["command_list"][index]["commands"]
    for i in range(len(cmd_list)):
        if cmd_list[i] == cmd:
            return i
    return -1


def json_save(data):
    with open(json_path, "w") as file:
        json.dump(data, file, indent=4)


def tell_help(server, player, num):
    if num == 0 or num == 1:
        server.tell(player, help)
        server.tell(player, rtext_cmd('§b============§e点击我去下一页§b============§r', '点击我去下一页', '!!qrcmd help ' + '2'))
    elif num == 2:
        server.tell(player, help2)
        server.tell(player, pline)
    else:
        server.tell(player, error_no_page)


def show_cmd(server, player, num):
    data = json_read()
    if len(data["command_list"]) < (num - 1) * 5:
        server.tell(player, error_no_page)
        return 0
    
    server.tell(player, '§b============§fquick_run_cmd§b============§r')
    if len(data["command_list"]) == 0:
            server.tell(player, error_no_cmd)
            server.tell(player, pline)
            return 0
    for i in range((num - 1) * 5, (num - 1) * 5 + 5):
        name = data["command_list"][i]["name"]
        description = data["command_list"][i]["info"]

        if description == '':
            description = 'None'
        server.tell(player, rtext_cmd('§a[' + str(i + 1) + ']§r §b' + name + '§e Info: §r' + description, 'click me to have more information about §b' + name + '§r', '!!qrcmd showcmd ' + name))
        
        if len(data["command_list"]) == i + 1:
            server.tell(player, pline)
            return 0
    server.tell(player, rtext_cmd('§b============§e点击我去下一页§b============§r', '点击我去下一页', '!!qrcmd show ' + str(num + 1)))


def add_cmd(server, player, name, new_info):
    data = json_read()
    if json_search(name, data) == -1:   
        data["command_list"].append({"name" : name, "info" : new_info, "delay": 0.5, "commands" : list('')})
        data["command_list"] = sorted(data["command_list"], key=lambda k: k['name'])
        json_save(data)
        server.tell(player, systemreturn + '成功添加脚本 §b' + name + '§r， 描述信息: §e' + new_info + '§r')
    else:
        server.tell(player, error_cmd_exist)


def del_cmd(server, player, name):
    data = json_read()
    index = json_search(name, data)
    if index != -1:
        del data["command_list"][index]
        data["command_list"] = sorted(data["command_list"], key=lambda k: k['name'])
        json_save(data)
        server.tell(player, systemreturn + '成功移除脚本 §b' + name + '§r')
    else:
        server.tell(player, error_no_script)


def edit_cmd(server, player, name, new_name):
    data = json_read()
    index = json_search(name, data)
    if index != -1:
        old_name = data["command_list"][index]["name"]
        data["command_list"][index]["name"] = new_name
        json_save(data)
        server.tell(player, systemreturn + '成功重命名脚本 §b' + old_name + '§r 至 §d' + new_name + '§r')
    else:
        server.tell(player, error_no_script)
        

def edit_cmd_info(server, player, name, new_info):
    data = json_read()
    index = json_search(name, data)
    if index != -1:
        old_info = str(data["command_list"][index]["info"])
        data["command_list"][index]["info"] = new_info
        json_save(data)
        if old_info == '':
            old_info = "None"
        server.tell(player, systemreturn + '成功将 §b' + name + '§r 的描述信息从 §e' + old_info + '§r 修改至 §d' + new_info + '§r')
    else:
        server.tell(player, error_no_script)


def edit_cmd_delay(server, player, name, new_delay):
    data = json_read()
    index = json_search(name, data)
    if index != -1:
        old_delay = str(data["command_list"][index]["delay"])
        data["command_list"][index]["delay"] = new_delay
        json_save(data)
        server.tell(player, systemreturn + '成功将 §b' + name + '§r 的延迟从 §e' + old_delay + '§r 修改至 §d' + str(new_delay) + '§r')
    else:
        server.tell(player, error_no_script)

def show_script(server, player, name, num):
    data = json_read()
    index = json_search(name, data)
    if index != -1:
        cmd = data["command_list"][index]["commands"]
        info = str(data["command_list"][index]["info"])
        delay = str(data["command_list"][index]["delay"])
        if info == '':
            info = 'None'

        if len(cmd) < (num - 1) * 5:
            server.tell(player, error_no_page)
            return 0

        server.tell(player, '§b============§fquick_run_cmd§b============§r')
        server.tell(player, '指令延迟: §d' + delay + '§r,§e 描述信息: §r' + info)
        server.tell(player, '§b' + name + "§r的指令为:")
        if len(cmd) == 0:
            server.tell(player, pline)
            return 0

        for i in range((num - 1) * 5, (num - 1) * 5 + 5):
            server.tell(player, '§a[' + str(i + 1) + ']§r ' + cmd[i])
            if len(cmd) == i + 1:
                server.tell(player, pline)
                return 0

        server.tell(player, rtext_cmd('§b============§e点击我去下一页§b============§r', '点击我去下一页', '!!qrcmd showcmd ' + name + ' ' + str(num + 1)))
    else:
        server.tell(player, error_no_script)


def add_script(server, player, name, cmd):
    print("add")
    data = json_read()
    index = json_search(name, data)
    if index != -1:
        data["command_list"][index]["commands"].append(cmd)
        json_save(data)
        server.tell(player, systemreturn + '成功将§d ' + cmd + '§r 添加至 §b' + name + '§r')
    else:
        server.tell(player, error_no_script)


def del_script(server, player, name, num):
    data = json_read()
    index = json_search(name, data)
    if index != -1:
        cmd = data["command_list"][index]["commands"][num -1]
        del data["command_list"][index]["commands"][num -1]
        json_save(data)
        server.tell(player, systemreturn + '成功将 §d' + cmd + '§r 从指令集 §b' + name + '§r中移除')
    else:
        server.tell(player, error_no_script)


def edit_script(server, player, name, num, cmd):
    data = json_read()
    index = json_search(name, data)
    if index != -1:
        old_cmd = data["command_list"][index]["commands"][num -1]
        data["command_list"][index]["commands"][num -1] = cmd
        json_save(data)
        server.tell(player, systemreturn + '成功将 §d' + name + '§r 的 §b' + old_cmd + ' §r指令换成§d ' + cmd + '§r')
    else:
        server.tell(player, error_no_script)


def run_script(server, player, name):
    data = json_read()
    index = json_search(name, data)
    if index != -1:
        cmd = data["command_list"][index]["commands"]
        for i in range(len(cmd)):
            server.execute(cmd[i])
            time.sleep(0.5)
        server.tell(player, "成功运行脚本: §b" + name)
    else:
        server.tell(player, error_no_script)


def onServerInfo(server, info):
    if info.content.startswith('!!qr') or info.content.startswith('!!qrcmd'):
        permission = permission_check(server, info)
        if info.content.endswith('<--[HERE]'):
            info.content = info.content.replace('<--[HERE]','')
        args = info.content.split(' ')
        if args[0] == '!!qrcmd':
            if (len(args) == 1 or args[1] == 'help'):
                if len(args) <= 2:
                    tell_help(server, info.player, 0)
                else:
                    if not_num(server, info.player, args[2]):
                        return 0
                    tell_help(server, info.player, int(args[2]))
            else:
                if args[1] == 'show':
                    if len(args) == 2 or args[2] == 'all':
                        show_cmd(server, info.player, 1)
                    else:
                        if not_num(server, info.player, args[2]):
                            return 0
                        show_cmd(server, info.player, int(args[2]))
                elif args[1] == 'showcmd':
                    if len(args) == 3:
                        show_script(server, info.player, args[2], 1)
                    elif len(args) == 4:
                        if not_num(server, info.player, args[3]):
                            return 0
                        show_script(server, info.player, args[2], int(args[3]))
                elif args[1] == 'add':
                    if permission < 2:
                        server.tell(info.player, error_permission)
                    elif len(args) >= 3:
                        if args[2] != 'all':
                            if len(args) != 3:
                                new_info = args[3]
                                for i in range(4, len(args)):
                                    new_info = new_info + ' ' + args[i]
                            else:
                                new_info = ''
                            add_cmd(server, info.player, args[2], new_info)
                        else:
                            server.tell(info.player, error_cmd_exist)
                    else:
                        server.tell(info.player, permission)
                elif args[1] == 'del' or args[1] == 'remove':
                    if permission < 2:
                        server.tell(info.player, error_permission)
                    elif len(args) == 3:
                        del_cmd(server, info.player, args[2])
                elif args[1] == 'addcmd':
                    if permission < 2:
                        server.tell(info.player, error_permission)
                    elif len(args) >= 4:
                        cmd = args[3]
                        for i in range(4, len(args)):
                            cmd = cmd + ' ' + args[i]
                        add_script(server, info.player, args[2], cmd)
                    else:
                        server.tell(info.player, error_syntax)
                elif args[1] == 'delcmd':
                    if permission < 2:
                        server.tell(info.player, error_permission)
                    elif len(args) >= 4:
                        if not_num(server, info.player, args[3]):
                            return 0
                        del_script(server, info.player, args[2], int(args[3]))
                    else:
                        server.tell(info.player, error_syntax)
                elif args[1] == 'edit':
                    if permission < 2:
                        server.tell(info.player, error_permission)
                    elif len(args) == 4:
                        edit_cmd(server, info.player, args[2], args[3])
                    else:
                        server.tell(info.player, error_syntax)
                elif args[1] == 'editcmd':
                    if permission < 2:
                        server.tell(info.player, error_permission)
                    elif len(args) >= 4:
                        if not_num(server, info.player, args[3]):
                            return 0
                        cmd = args[4]
                        for i in range(5, len(args)):
                            cmd = cmd + ' ' + args[i]
                        edit_script(server, info.player, args[2], int(args[3]), cmd)
                    else:
                        server.tell(info.player, error_syntax)
                elif args[1] == 'editinfo':
                    if permission < 2:
                        server.tell(info.player, error_permission)
                    elif len(args) >= 4:
                        new_info = args[3]
                        for i in range(4, len(args)):
                            new_info = new_info + ' ' + args[i]
                        edit_cmd_info(server, info.player, args[2], new_info)
                    else:
                        server.tell(info.player, error_syntax)
                elif args[1] == 'editdelay':
                    if permission < 2:
                        server.tell(info.player, error_permission)
                    elif len(args) >= 4:
                        if not_num(server, info.player, args[3]):
                            return 0
                        edit_cmd_delay(server, info.player, args[2], float(args[3]))
                    else:
                        server.tell(info.player, error_syntax)
                else:
                    server.tell(info.player, error_unknown_command)
        elif args[0] == '!!qr':
            if len(args) == 1:
                tell_help(server, info.player, 0)
            else:
                run_script(server, info.player, args[1])
        else:
            server.tell(info.player, error_unknown_command)

def on_load(server, old):
    server.add_help_message(prefix,'一个快速运行自定义脚本的插件(用于配置)')
    server.add_help_message(prefix1,'一个快速运行自定义脚本的插件(用于运行指令)')


def on_info(server, info):
    info2 = copy.deepcopy(info)
    info2.isPlayer = info2.is_player
    onServerInfo(server, info2)