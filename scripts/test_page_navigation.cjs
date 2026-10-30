const assert=require('node:assert/strict'),vm=require('node:vm'),fs=require('node:fs'),path=require('node:path');
const source=fs.readFileSync(path.join(__dirname,'page-navigation.js'),'utf8');
function page(name='index.html',{store=new Map(),reduced=false,blocked=false}={}){
 const handlers={},classes=new Set(),animations=[],focus=[],frames=[];
 const media={matches:reduced,addEventListener:(name,fn)=>handlers.reduced=fn};
 const root={dataset:{},classList:{add:(...names)=>names.forEach(n=>classes.add(n)),remove:(...names)=>names.forEach(n=>classes.delete(n)),contains:n=>classes.has(n),toggle:(n,on)=>on?classes.add(n):classes.delete(n)}};
 const heading={setAttribute:()=>{},focus:options=>focus.push(options)};
 const main={animate:(...args)=>{animations.push(args);return{finished:Promise.resolve(),finish:()=>{}}}};
 const location={origin:'https://example.org',href:'https://example.org/'+name,pathname:'/'+name,hash:''};
 const context={document:{documentElement:root,addEventListener:(name,fn)=>handlers[name]=fn,querySelector:s=>s==='main h1'?heading:s==='main'?main:null},location,window:{},matchMedia:()=>media,URL,Date,sessionStorage:{getItem:key=>{if(blocked)throw Error('unavailable');return store.get(key)??null},setItem:(key,value)=>{if(blocked)throw Error('unavailable');store.set(key,value)},removeItem:key=>{if(blocked)throw Error('unavailable');store.delete(key)}},addEventListener:(name,fn)=>handlers[name]=fn,requestAnimationFrame:fn=>frames.push(fn)};
 vm.createContext(context);vm.runInContext(source,context);
 function click(href,extras={}){let prevented=false;const link={href:new URL(href,location.href).href,target:'',hasAttribute:()=>false,...extras.link};handlers.click({target:{closest:()=>link},button:0,defaultPrevented:false,preventDefault:()=>prevented=true,...extras});assert.equal(prevented,false,'links must never be intercepted')}
 return{handlers,classes,animations,focus,store,location,media,click,frames,window:context.window};
}
function transition(){let finish;return{skipped:false,skipTransition(){this.skipped=true;finish?.()},finished:new Promise(r=>finish=r),finish:()=>finish()}}
const flush=async()=>{for(let i=0;i<8;i++)await Promise.resolve()};
(async()=>{
 const out=page();out.click('about.html');assert.equal(JSON.parse(out.store.get('ariful-page-navigation')).to,'about');const t=transition();out.handlers.pageswap({viewTransition:t,activation:{entry:{url:'https://example.org/about.html'},navigationType:'push'}});assert(out.classes.has('nav-signature'));assert(!t.skipped);
 const incoming=page('about.html',{store:out.store}),v=transition();incoming.handlers.pagereveal({viewTransition:v});assert(incoming.classes.has('nav-signature'));assert(!incoming.classes.has('nav-signature-repeat'));v.finish();await flush();assert(!incoming.classes.has('nav-signature'));assert.equal(incoming.focus.length,1);
 incoming.click('projects.html');const repeat=page('projects.html',{store:incoming.store}),r=transition();repeat.handlers.pagereveal({viewTransition:r});assert(repeat.classes.has('nav-signature-repeat'));r.finish();await flush();
 for(const [href,extras] of [['about.html#education',{}],['https://elsewhere.org/about.html',{}],['projects-smart.html',{}],['about.html',{ctrlKey:true}],['about.html',{button:1}],['about.html',{link:{target:'_blank'}}],['assets/cv.pdf',{link:{hasAttribute:()=>true}}],['index.html',{}]]){const p=page();p.click(href,extras);assert(!p.store.has('ariful-page-navigation'),href)}
 const hashed=page('about.html');hashed.location.href+='\u0023experience';hashed.location.hash='#experience';hashed.click('projects.html');assert(hashed.store.has('ariful-page-navigation'));
 const alias=page('');alias.click('index.html');assert(!alias.store.has('ariful-page-navigation'));
 const fast=page();fast.click('about.html');fast.click('projects.html');assert.equal(JSON.parse(fast.store.get('ariful-page-navigation')).skip,true);
 const back=page('about.html',{store:incoming.store}),b=transition();back.handlers.pagereveal({viewTransition:b,activation:{navigationType:'traverse'}});assert(b.skipped);back.handlers.pageshow({persisted:true});assert.equal(back.focus.length,0);assert.equal(back.animations.length,0);
 const restored=page();restored.window.navigation={activation:{navigationType:'traverse'}};restored.click('about.html');const restoredTransition=transition();restored.handlers.pageswap({viewTransition:restoredTransition,activation:{navigationType:'push',entry:{url:'https://example.org/about.html'}}});assert(!restoredTransition.skipped);
 const blocked=page('index.html',{blocked:true});blocked.click('about.html');const bt=transition();blocked.handlers.pageswap({viewTransition:bt});assert(bt.skipped);
 const raw=page();raw.click('about.html');const fallback=page('about.html',{store:raw.store});fallback.handlers.pageshow({persisted:false});fallback.frames.forEach(fn=>fn());await flush();assert.equal(fallback.animations[0][1].duration,150);assert.equal(fallback.focus.length,1);
 const rm=page();rm.click('about.html');const reduced=page('about.html',{store:rm.store,reduced:true}),rt=transition();reduced.handlers.pagereveal({viewTransition:rt});assert(rt.skipped);reduced.handlers.pageshow({persisted:false});reduced.frames.forEach(fn=>fn());assert.equal(reduced.animations.length,0);assert.equal(reduced.focus.length,1);
 const first=page();first.handlers.pageshow({persisted:false});first.frames.forEach(fn=>fn());assert.equal(first.focus.length,0);assert.equal(first.animations.length,0);
 const interrupted=page();interrupted.click('about.html');interrupted.classes.add('theme-revealing');const it=transition();interrupted.handlers.pageswap({viewTransition:it});assert(it.skipped);
 const failOut=page();failOut.click('about.html');const failed=page('about.html',{store:failOut.store});failed.handlers.pagereveal({viewTransition:{finished:Promise.reject(Error('skipped'))}});await flush();assert(!failed.classes.has('nav-signature'));
 console.log('Passed: native links, full/repeat signatures, heading focus, hash/external/download/modified-click exclusions, aliases, rapid clicks, back/forward, unavailable storage, fallback, reduced motion and theme/failure cleanup.');
})().catch(error=>{console.error(error);process.exitCode=1});
