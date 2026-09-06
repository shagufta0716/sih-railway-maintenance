"use client";
import { useRouter } from "next/navigation";
import { signOut } from "next-auth/react";
import Dashboard from "@/components/Dashboard";

export default function DashboardRoute() {
  const router = useRouter();
  
  const handleLogout = async () => {
    await signOut({ redirect: false });
    router.push("/");
  };
  
  return <Dashboard onLogout={handleLogout} />;
}
