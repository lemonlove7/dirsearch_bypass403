
from lib.core.options import parse_options

if (parse_options()['bypass']) ==None:
    exit(1)
print("".join(parse_options()['bypass']))