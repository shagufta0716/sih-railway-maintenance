import React from "react";
import { ArrowRight, GitBranch, ShieldCheck, Activity } from "lucide-react";

const FONT_LINK =
  "https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap";

export default function LandingPage({ onLogin, onRegister }) {
  return (
    <div
      className="min-h-screen w-full bg-[#0E1318] text-[#E7EBEF]"
      style={{ fontFamily: "'IBM Plex Sans', sans-serif" }}
    >
      <link rel="stylesheet" href={FONT_LINK} />

      {/* Top bar */}
      <header className="border-b border-[#232B36]">
        <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="w-7 h-7 rounded-[3px] bg-[#4C7A92] flex items-center justify-center">
              <GitBranch size={15} className="text-[#0E1318]" strokeWidth={2.5} />
            </div>
            <span className="text-[15px] font-medium tracking-tight">Trackline</span>
          </div>
          <nav className="flex items-center gap-8 text-[13.5px] text-[#8C97A5]">
            <a href="#platform" className="hover:text-[#E7EBEF] transition-colors">Platform</a>
            <a href="#coverage" className="hover:text-[#E7EBEF] transition-colors">Coverage</a>
            <button
              onClick={onLogin}
              className="text-[#E7EBEF] hover:text-white transition-colors"
            >
              Sign in
            </button>
            <button
              onClick={onRegister}
              className="bg-[#E7EBEF] text-[#0E1318] px-3.5 py-1.5 rounded-[3px] font-medium hover:bg-white transition-colors"
            >
              Request access
            </button>
          </nav>
        </div>
      </header>

      {/* Hero */}
      <section className="max-w-6xl mx-auto px-6 pt-20 pb-16 grid grid-cols-1 md:grid-cols-12 gap-10">
        <div className="md:col-span-7">
          <p
            className="text-[#4C7A92] text-[13px] mb-5"
            style={{ fontFamily: "'IBM Plex Mono', monospace" }}
          >
            Block planning — Engineering / TRD / S&amp;T
          </p>
          <h1 className="text-[42px] leading-[1.12] font-medium tracking-tight max-w-[560px]">
            One schedule for every maintenance block on the section.
          </h1>
          <p className="mt-5 text-[16px] leading-relaxed text-[#8C97A5] max-w-[480px]">
            Trackline merges defect data from TMS, SMMS and TDMS with the
            working timetable, then produces a conflict-free block plan
            departments can actually run against — instead of three teams
            requesting the same corridor separately.
          </p>
          <div className="mt-8 flex items-center gap-4">
            <button
              onClick={onRegister}
              className="flex items-center gap-2 bg-[#4C7A92] text-[#0E1318] px-4 py-2.5 rounded-[3px] text-[14px] font-medium hover:bg-[#5a8ba5] transition-colors"
            >
              Request access <ArrowRight size={15} />
            </button>
            <button
              onClick={onLogin}
              className="text-[14px] text-[#E7EBEF] border border-[#2A323D] px-4 py-2.5 rounded-[3px] hover:border-[#4C7A92] transition-colors"
            >
              Sign in
            </button>
          </div>
        </div>

        <div className="md:col-span-5 border border-[#232B36] rounded-[4px] bg-[#161C24] p-5">
          <div
            className="text-[11px] text-[#8C97A5] mb-3"
            style={{ fontFamily: "'IBM Plex Mono', monospace" }}
          >
            Next 7 days — Chakradharpur Div.
          </div>
          {[
            { sec: "TATA–SINI", type: "Track relaying", urgency: "Critical", color: "#C4453D" },
            { sec: "SINI–GOMOH", type: "OHE maintenance", urgency: "High", color: "#C98A3B" },
            { sec: "ROU–GP", type: "Signal renewal", urgency: "Medium", color: "#4C8B63" },
          ].map((row, i) => (
            <div
              key={i}
              className="flex items-center justify-between py-3 border-t border-[#232B36] first:border-t-0"
            >
              <div>
                <div className="text-[13.5px]">{row.sec}</div>
                <div className="text-[12px] text-[#8C97A5]">{row.type}</div>
              </div>
              <span
                className="text-[11px] px-2 py-0.5 rounded-[2px]"
                style={{
                  color: row.color,
                  border: `1px solid ${row.color}55`,
                  fontFamily: "'IBM Plex Mono', monospace",
                }}
              >
                {row.urgency}
              </span>
            </div>
          ))}
        </div>
      </section>

      {/* Feature row */}
      <section id="platform" className="border-t border-[#232B36]">
        <div className="max-w-6xl mx-auto px-6 py-14 grid grid-cols-1 md:grid-cols-3 gap-8">
          {[
            {
              icon: Activity,
              title: "Priority scoring",
              body: "Every job is scored on overdue days, defect severity and traffic exposure, so critical work never waits behind routine tasks.",
            },
            {
              icon: GitBranch,
              title: "Zero-conflict blocks",
              body: "Blocks are placed against the live timetable — no possession is ever granted over a train movement, regardless of department.",
            },
            {
              icon: ShieldCheck,
              title: "Coordinated requests",
              body: "Overlapping requests from Engineering, TRD and S&T on the same corridor are merged into a single possession automatically.",
            },
          ].map((f, i) => (
            <div key={i}>
              <f.icon size={18} className="text-[#4C7A92] mb-3" strokeWidth={1.75} />
              <h3 className="text-[14.5px] font-medium mb-1.5">{f.title}</h3>
              <p className="text-[13.5px] text-[#8C97A5] leading-relaxed">{f.body}</p>
            </div>
          ))}
        </div>
      </section>

      <footer className="border-t border-[#232B36] py-6">
        <div className="max-w-6xl mx-auto px-6 text-[12px] text-[#8C97A5]">
          Trackline — decision support for fixed infrastructure maintenance
        </div>
      </footer>
    </div>
  );
}
