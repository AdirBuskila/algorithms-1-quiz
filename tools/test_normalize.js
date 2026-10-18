// Plain-node unit tests for normalize.js:  node tools/test_normalize.js
const assert = require("assert");
const path = require("path");
global.window = {};
require(path.join(__dirname, "..", "normalize.js"));
const N = global.window.Normalize;

assert.ok(N && typeof N.text === "function" && typeof N.complexity === "function" && typeof N.number === "function", "Normalize API");

// complexity: spaces, log spellings, superscripts, case, Theta/O
assert.strictEqual(N.complexity("O(n log n)"), N.complexity("O(nlogn)"));
assert.strictEqual(N.complexity("O(n²)"), N.complexity("O(n^2)"));
assert.strictEqual(N.complexity("O(n log n)"), N.complexity("o( N LG N )"));
assert.strictEqual(N.complexity("O(log n)"), N.complexity("O(lg n)"));
assert.strictEqual(N.complexity("O(log_2 n)"), N.complexity("O(log n)"));
assert.strictEqual(N.complexity("O(n^{2})"), N.complexity("O(n^2)"));
assert.notStrictEqual(N.complexity("O(n log n)"), N.complexity("O(n^2)"));
// both Theta and O are accepted as written
assert.strictEqual(N.complexity("Θ(n)"), N.complexity("O(n)"));
assert.notStrictEqual(N.complexity("O(n)"), N.complexity("O(n^2)"));

// number: comma decimal, unicode minus, fractions, junk
assert.strictEqual(N.number("2,5"), 2.5);
assert.strictEqual(N.number(" 3.25 "), 3.25);
assert.strictEqual(N.number("−4"), -4);
assert.strictEqual(N.number("1/4"), 0.25);
assert.ok(Number.isNaN(N.number("abc")));
assert.ok(Number.isNaN(N.number("")));

// text: trim, collapse whitespace, case-insensitive
assert.strictEqual(N.text("  Hello   World "), N.text("hello world"));
assert.strictEqual(N.text("O(1)."), N.text("o(1)"));

console.log("test_normalize: ok");
