# quick_run_cmd
-----
[English](https://github.com/rickyhoho/quick_run_cmd/blob/master/README.md)

一个用于 [MCDReforged](https://github.com/Fallen-Breath/MCDReforged) 快速运行命令的插件
输入 `!!qrcmd` 或 `!!qr` 去查看帮助页面
你可以在 `MCDR/config/quick_run_cmd.json` 修改配置文件，或者使用 `!!qrcmd` 修改配置（建议小白使用命令）

# permission

`user` 以上的权限可以运行脚本和查看脚本列表
  
`helper` 以上的权限可以使用所有插件内容，包括修改配置
  
# config
-----
如果你没有任何关于json的知识，建议`不要`修改任何json，请使用`!!qrcmd`来配置

`"command_list"`   脚本列表
|name|type|example|funtion|
|---|---|---|---|
|"name"|`str`|`"whp"`|脚本名|
|"info"|`str`|`"testing"`|脚背描述|
|"delay"|`float`|`"0.5"`|运行脚本延迟|
|"commands"|`list`|`"player alex spawn"`, `"player alex use"`|脚本命令列表|
