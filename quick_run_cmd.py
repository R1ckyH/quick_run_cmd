# -*- coding: utf-8 -*-
import json
import copy
import time
from utils.rtext import *


def rtext_cmd(txt, msg, cmd):
    return RText(txt).h(msg).c(RAction.run_command, cmd)

def rtext_paste(txt, msg, cmd):
    return RText(txt).h(msg).c(RAction.suggest_command, cmd)


plugin = 'quick_run_cmd'
prefix = '!!qrcmd'
prefix1 = '!!qr'
prefix2 = '!!ql'
delay = 0.5
page_cmd = 5
page_list = 5
json_path = 'config/' + plugin + '.json'

systemreturn = '''§b[§rquick_run_cmd§b] §r'''
error = systemreturn + '''§cError: '''

error_no_script = error + '''Unknown script§r
''' + rtext_cmd('Type §7!!qrcmd show§r to show script list', 'Click me to show script list', '!!qrcmd show')
error_cmd_exist = '''The script already exist§r
''' + rtext_cmd('Type §7!!qrcmd show§r to show script detail', 'Click me to Show script detail', '!!qrcmd show')
error_unknown_command = error + '''Unknown command§r
''' + rtext_cmd('Type §7!!qrcmd help§r for more information', 'Click me to Show help', '!!qrcmd help')
error_syntax = error + '''Syntax error
''' + rtext_cmd('Type §7!!qrcmd help§r for more information', 'Click me to Show help', '!!qrcmd help')
error_permission = error + 'You have no Permission to use this command'
error_no_cmd = error + 'No script here'
error_no_page = error + 'This page does not exist'

pline = '§b=====================================§r'
help = '''§b============§fquick_run_cmd§b============§r
''' + rtext_cmd('!!qr §b[name]§r §aquick run a script§r', ' ', '!!qrcmd help') + '''
''' + rtext_cmd('!!ql §e(page)§r §ashow list of cmd script§r', 'Click me to show list of cmd script', '!!ql') + '''
''' + rtext_cmd('!!qrcmd help §ashow help of quick_run_cmd§r', 'Click me to show help of qrcmd', '!!qrcmd help') + '''
''' + rtext_cmd('!!qrcmd show §e(page)§r §ashow list of cmd script§r', 'Click me to show list of cmd script', '!!qrcmd show') + '''
''' + rtext_cmd('!!qrcmd showcmd §b[name] §e(page)§r §ashow detail of a cmd script§r', 'Click me to show detail of a/all cmd script', '!!qrcmd showcmd') + '''
''' + rtext_paste('!!qrcmd add §b[name]§r §aadd a new script§r', ' ', prefix + 'add') + '''
''' + rtext_paste('!!qrcmd addcmd §b[name] §d[command]§r §aadd new command of a cmd script§r', ' ', prefix + 'addcmd')

help2 = '''§b============§fquick_run_cmd§b============§r
''' + rtext_paste('!!qrcmd del/remove §b[name]§r §adelete a cmd script§r', ' ', prefix + 'del') +  '''
''' + rtext_paste('!!qrcmd delcmd/removecmd §b[name] §e[number]§r §adelete a command of cmd script§r', ' ', prefix + 'delcmd') +  '''
''' + rtext_paste('!!qrcmd edit §b[name] §d[new name]§r §aedit the name of a cmd script§r', ' ', prefix + 'edit') + '''
''' + rtext_paste('!!qrcmd editdelay §b[name] §d[new delay]§r §aedit the delay of a cmd script§r', ' ', prefix + 'editdelay') + '''
''' + rtext_paste('!!qrcmd editcmd §b[name] §e[number] §d[new command]§r §aedit the command of a cmd script§r', ' ', prefix + 'editcmd') + '''
''' + rtext_paste('!!qrcmd editinfo §b[name] §d[new info]§r §aedit the description of a cmd script§r', ' ', prefix + 'editinfo')


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
        server.tell(player, rtext_cmd('§b========§eClick me to next page§b========§r', 'Click me to next page', '!!qrcmd help ' + '2'))
    elif num == 2:
        server.tell(player, help2)
        server.tell(player, pline)
    else:
        server.tell(player, error_no_page)


def show_cmd(server, player, num):
    data = json_read()
    if len(data["command_list"]) < (num - 1) * page_list:
        server.tell(player, error_no_page)
        return 0
    
    server.tell(player, '§b===============§fquick_run_cmd§b===============§r')
    if len(data["command_list"]) == 0:
            server.tell(player, error_no_cmd)
            server.tell(player, pline)
            return 0
    for i in range((num - 1) * page_list, (num - 1) * page_list + page_list):
        name = data["command_list"][i]["name"]
        description = data["command_list"][i]["info"]

        if description == '':
            description = 'None'
        server.tell(player, rtext_cmd('§a[' + str(i + 1) + ']§r §b' + name + '§e Info: §r' + description, 'click me to have more information about §b' + name + '§r', '!!qrcmd showcmd ' + name) + rtext_cmd("§c[run]", "§cclick me to run", "!!qr " + name))
        
        if len(data["command_list"]) == i + 1:
            server.tell(player, pline)
            return 0
    server.tell(player, rtext_cmd('§b========§eClick me to next page§b========§r', 'Click me to next page', '!!qrcmd show ' + str(num + 1)))


def add_cmd(server, player, name, new_info):
    data = json_read()
    if json_search(name, data) == -1:   
        data["command_list"].append({"name" : name, "info" : new_info, "delay": delay, "commands" : list('')})
        data["command_list"] = sorted(data["command_list"], key=lambda k: k['name'])
        json_save(data)
        server.tell(player, systemreturn + 'Success to add §b' + name + '§r with info: §e' + new_info + '§r')
    else:
        server.tell(player, error_cmd_exist)


def del_cmd(server, player, name):
    data = json_read()
    index = json_search(name, data)
    if index != -1:
        del data["command_list"][index]
        data["command_list"] = sorted(data["command_list"], key=lambda k: k['name'])
        json_save(data)
        server.tell(player, systemreturn + 'Success to remove §b' + name + '§r')
    else:
        server.tell(player, error_no_script)


def edit_cmd(server, player, name, new_name):
    data = json_read()
    index = json_search(name, data)
    if index != -1:
        old_name = data["command_list"][index]["name"]
        data["command_list"][index]["name"] = new_name
        json_save(data)
        server.tell(player, systemreturn + 'Success to rename §b' + old_name + '§r to §d' + new_name + '§r')
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
        server.tell(player, systemreturn + 'Success to edit info of §b' + name + '§r from §e' + old_info + '§r to §d' + new_info + '§r')
    else:
        server.tell(player, error_no_script)


def edit_cmd_delay(server, player, name, new_delay):
    data = json_read()
    index = json_search(name, data)
    if index != -1:
        old_delay = str(data["command_list"][index]["delay"])
        data["command_list"][index]["delay"] = new_delay
        json_save(data)
        server.tell(player, systemreturn + 'Success to edit delay of §b' + name + '§r from §e' + old_delay + '§r to §d' + str(new_delay) + '§r')
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

        if len(cmd) < (num - 1) * page_cmd:
            server.tell(player, error_no_page)
            return 0

        server.tell(player, '§b============§fquick_run_cmd§b============§r')
        server.tell(player, rtext_cmd('Delay: §d' + delay + '§r second,§e Info: §r' + info, 'Click me to run §b' + name, '!!qr ' + name))
        server.tell(player, rtext_cmd('command of §b' + name + "§r:", 'Click me to run §b' + name, '!!qr ' + name))
        if len(cmd) == 0:
            server.tell(player, pline)
            return 0

        for i in range((num - 1) * page_cmd, (num - 1) * page_cmd + page_cmd):
            server.tell(player, '§a[' + str(i + 1) + ']§r ' + cmd[i])
            if len(cmd) == i + 1:
                server.tell(player, pline)
                return 0

        server.tell(player, rtext_cmd('§b========§eClick me to next page§b========§r', 'Click me to next page', '!!qrcmd showcmd ' + name + ' ' + str(num + 1)))
    else:
        server.tell(player, error_no_script)


def add_script(server, player, name, cmd):
    print("add")
    data = json_read()
    index = json_search(name, data)
    if index != -1:
        data["command_list"][index]["commands"].append(cmd)
        json_save(data)
        server.tell(player, systemreturn + 'Success to add §d' + cmd + '§r in §b' + name + '§r')
    else:
        server.tell(player, error_no_script)


def del_script(server, player, name, num):
    data = json_read()
    index = json_search(name, data)
    if index != -1:
        cmd = data["command_list"][index]["commands"][num -1]
        del data["command_list"][index]["commands"][num -1]
        json_save(data)
        server.tell(player, systemreturn + 'Success to remove §d' + cmd + '§r in §b' + name + '§r')
    else:
        server.tell(player, error_no_script)


def edit_script(server, player, name, num, cmd):
    data = json_read()
    index = json_search(name, data)
    if index != -1:
        old_cmd = data["command_list"][index]["commands"][num -1]
        data["command_list"][index]["commands"][num -1] = cmd
        json_save(data)
        server.tell(player, systemreturn + 'Success to change §d' + old_cmd + ' §rto§d ' + cmd + '§r in §b' + name + '§r')
    else:
        server.tell(player, error_no_script)


def run_script(server, player, name):
    data = json_read()
    index = json_search(name, data)
    if index != -1:
        cmd = data["command_list"][index]["commands"]
        for i in range(len(cmd)):
            server.execute(cmd[i])
            time.sleep(float(data["command_list"][index]["delay"]))
        server.tell(player, "Success to run script of §b" + name)
    else:
        server.tell(player, error_no_script)


def onServerInfo(server, info):
    if info.content.startswith('!!qr') or info.content.startswith('!!qrcmd') or info.content.startswith('!!ql'):
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
        elif args[0] == '!!qr' and len(args) <= 2:
            if len(args) == 1:
                tell_help(server, info.player, 0)
            else:
                run_script(server, info.player, args[1])
        elif args[0] =='!!ql':
            if len(args) == 1 or args[1] == 'all':
                show_cmd(server, info.player, 1)
            else:
                if not_num(server, info.player, args[1]):
                    return 0
                show_cmd(server, info.player, int(args[1]))
        else:
            server.tell(info.player, error_unknown_command)

def on_load(server, old):
    server.add_help_message(prefix,'A plugin for run command quickly(use for config)')
    server.add_help_message(prefix1,'A plugin for run command quickly(use for run)')


def on_info(server, info):
    info2 = copy.deepcopy(info)
    info2.isPlayer = info2.is_player
    onServerInfo(server, info2)