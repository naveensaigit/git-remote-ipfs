from sys import stderr

from git_remote_ipfs.metadata import *
from git_remote_ipfs.util import stderr
from subprocess import check_output
import os
import json
import requests

class APIHandler:
  def __init__(self):
    self.metapath = os.path.join(os.getcwd(), ".dgit")
    self.metadata = json.load(open(self.metapath))

  def files_download_obj(self, path):
    filename = path.split("/")[-1]
    cid = GetCID(self.metadata, path)
    resp = requests.get("https://nftstorage.link/ipfs/" + cid)
    out = resp.content
    return 0, out

  def files_download_ref(self, path):
    filename = path.split("/")[-1]
    cid = GetCID(self.metadata, path)
    out = requests.get("https://nftstorage.link/ipfs/" + cid).content.decode("utf-8")
    return 0, out
  
  def file_upload(self, path):
    f_data = {'file': open(path, 'rb')}
    headers = {"Authorization": f"Bearer {os.environ.get('WEB3_API_TOKEN')}"}
    resp = requests.post("https://api.web3.storage/upload", headers=headers, files=f_data)
    stderr(f"Response: {resp.content.decode('utf-8')}")
    cid = json.loads(resp.content.decode('utf-8'))['cid']
    stderr(f"File CID: {cid}")
    return cid

  def files_upload(self, path):
    GeneratePath(self.metadata, path)
    cid = self.file_upload(path)
    UpdateCID(self.metadata, path, cid)

  def save_meta(self):
    json.dump(self.metadata, open(self.metapath, "w"), indent=4, sort_keys=True)
    self.file_upload(self.metapath)

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


# obj = APIHandler("djakglj")
# metadata = {"root": {"folder1": {}, "folder2": {"file1": "cid1", "file2": "cid2"}, "file3": "cid"}}
# obj.metadata = metadata
# print(obj.files_list_folder("root"))
# obj.files_delete("root/folder1/")
# print(obj.metadata)
# print(obj.files_list_folder("root/folder2"))
# obj.files_delete("root/folder2/file1")
# print(obj.files_list_folder("root/folder2"))