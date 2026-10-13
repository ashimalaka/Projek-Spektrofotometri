(function(){
if(!window.THREE){document.body.innerHTML='<p style="padding:24px;font:15px sans-serif">Three.js tidak dapat dimuat (perlu internet ke cdn.jsdelivr.net).</p>';return}
const T=THREE,C=CFG,$=i=>document.getElementById(i),V=(x,y,z)=>new T.Vector3(x,y,z),PI=Math.PI;
const box=$('v'),R=new T.WebGLRenderer({antialias:true});R.shadowMap.enabled=true;R.setPixelRatio(Math.min(devicePixelRatio,2));box.prepend(R.domElement);
const sc=new T.Scene();sc.background=new T.Color(0xdde4ea);
const cam=new T.PerspectiveCamera(38,1,.1,100);let th=.5,ph=1.15,rad=18;const tg=V(1.3,2,.8);
const setCam=()=>{cam.position.set(tg.x+rad*Math.sin(ph)*Math.sin(th),tg.y+rad*Math.cos(ph),tg.z+rad*Math.sin(ph)*Math.cos(th));cam.lookAt(tg)};
const fit=()=>{const w=box.clientWidth,h=box.clientHeight;R.setSize(w,h);cam.aspect=w/h;cam.updateProjectionMatrix()};addEventListener('resize',fit);
sc.add(new T.HemisphereLight(0xffffff,0x8899aa,.75));
const dl=new T.DirectionalLight(0xffffff,.8);dl.position.set(6,14,9);dl.castShadow=true;dl.shadow.mapSize.set(2048,2048);
Object.assign(dl.shadow.camera,{left:-14,right:14,top:14,bottom:-14});sc.add(dl);
const fl=new T.PointLight(0xff9a3c,0,8);fl.position.set(-.5,2.6,.4);sc.add(fl);
const M=(c,r=.45,m=.1,op=1)=>{const x=new T.MeshStandardMaterial({color:c,roughness:r,metalness:m,transparent:op<1,opacity:op,side:T.DoubleSide});x.userData.b=op;return x};
const B=(c,op)=>new T.MeshBasicMaterial({color:c,transparent:true,opacity:op,depthWrite:false,blending:T.AdditiveBlending});
const mWh=M(0xeef1f3,.35,.05),mGr=M(0x39444e,.5,.3),mMt=M(0xaab4bc,.3,.5),mGl=M(0xcfe6f5,.1,0,.32),mDk=M(0x111111,.6,0),mCu=M(0xb87333,.35,.8);
const bx=(w,h,d)=>new T.BoxGeometry(w,h,d),cy=(r,h,s=28,r2=r,o=false)=>new T.CylinderGeometry(r2,r,h,s,1,o),RX=[0,0,PI/2],RZ=[PI/2,0,0];
const G={},shellM=new Set(),pick=[],LB=[];
const grp=(id,ex,pos=[0,0,0],rot=0)=>{const g=new T.Group();g.position.set(...pos);g.rotation.y=rot;g.userData={id,ex:V(...ex),home:g.position.clone()};sc.add(g);G[id]=g;return g};
function mesh(id,geo,mat,p,o={}){const m=new T.Mesh(geo,mat);m.position.set(...p);if(o.r)m.rotation.set(...o.r);m.castShadow=m.receiveShadow=true;m.userData.id=id;(o.p||G[id]).add(m);
 if(!o.i)shellM.add(mat);if(!o.n)pick.push(m);return m}
const tube=(pts,r,mat,id,o={})=>{const c=new T.CatmullRomCurve3(pts);mesh(id,new T.TubeGeometry(c,24,r,8),mat,[0,0,0],o);return c};
const inner={};
function lab(id,txt,pos,i,par){const a=new T.Object3D();a.position.set(...pos);(par||G[id]).add(a);const e=document.createElement('div');e.textContent=(i?'':id+'. ')+txt;e.className=i?'i':'o';
 e.onclick=()=>sel(id);$('labs').appendChild(e);LB.push({a,e,i})}
// ---- bangku
const bench=new T.Mesh(bx(26,.3,11),M(0xb8c3cb,.6,0));bench.position.set(1,-.15,.5);bench.receiveShadow=true;sc.add(bench);
// ---- 1 casing
grp(1,[0,0,0]);const w=(a,b,c,x,y,z,m=mWh)=>mesh(1,bx(a,b,c),m,[x,y,z]);
w(11.2,.2,5.2,0,.1,0,mGr);w(11.2,3.4,.1,0,1.9,-2.55);w(.1,3.4,5.2,-5.55,1.9,0);w(.1,3.4,5.2,5.55,1.9,0);
w(3,3.4,.1,-4,1.9,2.55);w(3,3.4,.1,4,1.9,2.55);w(4,.8,.1,-.5,.6,2.55);
const door=new T.Object3D();door.position.set(-.5,3.6,2.55);G[1].add(door);
mesh(1,bx(4,2.8,.1),mWh,[0,-1.4,0],{p:door});mesh(1,bx(3.2,1.7,.04),M(0x223344,.1,0,.55),[0,-1.4,.07],{p:door});
const lidL=new T.Object3D(),lidR=new T.Object3D();lidL.position.set(-4,3.6,-2.55);lidR.position.set(3.5,3.6,-2.55);G[1].add(lidL,lidR);
mesh(1,bx(3,.1,5.1),mWh,[0,0,2.55],{p:lidL});mesh(1,bx(4,.1,5.1),mWh,[0,0,2.55],{p:lidR});
const cv=document.createElement('canvas');cv.width=512;cv.height=128;let x=cv.getContext('2d');x.fillStyle='#1c2833';x.fillRect(0,0,512,128);x.fillStyle='#fff';x.font='bold 46px sans-serif';x.fillText('AAS  Nyala',20,60);x.fillStyle='#e0a060';x.font='28px sans-serif';x.fillText('Cu 324,7 nm',20,105);
mesh(1,new T.PlaneGeometry(2.4,.6),new T.MeshBasicMaterial({map:new T.CanvasTexture(cv)}),[-4,2.9,2.62],{i:1,n:1});
lab(1,'Casing',[-5.4,3.2,2.6]);lab(1,'Tutup atas (lid)',[-4,3.7,0],1);lab(1,'Pintu atomisasi',[-.5,2.4,2.7],1);lab(1,'Panel depan',[4,.9,2.6],1);
// ---- 2 lampu HCL
grp(2,[-1.6,.9,0]);
mesh(2,cy(.22,.5),mGr,[-4.85,2.3,0],{r:RX});mesh(2,cy(.2,1.1),mGl,[-4.15,2.3,0],{r:RX});mesh(2,cy(.9,.08,32),mGr,[-4.3,1.9,0]);
mesh(2,cy(.09,.5),mCu,[-4.05,2.3,0],{r:RX,i:1});mesh(2,cy(.015,.8),mMt,[-4.2,2.3,.13],{r:RX,i:1});mesh(2,cy(.19,.03),M(0x9fd4ff,.1,0,.6),[-3.63,2.3,0],{r:RX,i:1});
const glow=new T.Mesh(new T.SphereGeometry(.13,16,12),new T.MeshBasicMaterial({color:0xc58cff,transparent:true,opacity:0}));glow.position.set(-3.85,2.3,0);G[2].add(glow);
lab(2,'Lampu HCL Cu',[-4.4,2.75,0]);lab(2,'Katoda Cu',[-4.05,2.3,0],1);lab(2,'Anoda',[-4.2,2.55,.13],1);lab(2,'Jendela kuarsa',[-3.6,2.65,0],1);lab(2,'Soket / basis',[-4.95,2.65,0],1);lab(2,'Turret lampu',[-4.3,1.8,.8],1);
// ---- 3 vial, 14 botol limbah
grp(3,[0,0,1.2]);mesh(3,cy(.35,.7),mGl,[-2,.35,3.2]);
const liq=M(0xd6ecff,.1,0,.85),liqM=mesh(3,cy(.31,.45),liq,[-2,.3,3.2],{i:1});lab(3,'Wadah sampel',[-2,1,3.2]);lab(3,'Larutan Cu²⁺',[-2,.3,3.2],1);
grp(14,[.8,0,1.2]);mesh(14,cy(.45,.9),mGl,[.2,.45,3.2]);mesh(14,cy(.4,.35),M(0xd9a441,.2,0,.85),[.2,.25,3.2],{i:1});lab(14,'Botol limbah',[.2,1.05,3.2]);lab(14,'Limbah cair',[.2,.25,3.2],1);
// ---- 4 nebulizer
grp(4,[-1.4,0,.9]);mesh(4,cy(.13,.5),mMt,[-2.05,1.2,0],{r:RX});
const cap=tube([V(-2.05,1.2,0),V(-2.05,.6,.4),V(-2.05,.5,2),V(-2,.5,3.1),V(-2,.2,3.2)],.035,M(0xf1c40f,.3,0),4);
lab(4,'Nebulizer',[-2.2,1.55,0]);lab(4,'Kapiler hisap',[-2.05,.5,1.5],1);lab(4,'Nosel venturi',[-2.05,1.2,.2],1);lab(4,'Impact bead',[-1.75,1.2,.2],1);
// ---- 5 spray chamber
grp(5,[0,-.3,1.3]);mesh(5,cy(.38,1.5),M(0xeaf2f8,.15,0,.4),[-1.1,1.2,0],{r:RX});
mesh(5,cy(.32,.03),mDk,[-.8,1.2,0],{r:RX,i:1});mesh(5,new T.SphereGeometry(.1,12,10),mWh,[-1.75,1.2,0],{i:1});
tube([V(-.7,.85,0),V(-.7,.45,.6),V(-.1,.4,2.6),V(.2,.95,3.2)],.05,M(0x7f8c8d,.4,.2),5,{i:1});
lab(5,'Spray chamber',[-1.1,1.75,0]);lab(5,'Flow spoiler',[-.8,1.2,.3],1);lab(5,'Selang drain',[-.4,.45,1.4],1);
// ---- 6 burner
grp(6,[0,.9,0]);mesh(6,cy(.22,.3),mMt,[-.5,1.7,0]);mesh(6,bx(1.1,.18,.3),mGr,[-.5,1.88,0]);mesh(6,bx(1,.02,.05),mDk,[-.5,1.98,0],{i:1});
lab(6,'Burner head',[-1.2,1.95,.4]);lab(6,'Slot burner',[-.5,2,.2],1);lab(6,'Leher burner',[-.5,1.7,.25],1);
// ---- 7 gas
grp(7,[0,0,-1.3]);const mA=M(0x3498db,.4,0),mF=M(0xe74c3c,.4,0);
const cA=tube([V(-1.7,.8,-2.5),V(-1.7,.8,-1),V(-1.9,1.1,-.3),V(-2,1.2,-.1)],.06,mA,7),cF=tube([V(-1.3,.8,-2.5),V(-1.3,.9,-1),V(-1.2,1.4,-.35),V(-1.15,1.52,-.1)],.06,mF,7);
lab(7,'Saluran gas',[-1.5,.55,-2.3]);lab(7,'Selang udara',[-1.7,.9,-1.6],1);lab(7,'Selang asetilena',[-1.3,1,-1.5],1);
// ---- 8 nyala
const fg=grp(8,[0,1.6,0],[-.5,1.97,0]);
const cone=(h,c,o)=>{const g=new T.ConeGeometry(.5,h,24,1,true);g.translate(0,h/2,0);const m=new T.Mesh(g,B(c,o));m.scale.z=.25;fg.add(m);return m};
const fS=cone(1.1,0xffd27a,.18),fI=cone(.75,0xff9a3c,.4),fP=cone(.3,0x3b82f6,.6);fg.visible=false;
lab(8,'Nyala',[.7,1.3,0]);lab(8,'Zona primer',[-.7,.12,.2],1,fg);lab(8,'Zona interkonal (serapan)',[.75,.5,0],1,fg);lab(8,'Zona sekunder',[-.7,.95,0],1,fg);
const sp=new T.Mesh(new T.SphereGeometry(.06,8,8),new T.MeshBasicMaterial({color:0xfff2a0}));sp.visible=false;sp.position.y=.1;fg.add(sp);
// ---- 9 monokromator
grp(9,[0,1.4,-1.4]);mesh(9,bx(2.9,1.6,2.6),M(0xaab7c2,.5,.2,.9),[3.05,2.3,-.1]);
mesh(9,bx(.04,.4,.08),mDk,[1.75,2.3,.07],{i:1});mesh(9,bx(.04,.4,.08),mDk,[1.75,2.3,-.07],{i:1});
mesh(9,bx(.05,.45,.55),mMt,[3.9,2.3,0],{r:[0,.55,0],i:1});mesh(9,bx(.05,.5,.7),M(0xb18cf0,.2,.8),[3.0,2.3,-.95],{r:[0,-.5,0],i:1});
mesh(9,bx(.05,.45,.55),mMt,[3.9,2.3,-.95],{r:[0,.4,0],i:1});mesh(9,bx(.04,.4,.08),mDk,[4.4,2.3,-.3],{i:1});mesh(9,bx(.04,.4,.08),mDk,[4.4,2.3,-.42],{i:1});
lab(9,'Monokromator',[3,3.3,.6]);lab(9,'Celah masuk',[1.75,2.7,0],1);lab(9,'Cermin kolimator',[3.9,2.7,0],1);lab(9,'Kisi difraksi',[3,2.75,-.95],1);lab(9,'Cermin fokus',[3.95,2.75,-.95],1);lab(9,'Celah keluar',[4.4,2.7,-.36],1);
// ---- 10 PMT
grp(10,[1.2,.8,0]);mesh(10,cy(.35,.8),mGr,[4.95,2.3,-.36],{r:RX});mesh(10,cy(.3,.03),M(0xf1948a,.3,0),[4.58,2.3,-.36],{r:RX,i:1});
[0,1,2].forEach(k=>mesh(10,bx(.04,.3,.3),M(0xf7dc6f,.3,.6),[4.78+k*.15,2.3+(k%2?-.1:.1),-.36],{i:1}));mesh(10,cy(.04,.2),mMt,[5.2,2.3,-.36],{r:RX,i:1});
lab(10,'Detektor PMT',[4.95,2.85,-.36]);lab(10,'Fotokatoda',[4.58,1.95,-.36],1);lab(10,'Dinoda',[4.9,2.1,-.1],1);lab(10,'Anoda PMT',[5.25,2.3,-.1],1);
// ---- 11 elektronik
grp(11,[0,-.2,-1]);mesh(11,bx(1.8,.6,1.1),M(0x6e7b86,.5,.2,.9),[3.2,.7,-1.2]);mesh(11,bx(1.4,.05,.8),M(0x1e8449,.5,.1),[3.2,.55,-1.2],{i:1});
mesh(11,bx(.25,.1,.25),mDk,[2.8,.62,-1.2],{i:1});mesh(11,bx(.25,.1,.25),M(0x2c3e50),[3.6,.62,-1.2],{i:1});
lab(11,'Elektronik',[3.2,1.2,-1.2]);lab(11,'Penguat lock-in',[2.8,.7,-1.2],1);lab(11,'Konverter A/D',[3.6,.7,-1.2],1);
// ---- 12 komputer
grp(12,[1,0,.6],[8.2,0,.6],-.45);mesh(12,cy(.5,.06),mGr,[0,.03,0]);mesh(12,bx(.15,.9,.1),mGr,[0,.5,-.1]);mesh(12,bx(3,1.9,.12),mGr,[0,1.8,0]);mesh(12,bx(2,.06,.7),mGr,[-.2,.03,1.4]);
const sc2=document.createElement('canvas');sc2.width=512;sc2.height=300;const sx=sc2.getContext('2d'),stex=new T.CanvasTexture(sc2);
mesh(12,new T.PlaneGeometry(2.8,1.7),new T.MeshBasicMaterial({map:stex}),[0,1.8,.07],{i:1});
lab(12,'Komputer & software',[0,3,0]);lab(12,'Layar',[1.3,1.5,.1],1);lab(12,'Perangkat lunak AAS',[-1.2,2.4,.1],1);
// ---- 13 hood
grp(13,[0,1.8,0],[-.5,0,0]);const hm=M(0xaab7c2,.4,.3);mesh(13,cy(1,.9,32,.35,true),hm,[0,4.1,0]);mesh(13,cy(.35,2.2,24,.35,true),hm,[0,5.6,0]);
const fan=new T.Mesh(bx(.6,.02,.1),mDk);fan.position.set(0,5.4,0);G[13].add(fan);
lab(13,'Exhaust hood',[1,4.2,0]);lab(13,'Saluran buang (duct)',[.4,5.2,0],1);lab(13,'Kipas penghisap',[0,5.45,.2],1);
// ---- berkas cahaya
const pts=[V(-3.6,2.3,0),V(-1,2.3,0),V(0,2.3,0),V(1.7,2.3,0),V(3.9,2.3,0),V(3,2.3,-.95),V(3.9,2.3,-.95),V(4.4,2.3,-.36),V(4.55,2.3,-.36)];
const bm=[0,1,2].map(i=>B(0xa855f7,.9)),bg=new T.Group();sc.add(bg);
pts.slice(0,-1).forEach((a,i)=>{const b=pts[i+1],m=new T.Mesh(cy(.03,a.distanceTo(b),8),i<1?bm[0]:i<2?bm[1]:bm[2]);m.position.copy(a).add(b).multiplyScalar(.5);m.quaternion.setFromUnitVectors(V(0,1,0),b.clone().sub(a).normalize());bg.add(m)});
// ---- partikel
const mkP=(n,c,s)=>{const g=new T.BufferGeometry();g.setAttribute('position',new T.BufferAttribute(new Float32Array(n*3),3));const p=new T.Points(g,new T.PointsMaterial({color:c,size:s,transparent:true,opacity:.9,depthWrite:false}));p.frustumCulled=false;sc.add(p);return p};
const pA=mkP(24,0x3498db,.09),pF=mkP(24,0xe74c3c,.09),pL=mkP(14,0x1f6fd1,.08),pR=mkP(60,0x5dade2,.05),pH=mkP(40,0xffe08a,.05);
const setP=(p,fn)=>{const a=p.geometry.attributes.position;for(let i=0;i<a.count;i++){const v=fn(i);a.setXYZ(i,v.x,v.y,v.z)}a.needsUpdate=true};
// ---- UI / data
const S={lamp:0,air:0,fuel:0,spark:0,flame:0,asp:0,A:0,on:0,conc:0},D={lamp:0,air:0,fuel:0,spark:0,flame:0,asp:0,A:0,conc:0};
const steps=['Exhaust ON & lampu HCL pemanasan','Udara tekan dibuka (oksidan)','Asetilena dibuka (bahan bakar)','Igniter memercikkan api','Nyala stabil (autozero blanko)','Siap aspirasi sampel'];
$('steps').innerHTML=steps.map(s=>'<li>'+s+'</li>').join('');
const stp=n=>[...$('steps').children].forEach((l,i)=>l.className=i<n?'d':i==n?'a':'');
const sleep=ms=>new Promise(r=>setTimeout(r,ms));let busy=false;
async function ignite(){if(S.on||busy)return;busy=true;S.exh=1;S.lamp=1;stp(0);await sleep(1300);S.air=1;stp(1);await sleep(1300);S.fuel=1;stp(2);await sleep(1300);S.spark=1;stp(3);await sleep(1500);S.flame=1;S.spark=0;stp(4);await sleep(1600);S.on=1;stp(5);busy=false}
async function shutdown(){if(busy)return;busy=true;S.asp=0;S.on=0;S.fuel=0;stp(-1);await sleep(1200);S.flame=0;await sleep(800);S.air=0;S.lamp=0;stp(-1);busy=false}
C.runs.forEach((r,i)=>{const o=document.createElement('option');o.value=i;o.textContent=r.type+' - '+r.name+' ('+r.conc+' mg/L)';$('sol').appendChild(o)});
async function meas(i){const r=C.runs[i];if(!S.on){$('info').innerHTML='<b>Nyalakan nyala dulu</b> (tombol ▶ Nyalakan).';return}
 S.conc=r.conc;S.asp=1;await sleep(2000);let s=0;for(const a of r.A){S.A=a;s+=a;await sleep(900)}
 const m=s/r.A.length,t=$('res').insertRow();t.innerHTML='<td>'+r.name+'</td><td>'+r.conc+'</td><td>'+m.toFixed(4)+'</td><td>'+(100*Math.pow(10,-m)).toFixed(1)+'</td>';
 S.asp=0;S.A=0;await sleep(900)}
$('m1').onclick=()=>meas(+$('sol').value);$('mall').onclick=async()=>{for(let i=0;i<C.runs.length;i++){$('sol').value=i;await meas(i);if(!S.on)break}};
$('on').onclick=ignite;$('off').onclick=shutdown;
const tw=(el,to)=>{const e=$(el),iv=setInterval(()=>{const d=to-+e.value;if(Math.abs(d)<.02){e.value=to;clearInterval(iv)}else e.value=+e.value+Math.sign(d)*.03},16)};
$('bo').onclick=()=>['lid','door'].forEach(e=>tw(e,1));$('bc').onclick=()=>['lid','door','ex'].forEach(e=>tw(e,0));
$('xr').onchange=()=>shellM.forEach(m=>{const x=$('xr').checked;m.transparent=x||m.userData.b<1;m.opacity=x?Math.min(m.userData.b,.14):m.userData.b;m.depthWrite=!x;m.needsUpdate=true});
let bh=null;function sel(id){const c=C.parts.find(p=>p.id==id);if(bh){sc.remove(bh)}bh=new T.BoxHelper(G[id],0xff8c00);sc.add(bh);
 $('info').innerHTML='<b>'+c.id+'. '+c.outer+'</b><br>'+c.fn+'<br><u>Isi / nama dalam:</u><ul class="inn">'+c.inner.map(n=>'<li>'+n+'</li>').join('')+'</ul>'}
// ---- kamera & interaksi
let dn=false,mv=0,lx=0,ly=0;const rc=new T.Raycaster(),mo=new T.Vector2();
R.domElement.onpointerdown=e=>{dn=true;mv=0;lx=e.clientX;ly=e.clientY};
addEventListener('pointerup',e=>{if(dn&&mv<4&&e.target===R.domElement){const h=hit(e);if(h)sel(h.userData.id)}dn=false});
R.domElement.onpointermove=e=>{if(dn){mv+=Math.abs(e.clientX-lx)+Math.abs(e.clientY-ly);th-=(e.clientX-lx)*.006;ph=Math.min(1.5,Math.max(.2,ph-(e.clientY-ly)*.006));lx=e.clientX;ly=e.clientY;$('tip').style.display='none'}
 else{const h=hit(e),t=$('tip');if(h){t.style.display='block';t.style.left=e.offsetX+14+'px';t.style.top=e.offsetY+14+'px';const c=C.parts.find(p=>p.id==h.userData.id);t.textContent=c.id+'. '+c.outer}else t.style.display='none'}};
R.domElement.onwheel=e=>{e.preventDefault();rad=Math.min(32,Math.max(5,rad*(1+Math.sign(e.deltaY)*.08)))};
function hit(e){const r=R.domElement.getBoundingClientRect();mo.set((e.clientX-r.left)/r.width*2-1,-(e.clientY-r.top)/r.height*2+1);rc.setFromCamera(mo,cam);
 const x=$('xr').checked,h=rc.intersectObjects(pick.filter(m=>!(x&&m.userData.id==1)))[0];return h&&h.object}
// ---- layar monitor
const trace=[];function screen(){const a=D.A,t=100*Math.pow(10,-a);sx.fillStyle='#0b2239';sx.fillRect(0,0,512,300);sx.fillStyle='#8fd3ff';sx.font='bold 20px sans-serif';sx.fillText('AAS - Cu '+C.params.line,14,28);
 sx.fillStyle='#fff';sx.font='bold 54px sans-serif';sx.fillText('A = '+a.toFixed(4),14,92);sx.font='20px sans-serif';sx.fillStyle='#b8e0ff';sx.fillText('%T = '+t.toFixed(1)+'   I0=100   It='+t.toFixed(1),14,124);
 sx.fillText(S.on?(D.asp>.5?'Mengukur: '+S.conc+' mg/L':'Nyala siap'):'Nyala mati',14,152);
 trace.push(a>0.001?a+(Math.random()-.5)*.004:0);if(trace.length>110)trace.shift();sx.strokeStyle='#27ae60';sx.beginPath();trace.forEach((v,i)=>{const X=14+i*4.4,Y=285-Math.min(1,v/.8)*120;i?sx.lineTo(X,Y):sx.moveTo(X,Y)});sx.stroke();stex.needsUpdate=true}
// ---- loop
const tmp=V(0,0,0),cc=new T.Color();let n=0;fit();setCam();
function loop(){requestAnimationFrame(loop);const t=performance.now()/1000;n++;
 for(const k of['lamp','air','fuel','spark','flame','asp','A','conc'])D[k]+=((S[k]||0)-D[k])*.1;
 const ex=+$('ex').value;for(const id in G){const g=G[id];g.position.copy(g.userData.home).addScaledVector(g.userData.ex,ex*1.6)}
 lidL.rotation.x=lidR.rotation.x=-1.7*$('lid').value;door.rotation.x=-1.9*$('door').value;
 glow.material.opacity=D.lamp*.9;fan.rotation.y=t*(S.exh?25:0);
 bg.visible=$('bm').checked&&ex<.1;const rel=Math.max(.06,Math.pow(10,-D.A));bm[0].opacity=.9*D.lamp;bm[1].opacity=bm[2].opacity=.9*D.lamp*rel;
 const cu=Math.min(1,D.conc/6)*D.asp;fg.visible=D.flame>.03;fg.scale.set(1,D.flame*(1+.05*Math.sin(t*20)),1);
 fS.material.opacity=.18*D.flame;fI.material.opacity=.4*D.flame*(.85+.15*Math.random());fP.material.opacity=.6*D.flame;
 fI.material.color.copy(cc.set(0xff9a3c).lerp(new T.Color(0x35e08a),cu));fS.material.color.copy(cc.set(0xffd27a).lerp(new T.Color(0x7dffb0),cu));
 fl.intensity=1.3*D.flame;fl.color.copy(fI.material.color);sp.visible=S.spark&&Math.random()<.5;sp.position.x=(Math.random()-.5)*.9;
 pA.visible=D.air>.05;pF.visible=D.fuel>.05;setP(pA,i=>cA.getPoint((i/24+t*.3)%1));setP(pF,i=>cF.getPoint((i/24+t*.3)%1));
 pL.visible=D.asp>.05;setP(pL,i=>cap.getPoint(1-((i/14+t*.4)%1)));liq.color.copy(cc.set(0xd6ecff).lerp(new T.Color(0x1f6fd1),Math.min(1,S.conc/6)));
 pR.visible=D.asp>.05;setP(pR,i=>V(-1.8+Math.random()*1.4,1.2+(Math.random()-.5)*.5,(Math.random()-.5)*.5));
 pH.visible=D.flame>.2;setP(pH,i=>{const u=(i/40+t*.5)%1;return V(-.5+(Math.sin(i*12.9)*.45),1.97+u*1.1*D.flame,Math.sin(i*7.3)*.05)});
 const xr=$('xr').checked,w=box.clientWidth,h=box.clientHeight;
 LB.forEach(l=>{const show=l.i?(xr&&$('li').checked):$('lo').checked;if(!show){l.e.style.display='none';return}l.a.getWorldPosition(tmp);tmp.project(cam);
  if(tmp.z>1){l.e.style.display='none';return}l.e.style.display='block';l.e.style.left=(tmp.x*.5+.5)*w+'px';l.e.style.top=(-tmp.y*.5+.5)*h+'px'});
 if(bh)bh.update();if(n%6==0)screen();setCam();R.render(sc,cam)}
loop();
})();
