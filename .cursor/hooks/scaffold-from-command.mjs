#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
const prompt = process.env.CURSOR_PROMPT || "";
const root = process.cwd();
const m = prompt.match(/sprint\s*(\d+)/i);
const sprint = process.env.SPRINT_NUMBER || (m ? m[1] : null);
function ensure(p) {
  fs.mkdirSync(p, { recursive: true });
  const gk = path.join(p, ".gitkeep");
  if (!fs.existsSync(gk)) fs.writeFileSync(gk, "");
}
if (/\/(implement-api|implement-ui|expand-test-coverage|generate-user-stories-from-transcript|generate-test-cases-from-user-stories|generate-brd|plan-sprint|plan-governed-stories)/.test(prompt)) {
  if (sprint) {
    ensure(path.join(root, `docs/sprint${sprint}`));
    ensure(path.join(root, `docs/sprint${sprint}/userstory`));
  }
  ensure(path.join(root, "artifacts/audit"));
  ensure(path.join(root, "artifacts/intake"));
  ensure(path.join(root, "docs/intake"));
  ensure(path.join(root, "docs/harness"));
}
