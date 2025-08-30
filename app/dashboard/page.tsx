"use client";
import { useState, useEffect } from "react";
import { Anchor, Ship, MessageSquare, Brain, Waves, Navigation, TrendingUp, FileText, Mic, Bell, ArrowRight, Sparkles } from "lucide-react";

interface MousePosition {
  x: number;
  y: number;
}

interface FeatureItem {
  icon: any;
  text: string;
}

interface Feature {
  id: string;
  title: string;
  subtitle: string;
  description: string;
  icon: any;
  gradient: string;
  features: FeatureItem[];
}

export default function DashboardPage() {
  const [activeCard, setActiveCard] = useState<string | null>(null);
  const [mousePosition, setMousePosition] = useState<MousePosition>({ x: 0, y: 0 });

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      setMousePosition({ x: e.clientX, y: e.clientY });
    };
    window.addEventListener("mousemove", handleMouseMove);
    return () => window.removeEventListener("mousemove", handleMouseMove);
  }, []);

  const features: Feature[] = [
    {
      id: "general",
      title: "General Chatbot",
      subtitle: "Conversational Maritime Assistant",
      description: "Ask questions about laytime, weather, distances, CP clauses, or upload documents for AI-assisted summaries. Perfect for conversational queries and proactive alerts.",
      icon: MessageSquare,
      gradient: "from-blue-600 via-blue-700 to-indigo-800",
      features: [
        { icon: Waves, text: "Answer laytime & voyage queries" },
        { icon: FileText, text: "Document summarization" },
        { icon: Mic, text: "Voice or chat interaction" },
        { icon: Bell, text: "Real-time alerts on weather & market" },
      ],
    },
    {
      id: "agentic",
      title: "Special Agentic Chatbot",
      subtitle: "AI Agent for Smart Planning",
      description: "AI agent for smart voyage planning, cargo-tonnage matching, and cost optimization. Generates actionable insights and detailed reports automatically.",
      icon: Brain,
      gradient: "from-emerald-600 via-teal-700 to-cyan-800",
      features: [
        { icon: Navigation, text: "Optimal route planning & fuel cost analysis" },
        { icon: Ship, text: "Cargo-ship pairing suggestions with profitability estimates" },
        { icon: TrendingUp, text: "Port intelligence & PDA cost management" },
        { icon: Sparkles, text: "Decision support with trade-offs & TCE ranking" },
      ],
    },
  ];

  const handleCardClick = (featureId: string) => {
    if (featureId === "general") window.location.href = "/general";
    if (featureId === "agentic") window.location.href = "/special";
  };

  return (
    <div 
      className="min-h-screen relative overflow-hidden"
      style={{
        background: `
          linear-gradient(135deg, #0f0f23 0%, #1a1a2e 25%, #16213e 50%, #1a1a2e 75%, #0f0f23 100%),
          radial-gradient(circle at 20% 80%, rgba(0, 212, 255, 0.1) 0%, transparent 50%),
          radial-gradient(circle at 80% 20%, rgba(135, 206, 250, 0.1) 0%, transparent 50%)
        `
      }}
    >
      {/* Animated background particles - matching layout.js */}
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

      {/* Cursor Glow */}
      <div
        className="absolute w-96 h-96 bg-blue-500/10 rounded-full blur-3xl pointer-events-none transition-all duration-300 ease-out"
        style={{ left: mousePosition.x - 192, top: mousePosition.y - 192 }}
      ></div>

      <main className="relative z-10 min-h-screen flex flex-col items-center py-12 px-4">
        {/* Header */}
        <header className="w-full max-w-7xl flex flex-col items-center mb-16">
          <div className="relative group">
            <div className="absolute -inset-4 bg-gradient-to-r from-blue-400 via-cyan-400 to-blue-400 rounded-full opacity-30 group-hover:opacity-50 blur-xl transition-all duration-500"></div>
            <div className="relative flex items-center space-x-6 bg-white/10 backdrop-blur-lg rounded-2xl px-8 py-4 border border-white/20">
              <div className="relative">
                <div className="w-16 h-16 bg-gradient-to-br from-blue-400 to-cyan-400 rounded-xl flex items-center justify-center">
                  <Anchor className="w-8 h-8 text-white" />
                </div>
              </div>
              <div>
                <h1 className="text-5xl font-black text-white bg-gradient-to-r from-blue-200 to-cyan-200 bg-clip-text text-transparent">
                  AquaBot
                </h1>
                <div className="flex items-center space-x-2 mt-1">
                  <span className="text-blue-200 text-sm font-medium">AI Maritime Intelligence • Online</span>
                </div>
              </div>
            </div>
          </div>
          <div className="mt-8 text-center max-w-4xl">
            <p className="text-xl text-blue-100/90 leading-relaxed">
              Next-generation maritime intelligence platform powered by advanced AI.{" "}
              <span className="text-cyan-300 font-semibold">Plan smarter voyages</span>,{" "}
              <span className="text-blue-300 font-semibold">optimize operations</span>, and{" "}
              <span className="text-indigo-300 font-semibold">maximize profitability</span>.
            </p>
          </div>
        </header>

        {/* Feature Cards */}
        <section className="w-full max-w-7xl flex flex-col lg:flex-row gap-8 lg:gap-12">
          {features.map((feature) => {
            const Icon = feature.icon;
            return (
              <div
                key={feature.id}
                className="group relative cursor-pointer"
                onClick={() => handleCardClick(feature.id)}
                onMouseEnter={() => setActiveCard(feature.id)}
                onMouseLeave={() => setActiveCard(null)}
              >
                <div
                  className={`absolute -inset-1 bg-gradient-to-r ${feature.gradient} rounded-3xl blur-xl opacity-0 group-hover:opacity-60 transition-all duration-500`}
                ></div>
                <div className="relative bg-white/5 backdrop-blur-2xl rounded-3xl border border-white/10 overflow-hidden transition-all duration-500 group-hover:bg-white/10 group-hover:border-white/20 group-hover:scale-[1.02] group-hover:shadow-2xl">
                  <div className={`relative bg-gradient-to-r ${feature.gradient} p-8`}>
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center space-x-4 mb-3">
                          <div className="w-12 h-12 bg-white/20 backdrop-blur-sm rounded-xl flex items-center justify-center">
                            <Icon className="w-6 h-6 text-white" />
                          </div>
                          <div>
                            <h2 className="text-2xl font-bold text-white">{feature.title}</h2>
                            <p className="text-white/80 text-sm font-medium">{feature.subtitle}</p>
                          </div>
                        </div>
                        <p className="text-white/90 leading-relaxed">{feature.description}</p>
                      </div>
                      <ArrowRight className="w-6 h-6 text-white/60 group-hover:text-white group-hover:translate-x-1 transition-all duration-300" />
                    </div>
                  </div>
                  <div className="p-8">
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                      {feature.features.map((item, index) => {
                        const FeatureIcon = item.icon;
                        return (
                          <div
                            key={index}
                            className="flex items-center space-x-3 p-3 rounded-xl bg-white/5 border border-white/10 transition-all duration-300"
                          >
                            <div
                              className={`w-8 h-8 bg-gradient-to-r ${feature.gradient} rounded-lg flex items-center justify-center flex-shrink-0`}
                            >
                              <FeatureIcon className="w-4 h-4 text-white" />
                            </div>
                            <span className="text-white/90 font-medium text-sm">{item.text}</span>
                          </div>
                        );
                      })}
                    </div>
                    <div className="mt-8">
                      <button
                        className={`w-full bg-gradient-to-r ${feature.gradient} text-white font-semibold py-4 px-6 rounded-xl hover:shadow-lg transform hover:scale-[1.02] transition-all duration-300 flex items-center justify-center space-x-2`}
                      >
                        <span>Launch {feature.title}</span>
                        <ArrowRight className="w-4 h-4 transition-transform duration-300" />
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </section>
      </main>
    </div>
  );
}