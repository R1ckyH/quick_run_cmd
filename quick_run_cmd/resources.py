plugin = 'quick_run_cmd'
PREFIX = '!!qrcmd'
PREFIX1 = '!!qr'
PREFIX2 = '!!ql'


delay = 0.5
page_cmd = 5
page_list = 5
json_path = "config/" + plugin + ".json"

system_return = f"""§b[§r{plugin}§b] §r"""
error = system_return + """§cError: """

p_start = f"""§b============§f{plugin}§b============§r"""
p_line = "§b=====================================§r"

permission = {
    "help": 1,
    "show": 1,
    "showcmd": 1,
    "add": 2,
    "addcmd": 2,
    "del": 2,
    "delcmd": 2,
    "edit": 2,
    "editcmd": 2,
    "editdelay": 2,
    "editinfo": 2,
}