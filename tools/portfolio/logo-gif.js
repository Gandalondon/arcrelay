// Relay logo loop for the portfolio: wordmark holds, the three signal lines draw in, hold, fade, repeat.
// Run from the repo root: node tools/portfolio/logo-gif.js  -> marketing/portfolio/relay-logo-loop.gif (1024 x 526, like sniff-logo-loop.gif)
const path=require("path"),fs=require("fs"),{execFileSync}=require("child_process");
const {chromium}=require(require.resolve("playwright",{paths:[path.resolve(__dirname,"../../tests"),process.cwd()]}));
const out=path.resolve(__dirname,"../../marketing/portfolio");const tmp=fs.mkdtempSync(path.join(require("os").tmpdir(),"relaygif-"));
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1024,height:526},deviceScaleFactor:2});
await p.goto("file://"+path.resolve(__dirname,"logo-gif.html"));await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);
const fps=25,dur=3.2;for(let i=0;i<Math.round(fps*dur);i++){await p.evaluate(t=>frame(t),i/fps);await p.screenshot({path:path.join(tmp,String(i).padStart(3,"0")+".png")});}
await b.close();
execFileSync("python3",["-c",`
import glob,sys
from PIL import Image
fs=sorted(glob.glob(sys.argv[1]+"/*.png"))
ims=[Image.open(f).convert("RGB").resize((1024,526),Image.LANCZOS) for f in fs]
pal=ims[len(ims)//2].quantize(colors=64,method=Image.Quantize.MEDIANCUT)
q=[im.quantize(palette=pal,dither=Image.Dither.NONE) for im in ims]
q[0].save(sys.argv[2],save_all=True,append_images=q[1:],duration=40,loop=0,optimize=True,disposal=1)
`,tmp,path.join(out,"relay-logo-loop.gif")]);
console.log("ok",fs.statSync(path.join(out,"relay-logo-loop.gif")).size);})();
