"use client";
import { useRouter } from "next/navigation";
import AuthPage from "@/components/AuthPage";

export default function Login() {
  const router = useRouter();
  return <AuthPage initialMode="login" onBack={() => router.push("/")} onSuccess={() => router.push("/dashboard")} />;
}
