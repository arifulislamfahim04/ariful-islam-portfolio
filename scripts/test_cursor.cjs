/* Cursor state and native-fallback coverage without depending on mouse hardware. */
const assert=require('node:assert/strict'),vm=require('node:vm'),fs=require('node:fs'),path=require('node:path');
const script=fs.readFileSync(path.join(__dirname,'shared-cursor.js'),'utf8');
function fixture({fine=true,reduced=false,enabled=true}={}){
 const events={},windowEvents={},observers=[],classes=new Set(),nodes=[],frames=new Map(),media={},classOps={remove:0};let nextFrame=0,time=0;
 function classList(){const all=new Set();return{add:x=>all.add(x),remove:x=>all.delete(x),contains:x=>all.has(x),toggle:(x,on)=>on?all.add(x):all.delete(x)}}
 const root={dataset:{customCursor:String(enabled)},clientWidth:1200,clientHeight:800,classList:{add:x=>classes.add(x),remove:x=>{classOps.remove++;classes.delete(x)},contains:x=>classes.has(x)}};
 const state={dialog:false,target:null};
 const document={documentElement:root,hidden:false,body:{append:(...items)=>nodes.push(...items)},querySelector:()=>state.dialog?{}:null,elementFromPoint:()=>state.target,createElement:()=>({style:{},dataset:{},hidden:false,classList:classList(),children:[],setAttribute:()=>{},append(...items){this.children.push(...items)},remove(){this.removed=true}}),addEventListener:(name,fn)=>{assert(!events[name],name+' must be delegated once');events[name]=fn}};
 for(const [name,matches] of [['(hover:hover) and (pointer:fine)',fine],['(prefers-reduced-motion:reduce)',reduced]])media[name]={matches,addEventListener:(name,fn)=>media[matches?'active':'other']=fn};
 const changes={};for(const [name,query] of Object.entries(media))query.addEventListener=(event,fn)=>changes[name]=fn;
 const context={document,matchMedia:name=>media[name],MutationObserver:class{constructor(fn){observers.push(fn)}observe(){}},requestAnimationFrame:fn=>(frames.set(++nextFrame,fn),nextFrame),cancelAnimationFrame:id=>frames.delete(id),addEventListener:(name,fn)=>windowEvents[name]=fn};
 vm.createContext(context);vm.runInContext(script,context);
 function target(options={}){const control=options.control?{querySelector:()=>options.image?{}:null,matches:()=>Boolean(options.image),closest:s=>s==='#site-dock'&&options.dock?{}:null}:null;return{nodeType:1,closest(selector){if(selector.startsWith('input'))return options.native?{}:null;if(selector.startsWith(':disabled'))return options.disabled?{}:null;if(selector.startsWith('.hero-card-grip'))return options.grip?{}:null;if(selector.startsWith('a[href]'))return control;if(selector==='.awards-carousel')return options.carousel?{}:null;return null}}}
 function move(options={},extra={}){const t=target(options);state.target=t;events.pointermove?.({target:t,pointerType:'mouse',clientX:100,clientY:100,...extra});return t}
 function flush(){const pending=[...frames.values()];frames.clear();time+=16;pending.forEach(fn=>fn(time))}
 return{events,windowEvents,changes,media,classes,nodes,observers,state,document,root,target,move,flush,classOps};
}
for(const options of [{fine:false},{reduced:true},{enabled:false}]){const f=fixture(options);f.move();f.flush();assert.equal(f.nodes.length,0);assert(!f.classes.has('custom-cursor-active'))}
const f=fixture();assert.equal(f.nodes.length,0);f.move();assert(!f.classes.has('custom-cursor-active'));f.flush();assert(f.classes.has('custom-cursor-active'));assert.equal(f.nodes.length,2);assert.equal(f.nodes[0].style.transform,'translate3d(100px,100px,0)');
f.move({}, {clientX:600,clientY:500});f.flush();assert.equal(f.nodes[0].style.transform,'translate3d(600px,500px,0)');const xy=f.nodes[1].style.transform.match(/[\d.]+/g).slice(1).map(Number);assert(Math.hypot(600-xy[0],500-xy[1])<=14.01);
f.move({control:true});assert.equal(f.nodes[1].dataset.state,'button');f.events.pointerdown({pointerType:'mouse',button:0,target:f.state.target});assert(f.nodes[1].classList.contains('cursor-pressed'));f.events.pointerup();assert(!f.nodes[1].classList.contains('cursor-pressed'));
f.move({control:true,dock:true});assert.equal(f.nodes[1].dataset.state,'dock');f.move({control:true,image:true});assert.equal(f.nodes[1].children[0].textContent,'View');
f.move({carousel:true});assert.equal(f.nodes[1].children[0].textContent,'Drag');f.events.pointerdown({pointerType:'mouse',button:0,target:f.state.target});assert.equal(f.nodes[1].children[0].textContent,'Release');assert(!f.nodes[1].classList.contains('cursor-pressed'));f.events.pointerup();assert.equal(f.nodes[1].children[0].textContent,'Drag');
f.move({carousel:true,control:true});assert.equal(f.nodes[1].dataset.state,'button');f.move({disabled:true});assert.equal(f.nodes[1].dataset.state,'disabled');
for(const options of [{native:true},{}]){f.move(options);f.flush();if(options.native)assert(!f.classes.has('custom-cursor-active'))}
f.move({}, {clientX:1201});assert(!f.classes.has('custom-cursor-active'));f.move();f.flush();f.events.pointerout({relatedTarget:null});assert(!f.classes.has('custom-cursor-active'));
f.move();f.flush();f.events.keydown({key:'Tab'});assert(!f.classes.has('custom-cursor-active'));
f.move();f.flush();f.state.dialog=true;f.observers.forEach(fn=>fn());assert(!f.classes.has('custom-cursor-active'));const removals=f.classOps.remove;f.observers.forEach(fn=>fn());assert.equal(f.classOps.remove,removals,'native handoff must not trigger its own observer repeatedly');f.state.dialog=false;
f.move();f.flush();f.classes.add('theme-revealing');f.observers.forEach(fn=>fn());assert(!f.classes.has('custom-cursor-active'));f.classes.delete('theme-revealing');
f.move();f.flush();f.windowEvents.pageswap();assert(!f.classes.has('custom-cursor-active'));
f.move();f.flush();f.media['(prefers-reduced-motion:reduce)'].matches=true;f.changes['(prefers-reduced-motion:reduce)']();assert(f.nodes.every(n=>n.removed));assert(!f.classes.has('custom-cursor-active'));
const error=fixture();error.move();error.flush();Object.defineProperty(error.nodes[0].style,'transform',{set(){throw Error('render failed')}});error.move();error.flush();assert(!error.classes.has('custom-cursor-active'));
console.log('Passed: optional/touch/reduced-motion startup, precise dot, bounded lag, delegated states, drag vs button precedence, native fields, viewport/keyboard/dialog/transition handoff and render-failure recovery.');
