# quick_run_cmd
-----
[中文](https://github.com/rickyhoho/quick_run_cmd/blob/master/README_cn.md)

A plugin for [MCDReforged1.x](https://github.com/Fallen-Breath/MCDReforged) which can run command script quickly in server.

Type `!!qrcmd` or `!!qr` to see the help page

You may fill configure file `MCDR/config/quick_run_cmd.json` to edit it or edit by `!!qrcmd`

# permission

`user` or above permission can use script and check for script list

`helper` or above permission can use all of the command

# config
-----
If you dont have any knowledge about json, then dont edit it.

`"command_list"`   The script list
|name|type|example|funtion|
|---|---|---|---|
|"name"|`str`|`"whp"`|The name of script|
|"info"|`str`|`"testing"`|The info of script|
|"delay"|`float`|`"0.5"`|The dealy of running command|
|"commands"|`list`|`"player alex spawn"`, `"player alex use"`|The command list of script|
