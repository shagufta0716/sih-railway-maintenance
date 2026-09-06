import React, { useState } from "react";
import { signIn } from "next-auth/react";
import { GitBranch, ArrowLeft } from "lucide-react";

const FONT_LINK =
  "https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap";

function Field({ label, type = "text", placeholder, value, onChange }) {
  return (
    <label className="block mb-4">
      <span className="block text-[12.5px] text-[#8C97A5] mb-1.5">{label}</span>
      <input
        type={type}
        placeholder={placeholder}
        value={value}
        onChange={onChange}
        className="w-full bg-[#0E1318] border border-[#2A323D] rounded-[3px] px-3 py-2.5 text-[14px] text-[#E7EBEF] placeholder-[#5A6472] outline-none focus:border-[#4C7A92] transition-colors"
      />
    </label>
  );
}


export default function AuthPage({ initialMode = "login", onBack, onSuccess }) {
  const [mode, setMode] = useState(initialMode); // 'login' | 'register'
  const [form, setForm] = useState({
    email: "",
    password: "",
    name: "",
  });
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const set = (k) => (e) => {
    setForm((f) => ({ ...f, [k]: e.target.value }));
    setError(null);
  };

  const handleSubmit = async () => {
    setLoading(true);
    setError(null);
    try {
      if (mode === "login") {
        const res = await signIn("credentials", {
          redirect: false,
          email: form.email,
          password: form.password,
        });
        if (res?.error) {
          setError("Invalid email or password");
        } else {
          onSuccess();
        }
      } else {
        const res = await fetch("/api/register", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(form),
        });
        if (!res.ok) {
          const data = await res.json();
          setError(data.error || "Registration failed");
        } else {
          onSuccess();
        }
      }
    } catch (err) {
      setError("An unexpected error occurred");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      className="min-h-screen w-full bg-[#0E1318] text-[#E7EBEF] flex flex-col"
      style={{ fontFamily: "'IBM Plex Sans', sans-serif" }}
    >
      <link rel="stylesheet" href={FONT_LINK} />

      <div className="max-w-6xl mx-auto w-full px-6 pt-6">
        <button
          onClick={onBack}
          className="flex items-center gap-1.5 text-[13px] text-[#8C97A5] hover:text-[#E7EBEF] transition-colors"
        >
          <ArrowLeft size={14} /> Back
        </button>
      </div>

      <div className="flex-1 flex items-center justify-center px-6">
        <div className="w-full max-w-[380px]">
          <div className="flex items-center gap-2.5 mb-8">
            <div className="w-7 h-7 rounded-[3px] bg-[#4C7A92] flex items-center justify-center">
              <GitBranch size={15} className="text-[#0E1318]" strokeWidth={2.5} />
            </div>
            <span className="text-[15px] font-medium tracking-tight">Trackline</span>
          </div>

          <h1 className="text-[22px] font-medium mb-1">
            {mode === "login" ? "Sign in" : "Request access"}
          </h1>
          <p className="text-[13.5px] text-[#8C97A5] mb-7">
            {mode === "login"
              ? "Use your division-issued employee credentials."
              : "New accounts are reviewed by your division admin before activation."}
          </p>

          <div className="border border-[#232B36] rounded-[4px] bg-[#161C24] p-6">
            {mode === "login" ? (
              <>
                <Field
                  label="Email"
                  placeholder="name@rail.gov.in"
                  value={form.email}
                  onChange={set("email")}
                />
                <Field
                  label="Password"
                  type="password"
                  placeholder="••••••••"
                  value={form.password}
                  onChange={set("password")}
                />
                {error && <div className="text-red-500 text-[12.5px] mb-4">{error}</div>}
                <div className="flex justify-end mb-5">
                  <button className="text-[12.5px] text-[#4C7A92] hover:underline">
                    Forgot password
                  </button>
                </div>
                <button
                  onClick={handleSubmit}
                  disabled={loading}
                  className="w-full bg-[#4C7A92] text-[#0E1318] py-2.5 rounded-[3px] text-[14px] font-medium hover:bg-[#5a8ba5] transition-colors disabled:opacity-50"
                >
                  {loading ? "Signing in..." : "Sign in"}
                </button>
              </>
            ) : (
              <>
                <Field label="Full name" placeholder="Ananya Rao" value={form.name} onChange={set("name")} />
                <Field label="Email" placeholder="name@rail.gov.in" value={form.email} onChange={set("email")} />
                <Field
                  label="Password"
                  type="password"
                  placeholder="Minimum 8 characters"
                  value={form.password}
                  onChange={set("password")}
                />
                {error && <div className="text-red-500 text-[12.5px] mb-4">{error}</div>}
                <button
                  onClick={handleSubmit}
                  disabled={loading}
                  className="w-full bg-[#4C7A92] text-[#0E1318] py-2.5 rounded-[3px] text-[14px] font-medium hover:bg-[#5a8ba5] transition-colors mt-1 disabled:opacity-50"
                >
                  {loading ? "Submitting..." : "Submit request"}
                </button>
              </>
            )}
          </div>

          <p className="text-center text-[13px] text-[#8C97A5] mt-5">
            {mode === "login" ? (
              <>No account yet?{" "}
                <button onClick={() => setMode("register")} className="text-[#4C7A92] hover:underline">
                  Request access
                </button>
              </>
            ) : (
              <>Already have credentials?{" "}
                <button onClick={() => setMode("login")} className="text-[#4C7A92] hover:underline">
                  Sign in
                </button>
              </>
            )}
          </p>
        </div>
      </div>
    </div>
  );
}
