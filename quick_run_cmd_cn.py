# -*- coding: utf-8 -*-
import os
import json
import time
from mcdreforged.api.types import *
from mcdreforged.api.command import *
from mcdreforged.api.rtext import *
from mcdreforged.api.decorator import new_thread


PLUGIN_METADATA = {
    'id': 'quick_run_cmd',
    'version': '1.6.2-cn',
    'name': 'quick_run_cmd_cn',
    'description': '一个快速运行自定义脚本的插件.',
    'author': 'ricky',
    'link': 'https://github.com/rickyhoho/quick_run_cmd',
    'dependencies': {
        'mcdreforged': '>=1.0.0'
    }
}


permission = {
    "help" : 1,
    "show" : 1,
    "showcmd" : 1,
    "add" : 2,
    "addcmd" : 2,
    "del" : 2,
    "delcmd" : 2,
    "edit" : 2,
    "editcmd" : 2,
    "editdelay" : 2,
    "editinfo" : 2,
}


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
error_no_cmd = '这里没有任何脚本'
error_no_page = error + '404 此页面不存在'

pline = '§b=====================================§r'
help = '''§b============§fquick_run_cmd§b============§r
''' + rtext_cmd('!!qr §b[脚本名]§r §a快速运行脚本§r', '点击我运行脚本', '!!qrcmd help') + '''
''' + rtext_cmd('!!qrcmd help §a显示帮助信息§r', '点击我显示帮助信息', '!!qrcmd help') + '''
''' + rtext_cmd('!!qrcmd show §e(页数)§r §a显示脚本列表§r', '点击我显示脚本列表', '!!qrcmd show') + '''
''' + rtext_cmd('!!qrcmd showcmd §b[脚本名] §e(页数)§r §a显示脚本中详细信息§r', '点击我显示脚本详细信息', '!!qrcmd show') + '''
''' + rtext_cmd('!!qrcmd add §b[脚本名]§r §a加入一个新脚本§r', '', prefix) + '''
''' + rtext_cmd('!!qrcmd addcmd §b[脚本名] §d[command]§r §a在脚本中添加一个新指令§r', '', prefix)

help2 = '''§b============§fquick_run_cmd§b============§r
''' + rtext_cmd('!!qrcmd del §b[脚本名]§r §a删除一个脚本§r', '', prefix) +  '''
''' + rtext_cmd('!!qrcmd delcmd §b[脚本名] §e[number]§r §a在脚本中删除指令§r', '', prefix) +  '''
''' + rtext_cmd('!!qrcmd edit §b[脚本名] §d[新脚本名]§r §a编辑脚本名称§r', '', prefix) + '''
''' + rtext_cmd('!!qrcmd editcmd §b[脚本名] §e[指令编号] §d[新指令]§r §a在脚本中编辑指令§r', '', prefix) + '''
''' + rtext_cmd('!!qrcmd editinfo §b[脚本名] §d[新描述信息]§r §a编辑脚本描述信息§r', '', prefix) + '''
''' + rtext_cmd('!!qrcmd editdelay §b[脚本名] §d[新延迟]§r §a编辑脚本指令运行间隔§r', '', prefix)


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


@new_thread('qrcmd')
def tell_help(src : CommandSource, num):
    if num == 0 or num == 1:
        src.reply(help)
        src.reply(rtext_cmd('§b============§e点击我去下一页§b============§r', '点击我去下一页', '!!qrcmd help ' + '2'))
    elif num == 2:
        src.reply(help2)
        src.reply(pline)
    else:
        src.reply(error_no_page)


@new_thread('qrcmd')
def show_cmd(src : CommandSource, num):
    data = json_read()
    if len(data["command_list"]) < (num - 1) * 5:
        src.reply(error_no_page)
        return 0
    
    src.reply('§b============§fquick_run_cmd§b============§r')
    if len(data["command_list"]) == 0:
            src.reply(error_no_cmd)
            src.reply(pline)
            return 0
    for i in range((num - 1) * 5, (num - 1) * 5 + 5):
        name = data["command_list"][i]["name"]
        description = data["command_list"][i]["info"]

        if description == '':
            description = 'None'
        src.reply(rtext_cmd('§a[' + str(i + 1) + ']§r §b' + name + '§e 描述信息: §r' + description, 'click me to have more information about §b' + name + '§r', '!!qrcmd showcmd ' + name))
        
        if len(data["command_list"]) == i + 1:
            src.reply(pline)
            return 0
    src.reply(rtext_cmd('§b============§e点击我去下一页§b============§r', '点击我去下一页', '!!qrcmd show ' + str(num + 1)))


@new_thread('qrcmd_process')
def add_cmd(src : CommandSource, name, new_info):
    data = json_read()
    if json_search(name, data) == -1:   
        data["command_list"].append({"name" : name, "info" : new_info, "delay": 0.5, "commands" : list('')})
        data["command_list"] = sorted(data["command_list"], key=lambda k: k['name'])
        json_save(data)
        if new_info == '':
            new_info = '无'
        src.reply(systemreturn + '成功添加脚本 §b' + name + '§r， 描述信息: §e' + new_info + '§r')
    else:
        src.reply(error_cmd_exist)


@new_thread('qrcmd_process')
def del_cmd(src : CommandSource, name):
    data = json_read()
    index = json_search(name, data)
    if index != -1:
        del data["command_list"][index]
        data["command_list"] = sorted(data["command_list"], key=lambda k: k['name'])
        json_save(data)
        src.reply(systemreturn + '成功移除脚本 §b' + name + '§r')
    else:
        src.reply(error_no_script)


@new_thread('qrcmd_process')
def edit_cmd_name(src : CommandSource, name, new_name):
    data = json_read()
    index = json_search(name, data)
    if index != -1:
        old_name = data["command_list"][index]["name"]
        data["command_list"][index]["name"] = new_name
        json_save(data)
        src.reply(systemreturn + '成功重命名脚本 §b' + old_name + '§r 至 §d' + new_name + '§r')
    else:
        src.reply(error_no_script)
        

@new_thread('qrcmd_process')
def edit_cmd_info(src : CommandSource, name, new_info):
    data = json_read()
    index = json_search(name, data)
    if index != -1:
        old_info = str(data["command_list"][index]["info"])
        data["command_list"][index]["info"] = new_info
        json_save(data)
        if old_info == '':
            old_info = "None"
        src.reply(systemreturn + '成功将 §b' + name + '§r 的描述信息从 §e' + old_info + '§r 修改至 §d' + new_info + '§r')
    else:
        src.reply(error_no_script)


@new_thread('qrcmd_process')
def edit_cmd_delay(src : CommandSource, name, new_delay):
    data = json_read()
    index = json_search(name, data)
    if index != -1:
        old_delay = str(data["command_list"][index]["delay"])
        data["command_list"][index]["delay"] = new_delay
        json_save(data)
        src.reply(systemreturn + '成功将 §b' + name + '§r 的延迟从 §e' + old_delay + '§r 修改至 §d' + str(new_delay) + '§r')
    else:
        src.reply(error_no_script)


@new_thread('qrcmd_process')
def show_script(src : CommandSource, name, num):
    data = json_read()
    index = json_search(name, data)
    if index != -1:
        cmd = data["command_list"][index]["commands"]
        info = str(data["command_list"][index]["info"])
        delay = str(data["command_list"][index]["delay"])
        if info == '':
            info = 'None'

        if len(cmd) < (num - 1) * 5:
            src.reply(error_no_page)
            return 0

        src.reply('§b============§fquick_run_cmd§b============§r')
        src.reply(rtext_cmd('指令延迟: §d' + delay + '§r 秒,§e 描述信息: §r' + info, '点击我运行 §b' + name, '!!qr ' + name))
        src.reply(rtext_cmd('§b' + name + "§r的指令为:", '点击我运行 §b' + name, '!!qr ' + name))
        if len(cmd) == 0:
            src.reply(pline)
            return 0

        for i in range((num - 1) * 5, (num - 1) * 5 + 5):
            src.reply('§a[' + str(i + 1) + ']§r ' + cmd[i])
            if len(cmd) == i + 1:
                src.reply(pline)
                return 0

        src.reply(rtext_cmd('§b============§e点击我去下一页§b============§r', '点击我去下一页', '!!qrcmd showcmd ' + name + ' ' + str(num + 1)))
    else:
        src.reply(error_no_script)


@new_thread('qrcmd_process')
def add_script(src : ServerInterface, name, cmd):
    data = json_read()
    index = json_search(name, data)
    if index != -1:
        data["command_list"][index]["commands"].append(cmd)
        json_save(data)
        src.reply(systemreturn + '成功将§d ' + cmd + '§r 添加至 §b' + name + '§r')
    else:
        src.reply(error_no_script)


@new_thread('qrcmd_process')
def del_script(src : CommandSource, name, num):
    data = json_read()
    index = json_search(name, data)
    if index != -1:
        if num > len(data["command_list"][index]["commands"]) or num == 0:
            src.reply(error_no_page)
            return
        cmd = data["command_list"][index]["commands"][num -1]
        del data["command_list"][index]["commands"][num -1]
        json_save(data)
        src.reply(systemreturn + '成功将 §d' + cmd + '§r 从指令集 §b' + name + '§r中移除')
    else:
        src.reply(error_no_script)


@new_thread('qrcmd_process')
def edit_script(src : CommandSource, name, num, cmd):
    data = json_read()
    index = json_search(name, data)
    if index != -1:
        if num > len(data["command_list"][index]["commands"]) or num == 0:
            src.reply(error_no_page)
            return
        old_cmd = data["command_list"][index]["commands"][num -1]
        data["command_list"][index]["commands"][num -1] = cmd
        json_save(data)
        src.reply(systemreturn + '成功将 §d' + name + '§r 的 §b' + old_cmd + ' §r指令换成§d ' + cmd + '§r')
    else:
        src.reply(error_no_script)


@new_thread('qrcmd_process')
def run_script(server : ServerInterface, player, name):
    data = json_read()
    index = json_search(name, data)
    if index != -1:
        cmd = data["command_list"][index]["commands"]
        for i in range(len(cmd)):
            server.execute(cmd[i])
            time.sleep(float(data["command_list"][index]["delay"]))
        server.tell(player, "成功运行脚本: §b" + name)
    else:
        server.tell(player, error_no_script)


def permission_check(src : CommandSource, cmd):
    if src.get_permission_level() >= permission[cmd]:
        return True
    else:
        return False


def on_info(server : ServerInterface, info : Info):
    if info.content.startswith('!!qr') or info.content.startswith('!!qrcmd'):
        if info.content.endswith('<--[HERE]'):
            info.content = info.content.replace('<--[HERE]','')
        args = info.content.split(' ')
        if args[0] == '!!qr' and len(args) <= 2:
            if len(args) == 1:
                server.reply(info, error_syntax)
            else:
                run_script(server, info.player, args[1])


def register_command(server : ServerInterface):
    server.register_command(
        Literal(prefix).
        runs(lambda src : tell_help(src, 1)).
        on_error(UnknownArgument, lambda src : src.reply(error_unknown_command), handled = True).
        then(
            Literal('help').
            requires(lambda src : permission_check(src, 'help')).
            runs(lambda src : tell_help(src, 1)).
            on_error(RequirementNotMet, lambda src : src.reply(error_permission), handled = True).
            then(
                Integer('num').
                runs(lambda src, cmdict : tell_help(src, cmdict['num'])).
                on_error(InvalidInteger, lambda src : src.reply(error_syntax), handled = True).
                on_error(UnknownArgument, lambda src : src.reply(error_syntax), handled = True)
            )
        ).then(
            Literal('show').
            requires(lambda src : permission_check(src, 'show')).
            runs(lambda src : show_cmd(src, 1)).
            on_error(RequirementNotMet, lambda src : src.reply(error_permission), handled = True).
            then(
                Integer('num').
                runs(lambda src, cmdict : show_cmd(src, cmdict['num'])).
                on_error(InvalidInteger, lambda src : src.reply(error_syntax), handled = True).
                on_error(UnknownArgument, lambda src : src.reply(error_syntax), handled = True)
            )
        ).then(
            Literal('showcmd').
            requires(lambda src : permission_check(src, 'showcmd')).
            on_error(RequirementNotMet, lambda src : src.reply(error_permission), handled = True).
            on_error(UnknownCommand, lambda src : src.reply(error_syntax), handled = True).
            then(
                Text('name').
                runs(lambda src, cmdict : show_script(src, cmdict['name'], 1)).
                then(
                    Integer('num').
                    runs(lambda src, cmdict : show_script(src, cmdict['name'], cmdict['num'])).
                    on_error(InvalidInteger, lambda src : src.reply(error_syntax), handled = True).
                    on_error(UnknownArgument, lambda src : src.reply(error_syntax), handled = True)
                )
            )
        ).then(
            Literal('addcmd').
            requires(lambda src : permission_check(src, 'addcmd')).
            on_error(RequirementNotMet, lambda src : src.reply(error_permission), handled = True).
            on_error(UnknownCommand, lambda src : src.reply(error_syntax), handled = True).
            then(
                Text('name').
                on_error(UnknownCommand, lambda src : src.reply(error_syntax), handled = True).
                then(
                    GreedyText('cmd').
                    runs(lambda src, cmdict : add_script(src, cmdict['name'], cmdict['cmd']))
                )
            )
        ).then(
            Literal('delcmd').
            requires(lambda src : permission_check(src, 'delcmd')).
            on_error(RequirementNotMet, lambda src : src.reply(error_permission), handled = True).
            on_error(UnknownCommand, lambda src : src.reply(error_syntax), handled = True).
            then(
                Text('name').
                on_error(UnknownCommand, lambda src : src.reply(error_syntax), handled = True).
                then(
                    Integer('num').
                    runs(lambda src, cmdict : del_script(src, cmdict['name'], cmdict['num'])).
                    on_error(InvalidInteger, lambda src : src.reply(error_syntax), handled = True).
                    on_error(UnknownArgument, lambda src : src.reply(error_syntax), handled = True)
                )
            )
        ).then(
            Literal('edit').
            requires(lambda src : permission_check(src, 'edit')).
            on_error(RequirementNotMet, lambda src : src.reply(error_permission), handled = True).
            on_error(UnknownCommand, lambda src : src.reply(error_syntax), handled = True).
            then(
                Text('name').
                on_error(UnknownCommand, lambda src : src.reply(error_syntax), handled = True).
                then(
                    Text('new_name').
                    runs(lambda src, cmdict : edit_cmd_name(src, cmdict['name'], cmdict['new_name'])).
                    on_error(UnknownArgument, lambda src : src.reply(error_syntax), handled = True)
                )
            )
        ).then(
            Literal('editcmd').
            requires(lambda src : permission_check(src, 'editcmd')).
            on_error(RequirementNotMet, lambda src : src.reply(error_permission), handled = True).
            on_error(UnknownCommand, lambda src : src.reply(error_syntax), handled = True).
            then(
                Text('name').
                on_error(UnknownCommand, lambda src : src.reply(error_syntax), handled = True).
                then(
                    Integer('num').
                    on_error(InvalidInteger, lambda src : src.reply(error_syntax), handled = True).
                    on_error(UnknownCommand, lambda src : src.reply(error_syntax), handled = True).
                    then(
                        GreedyText('new_cmd').
                        runs(lambda src, cmdict : edit_script(src, cmdict['name'], cmdict['num'], cmdict['new_cmd']))
                    )
                )
            )
        ).then(
            Literal('editinfo').
            requires(lambda src : permission_check(src, 'editinfo')).
            on_error(RequirementNotMet, lambda src : src.reply(error_permission), handled = True).
            on_error(UnknownCommand, lambda src : src.reply(error_syntax), handled = True).
            then(
                Text('name').
                on_error(UnknownCommand, lambda src : src.reply(error_syntax), handled = True).
                then(
                    GreedyText('new_info').
                    runs(lambda src, cmdict : edit_cmd_info(src, cmdict['name'], cmdict['new_info']))
                )
            )
        ).then(
            Literal('editdelay').
            requires(lambda src : permission_check(src, 'editdelay')).
            on_error(RequirementNotMet, lambda src : src.reply(error_permission), handled = True).
            on_error(UnknownCommand, lambda src : src.reply(error_syntax), handled = True).
            then(
                Text('name').
                on_error(UnknownCommand, lambda src : src.reply(error_syntax), handled = True).
                then(
                    Float('new_delay').
                    runs(lambda src, cmdict : edit_cmd_delay(src, cmdict['name'], cmdict['new_delay'])).
                    on_error(InvalidFloat, lambda src : src.reply(error_syntax), handled = True).
                    on_error(UnknownArgument, lambda src : src.reply(error_syntax), handled = True)
                )
            )
        ).then(
            Literal('add').
            requires(lambda src : permission_check(src, 'add')).
            on_error(RequirementNotMet, lambda src : src.reply(error_permission), handled = True).
            on_error(UnknownCommand, lambda src : src.reply(error_syntax), handled = True).
            then(
                Text('name').
                runs(lambda src, cmdict : add_cmd(src, cmdict['name'], '')).
                on_error(UnknownArgument, lambda src : src.reply(error_syntax), handled = True).
                then(
                    GreedyText('new_info').
                    runs(lambda src, cmdict : add_cmd(src, cmdict['name'], cmdict['new_info']))
                )
            )
        ).then(
            Literal('del').
            requires(lambda src : permission_check(src, 'del')).
            on_error(RequirementNotMet, lambda src : src.reply(error_permission), handled = True).
            on_error(UnknownCommand, lambda src : src.reply(error_syntax), handled = True).
            then(
                Text('name').
                runs(lambda src, cmdict : del_cmd(src, cmdict['name'])).
                on_error(UnknownArgument, lambda src : src.reply(error_syntax), handled = True)
            )
        )
    )


def on_load(server : ServerInterface, old):
    if not os.path.isfile(json_path):
        server.logger.info(systemreturn + '正在创建json文件')
        json_save({"command_list" : []})
    register_command(server)
    server.register_help_message(prefix,'一个快速运行自定义脚本的插件(用于配置)')
    server.register_help_message(prefix1,'一个快速运行自定义脚本的插件(用于运行指令)')