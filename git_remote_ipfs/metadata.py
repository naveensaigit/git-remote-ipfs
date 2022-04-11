import json

def ReadData(path):
  file = open(path, "r")
  metadata = json.load(file)
  file.close()
  print("Metadata loaded!")
  return metadata

def SaveData(metadata, path):
  file = open(path, "w")
  json.dump(metadata, file)
  print("Metadata saved!")
  file.close()

def CheckPath(metadata, path):
  path = path.strip("/")
  tokens = path.split("/")
  temp = metadata
  for tok in tokens:
    if tok in temp.keys():
      temp = temp[tok]
    else:
      return False
  return True

def TraversePath(metadata, path):
  path = path.strip("/")
  tokens = path.split("/")
  temp = metadata
  for tok in tokens:
    temp = temp[tok]
  return temp

def AddFile(metadata, path, cid = "default_cid"):
  path = path.strip("/")

  filename = path.split("/")[-1]
  path = "/".join(path.split("/")[:-1])

  if not CheckPath(metadata, path):
    raise RuntimeError(f"Path {path} does not exist!")
  end = TraversePath(metadata, path)
  end[filename] = cid
  print(f"File {filename} added!")

def AddFolder(metadata, path):
  path = path.strip("/")

  foldername = path.split("/")[-1]
  path = "/".join(path.split("/")[:-1])

  if not CheckPath(metadata, path):
    raise RuntimeError(f"Path {path} does not exist!")
  end = TraversePath(metadata, path)
  end[foldername] = {}
  print(f"Folder {foldername} added!")

def GeneratePath(metadata, path, file = True):
  path = path.strip("/")
  tokens = path.split("/")
  temp = metadata

  for i in range(len(tokens)-1):
    if tokens[i] not in temp.keys():
      temp[tokens[i]] = {}
    temp = temp[tokens[i]]

  if file:
    temp[tokens[-1]] = "default_cid"
  else:
    temp[tokens[-1]] = {}

def UpdateCID(metadata, path, new_cid):
  path = path.strip("/")
  filename = path.split("/")[-1]
  path = "/".join(path.split("/")[:-1])

  if not CheckPath(metadata, path):
    raise RuntimeError(f"Path {path} does not exist!")
  
  end = TraversePath(metadata, path)
  end[filename] = new_cid

def GetCID(metadata, path):
  path = path.strip("/")
  filename = path.split("/")[-1]
  path = "/".join(path.split("/")[:-1])

  if not CheckPath(metadata, path):
    raise RuntimeError(f"Path {path} does not exist!")
  
  end = TraversePath(metadata, path)
  return end[filename]
