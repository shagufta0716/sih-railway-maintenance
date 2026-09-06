"use client";
import { useRouter } from "next/navigation";
import AuthPage from "@/components/AuthPage";

export default function Register() {
  const router = useRouter();
  return <AuthPage initialMode="register" onBack={() => router.push("/")} onSuccess={() => router.push("/dashboard")} />;
}
