def find_command(command_name, command):
    list_command = {"man":      "#!/bin/bash\n"
                                "MAN_KEEP_FORMATTING=1 COLUMNS=80 " + command +
                                " | ul | aha | html2text -width 999 > output.txt",

                    "normal":   "#!/bin/bash\n"
                                "script test.log -q -c " + "\"" + command + "\""
                                "\ncat test.log | aha |  html2text -width 999 > output.txt",
                    }
    return list_command[command_name] if command_name in list_command.keys() else list_command["normal"]


non_supported_command = ["htop"]
