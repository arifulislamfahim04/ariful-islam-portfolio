/* Runs in the head: links retain their native navigation and document lifecycle. */
(()=>{'use strict';
const root=document.documentElement,reduced=matchMedia('(prefers-reduced-motion:reduce)'),key='ariful-page-navigation',seenKey='ariful-signature-seen',pages=new Set(['index','about','projects','gallery','blogs','contact']);
let native=false,active=null,fallback=null,lastClick=0;
function read(){try{return JSON.parse(sessionStorage.getItem(key)||'null')}catch{return null}}
function clear(){try{sessionStorage.removeItem(key)}catch{}}
function route(value,allowHash=false){try{const u=new URL(value,location.href),name=u.pathname.split('/').filter(Boolean).at(-1)||'index';return u.origin===location.origin&&(!u.hash||allowHash)&&pages.has(name.replace(/\.html$/,''))?name.replace(/\.html$/,''):null}catch{return null}}
function fresh(record){return record&&typeof record.from==='string'&&typeof record.to==='string'&&Date.now()-record.time>=0&&Date.now()-record.time<15000}
function incoming(){const record=read();return fresh(record)&&record.to===route(location.href,true)&&record.from!==record.to?record:null}
function traversal(event){return (event?.activation||window.navigation?.activation)?.navigationType==='traverse'}
function focusHeading(){if(location.hash)return;const heading=document.querySelector('main h1');if(heading){heading.setAttribute('tabindex','-1');heading.focus({preventScroll:true})}}
function cleanup(){root.classList.remove('nav-signature','nav-signature-repeat')}
document.addEventListener('click',event=>{
 const link=event.target.closest?.('a[href]');if(!link||event.defaultPrevented||event.button!==0||event.ctrlKey||event.metaKey||event.shiftKey||event.altKey||link.hasAttribute('download')||(link.target&&link.target!=='_self'))return;
 const from=route(location.href,true),to=route(link.href);
 if(!from||!to||from===to){clear();return}
 const now=Date.now(),record={from,to,time:now,skip:now-lastClick<350};lastClick=now;
 try{sessionStorage.setItem(key,JSON.stringify(record))}catch{}
});
addEventListener('pageswap',event=>{
 const transition=event.viewTransition;if(!transition)return;const record=read();
 const destination=event.activation?.entry?.url;
 if(root.dataset.pageSignature==='false'||reduced.matches||traversal(event)||root.classList.contains('theme-revealing')||!fresh(record)||record.skip||record.from!==route(location.href,true)||(destination&&route(destination)!==record.to)){
  transition.skipTransition();return;
 }
 root.classList.add('nav-signature');
 try{root.classList.toggle('nav-signature-repeat',sessionStorage.getItem(seenKey)==='1')}catch{}
 transition.finished.catch(()=>{}).finally(cleanup);
});
addEventListener('pagereveal',event=>{
 const transition=event.viewTransition;if(!transition)return;const record=incoming();
 if(root.dataset.pageSignature==='false'||!record||record.skip||reduced.matches||traversal(event)){transition.skipTransition();return}
 native=true;active=transition;clear();root.classList.add('nav-signature');
 try{root.classList.toggle('nav-signature-repeat',sessionStorage.getItem(seenKey)==='1');sessionStorage.setItem(seenKey,'1')}catch{}
 root.dataset.navigationMotion=root.classList.contains('nav-signature-repeat')?'signature-repeat':'signature-first';
 transition.finished.then(focusHeading,()=>{}).finally(()=>{active=null;cleanup()});
});
addEventListener('pageshow',event=>{
 if(event.persisted){cleanup();clear();return}
 requestAnimationFrame(()=>{
  if(native)return;const record=incoming();clear();if(!record)return;
  if(!reduced.matches&&document.querySelector('main')?.animate){
   fallback=document.querySelector('main').animate([{opacity:.8},{opacity:1}],{duration:150,easing:'ease-out'});
   fallback.finished.then(focusHeading,()=>{}).finally(()=>fallback=null);
  }else focusHeading();
 });
});
reduced.addEventListener('change',()=>{if(reduced.matches){active?.skipTransition();fallback?.finish();cleanup()}});
})();
