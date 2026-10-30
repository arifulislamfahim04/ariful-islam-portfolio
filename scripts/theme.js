/* Shared theme controller: initial paint is handled by theme-init.js in the head. */
(()=>{'use strict';
const root=document.documentElement,key='portfolio-theme-v2',system=matchMedia('(prefers-color-scheme:dark)'),reduced=matchMedia('(prefers-reduced-motion:reduce)'),buttons=[...document.querySelectorAll('[data-theme-toggle]')];
let preference=window.PORTFOLIO_THEME_PREFERENCE||'system',desired=root.dataset.theme,running=false,active=null,reveal=null,fallbackTimer=0,requestedMotion=true,origin=buttons[0];
function sync(){const dark=root.dataset.theme==='dark';buttons.forEach(button=>{button.setAttribute('aria-pressed',String(dark));button.setAttribute('aria-label',dark?'Switch to light mode':'Switch to dark mode');const tip=button.querySelector('[data-theme-label]');if(tip)tip.textContent=button.getAttribute('aria-label')});const meta=document.querySelector('meta[name="theme-color"]');if(meta)meta.content=dark?'#101612':'#f6f7f2';root.style.colorScheme=dark?'dark':'light'}
function apply(next){root.dataset.theme=next;sync()}
function cancelMotion(){active?.skipTransition();reveal?.cancel();root.classList.remove('theme-color-fade');clearTimeout(fallbackTimer)}
function fallback(next,animate){if(animate&&!reduced.matches){root.classList.add('theme-color-fade');void root.offsetWidth;clearTimeout(fallbackTimer);fallbackTimer=setTimeout(()=>root.classList.remove('theme-color-fade'),320)}apply(next)}
async function drain(animateNext=true){requestedMotion=animateNext;if(running)return;running=true;
 try{while(root.dataset.theme!==desired){const next=desired,button=origin,animate=requestedMotion;
  if(!animate||reduced.matches||!document.startViewTransition||!root.animate){fallback(next,animate);continue}
  const rect=button?.getBoundingClientRect(),x=rect?rect.left+rect.width/2:innerWidth/2,y=rect?rect.top+rect.height/2:0;
  const radius=Math.ceil(Math.hypot(Math.max(x,innerWidth-x),Math.max(y,innerHeight-y)))+2;
  root.classList.remove('theme-color-fade');root.classList.add('theme-revealing');
  let transition;
  try{transition=document.startViewTransition(()=>apply(next));active=transition;
   await transition.ready;
   if(reduced.matches){transition.skipTransition()}else{
    reveal=root.animate({clipPath:[`circle(0px at ${x}px ${y}px)`,`circle(${radius}px at ${x}px ${y}px)`]},{duration:500,easing:'cubic-bezier(.22,1,.36,1)',pseudoElement:'::view-transition-new(root)'});
    await reveal.finished.catch(()=>{});
   }
   await transition.finished;
  }catch{if(transition){transition.skipTransition();await transition.updateCallbackDone.catch(()=>{})}apply(next)}
  finally{active=null;reveal=null;root.classList.remove('theme-revealing')}
 }}finally{running=false;sync()}}
function toggle(event){origin=event?.currentTarget?.matches?.('[data-theme-toggle]')?event.currentTarget:buttons[0];preference=desired==='dark'?'light':'dark';desired=preference;try{localStorage.setItem(key,preference)}catch{}void drain()}
buttons.forEach(button=>button.addEventListener('click',toggle));
document.querySelectorAll('[data-theme-command]').forEach(button=>button.addEventListener('click',()=>{button.closest('dialog')?.close();toggle()}));
system.addEventListener('change',()=>{if(preference!=='system')return;desired=system.matches?'dark':'light';cancelMotion();void drain(false)});
addEventListener('storage',event=>{if(event.key!==key&&event.key!==null)return;preference=['light','dark'].includes(event.newValue)?event.newValue:'system';desired=preference==='system'?(system.matches?'dark':'light'):preference;cancelMotion();void drain(false)});
reduced.addEventListener('change',()=>{if(reduced.matches)cancelMotion()});
sync();
})();
