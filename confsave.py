#
# Copyright (c) 2020 unendingPattern (unendingpattern.github.io) <kei.trei.a52@gmail.com>
#
# Everyone is permitted to copy and distribute verbatim or modified
# copies of this license document, and changing it is allowed as long
# as the name is changed.
#
# DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
# TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
#
# 0. You just DO WHAT THE FUCK YOU WANT TO.
#

#
# confsave.py
#   Save non-default config variables to a file in various formats.
#   Note: will attempt to exclude plaintext passwords.
#
# Usage:
#   /confsave [filename] [format]
#
#   filename: target file (must not exist)
#   format: raw, markdown or commands
#
# History:
#   2020-04-01, unendingPattern <kei.trei.a52@gmail.com>
#       version 0.1: initial release
#

try:
    import weechat as w
except Exception:
    print("This script must be run under WeeChat.")
    print("Get WeeChat now at: https://weechat.org")
    quit()
from os.path import exists

SCRIPT_NAME    = "confsave"
SCRIPT_AUTHOR  = "unendingPattern <kei.trei.a52@gmail.com>"
SCRIPT_LINK    = "https://github.com/unendingPattern/weechat-confsave"
SCRIPT_VERSION = "0.1"
SCRIPT_LICENSE = "WTFPL"
SCRIPT_DESC    = "Save non-default config variables to a file in various formats."
SCRIPT_COMMAND = SCRIPT_NAME


if w.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION, SCRIPT_LICENSE, SCRIPT_DESC, "", ""):
    w.hook_command(SCRIPT_COMMAND,
            SCRIPT_DESC + "\nnote: will attempt to exclude plaintext passwords.",
            "[filename] [format]",
            "   filename: target file (must not exist)\n   format: raw, markdown or commands\n",
            "%f",
            "confsave_cmd",
            '')

def confsave_cmd(data, buffer, args):
    args = args.split(" ")
    filename_raw = args[0]
    output_format = args[1]
    acceptable_formats = ["raw", "markdown", "commands"]
    output = ""
    currentheader = ""
    lastheader = ""
        
    if not filename_raw:
        w.prnt('', 'Error: filename not specified!')
        w.command('', '/help %s' %SCRIPT_COMMAND)
        return w.WEECHAT_RC_OK

    if output_format not in acceptable_formats:
        w.prnt('', 'Error: format incorrect or not specified!')
        w.command('', '/help %s' %SCRIPT_COMMAND)
        return w.WEECHAT_RC_OK
    
    filename = w.string_eval_path_home(filename_raw, {}, {}, {})
    infolist = w.infolist_get("option", "", "")
    variable_dict = {}
    if infolist:
        while w.infolist_next(infolist):
            infolist_name = w.infolist_string(infolist, "full_name")
            infolist_default = w.infolist_string(infolist, "default_value")
            infolist_value = w.infolist_string(infolist, "value")
            infolist_type = w.infolist_string(infolist, "type")
            if infolist_value != infolist_default:
                variable_dict[infolist_name] = {}
                variable_dict[infolist_name]['main'] = infolist_name.split(".")[0]
                variable_dict[infolist_name]['name'] = infolist_name
                variable_dict[infolist_name]['value'] = infolist_value
                variable_dict[infolist_name]['type'] = infolist_type
        w.infolist_free(infolist)

    if output_format == "markdown":
        output += "## weechat configuration"
        output += "\n*automatically generated using [" + SCRIPT_NAME + ".py](" + SCRIPT_LINK + ")*"
    # w.prnt("", str(variable_dict.values())) # debug
    for config in variable_dict.values():
        if output_format == "markdown":
            currentheader = config['main']
            if not ("password" in config['name']) and ("sec.data" not in config['value']):
                if currentheader != lastheader:
                    output += "\n### " + config['main']
                    lastheader = currentheader

        if not ("password" in config['name']) and ("sec.data" not in config['value']):
            write_name = config['name']
            if config['type'] == "string":
                write_value = "\"" + config['value'] + "\""
            else:
                write_value = config['value']
            if output_format == "markdown":
                output += "\n\t/set " + write_name + " " + write_value
            if output_format == "raw":
                output += "\n" + write_name + " = " + write_value
            if output_format == "commands":
                output += "\n/set " + write_name + " " + write_value
    output += "\n"
    # w.prnt("", "\n" + output) # debug

    if exists(filename):
        w.prnt('', 'Error: target file already exists!')
        return w.WEECHAT_RC_OK

    try:
        fp = open(filename, 'w')
    except:
        w.prnt('', 'Error writing to target file!')
        return w.WEECHAT_RC_OK

    # w.prnt("", "\n" + output)
    fp.write(output)
    w.prnt("", "\nSuccessfully outputted to " + filename + " as " + output_format + "!")

    fp.close()

    return w.WEECHAT_RC_OK
