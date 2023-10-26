import re

PAT = r'^[a-zA-Z0-9]*$'
print(bool(re.match(PAT, 'asdA11/')))