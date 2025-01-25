class EmptyClass:
    def __init__(self):
        pass

    def __getitem__(self, key):
        return self._empty_list[key]

    def __setitem__(self, key, value):
        pass

    def __delitem__(self, key):
        pass

    def __iter__(self):
        return iter([])

    def __contains__(self, item):
        return False

    def __call__(self):
        return None

    def __eq__(self, other):
        return isinstance(other, EmptyClass)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        return False

    def __lt__(self, other):
        return False

    def __ge__(self, other):
        return self.__eq__(other)

    def __le__(self, other):
        return self.__eq__(other)
    
    def __str__(self):
        return ""

    @property
    def __dict__(self):
        return dict()



def null_wrapper(value):
    return value if value is not None else EmptyClass()

def wrap_json_escape(data: str):
    out = data.\
        replace('\\', '\\\\').\
        replace('"', '\\"').\
        replace('\r', '\\r').\
        replace('\t', '\\t').\
        replace('\n', '\\n')
    return out

def json_str(
        data, 
        indent_size=4, 
        exclude_keys = [], 
        indent=0, 
        start_indent=0, 
        is_first: bool = True,
        no_start_letter: bool = False):
    if isinstance(data, dict) and len(data) == 0:
        return '{}'

    if not no_start_letter:
        if is_first:
            o = f"{' '*(indent_size*start_indent)}"+'{' + f'\n' 
        else:
            o = '{'+ f'\n' 
    else:
        o = ''
    for k, v in data.items():
        if not (k in exclude_keys):
            o += f"{' '*(indent_size*(indent+1))}"+'"'+str(k)+'": '
            if isinstance(v, dict):
                o += json_str(v, indent_size=indent_size, exclude_keys=exclude_keys, indent=indent+2, is_first=False, start_indent=start_indent) + ',\n'
            elif isinstance(v, list):
                o += json_str({
                    i: item for i, item in enumerate(v)
                }, indent_size=indent_size, exclude_keys=exclude_keys, indent=indent+2, is_first=False, start_indent=start_indent) + ',\n'
            else:
                o += '"' + wrap_json_escape(str(v)) + '",\n'

    

    end = f""
    if not no_start_letter:
        if o[-2] == ',':
            o = o[:-2]+'\n'

        end = f"{' '*(indent_size*max(indent-1, start_indent))}" + '}'

    else:
        if o[-2] == ',':
            o = o[:-2]

    return o + end