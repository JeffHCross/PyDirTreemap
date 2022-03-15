from pathlib import Path
import pandas as pd

directory='/content'

def gen_file_row(f):
  return {'parent':str(f.parent),'type':f.suffix,'size':f.stat().st_size}

def process_dir(d):
  paths = {}
  dir_size = 0
  for p in d.iterdir():
    if p.is_dir():
      res = process_dir(p)
      paths.update(res)
      dir_size += res[str(p)]['size']
    elif p.is_file():
      res = gen_file_row(p)
      paths[str(p)] = res
      dir_size += res['size']
  paths[str(d)]={'parent':str(d.parent),'type':'directory','size':dir_size}
  return paths
  
data=process_dir(Path(directory))
df = pd.DataFrame.from_dict(data, orient='index')
df.reset_index().rename(columns={'index':'path'})
