'use client';

import { useEffect } from 'react';
import Link from 'next/link';

export default function Hero() {
  useEffect(() => {
    // Create floating particles
    function createParticles() {
      const particlesContainer = document.getElementById('particles');
      if (!particlesContainer) return;
      
      // Clear existing particles
      particlesContainer.innerHTML = '';
      
      for (let i = 0; i < 50; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        
        const size = Math.random() * 4 + 2;
        particle.style.cssText = `
          position: absolute;
          width: ${size}px;
          height: ${size}px;
          left: ${Math.random() * 100}%;
          top: ${Math.random() * 100}%;
          background: ${i % 3 === 0 ? 'rgba(255, 255, 255, 0.9)' : i % 2 === 0 ? 'rgba(255, 215, 0, 0.8)' : 'rgba(135, 206, 250, 0.9)'};
          border-radius: 50%;
          animation: floatParticle ${Math.random() * 3 + 4}s ease-in-out infinite;
          animation-delay: ${Math.random() * 2}s;
        `;
        
        particlesContainer.appendChild(particle);
      }
    }

    // Create glitter effects
    function createGlitter() {
      const glitter = document.createElement('div');
      glitter.style.cssText = `
        position: fixed;
        width: 6px;
        height: 6px;
        background: linear-gradient(45deg, #fff, #ffd700);
        border-radius: 50%;
        pointer-events: none;
        z-index: 1000;
        left: ${Math.random() * 100}%;
        animation: glitterFall ${Math.random() * 2 + 2}s linear forwards;
      `;
      
      document.body.appendChild(glitter);
      
      setTimeout(() => {
        if (glitter.parentNode) {
          glitter.parentNode.removeChild(glitter);
        }
      }, 4000);
    }

    // Add interactive hover effects
    function handleMouseMove(e) {
      if (Math.random() < 0.1) {
        const sparkle = document.createElement('div');
        sparkle.style.cssText = `
          position: fixed;
          left: ${e.clientX}px;
          top: ${e.clientY}px;
          width: 4px;
          height: 4px;
          background: radial-gradient(circle, #fff, #ffd700);
          border-radius: 50%;
          pointer-events: none;
          z-index: 1001;
          animation: sparkleAnim 0.6s ease-out forwards;
        `;
        
        document.body.appendChild(sparkle);
        
        setTimeout(() => {
          if (sparkle.parentNode) {
            sparkle.parentNode.removeChild(sparkle);
          }
        }, 600);
      }
    }

    // Add CSS animations to head
    const style = document.createElement('style');
    style.textContent = `
      @keyframes floatParticle {
        0%, 100% {
          transform: translateY(0px) translateX(0px) rotate(0deg);
          opacity: 0;
        }
        10% { opacity: 1; }
        90% { opacity: 1; }
        50% {
          transform: translateY(-100px) translateX(50px) rotate(180deg);
        }
      }

      @keyframes glitterFall {
        0% {
          transform: translateY(-100px) rotate(0deg);
          opacity: 0;
        }
        10% { opacity: 1; }
        90% { opacity: 1; }
        100% {
          transform: translateY(100vh) rotate(360deg);
          opacity: 0;
        }
      }

      @keyframes sparkleAnim {
        0% { transform: scale(0) rotate(0deg); opacity: 1; }
        100% { transform: scale(1.5) rotate(180deg); opacity: 0; }
      }

      @keyframes gradientShift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
      }

      @keyframes fadeInUp {
        from {
          opacity: 0;
          transform: translateY(30px);
        }
        to {
          opacity: 1;
          transform: translateY(0);
        }
      }

      @keyframes slideInDown {
        from {
          opacity: 0;
          transform: translateY(-30px);
        }
        to {
          opacity: 1;
          transform: translateY(0);
        }
      }

      @keyframes floatShip {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
      }

      @keyframes wave {
        0%, 100% {
          transform: scaleX(1) scaleY(1);
          opacity: 0;
        }
        50% {
          transform: scaleX(1.5) scaleY(0.5);
          opacity: 1;
        }
      }

      .gradient-text {
        background: linear-gradient(45deg, #00d4ff, #0099ff, #00d4ff);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradientShift 3s ease-in-out infinite;
      }

      .fade-in-up {
        animation: fadeInUp 1s ease-out forwards;
      }

      .fade-in-up-delay-1 {
        animation: fadeInUp 1s ease-out 0.3s both;
      }

      .fade-in-up-delay-2 {
        animation: fadeInUp 1s ease-out 0.6s both;
      }

      .fade-in-up-delay-3 {
        animation: fadeInUp 1s ease-out 0.9s both;
      }

      .fade-in-up-delay-4 {
        animation: fadeInUp 1s ease-out 1.2s both;
      }

      .slide-in-down {
        animation: slideInDown 0.8s ease-out forwards;
      }

      .ship-float {
        animation: floatShip 4s ease-in-out infinite;
      }

      .wave-anim {
        animation: wave 2s ease-in-out infinite;
      }

      .wave-anim-delay {
        animation: wave 2s ease-in-out infinite;
        animation-delay: -1s;
        opacity: 0.7;
      }
    `;
    
    document.head.appendChild(style);

    // Initialize effects
    createParticles();
    
    // Create glitter every 300ms
    const glitterInterval = setInterval(createGlitter, 300);
    
    // Add mouse event listener
    document.addEventListener('mousemove', handleMouseMove);

    // Cleanup
    return () => {
      clearInterval(glitterInterval);
      document.removeEventListener('mousemove', handleMouseMove);
      if (style.parentNode) {
        style.parentNode.removeChild(style);
      }
    };
  }, []);

  return (
    <div className="min-h-screen w-full relative overflow-hidden" 
         style={{
           background: 'linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%)'
         }}>
      
      {/* Navigation Bar */}
      <nav className="absolute top-0 left-0 right-0 z-40 px-6 py-4 slide-in-down">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          {/* Logo */}
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-gradient-to-r from-cyan-400 to-blue-500 rounded-lg flex items-center justify-center">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
              </svg>
            </div>
            <span className="text-white text-xl font-bold gradient-text">AquaBot</span>
          </div>

         

          {/* Right side buttons */}
          <div className="flex items-center space-x-4">
            {/* Dashboard Link */}
            <a 
              href="/dashboard" 
             
            >
            
           
            </a>

            {/* Mobile menu button */}
            <button className="md:hidden text-white p-2">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>
      </nav>

      {/* Animated particles background */}
      <div id="particles" className="fixed inset-0 pointer-events-none z-10"></div>

      {/* Main content */}
      <div className="relative z-20 min-h-screen flex flex-col items-center justify-center px-5 pt-20">
        
        {/* Header */}
        <header className="text-center mb-12 fade-in-up">
          <h1 className="gradient-text font-black text-4xl md:text-6xl lg:text-7xl mb-5 leading-tight"
              style={{ textShadow: '0 0 30px rgba(0, 212, 255, 0.5)' }}>
            Maritime Logistics<br />
            Reinvented with AI
          </h1>
          
          <p className="text-white text-2xl md:text-4xl mb-8 fade-in-up-delay-1"
             style={{ textShadow: '0 2px 10px rgba(0, 0, 0, 0.3)' }}>
            Digital First Mate
          </p>
          
          <p className="text-white/90 text-lg md:text-xl max-w-4xl mx-auto leading-relaxed mb-10 fade-in-up-delay-2">
            The AI-powered Digital First Mate for modern maritime operations.
            Optimize voyages, match cargo, and get critical market insights with cutting-edge technology.
          </p>
          
          <Link
  href="/dashboard"
  className="inline-block bg-gradient-to-r from-red-400 via-red-500 to-red-400 text-white text-xl font-semibold px-10 py-5 rounded-full hover:shadow-2xl hover:-translate-y-1 transition-all duration-300 fade-in-up-delay-3 relative overflow-hidden group"
  style={{
    backgroundSize: '200% 200%',
    boxShadow: '0 10px 30px rgba(255, 107, 107, 0.4)'
  }}
>
  <span className="relative z-10">Get Started</span>
  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-500"></div>
</Link>
        </header>

        {/* Features Section */}
        <div className="mt-16 relative fade-in-up-delay-4 w-full max-w-6xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            
            {/* Feature 1: Smart Voyage Planning */}
            <div className="group bg-black/40 backdrop-blur-sm rounded-xl p-6 border border-cyan-500/30 hover:border-cyan-400/60 transition-all duration-300 hover:transform hover:-translate-y-2">
              <div className="flex items-center mb-4">
                <div className="w-12 h-12 bg-gradient-to-r from-cyan-400 to-blue-500 rounded-lg flex items-center justify-center mr-4">
                  <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
                  </svg>
                </div>
                <h3 className="text-white text-xl font-bold group-hover:text-cyan-400 transition-colors duration-300">
                  Smart Voyage Planning
                </h3>
              </div>
              <ul className="text-white/80 space-y-2 text-sm">
                <li className="flex items-start">
                  <span className="text-cyan-400 mr-2">•</span>
                  Optimal routes considering weather, currents, piracy zones
                </li>
                <li className="flex items-start">
                  <span className="text-cyan-400 mr-2">•</span>
                  Canal fees and fuel consumption optimization
                </li>
                <li className="flex items-start">
                  <span className="text-cyan-400 mr-2">•</span>
                  "What-if" scenarios for speed vs. efficiency
                </li>
              </ul>
            </div>

            {/* Feature 2: Cargo Matching */}
            <div className="group bg-black/40 backdrop-blur-sm rounded-xl p-6 border border-blue-500/30 hover:border-blue-400/60 transition-all duration-300 hover:transform hover:-translate-y-2">
              <div className="flex items-center mb-4">
                <div className="w-12 h-12 bg-gradient-to-r from-blue-400 to-purple-500 rounded-lg flex items-center justify-center mr-4">
                  <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
                  </svg>
                </div>
                <h3 className="text-white text-xl font-bold group-hover:text-blue-400 transition-colors duration-300">
                  Cargo Matching Assistant
                </h3>
              </div>
              <ul className="text-white/80 space-y-2 text-sm">
                <li className="flex items-start">
                  <span className="text-blue-400 mr-2">•</span>
                  Best cargo-ship pairings based on vessel specs
                </li>
                <li className="flex items-start">
                  <span className="text-blue-400 mr-2">•</span>
                  Profitability estimates for each match
                </li>
                <li className="flex items-start">
                  <span className="text-blue-400 mr-2">•</span>
                  Real-time tracking of vessels and cargoes
                </li>
              </ul>
            </div>

            {/* Feature 3: Market Insights */}
            <div className="group bg-black/40 backdrop-blur-sm rounded-xl p-6 border border-purple-500/30 hover:border-purple-400/60 transition-all duration-300 hover:transform hover:-translate-y-2">
              <div className="flex items-center mb-4">
                <div className="w-12 h-12 bg-gradient-to-r from-purple-400 to-pink-500 rounded-lg flex items-center justify-center mr-4">
                  <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 00-2-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v4a2 2 0 01-2 2H9z" />
                  </svg>
                </div>
                <h3 className="text-white text-xl font-bold group-hover:text-purple-400 transition-colors duration-300">
                  Market Intelligence
                </h3>
              </div>
              <ul className="text-white/80 space-y-2 text-sm">
                <li className="flex items-start">
                  <span className="text-purple-400 mr-2">•</span>
                  Market trend analysis and freight rates
                </li>
                <li className="flex items-start">
                  <span className="text-purple-400 mr-2">•</span>
                  Bunker price tracking and predictions
                </li>
                <li className="flex items-start">
                  <span className="text-purple-400 mr-2">•</span>
                  Benchmark voyages against market averages
                </li>
              </ul>
            </div>

            {/* Feature 4: Port Intelligence */}
            <div className="group bg-black/40 backdrop-blur-sm rounded-xl p-6 border border-green-500/30 hover:border-green-400/60 transition-all duration-300 hover:transform hover:-translate-y-2">
              <div className="flex items-center mb-4">
                <div className="w-12 h-12 bg-gradient-to-r from-green-400 to-teal-500 rounded-lg flex items-center justify-center mr-4">
                  <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                </div>
                <h3 className="text-white text-xl font-bold group-hover:text-green-400 transition-colors duration-300">
                  Port Intelligence
                </h3>
              </div>
              <ul className="text-white/80 space-y-2 text-sm">
                <li className="flex items-start">
                  <span className="text-green-400 mr-2">•</span>
                  Cheapest and fastest bunker ports en route
                </li>
                <li className="flex items-start">
                  <span className="text-green-400 mr-2">•</span>
                  Port efficiency and cost comparisons
                </li>
                <li className="flex items-start">
                  <span className="text-green-400 mr-2">•</span>
                  Real-time port availability updates
                </li>
              </ul>
            </div>

            {/* Feature 5: Automated PDA & Cost Management */}
            <div className="group bg-black/40 backdrop-blur-sm rounded-xl p-6 border border-orange-500/30 hover:border-orange-400/60 transition-all duration-300 hover:transform hover:-translate-y-2 md:col-span-2 lg:col-span-1">
              <div className="flex items-center mb-4">
                <div className="w-12 h-12 bg-gradient-to-r from-orange-400 to-red-500 rounded-lg flex items-center justify-center mr-4">
                  <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
                  </svg>
                </div>
                <h3 className="text-white text-xl font-bold group-hover:text-orange-400 transition-colors duration-300">
                  Cost Management
                </h3>
              </div>
              <ul className="text-white/80 space-y-2 text-sm">
                <li className="flex items-start">
                  <span className="text-orange-400 mr-2">•</span>
                  Auto-calculate PDA estimates and port charges
                </li>
                <li className="flex items-start">
                  <span className="text-orange-400 mr-2">•</span>
                  Canal fees and agency cost tracking
                </li>
                <li className="flex items-start">
                  <span className="text-orange-400 mr-2">•</span>
                  Actual vs. estimated cost analysis
                </li>
              </ul>
            </div>

          </div>
        </div>
        
      </div>
    </div>
  );
}