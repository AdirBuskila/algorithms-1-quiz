"use strict";
/* Answer normalisers for the step widgets (window.Normalize). Pure functions, no DOM, no state.
   text(s)       free text: trim, collapse whitespace, case-fold, drop a trailing period.
   complexity(s) asymptotic notation: spaces stripped, log/lg/log_2/log2 -> log, n² / n^{2} -> n^2,
                 Θ and O both accepted as written (Θ is folded onto O so either grades the same), case-insensitive.
   number(s)     decimal comma allowed, unicode minus, simple fractions "a/b"; NaN when it is not a number. */
(function (root) {
  const SUP = { "⁰": "0", "¹": "1", "²": "2", "³": "3", "⁴": "4", "⁵": "5", "⁶": "6", "⁷": "7", "⁸": "8", "⁹": "9" };

  function text(s) {
    return String(s == null ? "" : s).normalize("NFKC").toLowerCase().replace(/\s+/g, " ").trim().replace(/[.。]+$/, "").trim();
  }

  function complexity(s) {
    let t = String(s == null ? "" : s).normalize("NFC");
    t = t.replace(/[Θθ]/g, "O").replace(/\\(?:Theta|theta|Omicron)/g, "O");
    t = t.replace(/[⁰¹²³⁴⁵⁶⁷⁸⁹]+/g, m => "^" + [...m].map(c => SUP[c]).join(""));
    t = t.toLowerCase().replace(/\s+/g, "").replace(/\\/g, "");
    t = t.replace(/[·⋅*×]/g, "");                     // "n·log n" -> "nlog n"
    t = t.replace(/\^\{([^{}]*)\}/g, "^$1").replace(/_\{([^{}]*)\}/g, "_$1");
    t = t.replace(/log(?:_?2|₂)?(?![a-z])/g, "log");   // log, log2, log_2, log₂ -> log
    t = t.replace(/lg/g, "log");
    t = t.replace(/log(?:_?2|₂)/g, "log");
    return t;
  }

  function number(s) {
    let t = String(s == null ? "" : s).replace(/[−–—]/g, "-").replace(/\s+/g, "");
    if (!t) return NaN;
    const frac = /^(-?[0-9]+(?:[.,][0-9]+)?)\/([0-9]+(?:[.,][0-9]+)?)$/.exec(t);
    const val = x => Number(x.replace(",", "."));
    if (frac) { const d = val(frac[2]); return d === 0 ? NaN : val(frac[1]) / d; }
    if (!/^[+-]?(?:[0-9]+(?:[.,][0-9]*)?|[.,][0-9]+)$/.test(t)) return NaN;
    return val(t);
  }

  /* ---------- Bidi (window.Bidi): render-time fixes for Latin inside Hebrew (RTL) HTML ----------
     Ported from computer-systems-quiz 775f65b. render(html) = labelLines -> mathRuns -> isolate.
     labelLines: a line that starts with a Latin option label ("a." / "(b)" / "1)") gets the label, punctuation
                 included, in its own LTR isolate, so it sits at the start (right edge) with the period right after the letter.
     mathRuns:   line-final punctuation stays with its formula. Formulas separated by punctuation stay SEPARATE isolates
                 (gluing "$n=1$: $3=3\cdot1^2$" into one LTR run reversed their order for an RTL reader).
     isolate:    every other non-Hebrew run holding a digit or Latin letter becomes an LTR <bdi>: "4!" keeps its "!", a product/arithmetic
                 chain (· × + − = /) is one run, a bracket whose partner is outside the run stays outside (so it mirrors as a pair in RTL),
                 sentence-final . , ? : stay outside at the RTL end. A run ends at a clause / list boundary outside brackets
                 (". " ", " "; " ": " "? " "! ") and at an RLM, so "TP = 44, FN = 6" is two isolates read right to left.
     <pre>, <code>, MathML, formulas and existing LTR isolates are never touched. Idempotent. */
  const B_INLINE = /^<\/?(b|strong|i|em|u|sub|sup|code)\b[^>]*>$/i;
  const B_SKIP = /^<(code|bdi|pre|math)\b|class="[^"]*\b(lesson-formula|qref|math-inline|math-block|math-run|opt-ltr)\b|\bdir="ltr"/i;
  const B_START = /[A-Za-z0-9$"(\[|\u221a\u2016\u03a3\u2211\u2212\u0177\u0233\u03b1-\u03c9\u0394\u03b8]/;
  const B_END = /[A-Za-z0-9)\]|\u00b2\u00b3\u2016%\u221e'\u2032\u2033\u2019"\u2080-\u2089\u1d62\u2c7c\u2099\u2096\u0177\u0233\u0304\u03b1-\u03c9]/;
  const B_OP = /^[·×+−=\/*…]$/;      // · × + − = / * …  (the ASCII hyphen is not one: "ו-y")
  const bIsTag =p => p[0] === "<", bChr = p => (bIsTag(p) || p[0] === "&" && p.length > 1) ? "" : p;
  function isolate(html) {
    const toks = String(html).match(/<[^>]+>|[^<]+/g) || [];
    let out = "", run = [], skip = 0;
    const emit = parts => {
      if (!parts.length) return "";
      const s = parts.join("");
      { const st = [];                                                 // a bracket whose partner is outside this run stays outside, so it pairs with it in RTL
        for (let i = 0; i < parts.length; i++) { const c = bChr(parts[i]);
          if (c === "(" || c === "[") st.push([i, c]);
          else if (c === ")" || c === "]") { const top = st[st.length - 1];
            if (top && top[1] === (c === ")" ? "(" : "[")) st.pop(); else return emit(parts.slice(0, i)) + parts[i] + emit(parts.slice(i + 1)); } }
        if (st.length) { const i = st[st.length - 1][0]; return emit(parts.slice(0, i)) + parts[i] + emit(parts.slice(i + 1)); } }
      // a clause / list boundary outside brackets (". " ", " "; " ": " "? " "! ") splits the run: "TP = 44, FN = 6" or
      // "4: 79, 79" are separate LTR pieces that an RTL reader reads right to left. Checked after the bracket split above,
      // so a bracket whose partner is outside the run ("(clang++ -fsyntax-only: 0 שגיאות)") does not hide the boundary,
      // while "(3, 8, 2)" stays whole. "4! = 24" is one expression (a "!" before an operator is a factorial).
      for (let i = 0, d = 0; i < parts.length; i++) {
        const c = bChr(parts[i]);
        if ("([{".includes(c) && c) d++;
        else if (")]}".includes(c) && c) d = Math.max(0, d - 1);
        else if (d === 0 && /^[.,;:!?]$/.test(c)) {
          let k = i; while (k + 1 < parts.length && /^<\//.test(parts[k + 1])) k++;          // "<b>10.</b> 12": past the closing tag
          const nx = parts[k + 1];
          if ((nx === "&nbsp;" || /^\s$/.test(nx || "")) &&
              !(c === "!" && /^\s*[=+−×·*\/<>≤≥≠-]/.test(parts.slice(k + 1).map(bChr).join(""))))
            return emit(parts.slice(0, k + 1)) + emit(parts.slice(k + 1));
        }
      }
      let a = 0, b = parts.length - 1;
      while (a <= b && !B_START.test(bChr(parts[a]))) a++;
      while (b >= a && !B_END.test(bChr(parts[b]))) b--;

      if (a <= b) {
        while (b + 1 < parts.length && bChr(parts[b + 1]) === "!" && /[A-Za-z0-9)\]]/.test(bChr(parts[b]))) b++;   // factorial: "4!" stays one run
        while (b + 1 < parts.length && bChr(parts[b + 1]) === "*" && /[A-Za-z0-9)\]*]/.test(bChr(parts[b]))) b++;   // pointer stars: "Item**" keeps its stars
        while (a > 0 && bChr(parts[a - 1]) === "*" && /[A-Za-z(]/.test(bChr(parts[a]))) a--;                          // ... and "*ptr" its star
        for (let j = a; j > 0;) { let k = j - 1; while (k >= 0 && /^\s$/.test(parts[k])) k--;                       // arithmetic chain: leading operators join the run
          if (k >= 0 && B_OP.test(bChr(parts[k]))) { a = k; j = k; } else break; }
        for (let j = b; j < parts.length - 1;) { let k = j + 1; while (k < parts.length && /^\s$/.test(parts[k])) k++;  // ... and so do trailing ones
          if (k < parts.length && B_OP.test(bChr(parts[k]))) { b = k; j = k; } else break; }
      }
      { const tail = parts.slice(b + 1).join(""); if (b >= a && /^[,;]?\s*(\.\.\.|…)$/.test(tail)) b = parts.length - 1; }   // a trailing ellipsis stays with its list
      while (a > 0 && bIsTag(parts[a - 1]) && !/^<\//.test(parts[a - 1])) a--;     // pull in tags hugging the core: <b>3</b>
      while (b < parts.length - 1 && /^<\//.test(parts[b + 1])) b++;
      const balanced = arr => { const st = [];
        for (const t of arr) { if (!bIsTag(t)) continue;
          const m = t.match(/^<(\/?)(\w+)/); if (m[1]) { if (st.pop() !== m[2].toLowerCase()) return false; } else st.push(m[2].toLowerCase()); }
        return !st.length; };
      // a tag whose partner lies outside the run ("<b>10.</b> 12" cut after the period) stays outside the isolate
      while (b > a && /^<\//.test(parts[b]) && !balanced(parts.slice(a, b + 1))) b--;
      while (a < b && bIsTag(parts[a]) && !/^<\//.test(parts[a]) && !balanced(parts.slice(a, b + 1))) a++;
      const core = parts.slice(a, b + 1);
      const ok = a <= b && /[A-Za-z0-9]/.test(core.join("")) && balanced(core);
      return ok ? parts.slice(0, a).join("") + `<bdi class="ltr${core.join("").replace(/<[^>]+>/g, "").length <= 22 ? " nw" : ""}" dir="ltr">${core.join("")}</bdi>` + parts.slice(b + 1).join("") : s;
    };
    const flush = () => { if (run.length) out += emit(run.join("").match(/<[^>]+>|&[#\w]+;|[^<]/g)); run = []; };
    for (const t of toks) {
      if (t[0] === "<") {
        if (skip) { out += t; if (/^<\//.test(t)) skip--; else if (!/\/>$|^<(br|img|hr|wbr)\b/i.test(t)) skip++; continue; }
        if (B_SKIP.test(t)) { flush(); out += t; if (!/^<(br|img)\b/i.test(t)) skip = 1; continue; }
        if (B_INLINE.test(t)) { run.push(t); continue; }
        flush(); out += t; continue;
      }
      if (skip) { out += t; continue; }
      for (const piece of t.match(/[֐-׿\u200f]+|[^֐-׿\u200f]+/g)) {   // Hebrew text (or an RLM) ends a run
        if (/[֐-׿\u200f]/.test(piece)) { flush(); out += piece; } else run.push(piece);
      }
    }
    flush();
    return out;
  }

  /* apply fn to the parts of html outside <pre>/<code>/<math>; first = true only for the very start of the string */
  function outsideCode(html, fn) {
    return String(html).split(/(<pre\b[\s\S]*?<\/pre>|<code\b[\s\S]*?<\/code>|<math\b[\s\S]*?<\/math>)/i)
      .map((seg, i) => i % 2 ? seg : fn(seg, i === 0)).join("");
  }
  const LBL = String.raw`(\(?[A-Za-z]{1,2}\d?[.)]|\([A-Za-z0-9]{1,3}\)|\d{1,2}[.)])(?=\s|&nbsp;)`;
  const lbl = label => `<bdi class="ltr nw opt-label" dir="ltr">${label}</bdi>`;
  function labelLines(html) {
    return outsideCode(html, (seg, first) => {
      let out = seg.replace(new RegExp(String.raw`(<br\s*\/?>|<(?:li|p|div)\b[^>]*>)(\s*)` + LBL, "gi"), (m, lead, sp, label) => lead + sp + lbl(label));
      if (first) out = out.replace(new RegExp("^(\\s*)" + LBL), (m, sp, label) => sp + lbl(label));
      return out;
    });
  }

  const M_INL = '<span class="math-inline">(?:(?!</span>)[\\s\\S])*</span>';
  const M_RUN = '<span class="math-run" dir="rtl">(?:(?!</span></span>)[\\s\\S])*</span></span>';
  /* Only a formula and the punctuation that ends its line are glued. Formulas separated by punctuation are NOT
     joined: "\u05e2\u05d1\u05d5\u05e8 $n=1$: $3=3\cdot1^2$" or "$a$, $b$" as one LTR run would put the second formula first for an
     RTL reader. Each .math-inline is already its own isolate, so the ": " / ", " between them stays in RTL flow. */
  const RUN_OPEN = '<span class="math-run" dir="rtl">';
  function mathRuns(html) {
    return String(html).replace(new RegExp(`(${M_RUN}|${M_INL})([.,;:?!]+)(?=<br>|</[a-z]+>|$)`, "g"), (m, unit, punct0, at, all) => {
      if (all.slice(Math.max(0, at - RUN_OPEN.length), at) === RUN_OPEN) return m;   // already glued (idempotent)
      const punct = punct0.replace(/^[?!]/, "\u2060$&");   // a lone ? or ! is glued to the formula (word joiner): it must not wrap onto its own line
      return unit.startsWith(RUN_OPEN) ? unit.slice(0, -"</span>".length) + punct + "</span>"
        : `${RUN_OPEN}${unit}${punct}</span>`; });
  }
  const render = html => isolate(mathRuns(labelLines(html)));
  const bidi = { render, isolate, labelLines, mathRuns };
  root.Bidi = bidi;
  root.crsIsolate = render;

  const api = { text, complexity, number, Bidi: bidi };
  root.Normalize = api;
  if (typeof module !== "undefined" && module.exports) module.exports = api;
})(typeof window !== "undefined" ? window : globalThis);
