/* "Grade me with AI": builds a plain-text Hebrew grading prompt the student pastes into ChatGPT / Claude / Gemini.
   100% static: no network calls from this page. Uses only raw fields (question / solution / rubric), never *Html.
   API: window.AiPrompt = { build(q, {answerText, photo, context?}) -> string, open(target, text) } */
(function (root) {
  "use strict";

  var URLS = {
    chatgpt: "https://chatgpt.com/",
    claude: "https://claude.ai/new",
    gemini: "https://gemini.google.com/app"
  };

  var COMMON =
    "בדוק את התשובה לפי המחוון (ולא לפי הרושם הכללי). אם יש טעות, צטט את השורה השגויה הראשונה כפי שנכתבה. " +
    "אל תסתפק בהצגה מחודשת של הפתרון שלמעלה: התייחס למה שהסטודנט באמת כתב.";

  var KIND = {
    proof: "זו הוכחה: בדוק כל צעד לתקפות לוגית (האם הוא נובע ממה שלפניו), וסמן פערים, קפיצות לא מוצדקות והנחות שלא הוכחו.",
    computation: "זו שאלת חישוב: מצא את השורה השגויה הראשונה, ורק אחר כך בדוק את הערך הסופי. שים לב שטעות מוקדמת עלולה להשפיע על כל מה שאחריה.",
    algorithm: "זו שאלת אלגוריתם: בדוק נכונות (כולל מקרי קצה), ואת סיבוכיות הזמן והמקום שנטענו.",
    code: "זו שאלת קוד: בדוק איך הקוד מתנהג במקרי קצה (קלט ריק, איבר בודד, ערכים חוזרים, גבולות), ולא רק במקרה הרגיל.",
    truefalse: "זו שאלת נכון/לא נכון עם הוכחה: בדוק קודם אם ההכרעה נכונה, ואז בדוק את ההנמקה צעד אחר צעד.",
    mcq: "זו שאלה אמריקאית: בדוק אם התשובה שנבחרה נכונה והאם ההנמקה מחזיקה."
  };

  var FORMAT =
    "פורמט התשובה שלך, בעברית:\n" +
    "1. ציון לכל שורת מחוון (נקודות שהושגו מתוך הנקודות המקסימליות), עם הנמקה קצרה.\n" +
    "2. השורה השגויה הראשונה, מצוטטת, והסבר מה לא נכון בה (אם אין טעות, כתוב זאת).\n" +
    "3. ציון כולל.\n" +
    "4. טיפ אחד קצר לשיפור.";

  function str(v) { return v == null ? "" : String(v).trim(); }

  function contextText(c) {
    if (!c) return "";
    var body = str(c.kind === "code" ? c.code : c.text);
    if (!body && !c.title) return "";
    return (c.title ? str(c.title) + "\n" : "") + body;
  }

  function build(q, opts) {
    opts = opts || {};
    var out = [];
    out.push("אתה בודק מבחנים בקורס אוניברסיטאי. תפקידך לבדוק את הפתרון של סטודנט בצורה הוגנת ומדויקת.");
    var ctx = contextText(opts.context);
    if (ctx) out.push("רקע לשאלה:\n" + ctx);
    out.push("השאלה:\n" + str(q.question));
    if (q.image) out.push("(לשאלה מצורף איור שאינו כלול בטקסט הזה.)");
    var choices = Array.isArray(q.options) ? q.options : [];
    if (choices.length) {
      out.push("האפשרויות:\n" + choices.map(function (o) {
        return str(o.id) + ". " + (str(o.value) || "(אפשרות בתמונה)");
      }).join("\n"));
    }
    var label = q.official ? "הפתרון הרשמי" : "פתרון לדוגמה (לא רשמי)";
    var sol = str(q.solution);
    if (!sol && choices.length && q.correctId != null) {
      var ids = [q.correctId].concat(Array.isArray(q.acceptedIds) ? q.acceptedIds : []).map(String);
      sol = "התשובה הנכונה: " + ids.join(", ");
      var ex = str(q.explanation);
      if (ex) sol += "\n" + ex;
    }
    if (sol) out.push(label + ":\n" + sol);
    else out.push("(אין פתרון זמין לשאלה הזו. בדוק לפי הידע שלך ומחוון סביר.)");
    var rub = (Array.isArray(q.rubric) ? q.rubric : []).filter(function (r) { return r && str(r.text); });
    if (rub.length) {
      out.push("המחוון:\n" + rub.map(function (r, i) {
        return (i + 1) + ". " + str(r.text) + (r.points != null ? " (" + r.points + " נק׳)" : "");
      }).join("\n"));
    }
    out.push("הוראות בדיקה:\n" + COMMON + "\n" + (KIND[q.kind] || ""));
    var ans = str(opts.answerText);
    if (opts.photo) out.push("מצורפת תמונה של הפתרון שלי בכתב יד.");
    else if (ans) out.push("התשובה שלי:\n" + ans);
    out.push(FORMAT);
    return out.join("\n\n").replace(/\n{3,}/g, "\n\n") + "\n";
  }

  function showModal(text) {
    var doc = root.document;
    var old = doc.querySelector(".aip-modal");
    if (old) old.remove();
    var m = doc.createElement("div");
    m.className = "aip-modal";
    m.setAttribute("role", "dialog");
    m.setAttribute("aria-modal", "true");
    m.innerHTML =
      '<div class="aip-box"><p class="aip-msg">ההעתקה האוטומטית לא זמינה. סמנו והעתיקו את הטקסט (Ctrl+C), ואז הדביקו בצ׳אט שנפתח.</p>' +
      '<textarea class="aip-text" readonly rows="12" dir="auto"></textarea>' +
      '<button type="button" class="btn primary aip-close">סגירה</button></div>';
    var ta = m.querySelector("textarea");
    ta.value = text;
    var close = function () { m.remove(); };
    m.querySelector(".aip-close").addEventListener("click", close);
    m.addEventListener("click", function (e) { if (e.target === m) close(); });
    doc.addEventListener("keydown", function esc(e) {
      if (!m.isConnected) { doc.removeEventListener("keydown", esc); return; }
      if (e.key === "Escape") { close(); doc.removeEventListener("keydown", esc); }
    });
    doc.body.appendChild(m);
    try { ta.focus(); ta.select(); } catch (e) {}
  }

  function open(target, text) {
    var url = URLS[target];
    // Copy first (opening the tab moves focus and Chrome can then reject writeText), keep the promise,
    // then open the tab in the same synchronous click handler so the popup gesture is preserved.
    var cb = root.navigator && root.navigator.clipboard;
    var pending = null, failedNow = false;
    if (cb && typeof cb.writeText === "function") {
      try { pending = Promise.resolve(cb.writeText(text)); } catch (e) { failedNow = true; }
    } else {
      failedNow = true;
    }
    if (url) root.open(url, "_blank", "noopener");
    if (failedNow) showModal(text);
    else pending.catch(function () { showModal(text); });
  }

  root.AiPrompt = { build: build, open: open };
})(typeof window !== "undefined" ? window : this);
