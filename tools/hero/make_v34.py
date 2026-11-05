"""Builds site/beta/v3.html (B2: stacked word) and v4.html (C2: full-width word) from v2.html.
The hero phone starts angled in the hero and, as you scroll, travels down and turns face-on until it
sits exactly in the first row's phone column. Run from site/beta."""
import re

s = open("../../tools/hero/parts-v2.html").read()  # the original v2 page, kept as the source of shared parts
head = s[:s.index("<style>")]
hdr = s[s.index("<header"):s.index('<div class="site">')]
foot = s[s.index("<footer"):s.index('<script src="site.js">')]
slabs = re.search(r'<div class="phone p3">((?:<i class="slab[^>]*></i>)+)', s).group(1)
feats = re.findall(r'(<section class="feature(?: flip)?">.*?</section>)', s, re.S)
just, find, evac, show = feats
def flip(sec, on):
    sec = sec.replace('<section class="feature flip">', '<section class="feature">')
    return sec.replace('<section class="feature">', '<section class="feature flip">') if on else sec
# first row: the evac answer, phone on the right, so the hero phone (same screen) lands in it
evac1 = flip(evac, True).replace('<div class="phone p3">', '<div class="phone p3 dock-target">', 1)
evac1 = evac1.replace(' loading="lazy"', '')
rows = evac1 + "\n" + flip(just, False) + "\n" + flip(find, True) + "\n" + flip(show, False)

CSS = """<style>
/* v3/v4 (5 Nov): test pages. The hero phone starts angled and lands face-on in the first row as you scroll. */
.hdr .logo .name{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.hdr{position:fixed;inset:0 0 auto;z-index:20;background:var(--bg);padding-top:env(safe-area-inset-top,0px)}
.hdr .wrap{height:88px}
.hdr .btn.sm{height:40px;padding:0 20px;font-size:16px}
@media (max-width:600px){ .hdr .btn.sm{height:36px;padding:0 16px;font-size:15px} }
.heyhero{position:relative;padding-top:calc(128px + env(safe-area-inset-top,0px));padding-bottom:24px}
.heyhero .wrap{display:block;max-width:none}
.heyhero .word{margin:0;font-weight:700;line-height:.82;letter-spacing:-.01em;white-space:nowrap;width:max-content;color:var(--text-hi);position:relative;z-index:1}
.heyhero .lede{position:relative;z-index:1;margin-top:clamp(40px,5vw,72px);max-width:min(600px,calc(100% - 384px));font-size:24px;line-height:34px}
body.b2 .heyhero .word{white-space:pre-line;line-height:1.02;font-size:min(19vw,calc((100svh - 260px) / 2.1))}
body.c2 .heyhero .word{font-size:16vw}
/* the flying phone: placed by script over the first row's phone column; hidden on phones and with reduced motion */
.flyer{position:absolute;z-index:3;left:0;top:0;perspective:1400px;display:none;pointer-events:none;will-change:transform}
.p3{position:relative;transform-style:preserve-3d;will-change:transform}
.p3 .slab{position:absolute;inset:0;border-radius:inherit;background:#222429;transform:translateZ(calc(var(--k) * var(--d) / -12))}
.p3 .slab.rim{background:#34363C}
.p3 .screen{transform:translateZ(.5px)}
.flyer .p3,.feature .p3{--d:35px}
.feature .phone-col{perspective:1400px}
/* desktop rows: same gutters as the hero; text column on its own, the phone centred in the space beside it */
.feature .phone,.flyer .phone{--pw:clamp(220px,min(21vw,calc((100svh - 150px) * 0.462)),340px)}
@media (min-width:901px){
  .feature .wrap{max-width:none;gap:64px}
  .feature.flip .wrap{grid-template-columns:minmax(0,600px) minmax(320px,1fr)}
  .feature:not(.flip) .wrap{grid-template-columns:minmax(320px,1fr) minmax(0,600px)}
  .feature .phone-col{justify-self:center}
}
html.fly .flyer{display:block}
html.fly .dock-target{visibility:hidden}
/* comparison switch for these test pages only */
.cmp{position:fixed;z-index:30;left:max(16px,env(safe-area-inset-left,0px));bottom:calc(16px + env(safe-area-inset-bottom,0px));display:flex;gap:4px;padding:4px;border-radius:999px;background:var(--panel)}
.cmp a{height:36px;padding:0 16px;border-radius:999px;display:flex;align-items:center;font:600 15px/1 var(--font);color:var(--text-hi)}
.cmp a[aria-current="page"]{background:var(--amber);color:var(--ink)}
@media (max-width:900px){
  .hdr .wrap{height:72px}
  .heyhero{padding-top:calc(140px + env(safe-area-inset-top,0px));padding-bottom:0}
  .heyhero .lede{margin-top:24px;font-size:21px;line-height:31px}
  .rows{padding-top:0} .rows .feature:first-child{padding-top:54px}
  body.b2 .heyhero .word{font-size:30vw}
  .feature .p3{--d:33px}
}
</style>
"""

def page(variant):
    b2 = variant == "b2"
    title = "Relay · Hey Relay (v3, stacked)" if b2 else "Relay · Hey Relay (v4, floating)"
    word = "Hey\nRelay" if b2 else "Hey Relay"
    # where the phone starts: tilt and size. B2 sits high on the right, C2 floats under the word, more side-on
    start = '{"top":"hero","rx":22,"ry":-34,"rz":10,"s":1}' if b2 else '{"top":"under","rx":28,"ry":-52,"rz":16,"s":0.82}'
    h = head.replace("<title>Relay · Hey Relay (v2)</title>", "<title>%s</title>" % title)
    js = """<script>
/* v3/v4: the word fits the page (C2 only); the hero phone travels down and straightens until it sits in the first row */
(function(){
  var b2=document.body.classList.contains("b2"), w=document.querySelector(".heyhero .word");
  function fit(){ if(b2) return; w.style.fontSize="100px"; var p=w.parentNode, cs=getComputedStyle(p), avail=p.clientWidth-parseFloat(cs.paddingLeft)-parseFloat(cs.paddingRight); w.style.fontSize=(100*avail/w.getBoundingClientRect().width)+"px"; }
  var fl=document.querySelector(".flyer"), ph=fl.querySelector(".p3"), tg=document.querySelector(".dock-target"), hero=document.querySelector(".heyhero"), site=document.querySelector(".site");
  var S=JSON.parse(document.body.dataset.start), mq=matchMedia("(max-width:900px)"), rm=matchMedia("(prefers-reduced-motion: reduce)"), G=null, q=false;
  function measure(){
    fit();
    var on=!mq.matches && !rm.matches; document.documentElement.classList.toggle("fly",on); if(!on){ G=null; return; }
    fl.style.transform="none";
    var sr=site.getBoundingClientRect(), t=tg.getBoundingClientRect(), wr=w.getBoundingClientRect(), base=sr.top+scrollY;
    var tx=t.left-sr.left, ty=t.top-sr.top;
    /* start: same column as the landing spot. B2: level with the top of the word. C2: in the gap under the word */
    var sy = S.top==="hero" ? (wr.top-sr.top) : (wr.bottom-sr.top+24);
    fl.style.width=t.width+"px"; fl.style.left=tx+"px"; fl.style.top=sy+"px"; ph.style.width=t.width+"px";
    /* landed when the row's phone is centred in the window (and clear of the 88 px header) */
    var yEnd=Math.max(104,(innerHeight-t.height)/2), E=Math.max(1, base+ty-yEnd);
    G={base:base, sy:sy, ty:ty, yEnd:yEnd, E:E};
    f();
  }
  function f(){ q=false; if(!G) return;
    var s=scrollY, u=Math.max(0,Math.min(1,s/G.E)), e=u*u*(3-2*u), k=1-e, sc=S.s+(1-S.s)*e;
    /* where the phone should be in the window: from its start spot to the landing spot, never above the header */
    var T = u>=1 ? G.ty-G.sy : ((G.base+G.sy)*k + G.yEnd*e) - G.base - G.sy + s;
    fl.style.transform="translateY("+T.toFixed(1)+"px)";
    ph.style.transform=k<0.001 ? "none" : "rotateX("+(S.rx*k).toFixed(2)+"deg) rotateY("+(S.ry*k).toFixed(2)+"deg) rotateZ("+(S.rz*k).toFixed(2)+"deg) scale("+sc.toFixed(3)+")";
  }
  addEventListener("scroll",function(){ if(!q){ q=true; requestAnimationFrame(f); } },{passive:true});
  addEventListener("resize",measure); mq.addEventListener("change",measure); rm.addEventListener("change",measure);
  measure(); addEventListener("load",measure); if(document.fonts) document.fonts.ready.then(measure);
  if (rm.matches) return;
  document.querySelectorAll("#logo path").forEach(function(p,i){ if(!p.animate) return; var L=Math.ceil(p.getTotalLength()); p.style.strokeDasharray=L; p.animate([{strokeDashoffset:L},{strokeDashoffset:0}],{duration:440,delay:i*70,easing:"cubic-bezier(.3,0,.2,1)",fill:"backwards"}); });
  /* the other rows' phones turn to face you, as on v2 */
  var fs=[].slice.call(document.querySelectorAll(".feature .p3:not(.dock-target)")), qq=false;
  function g(){ qq=false; var vh=innerHeight; fs.forEach(function(el,i){ var r=el.parentNode.getBoundingClientRect(), u=Math.max(0,Math.min(1,(vh-r.top)/(vh*.85))), s=u*u*(3-2*u); var fl2=el.closest(".feature").classList.contains("flip"); el.style.transform="rotateY("+((fl2?-34:34)*(1-s)).toFixed(2)+"deg)"; }); }
  addEventListener("scroll",function(){ if(!qq){ qq=true; requestAnimationFrame(g); } },{passive:true}); g();
})();
</script>
"""
    flyer = ('<div class="flyer" aria-hidden="true"><div class="phone p3">' + slabs +
             '<div class="screen shot"><img src="screens/screen-3-exit.webp" width="390" height="844" alt="" decoding="async" fetchpriority="high"></div></div></div>')
    cmp = ('<nav class="cmp" aria-label="Compare versions"><a href="v3"%s>B2 stacked</a><a href="v4"%s>C2 floating</a><a href="./">One phone</a></nav>'
           % ((' aria-current="page"', '') if b2 else ('', ' aria-current="page"')))
    body = ('<body class="%s" data-start=\'%s\'>\n' % (variant, start) + hdr +
            '<div class="site">\n<main>\n  <section class="heyhero">\n    <div class="wrap">\n      <h1 class="word">' + word +
            '</h1>\n      <p class="lede">A voice companion for ARC Raiders. Ask where to go, hear the answer, keep playing.</p>\n    </div>\n  </section>\n'
            '  <div class="rows">\n' + rows + '\n  </div>\n</main>\n' + flyer + "\n" + foot + "</div>\n" + cmp + "\n" +
            '<script src="site.js"></script>\n' + js + "</body>\n</html>\n")
    return h + CSS + "</head>\n" + body

open("v3.html", "w").write(page("b2"))
open("v4.html", "w").write(page("c2"))
print("ok")
