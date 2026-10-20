"""Simulator-only warning and real ConfirmationActivity layout fixture."""
from pathlib import Path

Import('env')

FIXTURE = r'''
  if (std::getenv("CROSSPOINT_CONTEXT_FIXTURE")) {
    mappedInputManager.update();
    static int lastCase = -1;
    static int paintedCase = -1;
    const unsigned long elapsed = millis();
    const char* selectedCase = std::getenv("CROSSPOINT_CONTEXT_CASE");
    const int index = elapsed < 3000 ? -1
        : selectedCase ? std::clamp(std::atoi(selectedCase), 0, 287)
                       : std::min(287, int((elapsed - 3000) / 400));
    if (index >= 0) {
      const int mode = index / 144;
      const int local = index % 144;
      const int orientation = local / 36;
      const int theme = (local % 36) / 12;
      const int language = (local % 12) / 3;
      const int item = local % 3;
      const Language languages[] = {Language::EN, Language::ES, Language::CA, Language::CAV};
      const CrossPointSettings::UI_THEME themes[] = {
          CrossPointSettings::CLASSIC, CrossPointSettings::LYRA, CrossPointSettings::ROUNDEDRAFF};
      const StrId warnings[] = {StrId::STR_DICT_NO_DICT_SET, StrId::STR_DICT_DECOMPRESS_ERROR,
                                StrId::STR_CLIPPING_EXPORT_FAILED};
      if (index != lastCase) {
        {
          RenderLock lock;
          renderer.setOrientation(static_cast<GfxRenderer::Orientation>(orientation));
          I18N.setLanguage(languages[language]);
          UITheme::getInstance().setTheme(themes[theme]);
        }
        if (mode == 0) {
          activityManager.goHome();
        } else {
          const char* subject = item == 0
              ? "A long filename with spaces and accents - chapter one.epub"
              : item == 1 ? "A long book title that must wrap inside the confirmation dialog"
                          : "A long original sleep image filename - transparent cover.png";
          const StrId heading = item == 2 ? StrId::STR_SET_SLEEP_COVER_CONFIRM : StrId::STR_DELETE_ITEM_CONFIRM;
          const std::string question = std::getenv("CROSSPOINT_CONTEXT_BEFORE")
              ? I18N.get(item == 2 ? StrId::STR_SET_SLEEP_COVER : StrId::STR_DELETE) +
                    std::string(item == 2 ? "?" : "? ")
              : std::string(I18N.get(heading));
          activityManager.replaceActivity(std::make_unique<ConfirmationActivity>(
              renderer, mappedInputManager, question, subject));
        }
        lastCase = index;
        printf("[CONTEXT-FIXTURE] %d mode=%d orientation=%d theme=%d language=%d item=%d\n",
               index, mode, orientation, theme, language, item);
      }
      activityManager.loop();
      if (mode == 0 && paintedCase != index && (elapsed - 3000) % 400 >= 150) {
        RenderLock lock;
        renderer.clearScreen();
        GUI.drawPopup(renderer, I18N.get(warnings[item]));
        paintedCase = index;
      }
    }
    delay(1);
    return;
  }
'''


def replace_main(node):
    source = Path(node.srcnode().get_abspath()).read_text()
    assert source.count('void loop() {') == 1
    fixture = '#include <cstdlib>\n#include "activities/util/ConfirmationActivity.h"\n' + source.replace(
        'void loop() {', 'void loop() {\n' + FIXTURE)
    output = Path(env.subst('$BUILD_DIR')) / 'l10n-context-main.cpp'
    output.parent.mkdir(parents=True, exist_ok=True)
    if not output.exists() or output.read_text() != fixture:
        output.write_text(fixture)
    return env.File(str(output))


env.AddBuildMiddleware(replace_main, '*src/main.cpp')
