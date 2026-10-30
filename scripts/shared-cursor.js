/* A progressive enhancement: the native cursor remains the default and fallback. */
(()=>{'use strict';
const root=document.documentElement;if(root.dataset.customCursor!=='true')return;
const fine=matchMedia('(hover:hover) and (pointer:fine)'),reduced=matchMedia('(prefers-reduced-motion:reduce)');
const nativeSelector='input,textarea,select,[contenteditable]:not([contenteditable="false"]),iframe,object,embed,[data-native-cursor]';
let dot=null,ring=null,label=null,frame=0,active=false,pressed=false,dragging=false,target=null,x=0,y=0,rx=0,ry=0,lastTime=0,state='normal';
function blocked(){return !fine.matches||reduced.matches||document.hidden||root.classList.contains('theme-revealing')||root.classList.contains('nav-signature')||Boolean(document.querySelector('dialog[open]'))}
function hide(){if(root.classList.contains('custom-cursor-active'))root.classList.remove('custom-cursor-active');active=false;pressed=false;dragging=false;lastTime=0;if(frame)cancelAnimationFrame(frame);frame=0;if(dot)dot.hidden=true;if(ring)ring.hidden=true}
function destroy(){hide();dot?.remove();ring?.remove();dot=ring=label=null}
function build(){if(dot)return;dot=document.createElement('div');dot.className='portfolio-cursor-dot';dot.setAttribute('aria-hidden','true');ring=document.createElement('div');ring.className='portfolio-cursor-ring';ring.setAttribute('aria-hidden','true');label=document.createElement('span');ring.append(label);document.body.append(dot,ring);dot.hidden=ring.hidden=true}
function mode(element){
 if(element?.nodeType!==1||element.closest(nativeSelector))return 'native';
 if(element.closest(':disabled,[aria-disabled="true"]'))return 'disabled';
 if(element.closest('.hero-card-grip,[data-cursor-drag]'))return pressed?'release':'drag';
 const control=element.closest('a[href],button,[role="button"],summary');
 if(!control&&element.closest('.awards-carousel'))return pressed?'release':'drag';
 if(control){if(control.closest('#site-dock'))return 'dock';if(control.querySelector('img')&&control.matches('.moment-image,.learning-thumbnail,[data-credential-open],.preview-group a'))return 'view';return 'button'}
 return 'normal';
}
function setState(next){state=next;dragging=next==='release';ring.dataset.state=next;ring.classList.toggle('cursor-pressed',pressed&&!dragging);label.textContent=next==='drag'?'Drag':next==='release'?'Release':next==='view'?'View':''}
function draw(time){frame=0;if(!active)return;
 try{
  const dt=lastTime?Math.min(48,Math.max(1,time-lastTime)):16;lastTime=time;
  rx+=(x-rx)*(1-Math.exp(-dt/30));ry+=(y-ry)*(1-Math.exp(-dt/30));
  // Keep the ring near the precise dot even when the mouse moves quickly.
  const distance=Math.hypot(x-rx,y-ry);if(distance>14){rx=x+(rx-x)*14/distance;ry=y+(ry-y)*14/distance}
  dot.style.transform=`translate3d(${x}px,${y}px,0)`;ring.style.transform=`translate3d(${rx}px,${ry}px,0)`;
  dot.hidden=ring.hidden=false;if(!root.classList.contains('custom-cursor-active'))root.classList.add('custom-cursor-active');
  if(Math.abs(x-rx)+Math.abs(y-ry)>.1)frame=requestAnimationFrame(draw);
 }catch{destroy()}
}
function schedule(){if(!frame)frame=requestAnimationFrame(draw)}
function update(element){if(blocked()||x>=root.clientWidth||y>=root.clientHeight||x<0||y<0){hide();return}const next=mode(element);if(next==='native'){hide();return}build();if(!active){rx=x;ry=y;active=true;lastTime=0}target=element;setState(next);schedule()}
document.addEventListener('pointermove',event=>{if(event.pointerType!=='mouse'){hide();return}x=event.clientX;y=event.clientY;update(event.target)},{passive:true});
document.addEventListener('pointerover',event=>{if(event.pointerType==='mouse'&&active){x=event.clientX;y=event.clientY;update(event.target)}},{passive:true});
document.addEventListener('pointerdown',event=>{if(event.pointerType!=='mouse'||event.button!==0){hide();return}pressed=true;if(active){setState(mode(event.target));schedule()}},{passive:true});
function release(){pressed=false;dragging=false;if(active){update(document.elementFromPoint(x,y)||target)}}
document.addEventListener('pointerup',release,{passive:true});document.addEventListener('pointercancel',hide,{passive:true});document.addEventListener('lostpointercapture',release,{passive:true});
document.addEventListener('pointerout',event=>{if(!event.relatedTarget)hide()},{passive:true});
document.addEventListener('scroll',()=>{if(active)update(document.elementFromPoint(x,y)||target)},{passive:true,capture:true});
document.addEventListener('keydown',event=>{if(event.key==='Tab')hide()});
for(const name of ['blur','pagehide','pageswap','contextmenu','dragstart'])addEventListener(name,hide);
document.addEventListener('visibilitychange',()=>{if(document.hidden)hide()});
new MutationObserver(()=>{if(blocked())hide()}).observe(root,{attributes:true,attributeFilter:['class'],subtree:false});
new MutationObserver(()=>{if(blocked())hide()}).observe(document.body,{attributes:true,attributeFilter:['open'],subtree:true});
for(const query of [fine,reduced])query.addEventListener('change',()=>{if(!fine.matches||reduced.matches)destroy()});
})();
