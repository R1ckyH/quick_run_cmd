# -*- coding: utf-8 -*-
import os
import time

from mcdreforged.api.decorator import new_thread

from quick_run_cmd.utils import *


def get_help_msg(num):
    if num == 0:
        text = p_start + """
""" + help_formatter("!!qr", "", "§b[script_name]§a " + tr("qr"), tr("qr")) + """
""" + help_formatter("!!ql", "", "§e(page)§a " + tr("show"), tr("show")) + """
""" + help_formatter("!!qrcmd", "help", tr("help"), tr("help")) + """
""" + help_formatter("!!qrcmd", "show", "§e(page)§a " + tr("show"), tr("show")) + """
""" + help_formatter("!!qrcmd", "showcmd", "§b[name] §e(page)§a " + tr("showcmd"), tr("showcmd"), "!!qrcmd show") + """
""" + help_formatter("!!qrcmd", "add", "§b[name]§a " + tr("add_script"), tr("add_script"), paste=True) + """
""" + help_formatter("!!qrcmd", "addcmd", "§b[name] §d[command]§a " + tr("addcmd"), tr("addcmd"), paste=True)
    else:
        text = p_start + """
""" + help_formatter("!!qrcmd", "del/remove", "§b[name]§a " + tr("del"), tr("del"), "!!qrcmd del", paste=True) + """
""" + help_formatter("!!qrcmd", "delcmd/removecmd", "§b[name]§a " + tr("delcmd"), tr("delcmd"), "!!qrcmd delcmd", paste=True) + """
""" + help_formatter("!!qrcmd", "edit", "§b[name] §d[new name]§a " + tr("edit"), tr("edit"), paste=True) + """
""" + help_formatter("!!qrcmd", "editdelay", "§b[name] §d[new delay]§a " + tr("editdelay"), tr("editdelay"), paste=True) + """
""" + help_formatter("!!qrcmd", "editcmd", "§b[name] §e[number]§a " + tr("editcmd"), tr("editcmd"), paste=True) + """
""" + help_formatter("!!qrcmd", "editinfo", "§b[name] §d[new info]§a " + tr("editinfo"), tr("editinfo"), paste=True)
    return text


def error_msg(num):
    if num == 0:
        result = error + """Unknown script
""" + rtext_cmd("Type §7!!qrcmd show§r to show script list", "Click me to show script list", "!!qrcmd show")
    elif num == 1:
        result = error + """The script already exist
""" + rtext_cmd("Type §7!!qrcmd show§r to show script detail", "Click me to Show script detail",
                                "!!qrcmd show")
    elif num == 2:
        result = error + """Unknown command
""" + rtext_cmd("Type §7!!qrcmd help§r for more information", "Click me to Show help", "!!qrcmd help")
    elif num == 3:
        result = error + """Syntax error
""" + rtext_cmd("Type §7!!qrcmd help§r for more information", "Click me to Show help", "!!qrcmd help")
    elif num == 4:
        result = error + "You have no Permission to use this command"
    elif num == 5:
        result = error + "No script here"
    else:
        result = error + "404 not found"
    return result


@new_thread("qrcmd")
def tell_help(src: CommandSource, num):
    if num == 0 or num == 1:
        src.reply(get_help_msg(0))
        src.reply(
            rtext_cmd(f'§b========§e{tr("click_msg")} {tr("next_page")}§b========§r', tr("click_msg") + tr("next_page"),
                      "!!qrcmd help 2"))
    elif num == 2:
        src.reply(get_help_msg(1))
        src.reply(p_line)
    else:
        src.reply(error_msg(5))


@new_thread("qrcmd")
def show_cmd(src: CommandSource, num):
    data = json_read()
    if len(data["command_list"]) < (num - 1) * 5:
        src.reply(error_msg(5))
        return 0

    src.reply(p_start)
    if len(data["command_list"]) == 0:
        src.reply(error_msg(6))
        src.reply(p_line)
        return 0
    for i in range((num - 1) * page_list, (num - 1) * page_list + page_list):
        name = data["command_list"][i]["name"]
        description = data["command_list"][i]["info"]

        if description == "":
            description = "None"
        text = "§a[" + str(i + 1) + "]§r §b" + name + "§e Info: §r" + description
        src.reply(rtext_cmd(text, f'{tr("click_msg")} {tr("information")} §b{name}§r', "!!qrcmd showcmd " + name) +
                  rtext_cmd(f'§c[{tr("run")}]', f'§c{tr("click_msg")} {tr("run")}', "!!qr " + name))

        if len(data["command_list"]) == i + 1:
            src.reply(p_line)
            return 0
    src.reply(rtext_cmd(f'§b========§e{tr("click_msg")} {tr("next_page")}§b========§r',
                        tr("click_msg") + tr("next_page"), "!!qrcmd show " + str(num + 1)))


@new_thread("qrcmd_process")
def add_cmd(src: CommandSource, name, new_info):
    data = json_read()
    if json_search(name, data) == -1:
        data["command_list"].append({"name": name, "info": new_info, "delay": delay, "commands": list("")})
        data["command_list"] = sorted(data["command_list"], key=lambda k: k["name"])
        json_save(data)
        if new_info == "":
            new_info = "None"
        src.reply(system_return + tr('success_add', name, new_info))
    else:
        src.reply(error_msg(1))


@new_thread("qrcmd_process")
def del_cmd(src: CommandSource, name):
    data = json_read()
    index = json_search(name, data)
    if index != -1:
        del data["command_list"][index]
        data["command_list"] = sorted(data["command_list"], key=lambda k: k["name"])
        json_save(data)
        src.reply(system_return + tr("success_del", name))
    else:
        src.reply(error_msg(0))


@new_thread("qrcmd_process")
def edit_cmd_name(src: CommandSource, name, new_name):
    data = json_read()
    index = json_search(name, data)
    if index != -1:
        old_name = data["command_list"][index]["name"]
        data["command_list"][index]["name"] = new_name
        json_save(data)
        src.reply(system_return + tr("success_rename", old_name, new_name))
    else:
        src.reply(error_msg(0))


@new_thread("qrcmd_process")
def edit_cmd_info(src: CommandSource, name, new_info):
    data = json_read()
    index = json_search(name, data)
    if index != -1:
        old_info = str(data["command_list"][index]["info"])
        data["command_list"][index]["info"] = new_info
        json_save(data)
        if old_info == "":
            old_info = "None"
        src.reply(system_return + tr("success_editinfo", name, old_info, new_info))
    else:
        src.reply(error_msg(0))


@new_thread("qrcmd_process")
def edit_cmd_delay(src: CommandSource, name, new_delay):
    data = json_read()
    index = json_search(name, data)
    if index != -1:
        old_delay = str(data["command_list"][index]["delay"])
        data["command_list"][index]["delay"] = new_delay
        json_save(data)
        src.reply(system_return + tr("success_editdelay", name, old_delay, str(new_delay)))
    else:
        src.reply(error_msg(0))


@new_thread("qrcmd_process")
def show_script(src: CommandSource, name, num):
    data = json_read()
    index = json_search(name, data)
    if index != -1:
        cmd = data["command_list"][index]["commands"]
        info = str(data["command_list"][index]["info"])
        delay = str(data["command_list"][index]["delay"])
        if info == "":
            info = "None"

        if len(cmd) < (num - 1) * page_cmd:
            src.reply(error_msg(5))
            return 0

        src.reply(p_start)
        src.reply(rtext_cmd(tr("info", delay, info, name), f"{tr('click_msg')} {tr('run')} §b" + name, "!!qr " + name))
        if len(cmd) == 0:
            src.reply(p_line)
            return 0

        for i in range((num - 1) * page_cmd, (num - 1) * page_cmd + page_cmd):
            src.reply("§a[" + str(i + 1) + "]§r " + cmd[i])
            if len(cmd) == i + 1:
                src.reply(p_line)
                return 0

        src.reply(rtext_cmd(f'§b========§e{tr("click_msg")} {tr("next_page")}§b========§r',
                            tr("click_msg") + tr("next_page"), "!!qrcmd showcmd " + name + " " + str(num + 1)))
    else:
        src.reply(error_msg(0))


@new_thread("qrcmd_process")
def add_script(src: CommandSource, name, cmd):
    data = json_read()
    index = json_search(name, data)
    if index != -1:
        data["command_list"][index]["commands"].append(cmd)
        json_save(data)
        src.reply(system_return + tr("success_addcmd", cmd, name))
    else:
        src.reply(error_msg(0))


@new_thread("qrcmd_process")
def del_script(src: CommandSource, name, num):
    data = json_read()
    index = json_search(name, data)
    if index != -1:
        if num > len(data["command_list"][index]["commands"]) or num == 0:
            src.reply(error_msg(5))
            return
        cmd = data["command_list"][index]["commands"][num - 1]
        del data["command_list"][index]["commands"][num - 1]
        json_save(data)
        src.reply(system_return + tr("success_delcmd", cmd, name))
    else:
        src.reply(error_msg(0))


@new_thread("qrcmd_process")
def edit_script(src: CommandSource, name, num, cmd):
    data = json_read()
    index = json_search(name, data)
    if index != -1:
        if num > len(data["command_list"][index]["commands"]) or num == 0:
            src.reply(error_msg(5))
            return
        old_cmd = data["command_list"][index]["commands"][num - 1]
        data["command_list"][index]["commands"][num - 1] = cmd
        json_save(data)
        src.reply(system_return + tr("success_editcmd", old_cmd, cmd, name))
    else:
        src.reply(error_msg(0))


@new_thread("qrcmd_process")
def run_script(server: ServerInterface, player, name):
    data = json_read()
    index = json_search(name, data)
    if index != -1:
        cmd = data["command_list"][index]["commands"]
        for i in range(len(cmd)):
            if cmd[i].startswith("!!"):
                server.execute_command(cmd[i])
            else:
                server.execute(cmd[i])
            time.sleep(float(data["command_list"][index]["delay"]))
        server.tell(player, tr("success_run", name))
    else:
        server.tell(player, error_msg(0))


def permission_check(src: CommandSource, cmd):
    if src.get_permission_level() >= permission[cmd]:
        return True
    else:
        return False


def on_info(server: ServerInterface, info: Info):
    if info.content.startswith("!!qr") or info.content.startswith("!!qrcmd"):
        if info.content.endswith("<--[HERE]"):
            info.content = info.content.replace("<--[HERE]", "")
        args = info.content.split(" ")
        if args[0] == "!!qr" and len(args) <= 2:
            if len(args) == 1:
                server.reply(info, get_help_msg(0))
                server.reply(info, rtext_cmd(f'§b========§e{tr("click_msg")} {tr("next_page")}§b========§r',
                                             tr("click_msg") + tr("next_page"), "!!qrcmd help 2"))
            else:
                run_script(server, info.player, args[1])


def register_command(server: PluginServerInterface):
    server.register_command(
        Literal(PREFIX).
            runs(lambda src: tell_help(src, 1)).
            on_error(UnknownArgument, lambda src: src.reply(error_msg(2)), handled=True).
            then(
            Literal("help").
                requires(lambda src: permission_check(src, "help")).
                runs(lambda src: tell_help(src, 1)).
                on_error(RequirementNotMet, lambda src: src.reply(error_msg(4)), handled=True).
                then(
                Integer("num").
                    runs(lambda src, cmd_dict: tell_help(src, cmd_dict["num"])).
                    on_error(InvalidInteger, lambda src: src.reply(error_msg(3)), handled=True).
                    on_error(UnknownArgument, lambda src: src.reply(error_msg(3)), handled=True)
            )
        ).then(
            Literal("show").
                requires(lambda src: permission_check(src, "show")).
                runs(lambda src: show_cmd(src, 1)).
                on_error(RequirementNotMet, lambda src: src.reply(error_msg(4)), handled=True).
                then(
                Integer("num").
                    runs(lambda src, cmd_dict: show_cmd(src, cmd_dict["num"])).
                    on_error(InvalidInteger, lambda src: src.reply(error_msg(3)), handled=True).
                    on_error(UnknownArgument, lambda src: src.reply(error_msg(3)), handled=True)
            )
        ).then(
            Literal("showcmd").
                requires(lambda src: permission_check(src, "showcmd")).
                on_error(RequirementNotMet, lambda src: src.reply(error_msg(4)), handled=True).
                on_error(UnknownCommand, lambda src: src.reply(error_msg(3)), handled=True).
                then(
                Text("name").
                    runs(lambda src, cmd_dict: show_script(src, cmd_dict["name"], 1)).
                    then(
                    Integer("num").
                        runs(lambda src, cmd_dict: show_script(src, cmd_dict["name"], cmd_dict["num"])).
                        on_error(InvalidInteger, lambda src: src.reply(error_msg(3)), handled=True).
                        on_error(UnknownArgument, lambda src: src.reply(error_msg(3)), handled=True)
                )
            )
        ).then(
            Literal("addcmd").
                requires(lambda src: permission_check(src, "addcmd")).
                on_error(RequirementNotMet, lambda src: src.reply(error_msg(4)), handled=True).
                on_error(UnknownCommand, lambda src: src.reply(error_msg(3)), handled=True).
                then(
                Text("name").
                    on_error(UnknownCommand, lambda src: src.reply(error_msg(3)), handled=True).
                    then(
                    GreedyText("cmd").
                        runs(lambda src, cmd_dict: add_script(src, cmd_dict["name"], cmd_dict["cmd"]))
                )
            )
        ).then(
            Literal("delcmd").
                requires(lambda src: permission_check(src, "delcmd")).
                on_error(RequirementNotMet, lambda src: src.reply(error_msg(4)), handled=True).
                on_error(UnknownCommand, lambda src: src.reply(error_msg(3)), handled=True).
                then(
                Text("name").
                    on_error(UnknownCommand, lambda src: src.reply(error_msg(3)), handled=True).
                    then(
                    Integer("num").
                        runs(lambda src, cmd_dict: del_script(src, cmd_dict["name"], cmd_dict["num"])).
                        on_error(InvalidInteger, lambda src: src.reply(error_msg(3)), handled=True).
                        on_error(UnknownArgument, lambda src: src.reply(error_msg(3)), handled=True)
                )
            )
        ).then(
            Literal("edit").
                requires(lambda src: permission_check(src, "edit")).
                on_error(RequirementNotMet, lambda src: src.reply(error_msg(4)), handled=True).
                on_error(UnknownCommand, lambda src: src.reply(error_msg(3)), handled=True).
                then(
                Text("name").
                    on_error(UnknownCommand, lambda src: src.reply(error_msg(3)), handled=True).
                    then(
                    Text("new_name").
                        runs(lambda src, cmd_dict: edit_cmd_name(src, cmd_dict["name"], cmd_dict["new_name"])).
                        on_error(UnknownArgument, lambda src: src.reply(error_msg(3)), handled=True)
                )
            )
        ).then(
            Literal("editcmd").
                requires(lambda src: permission_check(src, "editcmd")).
                on_error(RequirementNotMet, lambda src: src.reply(error_msg(4)), handled=True).
                on_error(UnknownCommand, lambda src: src.reply(error_msg(3)), handled=True).
                then(
                Text("name").
                    on_error(UnknownCommand, lambda src: src.reply(error_msg(3)), handled=True).
                    then(
                    Integer("num").
                        on_error(InvalidInteger, lambda src: src.reply(error_msg(3)), handled=True).
                        on_error(UnknownCommand, lambda src: src.reply(error_msg(3)), handled=True).
                        then(
                        GreedyText("new_cmd").
                            runs(lambda src, cmd_dict: edit_script(src, cmd_dict["name"], cmd_dict["num"],
                                                                   cmd_dict["new_cmd"]))
                    )
                )
            )
        ).then(
            Literal("editinfo").
                requires(lambda src: permission_check(src, "editinfo")).
                on_error(RequirementNotMet, lambda src: src.reply(error_msg(4)), handled=True).
                on_error(UnknownCommand, lambda src: src.reply(error_msg(3)), handled=True).
                then(
                Text("name").
                    on_error(UnknownCommand, lambda src: src.reply(error_msg(3)), handled=True).
                    then(
                    GreedyText("new_info").
                        runs(lambda src, cmd_dict: edit_cmd_info(src, cmd_dict["name"], cmd_dict["new_info"]))
                )
            )
        ).then(
            Literal("editdelay").
                requires(lambda src: permission_check(src, "editdelay")).
                on_error(RequirementNotMet, lambda src: src.reply(error_msg(4)), handled=True).
                on_error(UnknownCommand, lambda src: src.reply(error_msg(3)), handled=True).
                then(
                Text("name").
                    on_error(UnknownCommand, lambda src: src.reply(error_msg(3)), handled=True).
                    then(
                    Float("new_delay").
                        runs(lambda src, cmd_dict: edit_cmd_delay(src, cmd_dict["name"], cmd_dict["new_delay"])).
                        on_error(InvalidFloat, lambda src: src.reply(error_msg(3)), handled=True).
                        on_error(UnknownArgument, lambda src: src.reply(error_msg(3)), handled=True)
                )
            )
        ).then(
            Literal("add").
                requires(lambda src: permission_check(src, "add")).
                on_error(RequirementNotMet, lambda src: src.reply(error_msg(4)), handled=True).
                on_error(UnknownCommand, lambda src: src.reply(error_msg(3)), handled=True).
                then(
                Text("name").
                    runs(lambda src, cmd_dict: add_cmd(src, cmd_dict["name"], "")).
                    on_error(UnknownArgument, lambda src: src.reply(error_msg(3)), handled=True).
                    then(
                    GreedyText("new_info").
                        runs(lambda src, cmd_dict: add_cmd(src, cmd_dict["name"], cmd_dict["new_info"]))
                )
            )
        ).then(
            Literal("del").
                requires(lambda src: permission_check(src, "del")).
                on_error(RequirementNotMet, lambda src: src.reply(error_msg(4)), handled=True).
                on_error(UnknownCommand, lambda src: src.reply(error_msg(3)), handled=True).
                then(
                Text("name").
                    runs(lambda src, cmd_dict: del_cmd(src, cmd_dict["name"])).
                    on_error(UnknownArgument, lambda src: src.reply(error_msg(3)), handled=True)
            )
        )
    )


def on_load(server: PluginServerInterface, old):
    if not os.path.isfile(json_path):
        server.logger.info(system_return + "creating json file")
        json_save({"command_list": []})
    register_command(server)
    server.register_command(
        Literal(PREFIX2).
            requires(lambda src: permission_check(src, "show")).
            runs(lambda src: show_cmd(src, 1)).
            on_error(RequirementNotMet, lambda src: src.reply(error_msg(4)), handled=True).
            then(
            Integer("num").
                runs(lambda src, cmd_dict: show_cmd(src, cmd_dict["num"])).
                on_error(InvalidInteger, lambda src: src.reply(error_msg(3)), handled=True).
                on_error(UnknownArgument, lambda src: src.reply(error_msg(3)), handled=True)
        )
    )
    server.register_help_message(PREFIX, tr("main_msg"))
    server.register_help_message(PREFIX1, tr("main_msg2"))
