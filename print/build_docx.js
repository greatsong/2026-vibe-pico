// 피코 바이브코딩 교재 → A5 판형 docx (A4 '2쪽 모아찍기' 인쇄용)
// 사용: python3 print/export_content.py && node print/build_docx.js
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  Table, TableRow, TableCell, WidthType, ShadingType, BorderStyle,
  Footer, PageNumber, TableOfContents, LevelFormat, VerticalAlign,
} = require("docx");

const ROOT = path.dirname(__dirname);
const TEACHER = process.argv.includes("--teacher");
const CH = JSON.parse(fs.readFileSync(
  path.join(__dirname, TEACHER ? "content_teacher.json" : "content.json"), "utf-8"));

// ── 판형: A5 (148×210mm). A4 가로 '한 면에 2쪽'으로 찍으면 실물 크기 그대로.
const PAGE = { width: 8392, height: 11907 };
const MARGIN = { top: 880, bottom: 880, left: 820, right: 820 };
const TEXTW = PAGE.width - MARGIN.left - MARGIN.right; // 6752

const KO = "Malgun Gothic";       // 없는 환경(Mac)은 자동 대체됨
const MONO = "Consolas";
const WEB = "greatsong.github.io/2026-vibe-pico";

const KIND = { // 콜아웃 배경/테두리/제목색
  tip:  { fill: "FFF8E7", border: "E3C77E", title: "8A6A1F", icon: "💡" },
  warn: { fill: "FDEDEC", border: "E5A19B", title: "9F3730", icon: "⚠️" },
  info: { fill: "EEF4FD", border: "A9C2EA", title: "2F5496", icon: "ℹ️" },
  key:  { fill: "EBF6EF", border: "8FC8A3", title: "1F6B3A", icon: "🔑" },
};
const CIRCLED = "①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮";

// ── 인라인 HTML → TextRun[]  (<b> <code> <br> <a> 지원, 나머지 태그 제거)
function decode(s) {
  return s.replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&quot;/g, '"')
          .replace(/&#39;/g, "'").replace(/&nbsp;/g, " ").replace(/&amp;/g, "&");
}
function runsFromHtml(html, base = {}) {
  const runs = [];
  let bold = 0, code = 0, buf = "", pendingBreak = false;
  const flush = () => {
    if (!buf) return;
    runs.push(new TextRun({
      text: decode(buf), bold: !!bold || base.bold,
      font: code ? MONO : (base.font || KO),
      size: code ? (base.size ? base.size - 2 : 18) : base.size,
      color: base.color, italics: base.italics,
      shading: code ? { type: ShadingType.CLEAR, fill: "F3EEE3" } : undefined,
      break: pendingBreak ? 1 : undefined,
    }));
    buf = ""; pendingBreak = false;
  };
  const parts = String(html).split(/(<[^>]+>)/);
  for (const p of parts) {
    if (!p) continue;
    if (p[0] === "<") {
      const tag = p.toLowerCase();
      if (tag.startsWith("<b>") || tag.startsWith("<b ")) { flush(); bold++; }
      else if (tag === "</b>") { flush(); bold = Math.max(0, bold - 1); }
      else if (tag.startsWith("<code")) { flush(); code++; }
      else if (tag === "</code>") { flush(); code = Math.max(0, code - 1); }
      else if (tag.startsWith("<br")) { flush(); pendingBreak = true; buf = ""; runs.push(new TextRun({ text: "", break: 1 })); pendingBreak = false; }
      // <a>·<span>·기타 태그는 서식만 제거하고 내용 유지
    } else buf += p;
  }
  flush();
  return runs.length ? runs : [new TextRun({ text: "" })];
}
function para(html, opt = {}) {
  return new Paragraph({
    children: runsFromHtml(html, opt.run || {}),
    spacing: { after: opt.after ?? 110, line: 264, before: opt.before ?? 0 },
    alignment: opt.align, heading: opt.heading, pageBreakBefore: opt.pageBreakBefore,
    indent: opt.indent, numbering: opt.numbering,
  });
}

// ── 1칸 박스(콜아웃·코드·프롬프트 공용)
function box(children, fill, border) {
  return new Table({
    width: { size: TEXTW, type: WidthType.DXA }, columnWidths: [TEXTW],
    borders: undefined,
    rows: [new TableRow({ children: [new TableCell({
      width: { size: TEXTW, type: WidthType.DXA },
      shading: { type: ShadingType.CLEAR, fill },
      margins: { top: 90, bottom: 90, left: 140, right: 140 },
      borders: {
        top: { style: BorderStyle.SINGLE, size: 6, color: border },
        bottom: { style: BorderStyle.SINGLE, size: 6, color: border },
        left: { style: BorderStyle.SINGLE, size: 6, color: border },
        right: { style: BorderStyle.SINGLE, size: 6, color: border },
      },
      children,
    })] })],
  });
}
const spacer = (h = 90) => new Paragraph({ children: [], spacing: { after: h } });

// ── 아이템 렌더러
function renderItem(it, accent, out) {
  const t = it.type;
  if (t === "text") out.push(para(it.html));
  else if (t === "step_head") out.push(para(it.html, { before: 70, after: 90 }));
  else if (t === "callout") {
    const k = KIND[it.kind] || KIND.info;
    out.push(box([
      para(`${k.icon} ${it.title}`, { run: { bold: true, color: k.title, size: 19 }, after: 50 }),
      para(it.html, { run: { size: 19 }, after: 0 }),
    ], k.fill, k.border), spacer());
  }
  else if (t === "dig") {
    out.push(box([
      para(`🔬 더 알아보기 — ${it.title}`, { run: { bold: true, color: "6B5836", size: 19 }, after: 50 }),
      para(it.html, { run: { size: 19 }, after: 0 }),
    ], "F6F1E6", "D8CBAF"), spacer());
  }
  else if (t === "concept") {
    for (const c of it.items)
      out.push(new Paragraph({
        children: [
          new TextRun({ text: "▪ ", color: accent, bold: true }),
          new TextRun({ text: decode(c.t.replace(/<[^>]+>/g, "")) + " — ", bold: true }),
          ...runsFromHtml(c.d),
        ],
        spacing: { after: 70, line: 264 }, indent: { left: 170, hanging: 170 },
      }));
    out.push(spacer(50));
  }
  else if (t === "steps") {
    it.items.forEach((s, i) => out.push(new Paragraph({
      children: [
        new TextRun({ text: (CIRCLED[i] || `${i + 1}.`) + " ", color: accent, bold: true }),
        new TextRun({ text: decode(s.t.replace(/<[^>]+>/g, "")) + "  ", bold: true }),
        ...runsFromHtml(s.d),
      ],
      spacing: { after: 80, line: 264 }, indent: { left: 240, hanging: 240 },
    })));
    out.push(spacer(50));
  }
  else if (t === "code") {
    const lines = (it.code || "").split("\n");
    const kids = [para(`〈 ${it.label || "코드"} 〉`, { run: { bold: true, size: 18, color: "5A4A28" }, after: 60 })];
    for (const ln of lines) kids.push(new Paragraph({
      children: [new TextRun({ text: ln === "" ? " " : ln, font: MONO, size: 15 })],
      spacing: { after: 0, line: 220 },
    }));
    out.push(box(kids, "FBF8F0", "D8CBAF"), spacer());
  }
  else if (t === "prompt" || t === "improve") {
    const icon = t === "prompt" ? "🤖" : "✨";
    const kids = [para(`${icon} ${it.label}`, { run: { bold: true, size: 19, color: "1F6B3A" }, after: 60 })];
    for (const ln of String(it.text).split("\n"))
      kids.push(new Paragraph({ children: [new TextRun({ text: ln === "" ? " " : ln, size: 18 })], spacing: { after: 30, line: 240 } }));
    out.push(box(kids, "F0F7F2", "9CCBAA"), spacer());
  }
  else if (t === "mistakes") {
    const w = [1850, 2100, TEXTW - 3950];
    const head = ["증상", "원인", "해결"].map((h, i) => new TableCell({
      width: { size: w[i], type: WidthType.DXA },
      shading: { type: ShadingType.CLEAR, fill: "F1E9D8" },
      margins: { top: 60, bottom: 60, left: 90, right: 90 },
      children: [para(h, { run: { bold: true, size: 18 }, after: 0 })],
    }));
    const rows = [new TableRow({ children: head, tableHeader: true })];
    for (const m of it.items) rows.push(new TableRow({
      children: [m.sym, m.cause, m.fix].map((v, i) => new TableCell({
        width: { size: w[i], type: WidthType.DXA },
        margins: { top: 60, bottom: 60, left: 90, right: 90 },
        children: [para(v, { run: { size: 17 }, after: 0 })],
      })),
    }));
    out.push(new Table({ width: { size: TEXTW, type: WidthType.DXA }, columnWidths: w, rows }), spacer());
  }
  else if (t === "check") {
    for (const c of it.items) {
      out.push(new Paragraph({
        children: [new TextRun({ text: "Q. ", bold: true, color: accent }), ...runsFromHtml(c.q, { bold: true })],
        spacing: { after: 30, line: 264 },
      }));
      out.push(new Paragraph({
        children: [new TextRun({ text: "→ ", color: "888888" }), ...runsFromHtml(c.a, { size: 19 })],
        spacing: { after: 90, line: 264 }, indent: { left: 240 },
      }));
    }
  }
  else if (t === "check_list") {
    for (const c of it.items) out.push(new Paragraph({
      children: [new TextRun({ text: "☐ ", color: accent, bold: true }), ...runsFromHtml(c)],
      spacing: { after: 60, line: 264 }, indent: { left: 220, hanging: 220 },
    }));
    out.push(spacer(50));
  }
  else if (t === "ideas") {
    for (const c of it.items)
      out.push(new Paragraph({
        children: [
          new TextRun({ text: "★ ", color: accent, bold: true }),
          new TextRun({ text: decode(c.t.replace(/<[^>]+>/g, "")) + " — ", bold: true }),
          ...runsFromHtml(c.d),
        ],
        spacing: { after: 70, line: 264 }, indent: { left: 200, hanging: 200 },
      }));
    out.push(spacer(50));
  }
  else if (t === "linkbtn") {
    out.push(para(`🔗 <b>${it.label}</b><br>${it.href}`, { run: { size: 18 }, after: 90 }));
  }
  else if (t === "teacher") {
    const TK = { say: ["🗣", "진행 멘트"], ask: ["❓", "발문"], theory: ["📖", "이론 심화"], err: ["🚨", "예상 오류"] };
    const [icon, kindName] = TK[it.kind] || ["📝", "강사 메모"];
    // 제목이 이미 '진행 멘트 — …'처럼 종류로 시작하면 접두어를 겹쳐 붙이지 않는다
    const head = it.title.startsWith(kindName) ? it.title : `${kindName} — ${it.title}`;
    out.push(box([
      para(`${icon} ${head}`, { run: { bold: true, size: 19, color: "6D28D9" }, after: 50 }),
      para(it.html, { run: { size: 18 }, after: 0 }),
    ], "F6F2FE", "C4B5FD"), spacer());
  }
  else if (t === "raw" && it.rows) {
    // 운영 계획 시간표 — 웹의 HTML 대신 원본 rows로 표를 다시 만든다
    const w = [900, 3200, TEXTW - 4100];
    const head = ["시간", "내용", "비고"].map((h, i) => new TableCell({
      width: { size: w[i], type: WidthType.DXA },
      shading: { type: ShadingType.CLEAR, fill: "EBF6EF" },
      margins: { top: 60, bottom: 60, left: 90, right: 90 },
      children: [para(h, { run: { bold: true, size: 18 }, after: 0 })],
    }));
    const rows = [new TableRow({ children: head, tableHeader: true })];
    for (const r of it.rows) rows.push(new TableRow({
      children: r.map((v, i) => new TableCell({
        width: { size: w[i], type: WidthType.DXA },
        margins: { top: 60, bottom: 60, left: 90, right: 90 },
        children: [para(v, { run: { size: i === 2 ? 16 : 17, bold: i === 0, color: i === 0 ? "B45309" : undefined }, after: 0 })],
      })),
    }));
    out.push(new Table({ width: { size: TEXTW, type: WidthType.DXA }, columnWidths: w, rows }), spacer());
  }
  else if (t === "raw" || t === "figure_hw") {
    out.push(para(`※ 이 자리의 그림·배선표·인터랙티브 도구는 웹 교재에서 확인하세요 (${WEB})`,
      { run: { italics: true, size: 17, color: "8A7B5C" }, after: 90 }));
  }
}

// ── 본문 조립
const body = [];

// 표지
body.push(
  new Paragraph({ children: [], spacing: { after: 2600 } }),
  para("피코 바이브 피지컬 코딩", { align: AlignmentType.CENTER, run: { bold: true, size: 52, color: "B45309" }, after: 160 }),
  para(TEACHER ? "데이터로 탐구하는 피지컬 컴퓨팅 교재 · 강사용"
               : "데이터로 탐구하는 피지컬 컴퓨팅 교재",
    { align: AlignmentType.CENTER, run: { size: 26, color: "6B5836" }, after: 600 }),
  para("라즈베리파이 피코 2 WH · 그로브 쉴드 · WS2813 LED · MQ-2 가스센서", { align: AlignmentType.CENTER, run: { size: 19, color: "6B5836" }, after: 90 }),
  para("설치와 조립부터 와이파이·LED·공기질·날씨 API·구글 시트 기록·자유 프로젝트까지", { align: AlignmentType.CENTER, run: { size: 19, color: "6B5836" }, after: 1800 }),
  para(`웹 교재(그림·인터랙티브 포함) : https://${WEB}`, { align: AlignmentType.CENTER, run: { size: 19 }, after: 90 }),
  para(TEACHER ? "2026. 7.  ·  강사용(인쇄판) — 진행 멘트·발문·예상 오류·운영 계획 포함"
               : "2026. 7.  ·  학생용(인쇄판)",
    { align: AlignmentType.CENTER, run: { size: 19, color: "888888" }, after: 0 }),
);

// 목차
body.push(
  para("목차", { heading: HeadingLevel.HEADING_1, pageBreakBefore: true }),
  para("※ 페이지 번호가 비어 보이면 Word에서 열어 목차를 클릭 → F9(필드 업데이트)를 누르세요.",
    { run: { italics: true, size: 17, color: "8A7B5C" }, after: 160 }),
  new TableOfContents("목차", { hyperlink: true, headingStyleRange: "1-1" }),
);

// 챕터
for (const c of CH) {
  const accent = (c.accent || "#B45309").replace("#", "");
  body.push(
    para(`${/^[0-9]/.test(c.num) ? "CHAPTER " + c.num + " · " : "부록 " + c.num + " · "}${c.title}`,
      { heading: HeadingLevel.HEADING_1, pageBreakBefore: true }),
    para(c.subtitle, { run: { size: 20, color: "6B5836" }, after: 140 }),
  );
  if (c.goals && c.goals.length) {
    const kids = [para("🎯 이 장을 마치면", { run: { bold: true, size: 19, color: "8A6A1F" }, after: 50 })];
    for (const g of c.goals) kids.push(new Paragraph({
      children: [new TextRun({ text: "· ", bold: true }), ...runsFromHtml(g, { size: 19 })],
      spacing: { after: 30, line: 250 },
    }));
    body.push(box(kids, "FFFBEF", "E3C77E"), spacer());
  }
  if (c.why) {
    body.push(box([
      para("💡 왜 배우나요?", { run: { bold: true, size: 19, color: "8A6A1F" }, after: 50 }),
      para(c.why, { run: { size: 19 }, after: 0 }),
    ], "FFFBEF", "E3C77E"), spacer(140));
  }
  c.sections.forEach((s, si) => {
    body.push(para(s.title, { heading: HeadingLevel.HEADING_2, before: si === 0 ? 0 : 120 }));
    for (const it of s.items) renderItem(it, accent, body);
  });
}

// ── 문서
const doc = new Document({
  features: { updateFields: true },
  styles: {
    default: {
      document: { run: { font: KO, size: 20, color: "3A2E1A" }, paragraph: { spacing: { line: 264 } } },
      heading1: { run: { font: KO, size: 30, bold: true, color: "B45309" },
                  paragraph: { spacing: { before: 160, after: 140 } } },
      heading2: { run: { font: KO, size: 24, bold: true, color: "6B4E1F" },
                  paragraph: { spacing: { before: 200, after: 110 },
                    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "E0D3B8", space: 2 } } } },
    },
  },
  sections: [{
    properties: { page: { size: PAGE, margin: MARGIN } },
    footers: {
      default: new Footer({ children: [new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ children: [PageNumber.CURRENT], size: 16, color: "9A8B6A", font: KO })],
      })] }),
    },
    children: body,
  }],
});

Packer.toBuffer(doc).then(buf => {
  const out = path.join(__dirname,
    TEACHER ? "피코_바이브코딩_교재_A5_강사용.docx" : "피코_바이브코딩_교재_A5_학생용.docx");
  fs.writeFileSync(out, buf);
  console.log("OK →", out, `(${Math.round(buf.length / 1024)} KB)`);
});
