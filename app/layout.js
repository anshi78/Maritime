import { Inter } from "next/font/google";
import "./globals.css";
const inter = Inter({ subsets: ["latin"] });
export const metadata = {
title: "AquaBot - AI Powered Maritime Intelligence",
description:
"Harness the power of AI to optimize voyages, match cargo, and gain critical market insights.",
};
export default function RootLayout({ children }) {
return (
<html lang="en">
<body
className={`${inter.className} bg-gradient-to-br from-slate-900 via-blue-900 to-slate-800`}
style={{
background: `
 linear-gradient(135deg, #0f0f23 0%, #1a1a2e 25%, #16213e 50%, #1a1a2e 75%, #0f0f23 100%),
 radial-gradient(circle at 20% 80%, rgba(0, 212, 255, 0.1) 0%, transparent 50%),
 radial-gradient(circle at 80% 20%, rgba(135, 206, 250, 0.1) 0%, transparent 50%)
`,
minHeight: '100vh'
}}
>
{/* Animated background particles */}
<div
className="fixed inset-0 pointer-events-none opacity-30"
style={{
backgroundImage: `
 radial-gradient(circle at 25% 25%, rgba(255, 255, 255, 0.1) 1px, transparent 1px),
 radial-gradient(circle at 75% 75%, rgba(0, 212, 255, 0.1) 1px, transparent 1px)
`,
backgroundSize: '100px 100px, 150px 150px'
}}
></div>
{/* header (if you add later) */}
<main className="min-h-screen relative z-10">{children}</main>
{/* Minimized footer */}
<footer className="relative z-10 bg-black/70 backdrop-blur-sm border-t border-cyan-500/30 text-white py-4">
<div className="container mx-auto px-4">
<div className="flex flex-col sm:flex-row justify-between items-center space-y-2 sm:space-y-0">
{/* Left side - Company info */}
<div className="flex items-center space-x-2">
<div className="w-6 h-6 bg-gradient-to-r from-cyan-400 to-blue-500 rounded-lg flex items-center justify-center">
<svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
<path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
</svg>
</div>
<span className="font-bold bg-gradient-to-r from-cyan-400 to-blue-400 bg-clip-text text-transparent">
 AquaBot
</span>
<span className="text-white/50 text-sm">AI Maritime Intelligence</span>
</div>
{/* Right side - Made by team */}
<div className="flex items-center space-x-2">
<span className="text-white/60 text-sm">Made by</span>
<span className="bg-gradient-to-r from-cyan-400 to-blue-400 bg-clip-text text-transparent font-semibold">
 CodeItUp
</span>
<div className="flex space-x-1">
<div className="w-1.5 h-1.5 bg-cyan-400 rounded-full animate-pulse"></div>
<div className="w-1.5 h-1.5 bg-blue-400 rounded-full animate-pulse" style={{animationDelay: '0.2s'}}></div>
<div className="w-1.5 h-1.5 bg-purple-400 rounded-full animate-pulse" style={{animationDelay: '0.4s'}}></div>
</div>
</div>
</div>
</div>
</footer>
</body>
</html>
 );
}