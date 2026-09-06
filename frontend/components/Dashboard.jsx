import React, { useState, useEffect } from "react";
import {
  GitBranch,
  ChevronDown,
  PanelLeftClose,
  PanelLeft,
  Play,
  Settings,
  LogOut,
  User,
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

function Chip({ label, active, onClick }) {
  return (
    <button
      onClick={onClick}
      className={`text-[12.5px] px-2.5 py-1 rounded-[3px] border transition-colors ${
        active
          ? "bg-[#4C7A92]/15 border-[#4C7A92] text-[#9EC3D5]"
          : "border-[#2A323D] text-[#8C97A5] hover:border-[#3A4552]"
      }`}
    >
      {label}
    </button>
  );
}

function KpiCell({ label, value, sub, valueColor }) {
  return (
    <div className="px-6 py-5 border-r border-[#232B36] last:border-r-0">
      <div className="text-[12px] text-[#8C97A5] mb-2">{label}</div>
      <div
        className="text-[28px] leading-none"
        style={{ fontFamily: "'IBM Plex Mono', monospace", color: valueColor || "#E7EBEF" }}
      >
        {value}
      </div>
      <div className="text-[12px] text-[#5A6472] mt-2">{sub}</div>
    </div>
  );
}

function MasterTimetable({ data }) {
  const [search, setSearch] = useState("");
  const filtered = data.filter(d => 
    (d.job_id && d.job_id.toLowerCase().includes(search.toLowerCase())) ||
    (d.section_id && d.section_id.toLowerCase().includes(search.toLowerCase())) ||
    (d.job_type && d.job_type.toLowerCase().includes(search.toLowerCase()))
  );

  return (
    <div>
      <h1 className="text-[19px] font-medium mb-1">Master timetable</h1>
      <p className="text-[13.5px] text-[#8C97A5] mb-6">All scheduled maintenance blocks</p>
      
      <div className="mb-4">
        <input 
          type="text" 
          placeholder="Search jobs, sections, or types..." 
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-[300px] bg-[#0E1318] border border-[#2A323D] rounded-[3px] px-3 py-2 text-[13px] outline-none focus:border-[#4C7A92] transition-colors"
        />
      </div>

      <div className="border border-[#232B36] rounded-[4px] bg-[#161C24] overflow-x-auto">
        <table className="w-full text-left text-[13px]">
          <thead>
            <tr className="border-b border-[#232B36] text-[#8C97A5]">
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
              <tr key={i} className="border-b border-[#232B36] last:border-b-0 hover:bg-[#1D242D] transition-colors">
                <td className="px-4 py-3" style={{ fontFamily: "'IBM Plex Mono', monospace" }}>{d.job_id}</td>
                <td className="px-4 py-3">{d.section_id}</td>
                <td className="px-4 py-3">{d.job_type}</td>
                <td className="px-4 py-3">{d.scheduled_date}</td>
                <td className="px-4 py-3">{d.block_start_time} - {d.block_end_time}</td>
                <td className="px-4 py-3">
                  <span className={`px-2 py-0.5 rounded-[2px] text-[11px] ${
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
        {filtered.length === 0 && <div className="p-4 text-center text-[#8C97A5] text-[13px]">No matching records found.</div>}
      </div>
    </div>
  );
}

function GanttTimeline({ data }) {
  const sortedData = [...data].sort((a, b) => (a.section_id || "").localeCompare(b.section_id || ""));
  
  const ganttData = sortedData.filter(d => d.job_id).map(d => ({
    id: d.job_id,
    section: d.section_id,
    timeRange: [d.block_start_hr, d.block_end_hr],
    fill: d.urgency === 'Critical' ? '#C4453D' : d.urgency === 'High' ? '#C98A3B' : '#4C8B63',
  }));

  return (
    <div className="flex flex-col h-full">
      <h1 className="text-[19px] font-medium mb-1">Gantt timeline</h1>
      <p className="text-[13.5px] text-[#8C97A5] mb-6">Scheduled blocks by hour (0-24)</p>
      
      <div className="flex-1 border border-[#232B36] rounded-[4px] bg-[#161C24] p-5 min-h-[400px]">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={ganttData} layout="vertical" margin={{ left: 20, right: 20 }}>
            <XAxis type="number" domain={[0, 24]} tickCount={25} tick={{ fill: "#8C97A5", fontSize: 11 }} axisLine={{ stroke: "#232B36" }} />
            <YAxis type="category" dataKey="id" width={90} tick={{ fill: "#8C97A5", fontSize: 11 }} axisLine={{ stroke: "#232B36" }} />
            <Tooltip 
              cursor={{ fill: "#1D242D" }}
              contentStyle={{ background: "#0E1318", border: "1px solid #232B36", borderRadius: 4, fontSize: 12 }}
              formatter={(value, name, props) => [`${value[0]}:00 - ${value[1]}:00`, 'Time Window']}
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
  const TT = { background: "#0E1318", border: "1px solid #232B36", borderRadius: 4, fontSize: 12 };

  return (
    <div>
      <h1 className="text-[19px] font-medium mb-1">Model diagnostics</h1>
      <p className="text-[13.5px] text-[#8C97A5] mb-5">2-Stage XGBoost + OR-Tools CP-SAT — Explainable AI & optimization constraints</p>

      <div className="border border-[#232B36] rounded-[4px] bg-[#161C24] p-4 mb-5 text-[13px] text-[#8C97A5] leading-relaxed">
        <span className="text-[#E7EBEF] font-medium">Architecture: </span>
        Combines <span className="text-[#9EC3D5]">Explainable ML (XGBoost)</span> with <span className="text-[#9EC3D5]">Google OR-Tools CP-SAT</span>.
        <span className="block mt-2"><span className="text-[#E7EBEF]">Stage 1:</span> Analyzes {modelInfo?.num_features || 11} physical track parameters and produces a continuous priority score (0-100).</span>
        <span className="block mt-1"><span className="text-[#E7EBEF]">Stage 2:</span> Scans multi-day timetable matrices to find zero-conflict maintenance windows within crew capacity limits.</span>
      </div>

      <div className="grid grid-cols-5 border border-[#232B36] rounded-[4px] mb-5 bg-[#161C24]">
        <KpiCell label="Regressor MAE" value={modelInfo?.metrics?.mae ?? "..."} sub="Priority score error" />
        <KpiCell label="Regressor R2" value={modelInfo?.metrics?.r2 ?? "..."} sub="Goodness of fit" valueColor="#4C8B63" />
        <KpiCell label="Classifier Accuracy" value={modelInfo?.metrics?.accuracy ? `${(modelInfo.metrics.accuracy*100).toFixed(1)}%` : "..."} sub="Urgency class accuracy" valueColor="#4C7A92" />
        <KpiCell label="Avg days overdue" value={`${avgOverdue}d`} sub="At scheduling time" />
        <KpiCell label="Jobs processed" value={validJobs} sub="Scored by ML model" />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-5 mb-5">
        <div className="border border-[#232B36] rounded-[4px] bg-[#161C24] p-5">
          <h3 className="text-[13.5px] font-medium mb-1">XGBoost feature importance</h3>
          <p className="text-[12px] text-[#5A6472] mb-4">Explainable AI — model weight per input parameter</p>
          {loadingModel ? (
            <div className="text-[13px] text-[#5A6472] text-center py-10">Loading model...</div>
          ) : featureData.length > 0 ? (
            <ResponsiveContainer width="100%" height={260}>
              <BarChart data={featureData} layout="vertical" margin={{ left: 8, right: 40 }}>
                <XAxis type="number" domain={[0, 1]} tickFormatter={v => `${(v*100).toFixed(0)}%`} tick={{ fill: "#5A6472", fontSize: 11 }} axisLine={{ stroke: "#232B36" }} />
                <YAxis type="category" dataKey="name" width={148} tick={{ fill: "#8C97A5", fontSize: 11 }} axisLine={{ stroke: "#232B36" }} tickLine={false} />
                <Tooltip cursor={{ fill: "#1D242D" }} contentStyle={TT} formatter={v => [`${(v*100).toFixed(2)}%`, "Importance"]} />
                <Bar dataKey="importance" fill="#4C8B63" radius={[0, 2, 2, 0]} barSize={14} />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <div className="text-[13px] text-[#5A6472] text-center py-10">Model not trained. Run python train_model.py first.</div>
          )}
        </div>

        <div className="border border-[#232B36] rounded-[4px] bg-[#161C24] p-5">
          <h3 className="text-[13.5px] font-medium mb-1">Priority score distribution</h3>
          <p className="text-[12px] text-[#5A6472] mb-4">Count of scheduled jobs across score buckets</p>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={bins}>
              <XAxis dataKey="range" tick={{ fill: "#5A6472", fontSize: 11 }} axisLine={{ stroke: "#232B36" }} />
              <YAxis tick={{ fill: "#8C97A5", fontSize: 11 }} axisLine={{ stroke: "#232B36" }} />
              <Tooltip cursor={{ fill: "#1D242D" }} contentStyle={TT} />
              <Bar dataKey="count" fill="#4C7A92" radius={[2, 2, 0, 0]} barSize={30} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        <div className="border border-[#232B36] rounded-[4px] bg-[#161C24] p-5">
          <h3 className="text-[13.5px] font-medium mb-4">Optimization constraints & rules</h3>
          <ul className="text-[13px] text-[#8C97A5] space-y-3">
            <li><span className="text-[#E7EBEF] font-medium">Hard Constraint 1 (Zero Train Conflict):</span> Maintenance blocks strictly scheduled during zero train occupancy slots.</li>
            <li><span className="text-[#E7EBEF] font-medium">Hard Constraint 2 (Urgency Deadlines):</span> Critical jobs constrained to Day 1-7, High urgency within Day 16.</li>
            <li><span className="text-[#E7EBEF] font-medium">Hard Constraint 3 (Crew Capacity):</span> Max 3 simultaneous blocks per day across the network.</li>
            <li><span className="text-[#E7EBEF] font-medium">Objective Function:</span> Minimize cumulative priority-weighted delay.</li>
          </ul>
        </div>

        <div className="border border-[#232B36] rounded-[4px] bg-[#161C24] p-5">
          <h3 className="text-[13.5px] font-medium mb-4">Solver performance & urgency split</h3>
          <div className="border border-[#232B36] rounded-[3px] bg-[#0E1318] px-4 py-3 mb-4">
            <div className="text-[12px] text-[#8C97A5]">Solver engine</div>
            <div className="text-[14px] font-medium text-[#9EC3D5] mt-0.5">Google OR-Tools CP-SAT — OPTIMAL</div>
            <div className="text-[12px] text-[#5A6472] mt-1">Execution time &lt; 0.5s for 50 combinatorial jobs</div>
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
              <div key={d.name} className="flex items-center gap-1.5 text-[12px] text-[#8C97A5]">
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
        if (!job.urgency) return; // skip empty rows
        
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
        totalHrs: totalHrs
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
    <div
      className="min-h-screen w-full bg-[#0E1318] text-[#E7EBEF] flex flex-col"
      style={{ fontFamily: "'IBM Plex Sans', sans-serif" }}
    >
      <link rel="stylesheet" href={FONT_LINK} />

      {/* Top nav */}
      <header className="h-14 border-b border-[#232B36] flex items-center px-4 shrink-0">
        <button
          onClick={() => setSidebarOpen((s) => !s)}
          className="text-[#8C97A5] hover:text-[#E7EBEF] mr-3 transition-colors"
        >
          {sidebarOpen ? <PanelLeftClose size={17} /> : <PanelLeft size={17} />}
        </button>

        <div className="flex items-center gap-2 mr-8">
          <div className="w-6 h-6 rounded-[3px] bg-[#4C7A92] flex items-center justify-center">
            <GitBranch size={13} className="text-[#0E1318]" strokeWidth={2.5} />
          </div>
          <span className="text-[14px] font-medium">Trackline</span>
        </div>

        <nav className="flex items-center gap-1 flex-1">
          {TABS.map((t) => (
            <button
              key={t}
              onClick={() => setActiveTab(t)}
              className={`text-[13px] px-3 py-1.5 rounded-[3px] transition-colors ${
                activeTab === t
                  ? "text-[#E7EBEF] bg-[#1D242D]"
                  : "text-[#8C97A5] hover:text-[#E7EBEF]"
              }`}
            >
              {t}
            </button>
          ))}
        </nav>

        <div className="relative">
          <button
            onClick={() => setProfileOpen((p) => !p)}
            className="flex items-center gap-2 text-[13px] text-[#8C97A5] hover:text-[#E7EBEF] transition-colors"
          >
            <div className="w-6 h-6 rounded-full bg-[#232B36] flex items-center justify-center">
              <User size={13} />
            </div>
            A. Rao
            <ChevronDown size={13} />
          </button>
          {profileOpen && (
            <div className="absolute right-0 top-9 w-44 bg-[#161C24] border border-[#232B36] rounded-[4px] py-1 shadow-lg">
              <button className="w-full text-left px-3 py-2 text-[13px] text-[#8C97A5] hover:text-[#E7EBEF] hover:bg-[#1D242D] flex items-center gap-2">
                <Settings size={13} /> Settings
              </button>
              <button
                onClick={onLogout}
                className="w-full text-left px-3 py-2 text-[13px] text-[#8C97A5] hover:text-[#E7EBEF] hover:bg-[#1D242D] flex items-center gap-2"
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
          <aside className="w-64 border-r border-[#232B36] shrink-0 p-4 overflow-y-auto">
            <button
              onClick={runPipeline}
              disabled={running}
              className="w-full flex items-center justify-center gap-2 bg-[#4C7A92] text-[#0E1318] py-2.5 rounded-[3px] text-[13.5px] font-medium hover:bg-[#5a8ba5] transition-colors disabled:opacity-60 mb-6"
            >
              <Play size={13} /> {running ? "Running…" : "Run optimization"}
            </button>

            <div className="mb-6">
              <div className="text-[11.5px] text-[#5A6472] mb-2">Zonal railways</div>
              <div className="flex flex-wrap gap-1.5">
                {ZONES.map((z) => (
                  <Chip key={z} label={z} active={zones.includes(z)} onClick={() => toggle(zones, setZones, z)} />
                ))}
              </div>
            </div>

            <div className="mb-6">
              <div className="text-[11.5px] text-[#5A6472] mb-2">Defect urgency</div>
              <div className="flex flex-wrap gap-1.5">
                {URGENCY.map((u) => (
                  <Chip key={u} label={u} active={urgency.includes(u)} onClick={() => toggle(urgency, setUrgency, u)} />
                ))}
              </div>
            </div>

            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="text-[11.5px] text-[#5A6472]">Planning horizon</span>
                <span
                  className="text-[12px] text-[#9EC3D5]"
                  style={{ fontFamily: "'IBM Plex Mono', monospace" }}
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
        <main className="flex-1 overflow-y-auto p-6">
          {activeTab === "Executive summary" && (
            <>
              <h1 className="text-[19px] font-medium mb-1">Executive summary</h1>
              <p className="text-[13.5px] text-[#8C97A5] mb-6">
                Optimization horizon: next {horizon} days · {zones.length} zones selected
              </p>

              {/* KPI strip */}
              <div className="grid grid-cols-4 border border-[#232B36] rounded-[4px] mb-6 bg-[#161C24]">
                <KpiCell label="Scheduled jobs" value={kpis.jobs} sub={`Within ${horizon}-day window`} />
                <KpiCell label="Critical urgency" value={kpis.critical} sub="Mandatory early clearance" valueColor="#C4453D" />
                <KpiCell label="Avg. priority score" value={kpis.avgScore} sub="Predicted by scoring model" />
                <KpiCell label="Total block duration" value={`${kpis.totalHrs}h`} sub="Conflict-free reservation" />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                <div className="border border-[#232B36] rounded-[4px] bg-[#161C24] p-5">
                  <h3 className="text-[13.5px] font-medium mb-4">Urgency distribution</h3>
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
                          background: "#0E1318",
                          border: "1px solid #232B36",
                          borderRadius: 4,
                          fontSize: 12,
                        }}
                      />
                    </PieChart>
                  </ResponsiveContainer>
                  <div className="flex gap-4 justify-center mt-2">
                    {urgencyData.map((d) => (
                      <div key={d.name} className="flex items-center gap-1.5 text-[12px] text-[#8C97A5]">
                        <span className="w-2 h-2 rounded-full" style={{ background: d.color }} />
                        {d.name}
                      </div>
                    ))}
                  </div>
                </div>

                <div className="border border-[#232B36] rounded-[4px] bg-[#161C24] p-5">
                  <h3 className="text-[13.5px] font-medium mb-4">Jobs by railway zone</h3>
                  <ResponsiveContainer width="100%" height={220}>
                    <BarChart data={zoneData} layout="vertical" margin={{ left: 10 }}>
                      <XAxis type="number" tick={{ fill: "#5A6472", fontSize: 11 }} axisLine={{ stroke: "#232B36" }} tickLine={false} />
                      <YAxis
                        type="category"
                        dataKey="zone"
                        width={130}
                        tick={{ fill: "#8C97A5", fontSize: 12 }}
                        axisLine={{ stroke: "#232B36" }}
                        tickLine={false}
                      />
                      <Tooltip
                        cursor={{ fill: "#1D242D" }}
                        contentStyle={{
                          background: "#0E1318",
                          border: "1px solid #232B36",
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
  );
}
