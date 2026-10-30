/* State/race coverage without relying on a particular browser's transition implementation. */
const assert=require('node:assert/strict'),vm=require('node:vm'),fs=require('node:fs'),path=require('node:path');
const dir=__dirname,init=fs.readFileSync(path.join(dir,'theme-init.js'),'utf8'),runtime=fs.readFileSync(path.join(dir,'theme.js'),'utf8');
function fixture({saved=null,dark=false,reduced=false,blocked=false,api=true,fail=''}={}){
 const events={},handlers={},classes=new Set(),attrs={},calls=[],store=new Map(saved===null?[]:[['portfolio-theme-v2',saved]]),media={};
 for(const [name,matches] of [['(prefers-color-scheme:dark)',dark],['(prefers-reduced-motion:reduce)',reduced]])media[name]={matches,addEventListener:(key,fn)=>events[name]=fn};
 const root={dataset:{},style:{},offsetWidth:100,classList:{add:c=>classes.add(c),remove:c=>classes.delete(c)}};
 const button={setAttribute:(k,v)=>attrs[k]=v,getAttribute:k=>attrs[k],querySelector:()=>null,getBoundingClientRect:()=>({left:100,top:20,width:58,height:44}),addEventListener:(key,fn)=>handlers[key]=fn};
 let finish;root.animate=(frames,options)=>{calls.push({frames,options});let resolve;const finished=new Promise(r=>resolve=r);finish=resolve;return{finished,cancel:resolve}};
 const document={documentElement:root,querySelectorAll:s=>s==='[data-theme-toggle]'?[button]:[],querySelector:()=>({content:''})};
 if(api)document.startViewTransition=fn=>{if(fail==='start')throw Error('unavailable');const updateCallbackDone=Promise.resolve().then(fn);return{updateCallbackDone,ready:fail==='ready'?updateCallbackDone.then(()=>{throw Error('skipped')}):updateCallbackDone,finished:updateCallbackDone.then(()=>{}),skipTransition:()=>finish?.()}};
 const window={};const timers=[];const context={document,window,matchMedia:name=>media[name],innerWidth:1000,innerHeight:800,setTimeout:fn=>(timers.push(fn),timers.length),clearTimeout:()=>{},addEventListener:(name,fn)=>events[name]=fn,localStorage:{getItem:k=>{if(blocked)throw Error('blocked');return store.get(k)??null},setItem:(k,v)=>{if(blocked)throw Error('blocked');store.set(k,v)}}};
 vm.createContext(context);vm.runInContext(init,context);const initial=root.dataset.theme;vm.runInContext(runtime,context);
 return{root,attrs,calls,store,initial,classes,click:()=>handlers.click(),finish:()=>finish?.(),media,events,timers};
}
const flush=async()=>{for(let i=0;i<15;i++)await Promise.resolve()};
(async()=>{
 for(const saved of [null,'system','invalid']){const f=fixture({saved,dark:true});assert.equal(f.initial,'dark');assert.equal(f.store.get('portfolio-theme-v2'),saved??undefined)}
 assert.equal(fixture({saved:'light',dark:true}).initial,'light');assert.equal(fixture({blocked:true,dark:true}).initial,'dark');
 const f=fixture();f.click();await flush();assert.equal(f.root.dataset.theme,'dark');assert.equal(f.attrs['aria-pressed'],'true');assert.equal(f.attrs['aria-label'],'Switch to light mode');assert.equal(f.calls[0].options.duration,500);assert.match(f.calls[0].frames.clipPath[0],/129px 42px/);
 // Three activations during a reveal resolve to the last intended choice.
 f.click();f.click();f.click();f.finish();await flush();assert.equal(f.root.dataset.theme,'light');f.finish();await flush();assert.equal(f.store.get('portfolio-theme-v2'),'light');assert.equal(f.classes.has('theme-revealing'),false);
 for(const fail of ['start','ready']){const a=fixture({fail});a.click();await flush();assert.equal(a.root.dataset.theme,'dark');assert.equal(a.classes.has('theme-revealing'),false);a.click();await flush();assert.equal(a.root.dataset.theme,'light')}
 const fallback=fixture({api:false});fallback.click();await flush();assert.equal(fallback.root.dataset.theme,'dark');assert.equal(fallback.classes.has('theme-color-fade'),true);fallback.timers.at(-1)();assert.equal(fallback.classes.has('theme-color-fade'),false);
 const r=fixture({reduced:true,blocked:true});r.click();await flush();assert.equal(r.root.dataset.theme,'dark');assert.equal(r.calls.length,0);
 const s=fixture();s.media['(prefers-color-scheme:dark)'].matches=true;s.events['(prefers-color-scheme:dark)']();await flush();assert.equal(s.root.dataset.theme,'dark');assert.equal(s.calls.length,0);s.click();await flush();s.finish();await flush();s.events['(prefers-color-scheme:dark)']();await flush();assert.equal(s.root.dataset.theme,'light');
 const c=fixture();c.click();await flush();c.events.storage({key:'portfolio-theme-v2',newValue:'light'});await flush();assert.equal(c.root.dataset.theme,'light');assert.equal(c.classes.has('theme-revealing'),false);assert.equal(c.calls.length,1);
 const m=fixture();m.click();await flush();m.media['(prefers-reduced-motion:reduce)'].matches=true;m.events['(prefers-reduced-motion:reduce)']();await flush();assert.equal(m.root.dataset.theme,'dark');assert.equal(m.classes.has('theme-revealing'),false);
 console.log('Passed: first paint, saved/system/invalid preferences, blocked storage, rapid clicks, keyboard origin, API failures, fallback, reduced motion, system changes and cross-tab interruption.');
})().catch(error=>{console.error(error);process.exitCode=1});
