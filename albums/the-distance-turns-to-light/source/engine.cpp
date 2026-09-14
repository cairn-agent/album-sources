// Cairn's Night Engine. Original synthesis and effects; no sample libraries.
// Build: clang++ -O3 -std=c++17 engine.cpp -o night-engine
#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>
constexpr double SR=44100., PI=3.14159265358979323846, TAU=2*PI;
struct Stereo {float l=0,r=0; Stereo& operator+=(Stereo b){l+=b.l;r+=b.r;return *this;}};
uint32_t seed=19992001;
inline float noise(){seed^=seed<<13;seed^=seed>>17;seed^=seed<<5;return (seed/2147483648.f)-1.f;}
inline double clip(double x,double a,double b){return std::max(a,std::min(b,x));}
inline double soft(double x){return x/(1.+std::abs(x)*.28);}
inline double blep(double t,double dt){if(t<dt){t/=dt;return t+t-t*t-1;}if(t>1-dt){t=(t-1)/dt;return t*t+t+t+1;}return 0;}
inline double saw(double &p,double dt){p+=dt;if(p>=1)p-=1;return 2*p-1-blep(p,dt);}
struct SVF {double a=0,b=0;
  double tick(double v,double g,double q,bool band=false){double k=1./q;double s1=(a+g*(v-b))/(1+g*(g+k));double s2=b+g*s1;a=2*s1-a;b=2*s2-b;return band?s1:s2;}
};
struct Comb {std::vector<float> b;size_t at=0;double low=0;Comb(int n):b(n){} double tick(double x,double fb){double v=b[at];low=.57*low+.43*v;b[at]=x+low*fb;if(++at==b.size())at=0;return v;}};
struct Allpass {std::vector<float>b;size_t at=0;Allpass(int n):b(n){}double tick(double x){double z=b[at];double out=z-x*.5;b[at]=x+z*.5;if(++at==b.size())at=0;return out;}};
struct Event {double at,len,note,gain,pan,tone,motion;int voice;};
// 0 kick,1 clap,2 closed hat,3 open hat,4 snare,5 ride,6 bass,
// 7 seven-saw lead,8 acid,9 pad,10 glass,11 pluck,12 sweep,13 impact,14 gated choir.
void put(std::vector<Stereo>& v,size_t at,double l,double r){if(at<v.size()){v[at].l+=l;v[at].r+=r;}}
void synth(const Event&e,double beat,std::vector<Stereo>&dry,std::vector<Stereo>&music,
           std::vector<Stereo>&echo,std::vector<Stereo>&space){
  bool drum=e.voice<=5;double hold=e.len*beat,tail=.09;
  if(e.voice==0)tail=.43; if(e.voice==1||e.voice==4)tail=.26;
  if(e.voice==2)tail=.08;if(e.voice==3)tail=.23;if(e.voice==5)tail=.56;
  if(e.voice==7)tail=.19;if(e.voice==8)tail=.07;if(e.voice==9)tail=2.6;
  if(e.voice==10)tail=1.4;if(e.voice==11)tail=.21;if(e.voice==12)tail=.15;
  if(e.voice==13)tail=3.;if(e.voice==14)tail=.55;
  double total=drum?tail:hold+tail;
  size_t start=std::llround((e.at*beat+.04)*SR),n=std::min(size_t(total*SR),dry.size()-std::min(start,dry.size()));
  if(!n)return;
  double f=440*std::pow(2.,(e.note-69)/12),pl=std::cos((e.pan+1)*PI/4),pr=std::sin((e.pan+1)*PI/4);
  std::array<double,7>phase={.03,.19,.43,.63,.81,.29,.91};
  const std::array<double,7>cents={-22,-12,-5,0,5,12,22};
  const std::array<double,7>pans={-.92,.71,-.35,0,.35,-.71,.92};
  std::array<double,7>dt,ls,rs;
  double spread=e.voice==9?1.3:1.;
  for(int j=0;j<7;j++){dt[j]=f*std::pow(2.,cents[j]*spread/1200.)/SR;ls[j]=std::cos((pans[j]+1)*PI/4);rs[j]=std::sin((pans[j]+1)*PI/4);}
  SVF fl,fr,air,form1,form2;double low=0,lo2=0,osc=0,bodyPhase=0,g=0;
  double ds=0,rv=0;
  if(e.voice==7){ds=.21;rv=.15;}if(e.voice==8){ds=.16;rv=.05;}
  if(e.voice==9){ds=.08;rv=.33;}if(e.voice==10){ds=.32;rv=.36;}
  if(e.voice==11){ds=.29;rv=.19;}if(e.voice==14){ds=.15;rv=.32;}
  if(e.voice==1||e.voice==4)rv=.12;if(e.voice==12||e.voice==13)rv=.38;
  for(size_t i=0;i<n;i++){
    double t=i/SR,v=0,l=0,r=0,env=1,cut=0,q=.707;
    if(e.voice==0){
      double hz=46.+111*std::exp(-t*39)+24*std::exp(-t*11);
      bodyPhase+=TAU*hz/SR;
      v=std::sin(bodyPhase)*std::exp(-t*9.8)*(1-std::exp(-t*1700));
      v=soft(v*1.9)*.72 + noise()*.095*std::exp(-t*400);
    }else if(e.voice==1||e.voice==4){
      double z=noise();low+=.17*(z-low);lo2+=.025*(low-lo2);
      double ne=std::exp(-t*25);
      if(e.voice==1){ne=.23*std::exp(-t*18);for(double b:{0.,.011,.022,.034})if(t>=b)ne+=.4*std::exp(-(t-b)*210);}
      v=(low-lo2)*3.0*ne+.22*std::sin(TAU*184*t)*std::exp(-t*35);
    }else if(e.voice==2||e.voice==3||e.voice==5){
      double z=noise();low+=.29*(z-low);
      double metal=(std::sin(TAU*5273*t)>0?1.:-1.)+(std::sin(TAU*7361*t)>0?.45:-.45);
      double decay=e.voice==2?64:e.voice==3?19:9;
      v=((z-low)*.8+metal*.09)*std::exp(-t*decay)*(1-std::exp(-t*1800));
    }else if(e.voice==6){
      double s=saw(phase[0],f/SR),s2=saw(phase[1],f*1.002/SR);
      v=(s*.48+s2*.20+std::sin(TAU*f*t)*.40);
      cut=140+e.tone*1100+2600*std::exp(-t*26);q=.8;
      env=(1-std::exp(-t*700))*(.73+.27*std::exp(-t*18))*std::exp(-std::max(0.,t-hold)/.020);
    }else if(e.voice==7||e.voice==9){
      for(int j=0;j<7;j++){double s=saw(phase[j],dt[j]);l+=s*ls[j]/4.7;r+=s*rs[j]/4.7;}
      if(e.voice==7){env=std::min(1.,t/.007)*(.76+.24*std::exp(-t*7))*std::exp(-std::max(0.,t-hold)/.047);cut=850+e.tone*8200+e.motion*1600*std::exp(-t*6);q=.75;}
      else{env=std::min(1.,t/.7)*std::exp(-std::max(0.,t-hold)/.7);cut=500+e.tone*2600+120*std::sin(t*1.1);q=.72;}
    }else if(e.voice==8){
      double glide=1.+e.motion*.04*std::exp(-t*55);
      double s=saw(phase[0],f*glide/SR);double pp=phase[0]+.48;if(pp>=1)pp-=1;
      double sq=(phase[0]<.48?1.:-1.)+blep(phase[0],f/SR)-blep(pp,f/SR);
      v=soft((s*.65+sq*.28)*2.);cut=190+e.tone*4500*std::exp(-t*(8+e.motion*5));q=2.1+e.tone*.65;
      env=std::min(1.,t/.002)*std::exp(-std::max(0.,t-hold)/.017);
    }else if(e.voice==10){
      v=std::sin(TAU*f*t+1.9*std::exp(-t*4)*std::sin(TAU*f*2.001*t))*.7;
      v+=.18*std::sin(TAU*f*3.002*t)*std::exp(-t*8);
      env=(1-std::exp(-t*800))*std::exp(-t*1.7)*std::exp(-std::max(0.,t-hold)/.5);
      cut=4500+e.tone*5500;
    }else if(e.voice==11){
      v=(saw(phase[0],f/SR)+saw(phase[1],f*1.005/SR))*.48;
      cut=450+(2000+e.tone*7000)*std::exp(-t*15);q=1.05;
      env=std::min(1.,t/.002)*std::exp(-t*7)*std::exp(-std::max(0.,t-hold)/.055);
    }else if(e.voice==12){
      double u=clip(t/std::max(.01,hold),0.,1.);double z=noise();
      double freq=e.motion<0?700+7500*(1-u):400+8500*u*u;
      if(i%32==0)g=std::tan(PI*freq/SR);
      v=air.tick(z,g,1.3,true)*.52;
      env=std::pow(std::sin(PI*.5*u),1.4)*std::exp(-std::max(0.,t-hold)/.025);
      if(e.motion<0)env=std::exp(-t/std::max(.1,hold*.25));
    }else if(e.voice==13){
      double z=noise();low+=.1*(z-low);v=low*std::exp(-t*2.5)+.22*std::sin(TAU*53*t)*std::exp(-t*6);env=std::min(1.,t/.002);
    }else if(e.voice==14){
      double s=(saw(phase[0],f/SR)+saw(phase[1],f*.997/SR))*.5;
      v=form1.tick(s,std::tan(PI*730/SR),2.3,true)*.8+form2.tick(s,std::tan(PI*1260/SR),3.2,true)*.45;
      double steps=std::fmod(e.at+t/beat,.5)/.5;
      double gate=.22+.78*std::pow(std::sin(PI*steps),2);
      env=std::min(1.,t/.12)*std::exp(-std::max(0.,t-hold)/.15)*gate;
      cut=2000+e.tone*3000;
    }
    if(e.voice!=7&&e.voice!=9){l=v*pl;r=v*pr;}
    if(cut>0){if(i%32==0)g=std::tan(PI*clip(cut,35,15000)/SR);l=fl.tick(l,g,q);r=fr.tick(r,g,q);}
    l*=env*e.gain;r*=env*e.gain;
    if(e.voice==8){l=soft(l*1.4);r=soft(r*1.4);}
    size_t at=start+i;
    put(drum?dry:music,at,l,r);if(ds)put(echo,at,l*ds,r*ds);if(rv)put(space,at,l*rv,r*rv);
  }
}
void u16(std::ofstream &o,uint16_t x){o.put(x&255);o.put((x>>8)&255);}
void u32(std::ofstream &o,uint32_t x){u16(o,x&65535);u16(o,x>>16);}
int main(int argc,char**argv){try{
  if(argc!=3)throw std::runtime_error("Usage: night-engine score.tsv output.wav");
  std::ifstream in(argv[1]);if(!in)throw std::runtime_error("Cannot read score");
  double bpm,beats;in>>bpm>>beats>>seed;double beat=60./bpm,duration=beats*beat+6.04;
  size_t frames=std::ceil(duration*SR);std::vector<Stereo>dry(frames),music(frames),echo(frames),space(frames);
  std::vector<Event>events;Event e;while(in>>e.at>>e.len>>e.voice>>e.note>>e.gain>>e.pan>>e.tone>>e.motion){
    if(e.at<0||e.at>beats||e.len<=0||e.voice<0||e.voice>14||e.note<0||e.note>127||e.gain<0)throw std::runtime_error("Invalid event");events.push_back(e);
  }
  std::vector<float>duck(frames,1.f);
  for(auto&e:events){synth(e,beat,dry,music,echo,space);if(e.voice==0){size_t at=std::llround((e.at*beat+.04)*SR);for(size_t j=0;j<size_t(beat*.92*SR)&&at+j<frames;j++){double t=j/SR;duck[at+j]=std::min(duck[at+j],float(1.-.36*std::exp(-t/.073)));}}}
  std::cerr<<"Synthesized "<<events.size()<<" events; processing stereo effects\n";
  size_t delay=std::llround(beat*.75*SR);std::vector<Stereo>db(delay);size_t da=0;double el=0,er=0,hpl=0,hpr=0,prevl=0,prevr=0;
  std::vector<Comb>cl,cr;for(int n:{1557,1617,1491,1422,1277,1356}){cl.emplace_back(n*2);cr.emplace_back(n*2+37);}
  Allpass al1(556),al2(441),ar1(579),ar2(464);double outprevl=0,outprevr=0,outl=0,outr=0,peak=0,energy=0;
  for(size_t i=0;i<frames;i++){
    Stereo z=db[da];el+=.24*(z.l-el);er+=.24*(z.r-er);
    hpl=el-prevl+.982*hpl;hpr=er-prevr+.982*hpr;prevl=el;prevr=er;
    db[da]={float(echo[i].l+hpr*.39),float(echo[i].r+hpl*.39)};if(++da==delay)da=0;
    double il=space[i].l+hpl*.18,ir=space[i].r+hpr*.18,rl=0,rr=0;
    for(int j=0;j<6;j++){rl+=cl[j].tick(il,.81)/6.;rr+=cr[j].tick(ir,.813)/6.;}
    rl=al2.tick(al1.tick(rl));rr=ar2.tick(ar1.tick(rr));
    double l=dry[i].l+(music[i].l+hpl+rl*.66)*duck[i],r=dry[i].r+(music[i].r+hpr+rr*.66)*duck[i];
    // DC/subsonic highpass, then gentle saturation. Loudness mastering is separate.
    outl=l-outprevl+.9972*outl;outr=r-outprevr+.9972*outr;outprevl=l;outprevr=r;
    l=soft(outl*1.12);r=soft(outr*1.12);
    double fade=std::min({1.,i/(SR*.012),(frames-i)/(SR*1.5)});l*=fade;r*=fade;
    if(!std::isfinite(l+r))throw std::runtime_error("Non-finite audio");
    dry[i]={float(l),float(r)};peak=std::max({peak,std::abs(l),std::abs(r)});energy+=l*l+r*r;
  }
  if(peak<1e-6)throw std::runtime_error("Silent render");
  double gain=.84/peak;
  std::ofstream out(argv[2],std::ios::binary);uint32_t bytes=frames*6;
  out.write("RIFF",4);u32(out,36+bytes);out.write("WAVEfmt ",8);u32(out,16);u16(out,1);u16(out,2);u32(out,44100);u32(out,264600);u16(out,6);u16(out,24);out.write("data",4);u32(out,bytes);
  for(auto x:dry)for(double s:{double(x.l),double(x.r)}){int32_t v=std::llround(clip(s*gain,-.999999,.999999)*8388607);out.put(v&255);out.put((v>>8)&255);out.put((v>>16)&255);}
  out.close();std::cout<<"{\"seconds\":"<<duration<<",\"events\":"<<events.size()<<",\"sampleRate\":44100,\"bitDepth\":24,\"peak\":0.84,\"rmsDb\":"<<20*std::log10(std::sqrt(energy/(2*frames))*gain)<<"}\n";
}catch(const std::exception&e){std::cerr<<e.what()<<"\n";return 1;}}
