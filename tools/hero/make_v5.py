"""Builds site/beta/v5.html: one phone for the whole story (5 Nov).
Hero: the full-width word with the phone floating side-on under it (C2). As you scroll it travels down,
straightens and parks on the right. From then on it stays still while the four features scroll past on
the left, always left-aligned; the phone's screen cross-fades to match whichever feature is in the middle.
Text scrolls normally and never fades (motion goes on the picture, not the words). Phones and reduced
motion: the stacked rows, each with its own phone, as on the live site. Run from site/beta."""
import re

s = open("v2.html").read()
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

CSS = """<style>
/* v5 (5 Nov): one phone. It floats under the word, travels down, then parks while the story scrolls past. */
.hdr .logo .name{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.hdr{position:fixed;inset:0 0 auto;z-index:20;background:var(--bg);padding-top:env(safe-area-inset-top,0px)}
.hdr .wrap{height:88px}
.hdr .btn.sm{height:40px;padding:0 20px;font-size:16px}
@media (max-width:600px){ .hdr .btn.sm{height:36px;padding:0 16px;font-size:15px} }
.heyhero{position:relative;padding-top:calc(128px + env(safe-area-inset-top,0px));padding-bottom:24px}
.heyhero .wrap{display:block;max-width:none}
.heyhero .word{margin:0;font-weight:700;font-size:16vw;line-height:.82;letter-spacing:-.01em;white-space:nowrap;width:max-content;color:var(--text-hi);position:relative;z-index:1}
.heyhero .lede{position:relative;z-index:1;margin-top:clamp(40px,5vw,72px);max-width:min(600px,calc(100% - 384px));font-size:24px;line-height:34px}
.phone{--pw:clamp(220px,min(21vw,calc((100svh - 150px) * 0.462)),340px)}
.p3{position:relative;transform-style:preserve-3d;will-change:transform;--d:35px}
.p3 .slab{position:absolute;inset:0;border-radius:inherit;background:#222429;transform:translateZ(calc(var(--k) * var(--d) / -12))}
.p3 .slab.rim{background:#34363C}
.p3 .screen{position:absolute;inset:10px;width:auto;height:auto;transform:translateZ(.5px);opacity:0;transition:opacity .45s ease}
.p3 .screen.on{opacity:1}
/* the story: text column on the left gutter, the parked phone centred in the space to its right */
.story{position:relative;max-width:none}
.story .wrap{max-width:none;display:grid;grid-template-columns:minmax(0,600px) minmax(320px,1fr);gap:64px}
.steps{display:flex;flex-direction:column}
.step{min-height:calc(100svh - 88px);display:flex;align-items:center}
.step h2{font-size:clamp(40px,4.6vw,64px);line-height:1;font-weight:600;letter-spacing:0}
.step p{margin-top:24px;max-width:26em;font-size:20px;line-height:31px}
.step .btn{margin-top:40px}
.dock{position:sticky;top:88px;height:calc(100svh - 88px);display:flex;align-items:center;justify-content:center;perspective:1400px}
.dock .p3{visibility:hidden}
html.parked .dock .p3{visibility:visible}
.mphone{display:none}
.flyer{position:absolute;z-index:3;left:0;top:0;perspective:1400px;pointer-events:none;will-change:transform}
html.parked .flyer{visibility:hidden}
.ftr{padding-top:96px}
@media (max-width:900px){
  .hdr .wrap{height:72px}
  .heyhero{padding-top:calc(140px + env(safe-area-inset-top,0px));padding-bottom:0}
  .heyhero .lede{max-width:none;margin-top:24px;font-size:21px;line-height:31px}
  .story .wrap{display:block}
  .dock,.flyer{display:none}
  .step{min-height:0;display:block;padding-block:64px}
  .step:first-child{padding-top:54px}
  .mphone{display:flex;justify-content:center;margin-top:56px}
  .mphone .phone{--pw:min(300px,78vw)}
}
@media (prefers-reduced-motion:reduce){
  .flyer{display:none}
  .dock .p3{visibility:visible}
  .p3 .screen{transition:none}
}
</style>
"""

JS = """<script>
/* v5: fit the word; fly the phone from under the word to its parking spot; swap screens as the story scrolls */
(function(){
  var w=document.querySelector(".heyhero .word");
  function fit(){ w.style.fontSize="100px"; var p=w.parentNode, cs=getComputedStyle(p), avail=p.clientWidth-parseFloat(cs.paddingLeft)-parseFloat(cs.paddingRight); w.style.fontSize=(100*avail/w.getBoundingClientRect().width)+"px"; }
  var fl=document.querySelector(".flyer"), fp=fl.querySelector(".p3"), dock=document.querySelector(".dock"), dp=dock.querySelector(".p3"),
      story=document.querySelector(".story"), site=document.querySelector(".site"), steps=[].slice.call(document.querySelectorAll(".step")),
      mq=matchMedia("(max-width:900px)"), rm=matchMedia("(prefers-reduced-motion: reduce)"), G=null, q=false, cur=-1, root=document.documentElement;
  var S={rx:28, ry:-52, rz:16, s:.82};
  function show(i){ if(i===cur) return; cur=i; [fp,dp].forEach(function(ph){ [].forEach.call(ph.querySelectorAll(".screen"),function(sc){ sc.classList.toggle("on", +sc.dataset.i===i); }); }); }
  function measure(){
    fit();
    if(mq.matches){ G=null; root.classList.remove("parked"); return; }
    var sr=site.getBoundingClientRect(), base=sr.top+scrollY, st=story.getBoundingClientRect().top+scrollY;
    /* where the parked phone sits once the story column is stuck under the 88 px header */
    dp.style.transform="none";
    var dr=dp.getBoundingClientRect(), dk=dock.getBoundingClientRect(), oy=dr.top-dk.top, wr=w.getBoundingClientRect();
    var E=Math.max(1, st-88), yEnd=88+oy, tx=dr.left-sr.left, sy=wr.bottom-sr.top+24;
    fl.style.width=dr.width+"px"; fp.style.width=dr.width+"px"; fl.style.left=tx+"px"; fl.style.top=sy+"px";
    G={base:base, sy:sy, E:E, yEnd:yEnd};
    f();
  }
  function f(){ q=false;
    var vh=innerHeight, mid=vh/2, best=0, bd=1e9;
    steps.forEach(function(el,i){ var r=el.getBoundingClientRect(), d=Math.abs(r.top+r.height/2-mid); if(d<bd){ bd=d; best=i; } });
    show(best);
    if(!G || rm.matches) return;
    var s=scrollY, u=Math.max(0,Math.min(1,s/G.E)), e=u*u*(3-2*u), k=1-e, sc=S.s+(1-S.s)*e;
    root.classList.toggle("parked", u>=1);
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

cmp = '<nav class="cmp" aria-label="Compare versions"><a href="v3">B2 stacked</a><a href="v4">C2 floating</a><a href="v5" aria-current="page">One phone</a></nav>'
CMP_CSS = """<style>
.cmp{position:fixed;z-index:30;left:max(16px,env(safe-area-inset-left,0px));bottom:calc(16px + env(safe-area-inset-bottom,0px));display:flex;gap:4px;padding:4px;border-radius:999px;background:var(--panel)}
.cmp a{height:36px;padding:0 16px;border-radius:999px;display:flex;align-items:center;font:600 15px/1 var(--font);color:var(--text-hi)}
.cmp a[aria-current="page"]{background:var(--amber);color:var(--ink)}
</style>
"""
body = ("<body>\n" + hdr + '<div class="site">\n<main>\n  <section class="heyhero">\n    <div class="wrap">\n      <h1 class="word">Hey Relay</h1>\n'
        '      <p class="lede">A voice companion for ARC Raiders. Ask where to go, hear the answer, keep playing.</p>\n    </div>\n  </section>\n'
        '  <div class="story"><div class="wrap">\n  <div class="steps">\n' + steps + '  </div>\n  <div class="dock" aria-hidden="true">' + phone3d + '</div>\n  </div></div>\n'
        '</main>\n<div class="flyer" aria-hidden="true">' + phone3d + "</div>\n" + foot + "</div>\n" + cmp + "\n" +
        '<script src="site.js"></script>\n' + JS + "</body>\n</html>\n")
open("v5.html", "w").write(head + CSS + CMP_CSS + "</head>\n" + body)
print("ok")
