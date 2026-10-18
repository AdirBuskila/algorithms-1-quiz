// Loader for the guided-course level files (courses/<courseId>/<LEVEL>.js), shared by
// course_lint.js, course_dump.js and (through the CLI below) tools/build_courses.py.
//
//   node tools/course_load.js     -> prints {"levels":[{courseId,file,level}],"courseDirs":[...],"errors":[...]}
//
// Each level file calls   window.COURSE_LEVEL("<courseId>", { id, order, icon, title, goal, boss?, source,
// lesson:{html}, questions:[...] })   exactly once. The file is executed in a bare vm sandbox (no DOM),
// so level files must be plain data. Nothing here renders anything: the build (build_courses.py) turns
// the loaded data into the shipped courses.js with the math pre-rendered.
"use strict";
const fs = require("fs"), path = require("path"), vm = require("vm");

function load(root) {
  const base = path.join(root, "courses");
  const out = { levels: [], courseDirs: [], errors: [] };
  if (!fs.existsSync(base)) return out;
  for (const ent of fs.readdirSync(base, { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name))) {
    if (!ent.isDirectory()) {
      if (ent.name.endsWith(".js")) out.errors.push(`courses/${ent.name}: level files live in courses/<courseId>/`);
      continue;
    }
    out.courseDirs.push(ent.name);
    const dir = path.join(base, ent.name);
    for (const f of fs.readdirSync(dir).filter(n => n.endsWith(".js")).sort()) {
      const rel = `courses/${ent.name}/${f}`;
      const calls = [];
      const sandbox = {};
      sandbox.window = sandbox;
      sandbox.COURSE_LEVEL = (courseId, level) => { calls.push([courseId, level]); };
      sandbox.console = console;
      try {
        vm.runInNewContext(fs.readFileSync(path.join(dir, f), "utf8"), vm.createContext(sandbox), { filename: rel, timeout: 5000 });
      } catch (e) {
        out.errors.push(`${rel}: ${String(e && e.message || e).split("\n")[0]}`);
        continue;
      }
      if (calls.length !== 1) { out.errors.push(`${rel}: must call COURSE_LEVEL exactly once (called ${calls.length}x)`); continue; }
      const [courseId, level] = calls[0];
      if (courseId !== ent.name) { out.errors.push(`${rel}: COURSE_LEVEL("${courseId}") but the folder is "${ent.name}"`); continue; }
      if (!level || typeof level !== "object") { out.errors.push(`${rel}: COURSE_LEVEL needs a level object`); continue; }
      out.levels.push({ courseId, file: rel, level: JSON.parse(JSON.stringify(level)) });
    }
  }
  return out;
}

module.exports = { load };

if (require.main === module) {
  process.stdout.write(JSON.stringify(load(path.join(__dirname, ".."))));
}
