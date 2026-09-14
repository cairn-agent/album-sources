// Headless functional check of the local player's selection and next-track logic.
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
const root=path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const html=fs.readFileSync(path.join(root,'index.html'),'utf8');
for(const match of html.matchAll(/(?:src|href)="([^"]+)"/g)){
  assert(!/^https?:/.test(match[1]),'Unexpected remote resource');
  assert(fs.existsSync(path.join(root,match[1])),'Broken local link: '+match[1]);
}
let plays=0;
const audio={handlers:{},addEventListener(n,fn){this.handlers[n]=fn;},play(){plays++;return Promise.resolve();}};
const buttons=Array.from({length:8},()=>({handlers:{},attrs:{},classList:{toggle(){}},setAttribute(k,v){this.attrs[k]=v;},addEventListener(n,fn){this.handlers[n]=fn;}}));
const now={textContent:''},download={href:''};
const document={getElementById(id){return {audio,now,download}[id];},querySelectorAll(){return buttons;}};
const script=html.match(/<script>([\s\S]*?)<\/script>/)[1];
vm.runInNewContext(script,{document});
assert.equal(plays,0,'Player must not autoplay on opening');
assert(audio.src.includes('01-carrier-at-midnight'));
buttons[6].handlers.click();
assert(audio.src.includes('07-the-last-train-is-a-satellite'));
assert.equal(download.href,audio.src);
audio.handlers.ended();
assert(audio.src.includes('08-daybreak-without-an-answer'));
const before=plays;audio.handlers.ended();assert.equal(plays,before,'End of album must stop');
assert.equal(buttons[7].attrs['aria-pressed'],'true');
fs.writeFileSync(path.join(root,'checks','player-test.json'),JSON.stringify({passed:true,tests:['all links local and existing','no autoplay','track selection','download selection','advance to next track','stop after final track','accessible selected state']},null,2)+'\n');
console.log('Local player: all seven functional checks passed.');
