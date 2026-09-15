// Cairn — Astra Cathedral Engine. Original procedural opera synthesis, 2026.
// MIT software; original music/lyrics CC BY 4.0. No samples or speech engine.
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
struct Stereo {float l=0,r=0;};
#include "legacy/window.hpp"
#include "legacy/shelter.hpp"
#include "legacy/night.hpp"
constexpr double SR=44100., PI=3.14159265358979323846, TAU=2*PI;
inline double clamp(double x,double a,double b){return std::max(a,std::min(b,x));}
inline double soft(double x){return x/(1+.12*std::abs(x));}
std::array<double,65537> sine;
inline double sn(double phase){phase-=std::floor(phase);double q=phase*65536;size_t i=size_t(q);return sine[i]+(sine[i+1]-sine[i])*(q-i);}
struct RNG{uint32_t s;double next(){s^=s<<13;s^=s>>17;s^=s<<5;return s/2147483648.-1;}};
struct Event{double at,len,note,gain,pan,tone,motion,delay,reverb;int voice,pre,next;uint32_t seed;};
using Bus=std::vector<Stereo>;
inline void add(Bus&v,size_t i,double l,double r){if(i<v.size()){v[i].l+=l;v[i].r+=r;}}
static const double formants[23][3]={
 {280,2250,3050},{390,1990,2700},{560,1840,2550},{750,1710,2450},
 {640,1200,2500},{780,1120,2600},{540,900,2450},{430,1080,2500},
 {320,800,2250},{470,1330,1700},{500,1500,2450},{780,1120,2600},
 {530,1850,2500},{540,1050,2450},{750,1120,2600},{520,880,2450},
 {250,1050,2150},{290,1600,2650},{290,1600,2650},{370,1180,2700},
 {390,1200,1650},{280,750,2300},{260,2200,3000}};
// The room instruments are ported from Cairn's JavaScript oscillator recipes.
void modern(const Event&e,Bus&orch,Bus&solo,Bus&choir,Bus&echo,Bus&space){
 bool vocal=e.voice>=1000;int cast=vocal?(e.voice-1000)/100:0,ph=vocal?(e.voice-1000)%100:0;
 bool drum=e.voice==307||e.voice==308||e.voice==309||(e.voice>=112&&e.voice<=115);
 double tail=vocal?.035:drum?(e.voice==308?8:2.8):e.voice==300||e.voice==301?1.2:e.voice==302||e.voice==304?2.2:1.1;
 size_t begin=std::llround(e.at*SR),n=std::min(size_t((e.len+tail)*SR),orch.size()-std::min(begin,orch.size()));
 if(!n)return;
 double f=440*std::pow(2.,(e.note-69)/12),pl=std::cos((e.pan+1)*PI/4),pr=std::sin((e.pan+1)*PI/4);
 RNG rng{e.seed?e.seed:1};std::array<double,8>phase;for(auto&p:phase)p=(rng.next()+1)*.5;
 Window::Filter f1,f2,f3,air,filterL,filterR;
 double low=0,low2=0,body=0,formG1=0,formG2=0,formG3=0,fc=0;
 const double color[]={.90,1.015,1.13,.79,1.02,.85};
 Bus&target=vocal?(cast<4?solo:choir):orch;
 for(size_t i=0;i<n;i++){
  double t=i/SR,u=clamp(t/std::max(.001,e.len),0.,1.),env=1,v=0,l=0,r=0,cut=0;
  double rel=std::exp(-std::max(0.,t-e.len)/(vocal?.008:.24));
  if(vocal){
   const double rate[]={4.7,5.1,5.65,3.7,5.0,3.1};
   double vibr=(cast==3?.004:cast==5?.005:.0032)*std::sin(TAU*(rate[cast]+e.tone*.5)*(e.at+t))*(.35+.65*std::min(1.,t*4));
   double drift=.0009*std::sin((e.at+t)*2.19+e.seed%37);
   double glide=e.motion*std::exp(-t*13),freq=f*std::pow(2.,glide/12)*(1+vibr+drift);
   phase[0]+=freq/SR;phase[0]-=std::floor(phase[0]);
   // Antialiased glottal excitation plus sinusoidal body and shaped aspiration.
   double src=(2*phase[0]-1-Window::blep(phase[0],freq/SR))*.58+.25*sn(phase[0]);
   double nz=rng.next();low+=.17*(nz-low);double high=nz-low;
   double a=500,b=1450,c=2500;
   if(ph<23){a=formants[ph][0];b=formants[ph][1];c=formants[ph][2];
    int end=ph==11||ph==12||ph==15?0:ph==13||ph==14?8:-1;
    if(end>=0){double z=clamp((u-.34)/.58,0.,1.);a+=(formants[end][0]-a)*z;b+=(formants[end][1]-b)*z;c+=(formants[end][2]-c)*z;}
    // Coarticulation preserves the direction of consonant/vowel transitions.
    if(e.pre>=0&&e.pre<23){double z=.22*std::exp(-t*34);a+=(formants[e.pre][0]-a)*z;b+=(formants[e.pre][1]-b)*z;}
    if(e.next>=0&&e.next<23){double z=.20*clamp((u-.85)/.15,0.,1.);a+=(formants[e.next][0]-a)*z;b+=(formants[e.next][1]-b)*z;}
   }
   double col=color[cast]*(.96+.08*e.tone);a*=col;b*=col;c*=col;
   if(i%32==0){formG1=std::tan(PI*a/SR);formG2=std::tan(PI*b/SR);formG3=std::tan(PI*c/SR);}
   bool voiced=ph<=22||ph==28||ph==29||ph==30||ph==31||ph>=35;
   if(voiced){v=1.9*f1.tick(src,formG1,4.8,true)+1.15*f2.tick(src,formG2,6.4,true)+.42*f3.tick(src,formG3,7.4,true)+.075*sn(phase[0]);
    v+=low*(cast==1?.05:cast==2?.035:.017);if(ph>=16&&ph<=18)v*=.64;
    if(cast==3)v+=.065*sn((e.at+t)*freq*.5); // the Carrier's impossible lower shadow
   }
   if(ph>=23&&ph<=31){double center=ph==23||ph==29?6400:ph==24||ph==30?3400:ph==27?1650:4300;
    v=(voiced?v*.4:0)+air.tick(nz,std::tan(PI*center/SR),.9,true)*(ph==27?.6:1.15);}
   if(ph>=32){double onset=.012,burst=t>onset?std::exp(-(t-onset)*110):0;
    double center=ph==32||ph==35?1250:ph==34||ph==37?2850:5300;
    v=(voiced?v*.22:0)+air.tick(nz,std::tan(PI*center/SR),1.,true)*burst*1.6;
    if(ph>=38)v+=high*.32*std::exp(-t*19);}
   env=std::min(1.,t/.006)*rel;
   if(t>e.len-.008)env*=clamp((e.len+.015-t)/.023,0.,1.);
   cut=11500;
  }else if(e.voice>=100&&e.voice<=115){
   int k=e.voice-100;double w=f*t;
   double release=std::exp(-std::max(0.,t-e.len)/.25);
   if(k==0)v=(.76*sn(w)*std::exp(-1.8*t)+.28*sn(w*2.012)*std::exp(-3.8*t)+.14*sn(w*3.99)*std::exp(-6.5*t)+.07*sn(w*6.08)*std::exp(-10*t))*(1-std::exp(-650*t))*release;
   if(k==1)v=(sn(w)*std::exp(-.8*t)+.25*sn(w*2.001)*std::exp(-2.1*t)+.08*sn(w*3.007)*std::exp(-4.5*t))*(1-std::exp(-180*t))*release;
   if(k==2)v=(sn(w)+.32*sn(2*w)*std::exp(-3*t)+.11*sn(3*w)*std::exp(-5*t))*(1-std::exp(-160*t))*std::exp(-1.35*t)*release;
   if(k==3)v=(sn(w)+.4*sn(2*w)+.21*sn(3*w)+.1*sn(5*w))*(1-std::exp(-750*t))*std::exp(-7*t)*release;
   if(k==4)v=(sn(w)*std::exp(-3.2*t)+.3*sn(4*w)*std::exp(-12*t)+.1*sn(9.15*w)*std::exp(-23*t))*(1-std::exp(-1000*t))*release;
   if(k==5)v=(.7*sn(w+.095*std::exp(-2.2*t)*sn(2*w))+.18*sn(w*1.003))*(1-std::exp(-35*t))*std::exp(-1.25*t)*release;
   if(k==6){body+=f*(1+.0025*sn(t*5.1))/SR;low=.88*low+.12*rng.next();v=(sn(body)+.13*sn(2*body)+.035*low)*(1-std::exp(-24*t))*release;}
   if(k==7)v=(sn(w)+.14*sn(w*3.99)*std::exp(-3*t))*(.88+.12*sn(5.2*t))*(1-std::exp(-500*t))*std::exp(-.55*t)*release;
   if(k==8){body+=f*(1+.0016*sn(t*4.7))/SR;v=(sn(body)+.24*sn(3*body)+.08*sn(5*body))*(1-std::exp(-34*t))*release;}
   if(k==9)v=(.45*sn(w*.9987)+.45*sn(w*1.0013)+.12*sn(w*2.001))*(1-std::exp(-2.7*t))*release;
   if(k==10)v=(sn(w)+.33*sn(2*w)*std::exp(-2*t)+.16*sn(3*w)*std::exp(-4*t)+.07*sn(4*w)*std::exp(-7*t))*(1-std::exp(-700*t))*std::exp(-2.7*t)*release;
   if(k==11)v=(.7*sn(w)+.2*sn(2*w)+.12*sn(3*w)+.06*sn(4*w))*(1-std::exp(-75*t))*release;
   if(k==12){body+=(46+65*std::exp(-36*t))/SR;v=sn(body)*std::exp(-17*t)*(1-std::exp(-900*t));}
   if(k==13){double z=rng.next();low=.76*low+.24*z;v=((z-low)*.7+low*.5)*(1-std::exp(-180*t))*std::exp(-19*t);}
   if(k==14){double z=rng.next();low=.91*low+.09*z;v=(z-low)*std::exp(-55*t)*(1-std::exp(-1400*t));}
   if(k==15)v=(sn(780*t)+.32*sn(1171*t))*std::exp(-55*t)*(1-std::exp(-1400*t));
  }else if(e.voice==300||e.voice==301){
   // Pipe organ: principals, flutes, reeds, mutation stops and detuned ranks.
   const double ratios[]={.5,1,2,3,4,6,8,12,16};
   const double amps[]={.34,.65,.38,.12,.20,.075,.13,.055,.032};
   for(int h=0;h<9;h++)if(f*ratios[h]<SR*.43){double amp=amps[h]*(h>4?(.3+e.tone):1.);
    if(e.voice==301&&h>2)amp*=.09;
    l+=amp*(sn(f*t*ratios[h]*.9991+phase[h%8])+sn(f*t*ratios[h]*1.0009+phase[(h+1)%8]))*.5;
    r+=amp*(sn(f*t*ratios[h]*.9987+phase[(h+2)%8])+sn(f*t*ratios[h]*1.0013+phase[(h+3)%8]))*.5;}
   env=(1-std::exp(-t*(e.voice==301?18:45)))*std::exp(-std::max(0.,t-e.len)/.28);l*=pl;r*=pr;
  }else if(e.voice==302||e.voice==303||e.voice==304){
   // Eight bows, independently drifting pitch and unequal left/right sections.
   const double det[]={-.006,-.0041,-.0023,-.0008,.0007,.0021,.0038,.0057};
   for(int j=0;j<8;j++){double df=f*(1+det[j]+.0014*sn((e.at+t)*(4.1+j*.14)+j*.1));
    double s=Window::saw(phase[j],df/SR);l+=s*(j%2?.075:.15);r+=s*(j%2?.15:.075);}
   low+=.035*(rng.next()-low);l+=low*.12;r+=low*.10;
   cut=e.voice==304?1800:2200+e.tone*3300;
   env=(1-std::exp(-t*(e.voice==303?90:9)))*std::exp(-std::max(0.,t-e.len)/(e.voice==303?.10:.52));
   if(e.voice==303)env*=std::exp(-t*4.8);else env*=.83+.12*sn(t*.7+e.at*.03)+.05*sn(t*1.11);
   l*=pl;r*=pr;
  }else if(e.voice==305||e.voice==306){
   body+=f*(1+.0017*sn(4.5*t))/SR;double attack=1-std::exp(-t*13);
   v=sn(body)+(.25+.3*attack)*sn(2*body)+(.12+.1*e.tone)*sn(3*body)+.10*sn(4*body);
   v=std::tanh(v*(e.voice==306?1.4:.8));env=attack*rel;cut=e.voice==306?3900:1800;
  }else if(e.voice==307){
   // Four virtual kettles use struck membrane modes and a soft mallet impact.
   const double ratio[]={1.,1.505,1.998,2.437,2.916,3.43};
   const double amp[]={1.,.49,.29,.18,.12,.07};
   for(int j=0;j<6;j++)v+=amp[j]*sn(f*ratio[j]*(t+.003*(1-std::exp(-t*25))))*std::exp(-t*(.75+j*.46));
   low+=.14*(rng.next()-low);v+=low*.3*std::exp(-t*60);
   env=(1-std::exp(-t*950))*std::exp(-std::max(0.,t-e.len)/.7);cut=3400;
  }else if(e.voice==308){
   const double ratios[]={1.,1.414,1.932,2.619,3.477,4.73,6.117,8.61};
   for(int j=0;j<8;j++)v+=sn(f*ratios[j]*t+.15*sn((.1+j*.03)*t))*std::exp(-t*(.2+j*.1))/(1+j*.5);
   env=(1-std::exp(-t*140))*std::exp(-std::max(0.,t-e.len)/1.5);cut=8000;
  }else if(e.voice==309){
   body+=(f+f*.8*std::exp(-t*30))/SR;low+=.2*(rng.next()-low);
   v=.85*sn(body)*std::exp(-t*4)+.3*low*std::exp(-t*16);env=1-std::exp(-t*1200);
  }else if(e.voice==310){
   for(int j=0;j<6;j++)v+=sn(f*(1+j*1.317)*t+.25*sn(t*(.19+j*.033)))/(1+j*1.2);
   env=(1-std::exp(-t*1.7))*std::exp(-std::max(0.,t-e.len)/.9);cut=3200;
  }else if(e.voice==311){
   double bend=std::pow(2.,e.motion*u/12.);body+=f*bend/SR;
   v=.5*sn(body+.44*sn(body*std::sqrt(2.)))+.25*sn(body*1.618+.15*sn(t*7));
   env=std::pow(std::sin(PI*clamp(t/(e.len+.5),0.,1.)),.6);cut=1600+5300*e.tone;
  }else if(e.voice==312){
   double grain=std::fmod(t,.071)/.071;
   v=(sn(f*t*1.414)+.45*sn(f*t*2.718))*.6*std::pow(std::sin(PI*grain),2);
   env=(1-std::exp(-t*200))*rel;cut=2400+2500*e.tone;
  }else if(e.voice==313){
   body+=f*(1+.0032*sn(t*4.7)+.001*sn(t*.57))/SR;low+=.13*(rng.next()-low);
   v=.9*sn(body)+.11*sn(2*body)+.05*sn(3*body)+.12*low;
   env=(1-std::exp(-t*19))*std::exp(-std::max(0.,t-e.len)/.22);cut=5400;
  }else if(e.voice==314||e.voice==315){
   for(int j=1;j<=7;j++)v+=sn(f*j*(1+.0001*j*j)*t+phase[j])*(1./std::pow(j,1.5))*std::exp(-t*(e.voice==314?2.2:.55)*(.7+j*.3));
   env=(1-std::exp(-t*700))*std::exp(-std::max(0.,t-e.len)/.25);cut=6000;
  }else if(e.voice==316){
   v=.8*sn(f*t)+.18*sn(2*f*t)+.13*sn(3*f*t);low+=.03*(rng.next()-low);v+=low*.04;
   env=(1-std::exp(-t*6))*std::exp(-std::max(0.,t-e.len)/.6);cut=950;
  }
  if(e.voice!=300&&e.voice!=301&&e.voice!=302&&e.voice!=303&&e.voice!=304){l=v*pl;r=v*pr;}
  if(cut>0){if(i%32==0)fc=std::tan(PI*clamp(cut,35,15000)/SR);l=filterL.tick(l,fc,.707);r=filterR.tick(r,fc,.707);}
  l*=env*e.gain;r*=env*e.gain;
  add(target,begin+i,l,r);add(echo,begin+i,l*e.delay,r*e.delay);add(space,begin+i,l*e.reverb,r*e.reverb);
 }
}
void u16(std::ofstream&o,uint16_t x){o.put(x&255);o.put(x>>8);}void u32(std::ofstream&o,uint32_t x){u16(o,x&65535);u16(o,x>>16);}
void wav(const std::string&path,const Bus&buf,double gain){std::ofstream o(path,std::ios::binary);if(!o)throw std::runtime_error("Cannot write WAV");
 uint32_t bytes=buf.size()*6;o.write("RIFF",4);u32(o,36+bytes);o.write("WAVEfmt ",8);u32(o,16);u16(o,1);u16(o,2);u32(o,44100);u32(o,264600);u16(o,6);u16(o,24);o.write("data",4);u32(o,bytes);
 for(auto s:buf)for(double x:{double(s.l),double(s.r)}){int32_t v=std::llround(clamp(x*gain,-.999999,.999999)*8388607);o.put(v&255);o.put((v>>8)&255);o.put((v>>16)&255);}}
int main(int argc,char**argv){try{
 if(argc<3)throw std::runtime_error("Usage: astra-engine score.tsv output.wav [stem-prefix]");
 for(size_t i=0;i<sine.size();i++)sine[i]=std::sin(TAU*i/65536.);
 std::ifstream in(argv[1]);double duration,room,delay;int scene;uint32_t seed;in>>duration>>scene>>seed>>room>>delay;
 if(!in||duration<=0||duration>1200||scene<1||scene>12)throw std::runtime_error("Bad header");
 size_t frames=std::ceil(duration*SR);Bus orch(frames),solo(frames),choir(frames),echo(frames),space(frames);
 std::vector<Event>es;std::string line;std::getline(in,line);
 while(std::getline(in,line)){if(line.empty())continue;std::istringstream s(line);Event e;
  if(!(s>>e.at>>e.len>>e.voice>>e.note>>e.gain>>e.pan>>e.tone>>e.motion>>e.delay>>e.reverb>>e.pre>>e.next>>e.seed))throw std::runtime_error("Malformed event");
  if(!std::isfinite(e.at+e.len+e.note+e.gain)||e.at<0||e.len<=0||e.at+e.len>duration||e.note<0||e.note>127||e.gain<0||std::abs(e.pan)>1)throw std::runtime_error("Invalid event");
  es.push_back(e);
 }
 for(const auto&e:es){
  if(e.voice<80){Window::seed=e.seed;Window::E x{std::max(0.,e.at-.04),e.len,e.note,e.gain,e.pan,e.tone,e.motion,e.delay,e.reverb,e.voice};Window::synth(x,1.,(scene-1)%8+1,orch,orch,echo,space);}
  else if(e.voice>=200&&e.voice<=214){Night::seed=e.seed;Night::Event x{std::max(0.,e.at-.04),e.len,e.note,e.gain,e.pan,e.tone,e.motion,e.voice-200};Night::synth(x,1.,orch,orch,echo,space);}
  else if(e.voice>=400&&e.voice<=420){Shelter::seed=e.seed;Shelter::E x{std::max(0.,e.at-.04),e.len,e.note,e.gain,e.pan,e.tone,e.motion,e.delay,e.reverb,e.voice-400};Shelter::synth(x,1.,(scene-1)%8+1,orch,orch,echo,space);}
  else modern(e,orch,solo,choir,echo,space);
 }
 std::cerr<<"Scene "<<scene<<": "<<es.size()<<" notes/phones synthesized; cathedral returns\n";
 std::vector<Window::Comb>cl,cr;for(int k:{1557,1617,1491,1422,1277,1356,1781,1877}){cl.emplace_back(int(k*room));cr.emplace_back(int(k*room)+89);}
 Window::AP al1(1061),al2(631),ar1(1091),ar2(659);
 size_t dn=std::max(size_t(1),size_t(delay*SR));Bus db(dn);size_t dp=0;
 double dl=0,dr=0,prevL=0,prevR=0,hpL=0,hpR=0,peak=0,energy=0,duck=0;
 const double fb=clamp(.81+room*.015,.82,.91);
 for(size_t i=0;i<frames;i++){
  auto z=db[dp];dl+=.19*(z.l-dl);dr+=.19*(z.r-dr);db[dp]={float(echo[i].l+dr*.38),float(echo[i].r+dl*.38)};if(++dp==dn)dp=0;
  double il=space[i].l+dl*.08,ir=space[i].r+dr*.08,rl=0,rr=0;
  for(int j=0;j<8;j++){rl+=cl[j].tick(il,fb)/8;rr+=cr[j].tick(ir,fb+.002)/8;}
  rl=al2.tick(al1.tick(rl));rr=ar2.tick(ar1.tick(rr));
  double v=std::max(std::abs(solo[i].l),std::abs(solo[i].r));duck+=(v>duck?.008:.00015)*(v-duck);
  double orchestraGain=1.65-.25*clamp(duck*5,0.,1.); // Voice clarity, no kick pumping.
  double l=orch[i].l*orchestraGain+solo[i].l*.83+choir[i].l*1.25+dl+rl*1.8;
  double r=orch[i].r*orchestraGain+solo[i].r*.83+choir[i].r*1.25+dr+rr*1.8;
  hpL=l-prevL+.9978*hpL;hpR=r-prevR+.9978*hpR;prevL=l;prevR=r;
  l=soft(hpL);r=soft(hpR);double fade=std::min({1.,i/(SR*.014),(frames-i)/(SR*3.)});l*=fade;r*=fade;
  if(!std::isfinite(l+r))throw std::runtime_error("Non-finite audio");space[i]={float(l),float(r)};
  peak=std::max({peak,std::abs(l),std::abs(r)});energy+=l*l+r*r;
 }
 if(peak<1e-7)throw std::runtime_error("Silent render");double gain=.89/peak;wav(argv[2],space,gain);
 if(argc>3){std::string p=argv[3];wav(p+"-orchestra-dry.wav",orch,gain);wav(p+"-soloists-dry.wav",solo,gain);wav(p+"-choirs-dry.wav",choir,gain);}
 std::cout<<"{\"scene\":"<<scene<<",\"events\":"<<es.size()<<",\"seconds\":"<<duration<<",\"peak\":0.89,\"rmsDb\":"<<20*std::log10(std::sqrt(energy/(2*frames))*gain)<<",\"gain\":"<<gain<<"}\n";
}catch(const std::exception&e){std::cerr<<e.what()<<"\n";return 1;}}
