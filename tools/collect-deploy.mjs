#!/usr/bin/env node
/* ============================================================================
 *  时律盐创官网 · 生成「干净的部署文件夹」
 *  ---------------------------------------------------------------------------
 *  为什么需要它（这很可能是你网站更新推不上去的真正原因）：
 *
 *    整个仓库现在 3.48 GB，其中：
 *      · 项目10000822/                     2.74 GB  ← node_modules、安卓编译缓存
 *      · meeting_01.mp4                    265 MB   ← 单个文件就超 GitHub 的 100MB 上限
 *      · mus/、20261005/、20261017/ 等      合计约 700 MB
 *
 *    GitHub Pages 的建议上限是站点 1 GB，单个文件超过 100 MB 会被直接拒收。
 *    只要这些文件还在仓库里，每次 git push 都会失败或者慢到没法用 ——
 *    你改的网页自然永远上不了线。
 *
 *  这个脚本做的事：
 *    把「网站真正需要的东西」复制到一个独立目录，
 *    自动排除所有开发垃圾（node_modules、编译缓存、工作区目录、密码文件等）。
 *    生成出来的目录通常只有几十 MB，可以放心上传/推送。
 *
 *  用法（在网站仓库根目录下）：
 *      node tools/collect-deploy.mjs                      # 输出到同级 deploy-官网
 *      node tools/collect-deploy.mjs --out D:\deploy       # 指定输出目录
 *      node tools/collect-deploy.mjs --dry                 # 只统计，不复制
 *      YJX_VERBOSE=1 node tools/collect-deploy.mjs         # 打印完整跳过清单
 *
 *  注意：本脚本只做复制，不会删除或改动你任何原始文件。
 * ========================================================================== */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
/* 站点根目录 = tools/ 的上一级 */
const SITE_ROOT = path.resolve(__dirname, '..');
const SITE_NAME = path.basename(SITE_ROOT);

const args = process.argv.slice(2);
const DRY = args.includes('--dry');
const outArgIdx = args.indexOf('--out');
const OUT = outArgIdx >= 0 && args[outArgIdx + 1]
  ? path.resolve(args[outArgIdx + 1])
  : path.resolve(SITE_ROOT, '..', 'deploy-' + SITE_NAME);

/* ---------------------------------------------------------------------------
 *  排除清单 —— 本机开发用的东西，不该进网站仓库
 * ------------------------------------------------------------------------- */
const SKIP_DIRS = new Set([
  'node_modules',
  '.git', '.github',
  '.gradle', '.gradle-home', '.android-build-cache', '.android-sdk-home', '.npm-cache',
  'build', 'dist', 'output', '输出',
  '.idea', '.vscode', '.workbuddy', '.dsh',
  '卡密归档', '工具', '_acl-recovery',
  'win-unpacked',
  'deploy', 'deploy-官网',
]);

/* 目录名命中这些片段的也排除（放工作区 / 备份 / 测试目录）
   ⚠️ 注意：不要把 alpha0.2.0 这类「版本目录」排除掉 —— 那是手机版网页本体，
       yajinxia.html 的「网页版」按钮就指过去。历史上这里写成 /^alpha\d/ 把它
       误伤过，现在改成只匹配 alpha- 这种临时目录。 */
const SKIP_DIR_PATTERNS = [
  /(^|[-_\s])副本($|[-_\s])/,
  /^项目\d+/,
  /^alpha-/,
  /^beta-/,
  /^pentest-/,
  /^test(-|$)/i,
  /^新建/,
];

const SKIP_FILE_PATTERNS = [
  /\.zip$/i, /\.7z$/i, /\.rar$/i,
  /\.exe$/i, /\.apk$/i, /\.blockmap$/i,
  /\.log$/i, /\.psd$/i, /\.ai$/i,
  /(^|[_\-\s])备份/, /^新卡密/, /^卡密清单/,
  /^\.DS_Store$/i, /^Thumbs\.db$/i,
  /^Update Log\.txt$/i,
];

/* 单文件硬上限：GitHub 单文件 100 MB 会被拒收，这里留足余量 */
const MAX_FILE_BYTES = 90 * 1024 * 1024;

/* ------------------------------------------------------------------------- */
let copied = 0, bytes = 0, skippedFiles = 0, skippedDirs = 0;
const bigFiles = [];
const skippedList = [];

function shouldSkipDir(name) {
  if (SKIP_DIRS.has(name)) return true;
  for (const re of SKIP_DIR_PATTERNS) if (re.test(name)) return true;
  return false;
}

function shouldSkipFile(name, size) {
  for (const re of SKIP_FILE_PATTERNS) if (re.test(name)) return true;
  if (size > MAX_FILE_BYTES) { bigFiles.push({ name, size }); return true; }
  return false;
}

function walk(srcDir, dstDir, relPath) {
  let entries;
  try { entries = fs.readdirSync(srcDir, { withFileTypes: true }); }
  catch (e) { return; }

  for (const entry of entries) {
    const src = path.join(srcDir, entry.name);
    const rel = relPath ? relPath + '/' + entry.name : entry.name;

    if (entry.isDirectory()) {
      if (shouldSkipDir(entry.name)) { skippedDirs++; skippedList.push('目录  ' + rel); continue; }
      walk(src, path.join(dstDir, entry.name), rel);
      continue;
    }
    if (!entry.isFile()) continue;

    let size = 0;
    try { size = fs.statSync(src).size; } catch (e) { continue; }

    if (shouldSkipFile(entry.name, size)) {
      skippedFiles++;
      skippedList.push(`文件  ${rel}  (${(size / 1048576).toFixed(1)} MB)`);
      continue;
    }

    if (!DRY) {
      fs.mkdirSync(dstDir, { recursive: true });
      fs.copyFileSync(src, path.join(dstDir, entry.name));
    }
    copied++;
    bytes += size;
  }
}

/* ------------------------------------------------------------------------- */
console.log('');
console.log('  站点根目录：' + SITE_ROOT);
console.log('  输  出目录：' + OUT + (DRY ? '   （--dry 只统计，不复制）' : ''));
console.log('');

if (!fs.existsSync(SITE_ROOT)) {
  console.error('  [错误] 找不到站点根目录：' + SITE_ROOT);
  process.exit(1);
}

if (!DRY) {
  if (fs.existsSync(OUT)) {
    console.log('  输出目录已存在，先清空……');
    fs.rmSync(OUT, { recursive: true, force: true });
  }
  fs.mkdirSync(OUT, { recursive: true });
}

walk(SITE_ROOT, OUT, '');

console.log('  ────────────────────────────────────────────');
console.log(`  已复制：${copied} 个文件，合计 ${(bytes / 1048576).toFixed(1)} MB`);
console.log(`  已跳过：${skippedDirs} 个目录、${skippedFiles} 个文件`);
console.log('  ────────────────────────────────────────────');

if (bigFiles.length) {
  console.log('\n  因为「超过 90 MB」被排除的文件（GitHub 单文件上限 100MB）：');
  for (const f of bigFiles) console.log(`    ${(f.size / 1048576).toFixed(1)} MB   ${f.name}`);
  console.log('  → 这些请放网盘，网页里用链接指过去。');
}

if (process.env.YJX_VERBOSE) {
  console.log('\n  跳过清单：');
  for (const s of skippedList) console.log('    ' + s);
}

console.log('');
if (!DRY) {
  console.log('  完成。接下来：');
  console.log('    1) 打开输出目录，确认页面能正常打开、图片都在');
  console.log('    2) 把这个目录的内容作为网站仓库的内容上传/推送');
  console.log('    3) 安装包不要放进来，用网盘链接指过去');
  console.log('');
}
