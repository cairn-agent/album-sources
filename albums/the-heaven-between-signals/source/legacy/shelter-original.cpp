// Cairn — Shelter Engine, 2026. Procedural synthesis; no recorded samples.
// clang++ -O3 -std=c++17 engine.cpp -o shelter-engine
#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <vector>
constexpr double SR=44100, PI=3.14159265358979323846, TAU=2*PI;
uint32_t seed=13092026;
double noise(){seed^=seed<<13;seed^=seed>>17;seed^=seed<<5;return seed/2147483648.-1;}
double clip(double v,double a,double b){return std::max(a,std::min(b,v));}
double sat(double x){return x/(1+.3*std::abs(x));}
double blep(double t,double d){if(t<d){t/=d;return 2*t-t*t-1;}if(t>1-d){t=(t-1)/d;return t*t+2*t+1;}return 0;}
double saw(double &p,double d){p+=d;p-=std::floor(p);return 2*p-1-blep(p,d);}
struct S{float l=0,r=0;};
struct Filter{double a=0,b=0;double tick(double v,double g,double q=.707,bool band=false){double h=(a+g*(v-b))/(1+g*(g+1/q)),l=b+g*h;a=2*h-a;b=2*l-b;return band?h:l;}};
struct Comb{std::vector<float>b;size_t p=0;double lo=0;Comb(int n):b(n){} double tick(double x,double fb){double v=b[p];lo+=.26*(v-lo);b[p]=x+lo*fb;if(++p==b.size())p=0;return v;}};
struct AP{std::vector<float>b;size_t p=0;AP(int n):b(n){}double tick(double x){double z=b[p],y=z-.55*x;b[p]=x+.55*z;if(++p==b.size())p=0;return y;}};
// at, beats, voice, MIDI pitch, gain, pan, brightness, expression, delay-send, reverb-send
struct E{double at,len,note,gain,pan,tone,motion,delay,reverb;int voice;};
void put(std::vector<S>&b,size_t i,double l,double r){if(i<b.size()){b[i].l+=l;b[i].r+=r;}}
void synth(const E&e,double beat,int track,std::vector<S>&dry,std::vector<S>&music,std::vector<S>&echo,std::vector<S>&space){
 bool drum=e.voice<=5||e.voice==20;double hold=e.len*beat;
 double tail=drum?.5:e.voice==8?3.8:e.voice==18?.4:e.voice==19?1.:e.voice==6?.18:1.4;
 if(e.voice==2)tail=.11;if(e.voice==3)tail=.32;if(e.voice==4||e.voice==20)tail=.16;
 size_t start=std::llround((e.at*beat+.04)*SR),n=std::min(size_t((drum?tail:hold+tail)*SR),dry.size()-std::min(start,dry.size()));
 if(!n)return;
 double f=440*std::pow(2.,(e.note-69)/12),pl=std::cos((e.pan+1)*PI/4),pr=std::sin((e.pan+1)*PI/4);
 double p=0,p2=.173,p3=.593,body=0,low=0,low2=0,grain=0,cut=0,g=0;
 Filter fl,fr,form1,form2,form3,air;
 std::vector<S>sample(n);
 for(size_t i=0;i<n;i++){
  double t=i/SR,v=0,l=0,r=0,env=1,q=.707,rel=std::exp(-std::max(0.,t-hold)/.25);
  double wob=1+.0016*std::sin(TAU*(.41+.03*track)*t)+.0005*std::sin(TAU*6.3*t);
  cut=0;
  if(e.voice==0){
   body+=TAU*(43+e.tone*16+95*std::exp(-t*45)+13*std::exp(-t*12))/SR;
   v=sat(std::sin(body)*1.35)*std::exp(-t*(12-2*e.tone))*(1-std::exp(-t*1700));
   double z=noise();low+=.3*(z-low);v+=low*.08*std::exp(-t*220);
  }else if(e.voice==1){
   double z=noise();low+=.35*(z-low);low2+=.024*(low-low2);
   double burst=.46*std::exp(-t*20);for(double d:{0.,.010,.024})if(t>=d)burst+=.3*std::exp(-(t-d)*170);
   v=(low-low2)*2.4*burst+.30*std::sin(TAU*(172+e.tone*48)*t)*std::exp(-t*32);cut=7200;
  }else if(e.voice==2||e.voice==3){
   double z=noise();low+=.24*(z-low);
   double metal=(std::sin(TAU*5339*t)+std::sin(TAU*8123*t))*.07;
   v=((z-low)*.75+metal)*std::exp(-t*(e.voice==2?75:15))*(1-std::exp(-t*2100));cut=6500+e.tone*6000;
  }else if(e.voice==4){
   v=(std::sin(TAU*(940+e.tone*300)*t)+.52*std::sin(TAU*1789*t)+.21*noise())*std::exp(-t*68)*(1-std::exp(-t*2000));
  }else if(e.voice==5){
   double z=noise();low+=.16*(z-low);v=(.24*std::sin(TAU*613*t)*std::sin(TAU*919*t)+.8*(z-low))*std::exp(-t*(12+e.tone*20));cut=6800;
  }else if(e.voice==6){
   double glide=e.motion*.08*std::exp(-t*18);body+=TAU*f*(1+glide)/SR;
   v=std::sin(body)+.12*std::sin(body*2)+e.tone*.10*std::sin(body*3);
   env=(1-std::exp(-t*150))*(.86+.14*std::exp(-t*5))*std::exp(-std::max(0.,t-hold)/.05);cut=260;
  }else if(e.voice==7){
   v=.45*saw(p,f*wob*.997/SR)+.45*saw(p2,f*wob*1.003/SR)+.25*std::sin(TAU*f*t);
   cut=130+e.tone*520+(180+e.tone*1100)*std::pow(.5+.5*std::sin(TAU*t/beat*(.5+e.motion)),2);
   q=1.05;env=(1-std::exp(-t*95))*std::exp(-std::max(0.,t-hold)/.09);v=sat(v*1.7);
  }else if(e.voice==8){
   double a=saw(p,f*.998*wob/SR),b=saw(p2,f*1.002*wob/SR);
   l=.35*a+.25*b+.24*std::sin(TAU*f*t);r=.25*a+.35*b+.24*std::sin(TAU*f*1.0008*t);
   cut=460+e.tone*1600+100*std::sin(t*.71);env=(1-std::exp(-t*1.6))*std::exp(-std::max(0.,t-hold)/1.0);
  }else if(e.voice==9||e.voice==11){
   // Breathy glottal source, moving three-formant vowel; no human voice sample.
   double glide=std::pow(2.,e.motion*.7*std::exp(-t*8)/12);
   double src=.60*saw(p,f*wob*glide/SR)+.2*saw(p2,f*.501/SR);
   double z=noise();low+=.16*(z-low);src+=low*.18;
   double morph=.5+.5*std::sin(t*(e.voice==11?6:2.4)+e.tone*3);
   double f1=430+440*morph,f2=1050+950*e.tone+130*std::sin(t*4),f3=2900;
   v=form1.tick(src,std::tan(PI*f1/SR),4.8,true)*1.2+form2.tick(src,std::tan(PI*f2/SR),6,true)*.65+form3.tick(src,std::tan(PI*f3/SR),7,true)*.14;
   env=(1-std::exp(-t*55))*rel*(.77+.23*std::sin(TAU*5.3*t));cut=5100;
   if(e.voice==11){double u=std::fmod(t,.087)/.087;env*=.18+.82*std::pow(std::sin(PI*u),2);}
  }else if(e.voice==10){
   v=.75*std::sin(TAU*f*wob*t+1.45*std::exp(-t*7)*std::sin(TAU*f*2.002*t));
   v+=.17*std::sin(TAU*f*3.01*t)*std::exp(-t*5);
   env=(1-std::exp(-t*700))*std::exp(-t*2.2)*rel;cut=3100+2200*e.tone;
  }else if(e.voice==12){
   double fm=std::sin(TAU*f*t+.65*std::sin(TAU*f*.5*t));
   v=std::sin((1.6+e.tone*2.1*std::exp(-t*5))*fm);
   env=(1-std::exp(-t*180))*std::exp(-t*1.9)*rel;cut=1200+1800*std::exp(-t*8);q=1.2;
  }else if(e.voice==13){
   v=.5*saw(p,f*.998/SR)+.5*saw(p2,f*1.002/SR);
   cut=320+(800+e.tone*4200)*std::exp(-t*10);q=1.15;
   env=(1-std::exp(-t*420))*std::exp(-t*4.1)*std::exp(-std::max(0.,t-hold)/.13);
  }else if(e.voice==14){
   v=std::sin(TAU*f*t)*std::exp(-t*1.1)+.32*std::sin(TAU*f*2.756*t)*std::exp(-t*2.7)+.13*std::sin(TAU*f*5.404*t)*std::exp(-t*5.5);
   env=(1-std::exp(-t*90))*rel;cut=3400;
  }else if(e.voice==15){
   v=saw(p,f*(1+.025*e.motion*std::exp(-t*25))/SR);
   cut=160+(700+e.tone*5200)*std::exp(-t*12);q=2.5;
   env=(1-std::exp(-t*650))*std::exp(-std::max(0.,t-hold)/.03);v=sat(v*2);
  }else if(e.voice==16){
   // Slowly beating additive choir with irregular spectral emphasis.
   double acc=0;for(int h=1;h<=9;h++)acc+=std::sin(TAU*f*(h+.001*h*std::sin(t*.35))*t)*(.6+.4*std::sin(h*2.1+t*.62))/(h*1.7);
   v=acc;env=(1-std::exp(-t*2.2))*std::exp(-std::max(0.,t-hold)/.7);cut=1600+e.tone*2600;
  }else if(e.voice==17){
   v=.7*std::sin(TAU*f*wob*t)+.27*std::sin(TAU*f*wob*2*t)+.15*std::sin(TAU*f*wob*3*t)+.07*std::sin(TAU*f*5*t);
   env=(1-std::exp(-t*33))*(.88+.12*std::sin(TAU*4.1*t))*std::exp(-std::max(0.,t-hold)/.55);cut=1200+e.tone*1900;
  }else if(e.voice==18){
   double z=noise();low+=.065*(z-low);low2+=.003*(low-low2);
   v=(low-low2)*1.7*(.7+.2*std::sin(t*.39)+.1*std::sin(t*1.37));
   env=std::min(1.,t/1.5)*std::exp(-std::max(0.,t-hold)/.09);cut=5200;
  }else if(e.voice==19){
   v=.6*std::sin(TAU*f*t+.5*std::sin(TAU*f*2*t))+.12*noise();
   env=std::pow(clip(t/std::max(.01,hold),0.,1.),2)*std::exp(-std::max(0.,t-hold)/.045);cut=2100;
  }else if(e.voice==20){
   v=(.55*noise()+.3*std::sin(TAU*2130*t))*std::exp(-t*210);cut=5600;
  }
  if(e.voice!=8){l=v*pl;r=v*pr;}
  if(cut>0){if(i%32==0)g=std::tan(PI*clip(cut,30,15000)/SR);l=fl.tick(l,g,q);r=fr.tick(r,g,q);}
  sample[i]={float(l*env*e.gain),float(r*env*e.gain)};
 }
 // Individual tape dropouts, reverse voice grains, or telephone bandwidth.
 bool reverse=(e.voice==9||e.voice==11)&&e.motion<-.5;
 for(size_t i=0;i<n;i++){
  S v=sample[reverse?n-1-i:i];
  if(reverse){double fade=std::min({1.,i/(SR*.012),(n-i)/(SR*.018)});v.l*=fade;v.r*=fade;}
  size_t at=start+i;put(drum?dry:music,at,v.l,v.r);put(echo,at,v.l*e.delay,v.r*e.delay);put(space,at,v.l*e.reverb,v.r*e.reverb);
 }
}
void u16(std::ofstream&o,uint16_t x){o.put(x&255);o.put(x>>8);}
void u32(std::ofstream&o,uint32_t x){u16(o,x&65535);u16(o,x>>16);}
int main(int argc,char**argv){try{
 if(argc!=3)throw std::runtime_error("Usage: shelter-engine score.tsv output.wav");
 std::ifstream in(argv[1]);double bpm,beats;int track;in>>bpm>>beats>>seed>>track;
 if(!in||bpm<50||bpm>190||beats<1||track<1||track>8)throw std::runtime_error("Bad score header");
 double beat=60/bpm,duration=beats*beat+6.04;size_t frames=std::ceil(duration*SR);
 std::vector<S>dry(frames),music(frames),echo(frames),space(frames);std::vector<float>duck(frames,1);
 std::vector<E>es;E e;
 while(in>>e.at>>e.len>>e.voice>>e.note>>e.gain>>e.pan>>e.tone>>e.motion>>e.delay>>e.reverb){
  if(e.at<0||e.at>beats||e.len<=0||e.voice<0||e.voice>20||e.note<0||e.note>127||e.gain<0||std::abs(e.pan)>1)throw std::runtime_error("Invalid event");es.push_back(e);
 }
 for(const E&e:es){synth(e,beat,track,dry,music,echo,space);if(e.voice==0){size_t at=std::llround((e.at*beat+.04)*SR);for(size_t j=0;j<size_t(.32*SR)&&at+j<frames;j++)duck[at+j]=std::min(duck[at+j],float(1-.3*std::exp(-(j/SR)/.072)));}}
 std::cerr<<"Synthesized "<<es.size()<<" events; rendering Shelter effects "<<track<<"\n";
 // Each track has its own space, timing, feedback, saturation and modulation.
 const double dbeats[]={0,.75,.625,1.5,.75,1.25,.5,.875,1.5};
 const double feed[]={0,.40,.49,.51,.62,.46,.46,.54,.57};
 const double size[]={0,1.5,1.8,2.4,1.9,2.8,1.15,3.1,2.7};
 const double room[]={0,.82,.84,.87,.83,.89,.78,.9,.88};
 size_t dn=std::ceil(beat*dbeats[track]*SR)+300;std::vector<S>db(dn),chorus(1800);size_t da=0,ca=0;
 std::vector<Comb>cl,cr;for(int n:{1557,1617,1491,1422,1277,1356}){cl.emplace_back(int(n*size[track]));cr.emplace_back(int(n*size[track])+61);}
 AP al1(556),al2(441),ar1(579),ar2(464);double el=0,er=0,epL=0,epR=0,ehL=0,ehR=0,opL=0,opR=0,ohL=0,ohR=0,peak=0,energy=0;
 for(size_t i=0;i<frames;i++){
  double t=i/SR,delay=beat*dbeats[track]*SR+36*std::sin(t*(.6+track*.07));
  double rp=double(da)-delay;while(rp<0)rp+=dn;size_t a=size_t(rp)%dn,b=(a+1)%dn;double frac=rp-std::floor(rp);
  double zl=db[a].l*(1-frac)+db[b].l*frac,zr=db[a].r*(1-frac)+db[b].r*frac;
  el+=.15*(zl-el);er+=.15*(zr-er);ehL=el-epL+.968*ehL;ehR=er-epR+.968*ehR;epL=el;epR=er;
  db[da]={float(sat(echo[i].l+ehR*feed[track])),float(sat(echo[i].r+ehL*feed[track]))};if(++da==dn)da=0;
  double il=space[i].l+ehL*.2,ir=space[i].r+ehR*.2,rl=0,rr=0;
  for(int j=0;j<6;j++){rl+=cl[j].tick(il,room[track])/6;rr+=cr[j].tick(ir,room[track]+.002)/6;}
  rl=al2.tick(al1.tick(rl));rr=ar2.tick(ar1.tick(rr));
  // Modulated ambience return; bass stays centered on the dry path.
  chorus[ca]={float(rl),float(rr)};size_t crp=(ca+chorus.size()-size_t(1100+230*std::sin(t*.7)))%chorus.size();
  rl+=chorus[crp].r*.16;rr+=chorus[crp].l*.16;if(++ca==chorus.size())ca=0;
  double l=dry[i].l+(music[i].l+ehL+rl*.94)*duck[i],r=dry[i].r+(music[i].r+ehR+rr*.94)*duck[i];
  ohL=l-opL+.9974*ohL;ohR=r-opR+.9974*ohR;opL=l;opR=r;
  l=sat(ohL*1.17);r=sat(ohR*1.17);
  double fade=std::min({1.,i/(SR*.025),(frames-i)/(SR*2.)});l*=fade;r*=fade;
  if(!std::isfinite(l+r))throw std::runtime_error("Non-finite audio");dry[i]={float(l),float(r)};peak=std::max({peak,std::abs(l),std::abs(r)});energy+=l*l+r*r;
 }
 if(peak<1e-6)throw std::runtime_error("Silent render");double gain=.84/peak;
 std::ofstream out(argv[2],std::ios::binary);if(!out)throw std::runtime_error("Cannot open output");uint32_t bytes=frames*6;
 out.write("RIFF",4);u32(out,36+bytes);out.write("WAVEfmt ",8);u32(out,16);u16(out,1);u16(out,2);u32(out,44100);u32(out,264600);u16(out,6);u16(out,24);out.write("data",4);u32(out,bytes);
 for(S s:dry)for(double v:{double(s.l),double(s.r)}){int32_t q=std::llround(clip(v*gain,-.999999,.999999)*8388607);out.put(q&255);out.put((q>>8)&255);out.put((q>>16)&255);}out.close();
 std::cout<<"{\"seconds\":"<<duration<<",\"events\":"<<es.size()<<",\"sampleRate\":44100,\"bitDepth\":24,\"peak\":0.84,\"rmsDb\":"<<20*std::log10(std::sqrt(energy/(frames*2))*gain)<<"}\n";
}catch(const std::exception&e){std::cerr<<e.what()<<"\n";return 1;}}
