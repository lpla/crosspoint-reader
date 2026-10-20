"""Exercise actual cache activity entry/loop with controlled popup outcomes."""
import json
import sys
import tempfile
from pathlib import Path
import subprocess

PROJECT = Path(sys.argv[1]).resolve()
OUT = Path(tempfile.mkdtemp(prefix="crosspoint-source-check-"))
OUT.mkdir(exist_ok=True)
path = "src/activities/settings/ClearCacheActivity.cpp"


def method(source, signature):
    start = source.index(signature)
    opening = source.index("{",start)
    depth,end = 1,opening+1
    while depth:
        depth += (source[end]=="{")-(source[end]=="}")
        end += 1
    return source[start:end]


preamble = r'''
#include <functional>
#include <iostream>
#define tr(key) #key
#define LOG_DBG(...) ((void)0)
struct Activity { void onEnter() {} };
struct MappedInputManager {
 enum class Button {Confirm,Back};
 bool confirm=false,back=false;
 bool wasPressed(Button b)const{return b==Button::Confirm?confirm:back;}
 bool wasScreenTapped(int&,int&)const{return false;}
};
struct Popup {
 enum Outcome {None,Cancel,Clear,Back,Outside};
 Outcome outcome=None;bool active=false;std::function<void(int)> callback;
 void show(const char*,const char*const*,int,int,std::function<void(int)> f){active=true;callback=f;}
 void showMessage(const char* t,const char*,const char*const* o,int n,int i,std::function<void(int)> f){show(t,o,n,i,f);}
 bool isActive()const{return active;}
 bool handleInput(MappedInputManager&,std::function<void()> repaint){
   if(!active)return false;
   if(outcome!=None){active=false;if(outcome==Cancel||outcome==Clear)callback(outcome==Clear?1:0);repaint();}
   return true;
 }
};
struct ClearCacheActivity:Activity {
 enum State{WARNING,CLEARING,SUCCESS,FAILED};State state=WARNING;
 Popup confirmPopup;MappedInputManager mappedInput;int clears=0,backs=0;
 void onEnter();void loop();void requestUpdate(){}void goBack(){++backs;}
 void beginClear(){++clears;state=SUCCESS;}
};
'''
test = r'''
int main(){
 int count=0,failures=0;
 for(auto outcome:{Popup::Cancel,Popup::Back,Popup::Outside}){
   ClearCacheActivity a;a.onEnter();a.confirmPopup.outcome=outcome;a.loop();
   ++count;if(a.clears||a.backs!=1)++failures;
   a.mappedInput.confirm=true;a.loop();
   ++count;if(a.clears)++failures;
 }
 ClearCacheActivity clear;clear.onEnter();clear.confirmPopup.outcome=Popup::Clear;clear.loop();
 ++count;if(clear.clears!=1||clear.backs)++failures;
 ClearCacheActivity idle;idle.onEnter();idle.loop();
 ++count;if(idle.clears||idle.backs||!idle.confirmPopup.active)++failures;
 std::cout<<count<<" checks, "<<failures<<" failures\n";
 return failures?1:0;
}
'''
results = {}
for name,source in (
    ("baseline",subprocess.check_output(["git","show",f"e78f09fd1e2e1c9a7a9fb6cec28ee84cfdb53722:{path}"],cwd=PROJECT,text=True)),
    ("candidate",(PROJECT/path).read_text()),
):
    cpp,binary = OUT/f"{name}.cpp",OUT/name
    cpp.write_text(preamble+method(source,"void ClearCacheActivity::onEnter()")+"\n"+
                   method(source,"void ClearCacheActivity::loop()")+test)
    subprocess.run(["c++","-std=c++17","-O1","-fsanitize=address,undefined","-fno-omit-frame-pointer",
                    str(cpp),"-o",str(binary)],check=True)
    run = subprocess.run([str(binary)],text=True,capture_output=True)
    results[name]=dict(returncode=run.returncode,output=run.stdout,diagnostics=run.stderr)
    print(name,run.stdout.strip())
    assert run.returncode==(1 if name=="baseline" else 0),results[name]
    assert not run.stderr,run.stderr
(OUT/"results.json").write_text(json.dumps(results,indent=2)+"\n")
