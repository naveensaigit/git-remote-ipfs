from sys import stderr

from git_remote_ipfs.metadata import *
from git_remote_ipfs.util import stderr
from subprocess import check_output
import os
import json
import codecs

class APIHandler:
  def __init__(self):
    # out = check_output(("node", "D:/dgit/git-remote-ipfs/web3-storage/api.js", "download", metaCID)).decode("utf-8")
    self.metapath = os.path.join(os.getcwd(), ".dgit")
    self.metadata = json.load(open(self.metapath))

  def files_download(self, path):
    filename = path.split("/")[-1]
    cid = GetCID(self.metadata, path)
    out = check_output(("node", "D:/dgit/git-remote-ipfs/web3-storage/api.js", "download", cid, "D:/tmp2/"+filename))
    f = codecs.open("D:/tmp2/"+filename, mode='rb', encoding="utf-8", errors="ignore")
    out = f.read()
    f.close()
    return 0, out

  def files_upload(self, path):
    GeneratePath(self.metadata, path)
    out = check_output(("node", "D:/dgit/git-remote-ipfs/web3-storage/api.js", "upload", path)).decode("utf-8")
    UpdateCID(self.metadata, path, out[:-1])

  def save_meta(self):
    json.dump(self.metadata, open(self.metapath, "w"), indent=4, sort_keys=True)
    out = check_output(("node", "D:/dgit/git-remote-ipfs/web3-storage/api.js", "upload", self.metapath)).decode("utf-8")
    stderr(f"META CID: {out}")

  def files_delete(self, path):
    path = path.strip("/").split("/")
    filename = path[-1]
    path = '/'.join(path[:-1])
    end = TraversePath(self.metadata, path)

    end.pop(filename, None)
  
  def files_list_folder(self, path):
    end = TraversePath(self.metadata, path)
    files = []

    for i in end:
      if type(end[i]) == str:
         files.append(path + "/" + i)
      else:
        files.extend(self.files_list_folder(path + "/" + i))
    return files

  def update_meta(self, path):
    pass

# obj = APIHandler("djakglj")
# metadata = {"root": {"folder1": {}, "folder2": {"file1": "cid1", "file2": "cid2"}, "file3": "cid"}}
# obj.metadata = metadata
# print(obj.files_list_folder("root"))
# obj.files_delete("root/folder1/")
# print(obj.metadata)
# print(obj.files_list_folder("root/folder2"))
# obj.files_delete("root/folder2/file1")
# print(obj.files_list_folder("root/folder2"))