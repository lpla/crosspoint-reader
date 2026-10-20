"""Compile the actual baseline/candidate methods without the device frontend."""
import json
import sys
import tempfile
from pathlib import Path
import subprocess

PROJECT = Path(sys.argv[1]).resolve()
OUT = Path(tempfile.mkdtemp(prefix="crosspoint-source-check-"))
OUT.mkdir(exist_ok=True)
path = "src/activities/util/KeyboardEntryActivity.cpp"


def method(source, signature):
    start = source.index(signature)
    opening = source.index("{", start)
    depth = 1
    end = opening + 1
    while depth:
        depth += (source[end] == "{") - (source[end] == "}")
        end += 1
    return source[start:end]


preamble = r'''
#include <algorithm>
#include <iostream>
#include <string>
#include <vector>
enum class InputType {Text,Password,Url};
class KeyboardEntryActivity {
 public:
  std::string text; InputType inputType=InputType::Password;
  bool passwordVisible=false; bool cursorMode=false; size_t cursorPos=0;
  static size_t utf8Prev(const std::string&,size_t);
  std::string displayTextForCurrentState() const;
};
'''
test = r'''
int main() {
  const std::vector<std::string> samples={"", "ascii", u8"àéíòú",u8"漢字",u8"🔑📚",u8"xñ漢🔑tail"};
  int failures=0, count=0;
  for(const auto& text:samples) {
    std::vector<size_t> positions={0};
    for(size_t p=0;p<text.size();) {
      ++p; while(p<text.size()&&(static_cast<unsigned char>(text[p])&0xc0)==0x80)++p;
      positions.push_back(p);
    }
    for(size_t pos:positions) for(bool cursor:{false,true}) for(bool visible:{false,true})
      for(InputType type:{InputType::Text,InputType::Password,InputType::Url}) {
        KeyboardEntryActivity a; a.text=text;a.cursorPos=pos;a.cursorMode=cursor;
        a.passwordVisible=visible;a.inputType=type;
        std::string expected=text;
        if(type==InputType::Password&&!visible) {
          expected.assign(text.size(),'*');
          if(!cursor&&pos) {
            size_t start=pos-1;
            while(start&&(static_cast<unsigned char>(text[start])&0xc0)==0x80)--start;
            expected.replace(start,pos-start,text,start,pos-start);
          }
        }
        const auto actual=a.displayTextForCurrentState();
        ++count; if(actual!=expected||actual.size()!=text.size())++failures;
      }
  }
  std::cout << count << " checks, " << failures << " failures\n";
  return failures?1:0;
}
'''
results = {}
for name,source in (
    ("baseline",subprocess.check_output(["git","show",f"e78f09fd1e2e1c9a7a9fb6cec28ee84cfdb53722:{path}"],cwd=PROJECT,text=True)),
    ("candidate",(PROJECT/path).read_text()),
):
    cpp = OUT / f"{name}.cpp"
    binary = OUT / name
    cpp.write_text(preamble + method(source,"size_t KeyboardEntryActivity::utf8Prev(") + "\n" +
                   method(source,"std::string KeyboardEntryActivity::displayTextForCurrentState() const") + test)
    subprocess.run(["c++","-std=c++17","-O1","-fsanitize=address,undefined","-fno-omit-frame-pointer",
                    str(cpp),"-o",str(binary)],check=True)
    run = subprocess.run([str(binary)],text=True,capture_output=True)
    results[name] = dict(returncode=run.returncode,output=run.stdout,diagnostics=run.stderr)
    print(name, run.stdout.strip())
    assert run.returncode == (1 if name=="baseline" else 0), results[name]
    assert not run.stderr, run.stderr
(OUT/"results.json").write_text(json.dumps(results,indent=2)+"\n")
