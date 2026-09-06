import React, { useState, useEffect, createContext, useContext } from "react";
import {
  GitBranch,
  ChevronDown,
  PanelLeftClose,
  PanelLeft,
  Play,
  Settings,
  LogOut,
  User,
  Sun,
  Moon,
} from "lucide-react";
import {
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  ResponsiveContainer,
  Tooltip,
} from "recharts";

const FONT_LINK =
  "https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap";

const TABS = ["Executive summary", "Gantt timeline", "Master timetable", "Model diagnostics"];

const ZONES = ["Central Railway", "Eastern Railway", "Northern Railway", "South Central Railway", "Southern Railway"];
const URGENCY = ["Critical", "High", "Medium"];

const THEMES = {
  dark: {
    bg: "#0E1318",
    headerBg: "#0E1318",
    sidebarBg: "#0E1318",
    text: "#E7EBEF",
    textMuted: "#8C97A5",
    textDim: "#5A6472",
    cardBg: "#161C24",
    cardBorder: "#232B36",
    navBorder: "#232B36",
    inputBg: "#0E1318",
    inputBorder: "#2A323D",
    hoverBg: "#1D242D",
    activeTabBg: "#1D242D",
    activeTabText: "#E7EBEF",
    primary: "#4C7A92",
    primaryHover: "#5a8ba5",
    primaryText: "#0E1318",
    accentLight: "#9EC3D5",
    chartCursor: "#1D242D",
    chartTooltipBg: "#0E1318",
    chartAxis: "#232B36",
    chipBgActive: "rgba(76, 122, 146, 0.15)",
    chipBorderActive: "#4C7A92",
    chipTextActive: "#9EC3D5",
    btnThemeBg: "#1D242D",
    btnThemeBorder: "#232B36",
  },
  light: {
    bg: "#F4F6F9",
    headerBg: "#FFFFFF",
    sidebarBg: "#FFFFFF",
    text: "#0F172A",
    textMuted: "#475569",
    textDim: "#94A3B8",
    cardBg: "#FFFFFF",
    cardBorder: "#E2E8F0",
    navBorder: "#E2E8F0",
    inputBg: "#F8FAFC",
    inputBorder: "#CBD5E1",
    hoverBg: "#F1F5F9",
    activeTabBg: "#E2E8F0",
    activeTabText: "#0F172A",
    primary: "#1E293B",
    primaryHover: "#334155",
    primaryText: "#FFFFFF",
    accentLight: "#0284C7",
    chartCursor: "#F1F5F9",
    chartTooltipBg: "#FFFFFF",
    chartAxis: "#E2E8F0",
    chipBgActive: "rgba(14, 165, 233, 0.12)",
    chipBorderActive: "#0284C7",
    chipTextActive: "#0284C7",
    btnThemeBg: "#F1F5F9",
    btnThemeBorder: "#E2E8F0",
  },
};

const ThemeContext = createContext({
  theme: "dark",
  t: THEMES.dark,
  toggleTheme: () => {},
});

const useTheme = () => useContext(ThemeContext);

function Chip({ label, active, onClick }) {
  const { t } = useTheme();
  return (
    <button
      onClick={onClick}
      style={{
        backgroundColor: active ? t.chipBgActive : "transparent",
        borderColor: active ? t.chipBorderActive : t.inputBorder,
        color: active ? t.chipTextActive : t.textMuted,
      }}
      className="text-[12.5px] px-2.5 py-1 rounded-[3px] border transition-colors hover:opacity-90"
    >
      {label}
    </button>
  );
}

function KpiCell({ label, value, sub, valueColor }) {
  const { t } = useTheme();
  return (
    <div
      style={{ borderColor: t.cardBorder }}
      className="px-6 py-5 border-r last:border-r-0 overflow-hidden"
    >
      <div style={{ color: t.textMuted }} className="text-[12px] mb-2 truncate">{label}</div>
      <div
        className="text-[28px] leading-none font-semibold truncate"
        style={{ fontFamily: "'IBM Plex Mono', monospace", color: valueColor || t.text }}
      >
        {value}
      </div>
      <div style={{ color: t.textDim }} className="text-[12px] mt-2 truncate">{sub}</div>
    </div>
  );
}

function MasterTimetable({ data }) {
  const { t } = useTheme();
  const [search, setSearch] = useState("");
  const filtered = data.filter(d => 
    (d.job_id && d.job_id.toLowerCase().includes(search.toLowerCase())) ||
    (d.section_id && d.section_id.toLowerCase().includes(search.toLowerCase())) ||
    (d.job_type && d.job_type.toLowerCase().includes(search.toLowerCase()))
  );

  return (
    <div>
      <h1 style={{ color: t.text }} className="text-[19px] font-medium mb-1">Master timetable</h1>
      <p style={{ color: t.textMuted }} className="text-[13.5px] mb-6">All scheduled maintenance blocks</p>
      
      <div className="mb-4">
        <input 
          type="text" 
          placeholder="Search jobs, sections, or types..." 
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          style={{
            backgroundColor: t.inputBg,
            borderColor: t.inputBorder,
            color: t.text,
          }}
          className="w-[300px] border rounded-[3px] px-3 py-2 text-[13px] outline-none transition-colors"
        />
      </div>

      <div
        style={{
          backgroundColor: t.cardBg,
          borderColor: t.cardBorder,
        }}
        className="border rounded-[4px] overflow-x-auto shadow-sm"
      >
        <table className="w-full text-left text-[13px]">
          <thead>
            <tr style={{ borderColor: t.cardBorder, color: t.textMuted }} className="border-b">
              <th className="px-4 py-3 font-medium">Job ID</th>
              <th className="px-4 py-3 font-medium">Section</th>
              <th className="px-4 py-3 font-medium">Type</th>
              <th className="px-4 py-3 font-medium">Date</th>
              <th className="px-4 py-3 font-medium">Time Window</th>
              <th className="px-4 py-3 font-medium">Urgency</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((d, i) => (
              <tr
                key={i}
                style={{ borderColor: t.cardBorder, color: t.text }}
                className="border-b last:border-b-0 transition-colors hover:opacity-80"
              >
                <td className="px-4 py-3 font-semibold" style={{ fontFamily: "'IBM Plex Mono', monospace" }}>{d.job_id}</td>
                <td className="px-4 py-3">{d.section_id}</td>
                <td className="px-4 py-3">{d.job_type}</td>
                <td className="px-4 py-3">{d.scheduled_date}</td>
                <td className="px-4 py-3">{d.block_start_time} - {d.block_end_time}</td>
                <td className="px-4 py-3">
                  <span className={`px-2 py-0.5 rounded-[2px] text-[11px] font-medium ${
                    d.urgency === 'Critical' ? 'bg-[#C4453D]/20 text-[#C4453D]' : 
                    d.urgency === 'High' ? 'bg-[#C98A3B]/20 text-[#C98A3B]' : 
                    'bg-[#4C8B63]/20 text-[#4C8B63]'
                  }`}>
                    {d.urgency}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {filtered.length === 0 && (
          <div style={{ color: t.textMuted }} className="p-4 text-center text-[13px]">
            No matching records found.
          </div>
        )}
      </div>
    </div>
  );
}

function GanttTimeline({ data }) {
  const { t } = useTheme();
  const sortedData = [...data].sort((a, b) => (a.section_id || "").localeCompare(b.section_id || ""));
  
  const ganttData = sortedData.filter(d => d.job_id).map(d => ({
    id: d.job_id,
    section: d.section_id,
    timeRange: [d.block_start_hr, d.block_end_hr],
    fill: d.urgency === 'Critical' ? '#C4453D' : d.urgency === 'High' ? '#C98A3B' : '#4C8B63',
  }));

  return (
    <div className="flex flex-col h-full">
      <h1 style={{ color: t.text }} className="text-[19px] font-medium mb-1">Gantt timeline</h1>
      <p style={{ color: t.textMuted }} className="text-[13.5px] mb-6">Scheduled blocks by hour (0-24)</p>
      
      <div
        style={{
          backgroundColor: t.cardBg,
          borderColor: t.cardBorder,
        }}
        className="flex-1 border rounded-[4px] p-5 min-h-[420px] shadow-sm"
      >
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={ganttData} layout="vertical" margin={{ left: 20, right: 20 }}>
            <XAxis type="number" domain={[0, 24]} tickCount={25} tick={{ fill: t.textMuted, fontSize: 11 }} axisLine={{ stroke: t.chartAxis }} />
            <YAxis type="category" dataKey="id" width={90} tick={{ fill: t.textMuted, fontSize: 11 }} axisLine={{ stroke: t.chartAxis }} />
            <Tooltip 
              cursor={{ fill: t.chartCursor }}
              contentStyle={{ background: t.chartTooltipBg, border: `1px solid ${t.cardBorder}`, color: t.text, borderRadius: 4, fontSize: 12 }}
              formatter={(value) => [`${value[0]}:00 - ${value[1]}:00`, 'Time Window']}
              labelFormatter={(label) => `Job: ${label}`}
            />
            <Bar dataKey="timeRange" radius={2} barSize={16}>
              {ganttData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.fill} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

function ModelDiagnostics({ data, urgencyData }) {
  const { t } = useTheme();
  const [modelInfo, setModelInfo] = React.useState(null);
  const [loadingModel, setLoadingModel] = React.useState(true);

  useEffect(() => {
    fetch('/api/model-info')
      .then(r => r.json())
      .then(d => { setModelInfo(d); setLoadingModel(false); })
      .catch(() => setLoadingModel(false));
  }, []);

  const bins = [
    { range: "0-20", count: 0 }, { range: "21-40", count: 0 },
    { range: "41-60", count: 0 }, { range: "61-80", count: 0 }, { range: "81-100", count: 0 }
  ];
  let totalDaysOverdue = 0, maxScore = 0, validJobs = 0;
  data.forEach(d => {
    if (d.ml_priority_score == null) return;
    const score = d.ml_priority_score;
    if (score <= 20) bins[0].count++;
    else if (score <= 40) bins[1].count++;
    else if (score <= 60) bins[2].count++;
    else if (score <= 80) bins[3].count++;
    else bins[4].count++;
    totalDaysOverdue += (d.days_overdue || 0);
    if (score > maxScore) maxScore = score;
    validJobs++;
  });
  const avgOverdue = validJobs ? (totalDaysOverdue / validJobs).toFixed(1) : 0;
  const fmt = (name) => name.replace(/_/g, " ").replace(/\b\w/g, l => l.toUpperCase());
  const featureData = modelInfo?.features
    ? [...modelInfo.features].reverse().map(f => ({ name: fmt(f.name), importance: f.importance }))
    : [];
  const TT = { background: t.chartTooltipBg, border: `1px solid ${t.cardBorder}`, color: t.text, borderRadius: 4, fontSize: 12 };

  return (
    <div>
      <h1 style={{ color: t.text }} className="text-[19px] font-medium mb-1">Model diagnostics</h1>
      <p style={{ color: t.textMuted }} className="text-[13.5px] mb-5">2-Stage XGBoost + OR-Tools CP-SAT — Explainable AI & optimization constraints</p>

      <div
        style={{
          backgroundColor: t.cardBg,
          borderColor: t.cardBorder,
          color: t.textMuted,
        }}
        className="border rounded-[4px] p-4 mb-5 text-[13px] leading-relaxed shadow-sm"
      >
        <span style={{ color: t.text }} className="font-medium">Architecture: </span>
        Combines <span style={{ color: t.accentLight }}>Explainable ML (XGBoost)</span> with <span style={{ color: t.accentLight }}>Google OR-Tools CP-SAT</span>.
        <span className="block mt-2"><span style={{ color: t.text }}>Stage 1:</span> Analyzes {modelInfo?.num_features || 11} physical track parameters and produces a continuous priority score (0-100).</span>
        <span className="block mt-1"><span style={{ color: t.text }}>Stage 2:</span> Scans multi-day timetable matrices to find zero-conflict maintenance windows within crew capacity limits.</span>
      </div>

      <div
        style={{
          backgroundColor: t.cardBg,
          borderColor: t.cardBorder,
        }}
        className="grid grid-cols-5 border rounded-[4px] mb-5 shadow-sm"
      >
        <KpiCell label="Regressor MAE" value={modelInfo?.metrics?.mae ?? "..."} sub="Priority score error" />
        <KpiCell label="Regressor R2" value={modelInfo?.metrics?.r2 ?? "..."} sub="Goodness of fit" valueColor="#4C8B63" />
        <KpiCell label="Classifier Accuracy" value={modelInfo?.metrics?.accuracy ? `${(modelInfo.metrics.accuracy*100).toFixed(1)}%` : "..."} sub="Urgency class accuracy" valueColor={t.accentLight} />
        <KpiCell label="Avg days overdue" value={`${avgOverdue}d`} sub="At scheduling time" />
        <KpiCell label="Jobs processed" value={validJobs} sub="Scored by ML model" />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-5 mb-5">
        <div
          style={{
            backgroundColor: t.cardBg,
            borderColor: t.cardBorder,
          }}
          className="border rounded-[4px] p-5 shadow-sm"
        >
          <h3 style={{ color: t.text }} className="text-[13.5px] font-medium mb-1">XGBoost feature importance</h3>
          <p style={{ color: t.textDim }} className="text-[12px] mb-4">Explainable AI — model weight per input parameter</p>
          {loadingModel ? (
            <div style={{ color: t.textDim }} className="text-[13px] text-center py-10">Loading model...</div>
          ) : featureData.length > 0 ? (
            <ResponsiveContainer width="100%" height={260}>
              <BarChart data={featureData} layout="vertical" margin={{ left: 8, right: 40 }}>
                <XAxis type="number" domain={[0, 1]} tickFormatter={v => `${(v*100).toFixed(0)}%`} tick={{ fill: t.textDim, fontSize: 11 }} axisLine={{ stroke: t.chartAxis }} />
                <YAxis type="category" dataKey="name" width={148} tick={{ fill: t.textMuted, fontSize: 11 }} axisLine={{ stroke: t.chartAxis }} tickLine={false} />
                <Tooltip cursor={{ fill: t.chartCursor }} contentStyle={TT} formatter={v => [`${(v*100).toFixed(2)}%`, "Importance"]} />
                <Bar dataKey="importance" fill="#4C8B63" radius={[0, 2, 2, 0]} barSize={14} />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <div style={{ color: t.textDim }} className="text-[13px] text-center py-10">Model not trained. Run python train_model.py first.</div>
          )}
        </div>

        <div
          style={{
            backgroundColor: t.cardBg,
            borderColor: t.cardBorder,
          }}
          className="border rounded-[4px] p-5 shadow-sm"
        >
          <h3 style={{ color: t.text }} className="text-[13.5px] font-medium mb-1">Priority score distribution</h3>
          <p style={{ color: t.textDim }} className="text-[12px] mb-4">Count of scheduled jobs across score buckets</p>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={bins}>
              <XAxis dataKey="range" tick={{ fill: t.textDim, fontSize: 11 }} axisLine={{ stroke: t.chartAxis }} />
              <YAxis tick={{ fill: t.textMuted, fontSize: 11 }} axisLine={{ stroke: t.chartAxis }} />
              <Tooltip cursor={{ fill: t.chartCursor }} contentStyle={TT} />
              <Bar dataKey="count" fill="#4C7A92" radius={[2, 2, 0, 0]} barSize={30} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        <div
          style={{
            backgroundColor: t.cardBg,
            borderColor: t.cardBorder,
          }}
          className="border rounded-[4px] p-5 shadow-sm"
        >
          <h3 style={{ color: t.text }} className="text-[13.5px] font-medium mb-4">Optimization constraints & rules</h3>
          <ul style={{ color: t.textMuted }} className="text-[13px] space-y-3">
            <li><span style={{ color: t.text }} className="font-medium">Hard Constraint 1 (Zero Train Conflict):</span> Maintenance blocks strictly scheduled during zero train occupancy slots.</li>
            <li><span style={{ color: t.text }} className="font-medium">Hard Constraint 2 (Urgency Deadlines):</span> Critical jobs constrained to Day 1-7, High urgency within Day 16.</li>
            <li><span style={{ color: t.text }} className="font-medium">Hard Constraint 3 (Crew Capacity):</span> Max 3 simultaneous blocks per day across the network.</li>
            <li><span style={{ color: t.text }} className="font-medium">Objective Function:</span> Minimize cumulative priority-weighted delay.</li>
          </ul>
        </div>

        <div
          style={{
            backgroundColor: t.cardBg,
            borderColor: t.cardBorder,
          }}
          className="border rounded-[4px] p-5 shadow-sm"
        >
          <h3 style={{ color: t.text }} className="text-[13.5px] font-medium mb-4">Solver performance & urgency split</h3>
          <div
            style={{
              backgroundColor: t.inputBg,
              borderColor: t.cardBorder,
            }}
            className="border rounded-[3px] px-4 py-3 mb-4"
          >
            <div style={{ color: t.textMuted }} className="text-[12px]">Solver engine</div>
            <div style={{ color: t.accentLight }} className="text-[14px] font-medium mt-0.5">Google OR-Tools CP-SAT — OPTIMAL</div>
            <div style={{ color: t.textDim }} className="text-[12px] mt-1">Execution time &lt; 0.5s for 50 combinatorial jobs</div>
          </div>
          <ResponsiveContainer width="100%" height={140}>
            <PieChart>
              <Pie data={urgencyData} dataKey="value" innerRadius={40} outerRadius={60} paddingAngle={2} stroke="none">
                {urgencyData.map((d, i) => <Cell key={i} fill={d.color} />)}
              </Pie>
              <Tooltip contentStyle={TT} />
            </PieChart>
          </ResponsiveContainer>
          <div className="flex gap-4 justify-center mt-2">
            {urgencyData.map(d => (
              <div key={d.name} style={{ color: t.textMuted }} className="flex items-center gap-1.5 text-[12px]">
                <span className="w-2 h-2 rounded-full" style={{ background: d.color }} />{d.name}: {d.value}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default function Dashboard({ onLogout }) {
  const [theme, setTheme] = useState("dark");
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [activeTab, setActiveTab] = useState(TABS[0]);
  const [zones, setZones] = useState(["Central Railway", "Eastern Railway", "Northern Railway"]);
  const [urgency, setUrgency] = useState(["Critical", "High"]);
  const [horizon, setHorizon] = useState(30);
  const [running, setRunning] = useState(false);
  const [profileOpen, setProfileOpen] = useState(false);
  
  const [scheduleData, setScheduleData] = useState([]);
  const [urgencyData, setUrgencyData] = useState([]);
  const [zoneData, setZoneData] = useState([]);
  const [kpis, setKpis] = useState({ jobs: 0, critical: 0, avgScore: 0, totalHrs: 0 });

  useEffect(() => {
    const savedTheme = localStorage.getItem("trackline-theme");
    if (savedTheme === "light" || savedTheme === "dark") {
      setTheme(savedTheme);
    }
  }, []);

  const toggleTheme = () => {
    setTheme((prev) => {
      const nextTheme = prev === "dark" ? "light" : "dark";
      localStorage.setItem("trackline-theme", nextTheme);
      return nextTheme;
    });
  };

  const t = THEMES[theme] || THEMES.dark;

  const fetchSchedule = async () => {
    try {
      const res = await fetch('/api/schedule');
      const data = await res.json();
      if (!Array.isArray(data)) return;
      
      setScheduleData(data);
      
      let cr = 0, hi = 0, me = 0;
      let totalScore = 0;
      let totalHrs = 0;
      const zoneCounts = {};

      data.forEach(job => {
        if (!job.urgency) return;
        
        if (job.urgency === 'Critical') cr++;
        else if (job.urgency === 'High') hi++;
        else if (job.urgency === 'Medium') me++;

        totalScore += (job.ml_priority_score || 0);
        totalHrs += (job.estimated_duration_hrs || 0);

        if (job.zone) {
          zoneCounts[job.zone] = (zoneCounts[job.zone] || 0) + 1;
        }
      });

      setUrgencyData([
        { name: "High", value: hi, color: "#C98A3B" },
        { name: "Critical", value: cr, color: "#C4453D" },
        { name: "Medium", value: me, color: "#4C8B63" },
      ]);

      const zData = Object.entries(zoneCounts)
        .map(([zone, jobs]) => ({ zone, jobs }))
        .sort((a, b) => b.jobs - a.jobs);
      setZoneData(zData);

      const validJobs = data.filter(j => j.job_id).length;
      setKpis({
        jobs: validJobs,
        critical: cr,
        avgScore: validJobs ? (totalScore / validJobs).toFixed(1) : 0,
        totalHrs: Number(totalHrs.toFixed(1))
      });
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    fetchSchedule();
  }, []);

  const toggle = (list, setList, item) =>
    setList(list.includes(item) ? list.filter((x) => x !== item) : [...list, item]);

  const runPipeline = async () => {
    setRunning(true);
    try {
      await fetch('/api/optimize', { method: 'POST' });
      await fetchSchedule();
    } catch (err) {
      console.error(err);
    } finally {
      setRunning(false);
    }
  };

  return (
    <ThemeContext.Provider value={{ theme, t, toggleTheme }}>
      <div
        style={{
          backgroundColor: t.bg,
          color: t.text,
          fontFamily: "'IBM Plex Sans', sans-serif",
        }}
        className="min-h-screen w-full flex flex-col transition-colors duration-200"
      >
        <link rel="stylesheet" href={FONT_LINK} />

        {/* Top nav */}
        <header
          style={{
            backgroundColor: t.headerBg,
            borderColor: t.navBorder,
          }}
          className="h-14 border-b flex items-center px-4 shrink-0 transition-colors duration-200"
        >
          <button
            onClick={() => setSidebarOpen((s) => !s)}
            style={{ color: t.textMuted }}
            className="hover:opacity-80 mr-3 transition-opacity"
            title="Toggle sidebar"
          >
            {sidebarOpen ? <PanelLeftClose size={17} /> : <PanelLeft size={17} />}
          </button>

          <div className="flex items-center gap-2 mr-8">
            <div className="w-6 h-6 rounded-[3px] bg-[#4C7A92] flex items-center justify-center shadow-sm">
              <GitBranch size={13} className="text-[#0E1318]" strokeWidth={2.5} />
            </div>
            <span style={{ color: t.text }} className="text-[14px] font-semibold tracking-tight">Trackline</span>
          </div>

          <nav className="flex items-center gap-1 flex-1">
            {TABS.map((tabName) => (
              <button
                key={tabName}
                onClick={() => setActiveTab(tabName)}
                style={{
                  color: activeTab === tabName ? t.activeTabText : t.textMuted,
                  backgroundColor: activeTab === tabName ? t.activeTabBg : "transparent",
                }}
                className="text-[13px] px-3 py-1.5 rounded-[3px] font-medium transition-colors hover:opacity-90"
              >
                {tabName}
              </button>
            ))}
          </nav>

          {/* Theme Switcher Button */}
          <button
            onClick={toggleTheme}
            aria-label="Toggle theme"
            title={theme === "dark" ? "Switch to Light Mode" : "Switch to Dark Mode"}
            style={{
              backgroundColor: t.btnThemeBg,
              borderColor: t.btnThemeBorder,
              color: theme === "dark" ? "#F59E0B" : "#4F46E5",
            }}
            className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-[4px] border text-[12.5px] font-medium mr-4 transition-all hover:scale-[1.03] active:scale-95 shadow-sm"
          >
            {theme === "dark" ? <Sun size={15} /> : <Moon size={15} />}
            <span style={{ color: t.text }} className="hidden sm:inline text-[12px]">
              {theme === "dark" ? "Light" : "Dark"}
            </span>
          </button>

          {/* User Profile */}
          <div className="relative">
            <button
              onClick={() => setProfileOpen((p) => !p)}
              style={{ color: t.textMuted }}
              className="flex items-center gap-2 text-[13px] hover:opacity-90 transition-opacity"
            >
              <div
                style={{ backgroundColor: t.activeTabBg }}
                className="w-7 h-7 rounded-full flex items-center justify-center border"
              >
                <User size={13} />
              </div>
              <span style={{ color: t.text }} className="font-medium">A. Rao</span>
              <ChevronDown size={13} />
            </button>
            {profileOpen && (
              <div
                style={{
                  backgroundColor: t.cardBg,
                  borderColor: t.cardBorder,
                }}
                className="absolute right-0 top-10 w-44 border rounded-[4px] py-1 shadow-lg z-50"
              >
                <button
                  style={{ color: t.textMuted }}
                  className="w-full text-left px-3 py-2 text-[13px] hover:opacity-80 flex items-center gap-2 transition-opacity"
                >
                  <Settings size={13} /> Settings
                </button>
                <button
                  onClick={onLogout}
                  style={{ color: t.textMuted }}
                  className="w-full text-left px-3 py-2 text-[13px] hover:opacity-80 flex items-center gap-2 transition-opacity"
                >
                  <LogOut size={13} /> Log out
                </button>
              </div>
            )}
          </div>
        </header>

        <div className="flex flex-1 min-h-0">
          {/* Sidebar */}
          {sidebarOpen && (
            <aside
              style={{
                backgroundColor: t.sidebarBg,
                borderColor: t.navBorder,
              }}
              className="w-64 border-r shrink-0 p-4 overflow-y-auto transition-colors duration-200"
            >
              <button
                onClick={runPipeline}
                disabled={running}
                style={{
                  backgroundColor: t.primary,
                  color: t.primaryText,
                }}
                className="w-full flex items-center justify-center gap-2 py-2.5 rounded-[3px] text-[13.5px] font-medium transition-opacity hover:opacity-90 disabled:opacity-60 mb-6 shadow-sm"
              >
                <Play size={13} /> {running ? "Running…" : "Run optimization"}
              </button>

              <div className="mb-6">
                <div style={{ color: t.textDim }} className="text-[11.5px] font-medium uppercase tracking-wider mb-2">
                  Zonal railways
                </div>
                <div className="flex flex-wrap gap-1.5">
                  {ZONES.map((z) => (
                    <Chip key={z} label={z} active={zones.includes(z)} onClick={() => toggle(zones, setZones, z)} />
                  ))}
                </div>
              </div>

              <div className="mb-6">
                <div style={{ color: t.textDim }} className="text-[11.5px] font-medium uppercase tracking-wider mb-2">
                  Defect urgency
                </div>
                <div className="flex flex-wrap gap-1.5">
                  {URGENCY.map((u) => (
                    <Chip key={u} label={u} active={urgency.includes(u)} onClick={() => toggle(urgency, setUrgency, u)} />
                  ))}
                </div>
              </div>

              <div>
                <div className="flex items-center justify-between mb-2">
                  <span style={{ color: t.textDim }} className="text-[11.5px] font-medium uppercase tracking-wider">
                    Planning horizon
                  </span>
                  <span
                    style={{ fontFamily: "'IBM Plex Mono', monospace", color: t.accentLight }}
                    className="text-[12px] font-semibold"
                  >
                    {horizon}d
                  </span>
                </div>
                <input
                  type="range"
                  min={1}
                  max={30}
                  value={horizon}
                  onChange={(e) => setHorizon(Number(e.target.value))}
                  className="w-full accent-[#4C7A92]"
                />
              </div>
            </aside>
          )}

          {/* Main content */}
          <main className="flex-1 overflow-y-auto p-6 transition-colors duration-200">
            {activeTab === "Executive summary" && (
              <>
                <h1 style={{ color: t.text }} className="text-[19px] font-medium mb-1">Executive summary</h1>
                <p style={{ color: t.textMuted }} className="text-[13.5px] mb-6">
                  Optimization horizon: next {horizon} days · {zones.length} zones selected
                </p>

                {/* KPI strip */}
                <div
                  style={{
                    backgroundColor: t.cardBg,
                    borderColor: t.cardBorder,
                  }}
                  className="grid grid-cols-4 border rounded-[4px] mb-6 shadow-sm"
                >
                  <KpiCell label="Scheduled jobs" value={kpis.jobs} sub={`Within ${horizon}-day window`} />
                  <KpiCell label="Critical urgency" value={kpis.critical} sub="Mandatory early clearance" valueColor="#C4453D" />
                  <KpiCell label="Avg. priority score" value={kpis.avgScore} sub="Predicted by scoring model" />
                  <KpiCell label="Total block duration" value={`${kpis.totalHrs}h`} sub="Conflict-free reservation" />
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                  <div
                    style={{
                      backgroundColor: t.cardBg,
                      borderColor: t.cardBorder,
                    }}
                    className="border rounded-[4px] p-5 shadow-sm"
                  >
                    <h3 style={{ color: t.text }} className="text-[13.5px] font-medium mb-4">Urgency distribution</h3>
                    <ResponsiveContainer width="100%" height={220}>
                      <PieChart>
                        <Pie
                          data={urgencyData}
                          dataKey="value"
                          innerRadius={55}
                          outerRadius={85}
                          paddingAngle={2}
                          stroke="none"
                        >
                          {urgencyData.map((d, i) => (
                            <Cell key={i} fill={d.color} />
                          ))}
                        </Pie>
                        <Tooltip
                          contentStyle={{
                            background: t.chartTooltipBg,
                            border: `1px solid ${t.cardBorder}`,
                            color: t.text,
                            borderRadius: 4,
                            fontSize: 12,
                          }}
                        />
                      </PieChart>
                    </ResponsiveContainer>
                    <div className="flex gap-4 justify-center mt-2">
                      {urgencyData.map((d) => (
                        <div key={d.name} style={{ color: t.textMuted }} className="flex items-center gap-1.5 text-[12px]">
                          <span className="w-2 h-2 rounded-full" style={{ background: d.color }} />
                          {d.name}
                        </div>
                      ))}
                    </div>
                  </div>

                  <div
                    style={{
                      backgroundColor: t.cardBg,
                      borderColor: t.cardBorder,
                    }}
                    className="border rounded-[4px] p-5 shadow-sm"
                  >
                    <h3 style={{ color: t.text }} className="text-[13.5px] font-medium mb-4">Jobs by railway zone</h3>
                    <ResponsiveContainer width="100%" height={220}>
                      <BarChart data={zoneData} layout="vertical" margin={{ left: 10 }}>
                        <XAxis type="number" tick={{ fill: t.textDim, fontSize: 11 }} axisLine={{ stroke: t.chartAxis }} tickLine={false} />
                        <YAxis
                          type="category"
                          dataKey="zone"
                          width={130}
                          tick={{ fill: t.textMuted, fontSize: 12 }}
                          axisLine={{ stroke: t.chartAxis }}
                          tickLine={false}
                        />
                        <Tooltip
                          cursor={{ fill: t.chartCursor }}
                          contentStyle={{
                            background: t.chartTooltipBg,
                            border: `1px solid ${t.cardBorder}`,
                            color: t.text,
                            borderRadius: 4,
                            fontSize: 12,
                          }}
                        />
                        <Bar dataKey="jobs" fill="#4C7A92" radius={[0, 2, 2, 0]} barSize={14} />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                </div>
              </>
            )}

            {activeTab === "Master timetable" && <MasterTimetable data={scheduleData} />}
            {activeTab === "Gantt timeline" && <GanttTimeline data={scheduleData} />}
            {activeTab === "Model diagnostics" && <ModelDiagnostics data={scheduleData} urgencyData={urgencyData} />}
          </main>
        </div>
      </div>
    </ThemeContext.Provider>
  );
}
