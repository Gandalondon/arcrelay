"""Builds site/beta/index.html (the homepage, from 5 Nov) (v5 was its test page; retired once it became the homepage): one phone for the whole story (5 Nov).
Hero: "Hey / Relay" stacked, the phone angled level with the top of the word (B2, picked 5 Nov). As you scroll it travels down,
straightens and parks on the right. From then on it stays still while the four features scroll past on
the left, always left-aligned; the phone's screen cross-fades to match whichever feature is in the middle.
Text scrolls normally and never fades (motion goes on the picture, not the words). Phones and reduced
motion: the stacked rows, each with its own phone, as on the live site.
Finale: "Ask. / Find. / Get out." mirrors the hero; the parked phone stays put, turns to the mirror of its
opening angle and shows the home greeting for the visitor's time of day. Phones: the words only. Run from site/beta."""
import re

s = open("../../tools/hero/parts-v2.html").read()  # the original v2 page, kept as the source of shared parts
head = s[:s.index("<style>")].replace("<title>Relay · Hey Relay (v2)</title>", "<title>Relay · Hey Relay (v5, one phone)</title>")
hdr = s[s.index("<header"):s.index('<div class="site">')]
foot = s[s.index("<footer"):s.index('<script src="site.js">')]
slabs = re.search(r'<div class="phone p3">((?:<i class="slab[^>]*></i>)+)', s).group(1)
feats = {}
for sec in re.findall(r'(<section class="feature(?: flip)?">.*?</section>)', s, re.S):
    img = re.search(r'<img src="([^"]+)"[^>]*alt="([^"]*)"', sec)
    copy = re.search(r'<div class="reveal">\s*(.*?)\s*</div>\s*</div>\s*</section>', sec, re.S).group(1)
    feats[img.group(1)] = (img.group(2), copy)
order = ["screens/screen-3-exit.webp", "screens/screen-2-listening.webp", "screens/screen-4-find.webp", "screens/screen-5-pin.webp"]

steps = ""
for i, src in enumerate(order):
    alt, copy = feats[src]
    steps += ('    <section class="step" data-i="%d">\n      <div class="txt">%s</div>\n'
              '      <div class="mphone"><div class="phone"><div class="screen shot"><img src="%s" width="390" height="844" alt="%s" loading="lazy" decoding="async"></div></div></div>\n'
              '    </section>\n' % (i, copy, src, alt))
screens = "".join('<div class="screen shot%s" data-i="%d"><img src="%s" width="390" height="844" alt="" decoding="async"%s></div>'
                  % (" on" if i == 0 else "", i, src, ' fetchpriority="high"' if i == 0 else ' loading="lazy"') for i, src in enumerate(order))
phone3d = '<div class="phone p3">' + slabs + screens + '</div>'
COG = '<svg viewBox="0 -960 960 960" fill="currentColor" aria-hidden="true"><path d="M421-80q-14 0-25-9t-13-23l-15-94q-19-7-40-19t-37-25l-86 40q-14 6-28 1.5T155-226L97-330q-8-13-4.5-27t15.5-23l80-59q-2-9-2.5-20.5T185-480q0-9 .5-20.5T188-521l-80-59q-12-9-15.5-23t4.5-27l58-104q8-13 22-17.5t28 1.5l86 40q16-13 37-25t40-18l15-95q2-14 13-23t25-9h118q14 0 25 9t13 23l15 94q19 7 40.5 18.5T669-710l86-40q14-6 27.5-1.5T804-734l59 104q8 13 4.5 27.5T852-580l-80 57q2 10 2.5 21.5t.5 21.5q0 10-.5 21t-2.5 21l80 58q12 8 15.5 22.5T863-330l-58 104q-8 13-22 17.5t-28-1.5l-86-40q-16 13-36.5 25.5T592-206l-15 94q-2 14-13 23t-25 9H421Zm59-270q54 0 92-38t38-92q0-54-38-92t-92-38q-54 0-92 38t-38 92q0 54 38 92t92 38Z"/></svg>'
MIC = '<svg class="mic" viewBox="0 -960 960 960" fill="currentColor" aria-hidden="true"><path d="M408-453.92q-29-30.91-29-75.08v-251q0-41.67 29.44-70.83Q437.88-880 479.94-880t71.56 29.17Q581-821.67 581-780v251q0 44.17-29 75.08Q523-423 480-423t-72-30.92ZM450-150v-106q-96-11-166.5-77.5T202-498q-2-12.85 6.59-21.93 8.6-9.07 21.5-9.07 12.91 0 21.41 9t10.5 22q12 81 74.71 132.5Q399.42-314 479.65-314q81.35 0 143.85-51.5T698-498q2-13 10.68-22 8.67-9 21.5-9 12.82 0 21.32 9.07 8.5 9.08 6.5 21.93-11 97-81 164t-167 78v106q0 12.75-8.68 21.37-8.67 8.63-21.5 8.63-12.82 0-21.32-8.63-8.5-8.62-8.5-21.37Z"/></svg>'
HOME = ('<div class="screen home" data-i="9"><div class="top"><p class="greet" data-greet>Evening,\nRaider.</p><span class="cog">' + COG +
        '</span></div><div class="fill"></div><div class="dock">' + MIC + '</div></div>')
lastshot = '<div class="screen shot on" data-i="3"><img src="screens/screen-5-pin.webp" width="390" height="844" alt="" loading="lazy" decoding="async"></div>'
lander = '<div class="lander" aria-hidden="true"><div class="phone p3">' + slabs + lastshot + HOME + '</div></div>'
fphone = '<div class="phone p3 fphone">' + slabs + HOME.replace(' data-i="9"', ' data-i="9" style="opacity:1"') + '</div>'
finale = ('  <section class="finale"><div class="wrap">\n    <div class="ftxt"><h2 class="fin">Ask. Find.\nGet out.</h2><span class="btn">Coming soon to Android</span></div>\n'
          '    <div class="fslot" aria-hidden="true">' + fphone + '</div>\n  </div></section>\n')

CSS = """<style>
/* v5 (5 Nov): one phone. It floats under the word, travels down, then parks while the story scrolls past. */
.hdr .logo .name{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.hdr{position:fixed;inset:0 0 auto;z-index:20;background:var(--bg);padding-top:env(safe-area-inset-top,0px)}
.hdr .wrap{height:88px}
.hdr .btn.sm{height:40px;padding:0 20px;font-size:16px}
@media (max-width:600px){ .hdr .btn.sm{height:36px;padding:0 16px;font-size:15px} }
.heyhero{position:relative;padding-top:calc(128px + env(safe-area-inset-top,0px));padding-bottom:24px}
.heyhero .wrap{display:block;max-width:none}
.heyhero .word{margin:0;font-weight:700;font-size:min(15vw,calc((100svh - 300px) / 2.3));line-height:1.02;letter-spacing:-.01em;white-space:pre-line;width:max-content;color:var(--text-hi);position:relative;z-index:1}
.heyhero .lede{position:relative;z-index:1;margin-top:clamp(40px,5vw,72px);max-width:min(600px,calc(100% - 384px));font-size:24px;line-height:34px}
.phone{--pw:clamp(200px,min(19vw,calc((100svh - 200px) * 0.462)),320px)}
.p3{position:relative;transform-style:preserve-3d;will-change:transform;--d:35px}
.p3 .slab{position:absolute;inset:0;border-radius:inherit;background:#222429;transform:translateZ(calc(var(--k) * var(--d) / -12))}
.p3 .slab.rim{background:#34363C}
.p3 .screen{position:absolute;inset:calc(var(--pw) * .0333);width:auto;height:auto;transform:translateZ(.5px);opacity:0;transition:opacity .45s ease}
.p3 .screen.on{opacity:1}
/* the story: text column on the left gutter, the parked phone centred in the space to its right */
.story{position:relative;max-width:none}
.story .wrap{max-width:none;display:grid;grid-template-columns:minmax(0,600px) minmax(320px,1fr);gap:64px}
.steps{display:flex;flex-direction:column}
.step{min-height:calc(100svh - 88px);display:flex;align-items:center}
.step h2{font-size:clamp(40px,4.6vw,64px);line-height:1;font-weight:600;letter-spacing:0}
.step p{margin-top:24px;max-width:26em;font-size:20px;line-height:31px}
.step .btn{margin-top:40px}
.park{position:sticky;top:88px;height:calc(100svh - 88px);display:flex;align-items:center;justify-content:center;perspective:1400px}
.park .p3{visibility:hidden}
html.parked .park .p3{visibility:visible}
html.landing .park .p3{visibility:hidden}
.mphone{display:none}
.flyer{position:absolute;z-index:3;left:0;top:0;perspective:1400px;pointer-events:none;will-change:transform}
html.parked .flyer,html.landing .flyer{visibility:hidden}
.ftr{padding-top:96px}
/* finale: the hero's words mirrored, the phone turned the other way, showing the home greeting */
.finale .wrap{max-width:none;display:grid;grid-template-columns:minmax(0,600px) minmax(320px,1fr);gap:64px;min-height:calc(100svh - 88px - var(--fh,150px));align-items:center;padding-block:32px}
.fin{margin:0;font-weight:700;font-size:min(10vw,calc((100svh - 88px - var(--fh,150px) - 200px) / 2.1));line-height:1.02;letter-spacing:-.01em;white-space:pre-line;width:max-content;color:var(--text-hi)}
.ftxt .btn{margin-top:48px;cursor:default}
.ftxt .btn:hover{background:var(--amber)}
.fslot{display:flex;justify-content:center;perspective:1400px}
.fslot .phone{--pw:clamp(180px,min(15vw,calc((100svh - 260px) * 0.462)),260px)}
.fphone{transform:rotateX(22deg) rotateY(34deg) rotateZ(-10deg)}
html.fx .fphone{visibility:hidden}
.lander{position:absolute;z-index:3;left:0;top:0;perspective:1400px;pointer-events:none;will-change:transform;display:none}
html.landing .lander{display:block}
.screen.home{background:var(--bg)}
.screen.home .fill{flex:1 1 auto}
.screen.home .cog{color:var(--amber);width:1.75em;height:1.75em;flex:none}
.screen.home .cog svg{display:block;width:100%;height:100%}
@media (max-width:900px){
  .hdr .wrap{height:72px}
  .heyhero{padding-top:calc(140px + env(safe-area-inset-top,0px));padding-bottom:0}
  .heyhero .word{font-size:30vw}
  .heyhero .lede{max-width:none;margin-top:24px;font-size:21px;line-height:31px}
  .story .wrap{display:block}
  .park,.flyer,.lander,.fslot{display:none}
  .step{min-height:0;display:block;padding-block:64px}
  .step:first-child{padding-top:54px}
  .mphone{display:flex;justify-content:center;margin-top:56px}
  .mphone .phone{--pw:min(300px,78vw)}
  .finale .wrap{display:block;min-height:0;padding-block:112px 0}
  .fin{font-size:17vw}
}
@media (prefers-reduced-motion:reduce){
  .flyer{display:none}
  .park .p3{visibility:visible}
  .lander{display:none}
  .p3 .screen{transition:none}
}
</style>
"""

JS = """<script>
/* v5: fit the word; fly the phone from under the word to its parking spot; swap screens as the story scrolls */
(function(){
  var w=document.querySelector(".heyhero .word");
  function fit(){}  /* stacked word: sized in CSS */
  var fl=document.querySelector(".flyer"), fp=fl.querySelector(".p3"), dock=document.querySelector(".park"), dp=dock.querySelector(".p3"),
      story=document.querySelector(".story"), site=document.querySelector(".site"), steps=[].slice.call(document.querySelectorAll(".step")),
      mq=matchMedia("(max-width:900px)"), rm=matchMedia("(prefers-reduced-motion: reduce)"), G=null, q=false, cur=-1, root=document.documentElement;
  var S={rx:22, ry:-34, rz:10, s:1};
  var M={rx:22, ry:34, rz:-10};  /* the finale: the mirror of the opening angle */
  var ld=document.querySelector(".lander"), lp=ld.querySelector(".p3"), fpn=document.querySelector(".fphone"), F=null;
  var hr=new Date().getHours(), gw=hr<12?"Morning":hr<18?"Afternoon":"Evening";
  [].forEach.call(document.querySelectorAll("[data-greet]"),function(el){ el.textContent=gw+",\\nRaider."; });  /* starts angled, level with the top of the word (B2) */
  function show(i){ if(i===cur) return; cur=i; [fp,dp].forEach(function(ph){ [].forEach.call(ph.querySelectorAll(".screen"),function(sc){ sc.classList.toggle("on", +sc.dataset.i===i); }); }); }
  var ftr=document.querySelector(".ftr");
  function measure(){
    fit();
    if(ftr) root.style.setProperty("--fh", ftr.offsetHeight+"px");
    if(mq.matches){ G=null; F=null; root.classList.remove("parked","landing","fx"); return; }
    var sr=site.getBoundingClientRect(), base=sr.top+scrollY, st=story.getBoundingClientRect().top+scrollY;
    /* where the parked phone sits once the story column is stuck under the 88 px header */
    dp.style.transform="none";
    var dr=dp.getBoundingClientRect(), dk=dock.getBoundingClientRect(), oy=dr.top-dk.top, wr=w.getBoundingClientRect();
    var E=Math.max(1, st-88), yEnd=88+oy, tx=dr.left-sr.left, sy=Math.max(104-base, wr.top-sr.top-56);
    fl.style.width=dr.width+"px"; fp.style.width=dr.width+"px"; fl.style.left=tx+"px"; fl.style.top=sy+"px";
    G={base:base, sy:sy, E:E, yEnd:yEnd};
    /* finale: the parked phone stays where it is while the finale scrolls up to it, turning as it goes */
    root.classList.toggle("fx", !rm.matches);
    fpn.style.transform="none"; var fr=fpn.getBoundingClientRect(); fpn.style.transform="";
    var sb=story.getBoundingClientRect().bottom+scrollY, S0=sb-innerHeight, fy=fr.top-sr.top, S1=Math.max(S0+1, base+fy-yEnd);
    var fsc=fr.width/dr.width, ltop=fr.top-sr.top+(fr.height-dr.height)/2, lleft=fr.left-sr.left+(fr.width-dr.width)/2;
    var maxS=Math.max(0,document.documentElement.scrollHeight-innerHeight);
    fy=ltop; S1=Math.min(maxS, Math.max(S0+1, base+fy-yEnd));
    ld.style.width=dr.width+"px"; lp.style.width=dr.width+"px"; ld.style.left=lleft+"px"; ld.style.top=fy+"px";
    F={S0:S0, S1:S1, fy:fy, k:fsc, yT:base+fy-S1};
    f();
  }
  function f(){ q=false;
    var vh=innerHeight, mid=vh/2, best=0, bd=1e9;
    steps.forEach(function(el,i){ var r=el.getBoundingClientRect(), d=Math.abs(r.top+r.height/2-mid); if(d<bd){ bd=d; best=i; } });
    show(best);
    if(!G || rm.matches) return;
    var s=scrollY, u=Math.max(0,Math.min(1,s/G.E)), e=u*u*(3-2*u), k=1-e, sc=S.s+(1-S.s)*e;
    var land = F && s>=F.S0;
    root.classList.toggle("parked", u>=1 && !land); root.classList.toggle("landing", !!land);
    if(land){
      var v=Math.max(0,Math.min(1,(s-F.S0)/(F.S1-F.S0))), m=v*v*(3-2*v);
      ld.style.transform="translateY("+(s<F.S1 ? (G.yEnd*(1-m)+F.yT*m - (G.base+F.fy-s)) : 0).toFixed(1)+"px)";
      lp.style.transform="rotateX("+(M.rx*m).toFixed(2)+"deg) rotateY("+(M.ry*m).toFixed(2)+"deg) rotateZ("+(M.rz*m).toFixed(2)+"deg) scale("+(1+(F.k-1)*m).toFixed(3)+")";
      [].forEach.call(lp.querySelectorAll(".screen"),function(sc){ sc.classList.toggle("on", (sc.dataset.i==="9")===(v>.5)); });
      return;
    }
    var T=((G.base+G.sy)*k + G.yEnd*e) - G.base - G.sy + s;
    fl.style.transform="translateY("+T.toFixed(1)+"px)";
    fp.style.transform=k<0.001 ? "none" : "rotateX("+(S.rx*k).toFixed(2)+"deg) rotateY("+(S.ry*k).toFixed(2)+"deg) rotateZ("+(S.rz*k).toFixed(2)+"deg) scale("+sc.toFixed(3)+")";
  }
  addEventListener("scroll",function(){ if(!q){ q=true; requestAnimationFrame(f); } },{passive:true});
  addEventListener("resize",measure); mq.addEventListener("change",measure); rm.addEventListener("change",measure);
  measure(); addEventListener("load",measure); if(document.fonts) document.fonts.ready.then(measure);
  if (rm.matches) return;
  document.querySelectorAll("#logo path").forEach(function(p,i){ if(!p.animate) return; var L=Math.ceil(p.getTotalLength()); p.style.strokeDasharray=L; p.animate([{strokeDashoffset:L},{strokeDashoffset:0}],{duration:440,delay:i*70,easing:"cubic-bezier(.3,0,.2,1)",fill:"backwards"}); });
})();
</script>
"""

cmp = '<nav class="cmp" aria-label="Compare versions"><a href="v3">B2 stacked</a><a href="v4">C2 floating</a><a href="./" aria-current="page">One phone</a></nav>'
CMP_CSS = """<style>
.cmp{position:fixed;z-index:30;left:max(16px,env(safe-area-inset-left,0px));bottom:calc(16px + env(safe-area-inset-bottom,0px));display:flex;gap:4px;padding:4px;border-radius:999px;background:var(--panel)}
.cmp a{height:36px;padding:0 16px;border-radius:999px;display:flex;align-items:center;font:600 15px/1 var(--font);color:var(--text-hi)}
.cmp a[aria-current="page"]{background:var(--amber);color:var(--ink)}
</style>
"""
body = ("<body>\n" + hdr + '<div class="site">\n<main>\n  <section class="heyhero">\n    <div class="wrap">\n      <h1 class="word">Hey\nRelay</h1>\n'
        '      <p class="lede">A voice companion for ARC Raiders. Ask where to go, hear the answer, keep playing.</p>\n    </div>\n  </section>\n'
        '  <div class="story"><div class="wrap">\n  <div class="steps">\n' + steps + '  </div>\n  <div class="park" aria-hidden="true">' + phone3d + '</div>\n  </div></div>\n' +
        finale + '</main>\n<div class="flyer" aria-hidden="true">' + phone3d + "</div>\n" + lander + "\n" + foot + "</div>\n" + cmp + "\n" +
        '<script src="site.js"></script>\n' + JS + "</body>\n</html>\n")
home = (head.replace("<title>Relay · Hey Relay (v5, one phone)</title>", "<title>Relay</title>") + CSS + "</head>\n" + body.replace(cmp + "\n", ""))
open("index.html", "w").write(home)
print("ok")
