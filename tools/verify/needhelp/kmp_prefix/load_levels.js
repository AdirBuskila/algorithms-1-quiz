// prints every kmp_prefix level as JSON (stdout, utf8). ASCII-only source.
const fs = require("fs"), path = require("path"), vm = require("vm");
const dir = process.argv[2];
const out = [];
for (const f of fs.readdirSync(dir).filter(n => /^C\d+\.js$/.test(n)).sort()) {
  const ctx = { COURSE_LEVEL: (cid, obj) => out.push({ course: cid, file: f, level: obj }), String };
  vm.runInNewContext(fs.readFileSync(path.join(dir, f), "utf8"), ctx, { filename: f });
}
process.stdout.write(JSON.stringify(out));
