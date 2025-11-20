'use client';

import { ParticleBackground } from '@/components/ui/particle-background';
import { Navbar } from '@/components/layout/navbar';
import { Sidebar } from '@/components/layout/sidebar';
import { motion } from 'framer-motion';

export function AppShell({ children }: { children: React.ReactNode }) {
    return (
        <div className="min-h-screen bg-gradient-cosmic text-white overflow-hidden">
            {/* Ambient Background */}
            <ParticleBackground />

            {/* Mesh Gradients */}
            <div className="fixed top-0 left-0 w-[1000px] h-[1000px] bg-purple-500/10 rounded-full blur-[120px] -translate-x-1/2 -translate-y-1/2 pointer-events-none" />
            <div className="fixed bottom-0 right-0 w-[800px] h-[800px] bg-cyan-500/10 rounded-full blur-[100px] translate-x-1/3 translate-y-1/3 pointer-events-none" />

            {/* Navigation */}
            <Navbar />
            <Sidebar />

            {/* Main Content Area */}
            <main className="fixed top-28 left-[348px] right-6 bottom-6 overflow-y-auto custom-scrollbar rounded-2xl border border-white/5 bg-white/[0.02] backdrop-blur-sm shadow-glass p-8">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.2, duration: 0.5 }}
                >
                    {children}
                </motion.div>
            </main>
        </div>
    );
}
