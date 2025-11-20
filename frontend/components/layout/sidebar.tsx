'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    LayoutDashboard, CheckSquare, Folder, Calendar,
    BarChart2, Archive, Plus, ChevronLeft, Settings,
    Zap
} from 'lucide-react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cn } from '@/lib/utils';

const menuItems = [
    { icon: LayoutDashboard, label: 'Dashboard', href: '/dashboard', color: 'text-cyan-400' },
    { icon: CheckSquare, label: 'My Tasks', href: '/tasks', color: 'text-purple-400' },
    { icon: Folder, label: 'Projects', href: '/projects', color: 'text-pink-400' },
    { icon: Calendar, label: 'Calendar', href: '/calendar', color: 'text-orange-400' },
    { icon: BarChart2, label: 'Analytics', href: '/analytics', color: 'text-green-400' },
    { icon: Archive, label: 'Archive', href: '/archive', color: 'text-gray-400' },
];

const projects = [
    { name: 'Website Redesign', color: 'bg-purple-500', count: 12 },
    { name: 'Mobile App', color: 'bg-cyan-500', count: 8 },
    { name: 'Marketing Q4', color: 'bg-orange-500', count: 5 },
];

export function Sidebar() {
    const [isCollapsed, setIsCollapsed] = useState(false);
    const pathname = usePathname();

    return (
        <motion.aside
            initial={{ x: -100, opacity: 0 }}
            animate={{
                x: 0,
                opacity: 1,
                width: isCollapsed ? 80 : 300
            }}
            transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
            className="fixed left-6 top-28 bottom-6 z-40"
        >
            <div className="h-full rounded-2xl backdrop-blur-xl bg-cosmic-navy/60 border border-white/10 shadow-glass flex flex-col overflow-hidden transition-all duration-300">

                {/* Quick Actions */}
                <div className="p-4 space-y-3">
                    <motion.button
                        whileHover={{ scale: 1.02, y: -2 }}
                        whileTap={{ scale: 0.98 }}
                        className={cn(
                            "w-full h-12 rounded-xl bg-gradient-primary flex items-center justify-center shadow-lg group relative overflow-hidden",
                            isCollapsed && "w-12 h-12 p-0"
                        )}
                    >
                        <div className="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform duration-300" />
                        <Plus className={cn("w-5 h-5 text-white transition-transform duration-300 group-hover:rotate-90", !isCollapsed && "mr-2")} />
                        {!isCollapsed && <span className="font-semibold text-white">New Task</span>}
                    </motion.button>
                </div>

                {/* Navigation */}
                <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto custom-scrollbar">
                    {menuItems.map((item) => {
                        const isActive = pathname === item.href;
                        return (
                            <Link key={item.href} href={item.href}>
                                <motion.div
                                    whileHover={{ x: 4 }}
                                    className={cn(
                                        "relative flex items-center px-3 py-3 rounded-xl transition-all duration-200 group",
                                        isActive ? "bg-white/10 text-white" : "text-white/60 hover:bg-white/5 hover:text-white"
                                    )}
                                >
                                    {isActive && (
                                        <motion.div
                                            layoutId="active-nav"
                                            className="absolute left-0 w-1 h-6 bg-gradient-to-b from-cyan-400 to-purple-500 rounded-r-full"
                                        />
                                    )}
                                    <item.icon className={cn("w-5 h-5 transition-colors", isCollapsed ? "mx-auto" : "mr-3", isActive ? item.color : "group-hover:text-white")} />
                                    {!isCollapsed && (
                                        <span className="font-medium">{item.label}</span>
                                    )}
                                </motion.div>
                            </Link>
                        );
                    })}

                    {/* Projects Section */}
                    {!isCollapsed && (
                        <div className="mt-8 px-3">
                            <div className="text-xs font-bold text-white/30 uppercase tracking-widest mb-4">Projects</div>
                            <div className="space-y-1">
                                {projects.map((project) => (
                                    <motion.div
                                        key={project.name}
                                        whileHover={{ x: 4 }}
                                        className="flex items-center justify-between px-3 py-2.5 rounded-lg text-white/60 hover:text-white hover:bg-white/5 cursor-pointer group"
                                    >
                                        <div className="flex items-center">
                                            <div className={cn("w-2 h-8 rounded-full mr-3 opacity-50 group-hover:opacity-100 transition-opacity", project.color)} />
                                            <span className="text-sm font-medium truncate max-w-[140px]">{project.name}</span>
                                        </div>
                                        <span className="text-xs bg-white/5 px-2 py-0.5 rounded-full text-white/30 group-hover:text-white/60 transition-colors">
                                            {project.count}
                                        </span>
                                    </motion.div>
                                ))}
                            </div>
                        </div>
                    )}
                </nav>

                {/* Footer */}
                <div className="p-4 border-t border-white/5 bg-black/20">
                    {!isCollapsed ? (
                        <div className="space-y-4">
                            {/* Storage Indicator */}
                            <div>
                                <div className="flex justify-between text-xs text-white/40 mb-1">
                                    <span>Storage</span>
                                    <span>4.2 / 10 GB</span>
                                </div>
                                <div className="h-1.5 bg-white/10 rounded-full overflow-hidden">
                                    <div className="h-full w-[42%] bg-gradient-to-r from-cyan-500 to-purple-500" />
                                </div>
                            </div>

                            {/* Upgrade Button */}
                            <button className="w-full py-2 rounded-lg bg-gradient-to-r from-amber-500/10 to-orange-500/10 border border-orange-500/20 flex items-center justify-center gap-2 text-orange-400 text-sm font-medium hover:bg-orange-500/20 transition-colors">
                                <Zap className="w-4 h-4" />
                                <span>Upgrade to VIP</span>
                            </button>
                        </div>
                    ) : (
                        <div className="flex flex-col items-center gap-4">
                            <Settings className="w-5 h-5 text-white/40 hover:text-white cursor-pointer transition-colors" />
                        </div>
                    )}

                    {/* Collapse Toggle */}
                    <button
                        onClick={() => setIsCollapsed(!isCollapsed)}
                        className="absolute bottom-4 right-4 w-6 h-6 flex items-center justify-center text-white/20 hover:text-white transition-colors"
                    >
                        <ChevronLeft className={cn("w-4 h-4 transition-transform duration-300", isCollapsed && "rotate-180")} />
                    </button>
                </div>
            </div>
        </motion.aside>
    );
}
