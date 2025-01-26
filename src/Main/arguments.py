def get_arguments(text: str):
    splitted = list(map(lambda x:x.strip(), text.replace("\n", "").strip().split()))

    cmd = splitted[0]
    arguments = dict()

    for arg in splitted[1:]:
        arg = arg[2:]
        if arg.count('=') != 0:
            eq_splitted = arg.split('=')
            arguments[eq_splitted[0]] = " ".join(eq_splitted[1:])
        else:
            arguments[arg] = True
    
    return {
        "command": cmd,
        "arguments": arguments
    }

def check_arg(arguments: dict, arg: str) -> bool:
    return arg in arguments