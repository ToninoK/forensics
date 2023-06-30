import os
import pandas as pd
import hashlib
import magic
import mimetypes


search_hash = "c15e32d27635f248c1c8b66bb012850e5b342119"

FILEPATH = "./Dokaz"

filenames = []
extensions = []
md5s = []
sha1s = []
sha256s = []
magic_numbers = []
extension_matches = []

magico = magic.Magic()

for item in os.listdir(FILEPATH):
    if not os.path.isfile(os.path.join(FILEPATH, item)):
        continue
    extensions.append(os.path.splitext(item)[1])
    filenames.append(item)
    md5s.append(hashlib.md5(open(os.path.join(FILEPATH, item), 'rb').read()).hexdigest())
    sha1s.append(hashlib.sha1(open(os.path.join(FILEPATH, item), 'rb').read()).hexdigest())
    sha256s.append(hashlib.sha256(open(os.path.join(FILEPATH, item), 'rb').read()).hexdigest())
    magic_numbers.append(magico.from_file(os.path.join(FILEPATH, item)))

    # check if the magic number contains the file extension
    if os.path.splitext(item)[1] in magico.from_file(os.path.join(FILEPATH, item)):
        extension_matches.append(True)
    else:
        extension_matches.append(False)

# Search the dataframe for the hash

# create a Pandas dataframe with the file names
df = pd.DataFrame({'file_name': filenames, "extension": extensions, "md5": md5s, "sha1": sha1s, "sha256": sha256s, "real_type": magic_numbers, "extension_matches": extension_matches})

print(df[df['md5'] == search_hash])
print(df[df['sha1'] == search_hash])
print(df[df['sha256'] == search_hash])