// Adapted from Cairn's original engine; shared stereo bus, synthesis retained.
namespace Window {
// Cairn — Window Engine, 2026. Procedural synthesis; no recorded samples.
// clang++ -O3 -std=c++17 engine.cpp -o window-engine
constexpr double SR=44100, PI=3.14159265358979323846, TAU=2*PI;
uint32_t seed=13092026;
double noise(){seed^=seed<<13;seed^=seed>>17;seed^=seed<<5;return seed/2147483648.-1;}
double clip(double v,double a,double b){return std::max(a,std::min(b,v));}
double sat(double x){return x/(1+.3*std::abs(x));}
double blep(double t,double d){if(t<d){t/=d;return 2*t-t*t-1;}if(t>1-d){t=(t-1)/d;return t*t+2*t+1;}return 0;}
double saw(double &p,double d){p+=d;p-=std::floor(p);return 2*p-1-blep(p,d);}
using S=::Stereo;
struct Filter{double a=0,b=0;double tick(double v,double g,double q=.707,bool band=false){double h=(a+g*(v-b))/(1+g*(g+1/q)),l=b+g*h;a=2*h-a;b=2*l-b;return band?h:l;}};
struct Comb{std::vector<float>b;size_t p=0;double lo=0;Comb(int n):b(n){} double tick(double x,double fb){double v=b[p];lo+=.26*(v-lo);b[p]=x+lo*fb;if(++p==b.size())p=0;return v;}};
struct AP{std::vector<float>b;size_t p=0;AP(int n):b(n){}double tick(double x){double z=b[p],y=z-.55*x;b[p]=x+.55*z;if(++p==b.size())p=0;return y;}};
// at, beats, voice, MIDI pitch, gain, pan, brightness, expression, delay-send, reverb-send
struct E{double at,len,note,gain,pan,tone,motion,delay,reverb;int voice;};
void put(std::vector<S>&b,size_t i,double l,double r){if(i<b.size()){b[i].l+=l;b[i].r+=r;}}
void synth(const E&e,double beat,int track,std::vector<S>&dry,std::vector<S>&music,std::vector<S>&echo,std::vector<S>&space){
 bool drum=e.voice<=5||e.voice==20||e.voice==29;double hold=e.len*beat;
 double tail=drum?.5:e.voice==8?3.8:e.voice==18?.4:e.voice==19?1.:e.voice==6?.18:1.4;
 if(e.voice>=40)tail=.025;
 if(e.voice>=21&&e.voice<=28)tail=.8;
 if(e.voice==2)tail=.11;if(e.voice==3)tail=.32;if(e.voice==4||e.voice==20)tail=.16;
 size_t start=std::llround((e.at*beat+.04)*SR),n=std::min(size_t((drum?tail:hold+tail)*SR),dry.size()-std::min(start,dry.size()));
 if(!n)return;
 double f=440*std::pow(2.,(e.note-69)/12),pl=std::cos((e.pan+1)*PI/4),pr=std::sin((e.pan+1)*PI/4);
 double p=0,p2=.173,p3=.593,body=0,low=0,low2=0,grain=0,cut=0,g=0;
 Filter fl,fr,form1,form2,form3,air;
 double vocalPhase=0;
 std::vector<S>sample(n);
 for(size_t i=0;i<n;i++){
  double t=i/SR,v=0,l=0,r=0,env=1,q=.707,rel=std::exp(-std::max(0.,t-hold)/.25);
  double wob=1+.0016*std::sin(TAU*(.41+.03*track)*t)+.0005*std::sin(TAU*6.3*t);
  cut=0;
  if(e.voice==0){
   const double kbase[]={0,66,52,75,70,58,42,63,78};
   body+=TAU*(kbase[track]+e.tone*9+(track==6?63:80)*std::exp(-t*55))/SR;
   v=sat(std::sin(body)*1.35)*std::exp(-t*(track==6?9:track==3||track==8?24:17))*(1-std::exp(-t*1700));
   double z=noise();low+=.3*(z-low);v+=low*.08*std::exp(-t*220);
  }else if(e.voice==1){
   double z=noise();low+=.35*(z-low);low2+=.024*(low-low2);
   double burst=.46*std::exp(-t*(track==3||track==8?35:track==6?12:24));for(double d:{0.,.010,.024})if(t>=d)burst+=.3*std::exp(-(t-d)*170);
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
   cut=170+e.tone*750+150*std::sin(t*.21);
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
  // Additional original instruments for this album.
  if(e.voice==21){ // Rounded triangle pluck, little fundamental sustain.
   v=.8*std::sin(TAU*f*t)-.13*std::sin(TAU*f*3*t)+.04*std::sin(TAU*f*5*t);
   env=(1-std::exp(-t*210))*std::exp(-t*4.8)*std::exp(-std::max(0.,t-hold)/.09);cut=950;
  }else if(e.voice==22){ // Continuous foundation; no retrigger or periodic modulation.
   body+=TAU*f*(1+e.motion*.02*std::exp(-t*4))/SR;
   v=.8*std::sin(body)+.14*std::sin(body*2);env=(1-std::exp(-t*7))*std::exp(-std::max(0.,t-hold)/.32);cut=220;
  }else if(e.voice==23){ // Muted electric-string bass, audible wood and higher partials.
   v=.58*std::sin(TAU*f*t)+.34*std::sin(TAU*2*f*t)*std::exp(-t*2)+.22*std::sin(TAU*3*f*t)*std::exp(-t*4);
   v+=noise()*.035*std::exp(-t*65);env=(1-std::exp(-t*700))*std::exp(-t*1.6)*std::exp(-std::max(0.,t-hold)/.065);cut=1600;
  }else if(e.voice==24){ // Hollow organ bass, quarter-note releases with no LFO.
   v=.5*std::sin(TAU*f*t)+.4*std::sin(TAU*f*2*t)+.17*std::sin(TAU*f*4*t);
   env=(1-std::exp(-t*90))*std::exp(-std::max(0.,t-hold)/.11);cut=820;
  }else if(e.voice==25){ // Quiet bowed harmonic cloud, no sub-frequency fundamental.
   v=.3*std::sin(TAU*f*2.001*t)+.3*std::sin(TAU*f*3.002*t)+.17*std::sin(TAU*f*4*t);
   env=(1-std::exp(-t*1.9))*std::exp(-std::max(0.,t-hold)/.7);cut=2500;
  }else if(e.voice==26){ // Rounded electric piano with velocity-dependent FM bite.
   v=.72*std::sin(TAU*f*t+(1.1+e.tone*.8)*std::exp(-t*4)*std::sin(TAU*f*1.001*t));
   v+=.1*std::sin(TAU*f*7*t)*std::exp(-t*18);
   env=(1-std::exp(-t*550))*std::exp(-t*.9)*std::exp(-std::max(0.,t-hold)/.22);cut=4200;
  }else if(e.voice==27){ // Plucked upper string, soft pick and decaying harmonics.
   v=std::sin(TAU*f*t)+.31*std::sin(TAU*f*2*t)*std::exp(-t*2)+.17*std::sin(TAU*f*3*t)*std::exp(-t*5);
   env=(1-std::exp(-t*400))*std::exp(-t*2.7)*std::exp(-std::max(0.,t-hold)/.18);cut=3100;
  }else if(e.voice==28){ // Breath flute, clear fundamental and noise at the edge.
   body+=TAU*f*(1+.002*std::sin(TAU*4.7*t))/SR;double z=noise();low+=.1*(z-low);
   v=.7*std::sin(body)+.12*std::sin(body*2)+.16*low;
   env=(1-std::exp(-t*16))*std::exp(-std::max(0.,t-hold)/.20);cut=3400;
  }else if(e.voice==29){ // Shaker: multiple soft grains inside a single hit.
   double z=noise();low+=.24*(z-low);v=(z-low)*std::exp(-t*25)*(.6+.4*std::sin(t*181));cut=9000;
  }else if(e.voice>=40){
   // Original phonetic singer. Voiced phones = glottal excitation + three
   // moving formants; fricatives = shaped noise; stops = closure and burst.
   // No speech engine, learned voice, recorded speech, or vocoder is embedded.
   int ph=e.voice-40;double u=clip(t/std::max(.01,hold),0.,1.);
   static const double vowel[16][3]={
    {280,2250,3050},{390,1990,2700},{560,1840,2550},{750,1710,2450},
    {640,1200,2500},{780,1120,2600},{540,900,2450},{430,1080,2500},
    {320,800,2250},{470,1330,1700},{500,1500,2450},{780,1120,2600},
    {530,1850,2500},{540,1050,2450},{750,1120,2600},{520,880,2450}};
   double f1=500,f2=1450,f3=2500;
   if(ph<16){f1=vowel[ph][0];f2=vowel[ph][1];f3=vowel[ph][2];
    int end=ph==11?0:ph==12?0:ph==13?8:ph==14?8:ph==15?0:-1;
    if(end>=0){double m=clip((u-.25)/.65,0.,1.);f1+=(vowel[end][0]-f1)*m;f2+=(vowel[end][1]-f2)*m;f3+=(vowel[end][2]-f3)*m;}
   }else if(ph==16){f1=250;f2=1050;f3=2150;} // m
   else if(ph==17||ph==18){f1=290;f2=1600;f3=2650;} // n / ng
   else if(ph==19){f1=370;f2=1180;f3=2700;} // l
   else if(ph==20){f1=390;f2=1200;f3=1650;} // r
   else if(ph==21){f1=280;f2=750;f3=2300;} // w
   else if(ph==22){f1=260;f2=2200;f3=3000;} // y
   double singer=.99+e.tone*.22;
   f1*=singer;f2*=singer;f3*=singer;
   double vibrato=(ph<16?.0035:0)*std::sin(TAU*5.2*t)*clip((t-.16)*3,0.,1.);
   double glide=std::pow(2.,e.motion*std::exp(-t*18)/12.);
   vocalPhase+=TAU*f*glide*(1+vibrato)/SR;
   double src=.58*saw(p,f*glide*(1+vibrato)/SR)+.22*std::sin(vocalPhase);
   double z=noise();low+=.15*(z-low);double high=z-low;
   bool voiced=ph<=22||ph==28||ph==29||ph==30||ph==31||ph>=35;
   if(voiced){
    v=1.4*form1.tick(src,std::tan(PI*f1/SR),5.2,true)+.82*form2.tick(src,std::tan(PI*f2/SR),7.1,true)+.27*form3.tick(src,std::tan(PI*f3/SR),8,true);
    v+=.028*std::sin(vocalPhase);if(ph>=16&&ph<=18)v*=.6;
   }
   if(ph>=23&&ph<=31){
    double centre=ph==23||ph==29?6500:ph==24||ph==30?3600:ph==27?1700:4500;
    double nn=air.tick(z,std::tan(PI*centre/SR),.85,true);
    v=(voiced?v*.35:0)+nn*(ph==27?.48:.78);cut=10000;
   }
   if(ph>=32){ // p,t,k,b,d,g,ch,j
    double burst=std::exp(-std::max(0.,t-.018)*95)*(t>.018?1:0);
    double centre=ph==32||ph==35?1300:ph==34||ph==37?3000:5500;
    double nn=air.tick(z,std::tan(PI*centre/SR),1.1,true);
    v=(voiced?v*.16:0)+nn*burst*1.2;if(ph>=38)v+=high*.27*std::exp(-t*20);
   }
   env=std::min(1.,t/.009)*std::exp(-std::max(0.,t-hold)/.006);
   if(t>hold-.012)env*=clip((hold+.012-t)/.024,0.,1.);
   if(!cut)cut=7500;
  }
  if(e.voice!=8){l=v*pl;r=v*pr;}
  if(cut>0){if(i%32==0)g=std::tan(PI*clip(cut,30,15000)/SR);l=fl.tick(l,g,q);r=fr.tick(r,g,q);}
  sample[i]={float(l*env*e.gain),float(r*env*e.gain)};
 }
 // Reversed vowel grains retain their own fades.
 bool reverse=(e.voice==9||e.voice==11)&&e.motion<-.5;
 for(size_t i=0;i<n;i++){
  S v=sample[reverse?n-1-i:i];
  if(reverse){double fade=std::min({1.,i/(SR*.012),(n-i)/(SR*.018)});v.l*=fade;v.r*=fade;}
  size_t at=start+i;put(drum?dry:music,at,v.l,v.r);put(echo,at,v.l*e.delay,v.r*e.delay);put(space,at,v.l*e.reverb,v.r*e.reverb);
 }
}

}
