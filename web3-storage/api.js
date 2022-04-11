import {Web3Storage, getFilesFromPath} from 'web3.storage';
import axios, * as others from 'axios';
import * as fs from 'fs';
// import dotenv from 'dotenv';

// dotenv.config();
// const apiToken = process.env.API_TOKEN;
const apiToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaWQ6ZXRocjoweDMxOTA3ZmEzQjMxOEE2ODk4ZTI4MDZDOGM3NWYyMEY1RjI0RUIyNTkiLCJpc3MiOiJ3ZWIzLXN0b3JhZ2UiLCJpYXQiOjE2NDkyNTg2OTA0NjUsIm5hbWUiOiJUZXN0X0FQSSJ9.xACTkv2Y6jDkuY25W-YtGpc2F4wyVlH2k3RhtqcOoJw";
const args = process.argv.slice(2);
const client = new Web3Storage({token: apiToken});

function toBuffer(ab) {
    const buf = Buffer.alloc(ab.byteLength);
    const view = new Uint8Array(ab);
    for (let i = 0; i < buf.length; ++i) {
        buf[i] = view[i];
    }
    return buf;
}

async function getLinks(folderIPFSPath) {
    axios({
        method: 'get',
        url: `https://dweb.link/api/v0/ls?arg=${folderIPFSPath}`,
    }).then(res => {
        console.log(res.data["Objects"][0]["Links"][0]["Hash"])
    }).catch(error => console.error(error));
}

async function uploadFiles(path) {
    let folder_cid = '', files = [];
    for(let i=0; i<path.length; i++)
        files.push(... await getFilesFromPath(path[i]));
    const onRootCidReady = cid => folder_cid = cid;
    await client.put(files, {onRootCidReady, maxRetries: 1, wrapWithDirectory: true});
    await getLinks(folder_cid);
}

async function downloadFile(cid, path) {
    const res = await client.get(cid);

    if(res == undefined)
        return 0;
    const files = await res.files();
    for (const file of files) {
        console.log(await file.text())
        const arrBuf = await file.arrayBuffer();
        const buf = toBuffer(arrBuf);
        fs.writeFile(path, buf, err => {
            if(err)
                throw err;
        });
    }
}

// async function downloadFiles(info) {
//     let success = true;
//     for(let i=0; i<info.length && success; i+=2)
//         success &&= await downloadFile(info[i], info[i+1]);
// }

if(args[0] == 'upload')
  await uploadFiles(args.slice(1));
else if(args[0] == 'download')
  await downloadFile(args[1], args[2]);
else {
    console.error("Unknown argument passed: " + args[0]);
    process.exit(1);
}