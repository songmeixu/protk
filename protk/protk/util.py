def get_arg_param(arg):
    parts = arg.split('=')
    if len(parts) > 2:
        return '='.join(parts[1:])
    elif len(parts) == 1:
        return None
    else:
        return parts[1]
