'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    Search, Bell, Sparkles, Moon, Sun, User,
    Command, Settings, LogOut
} from 'lucide-react';
import { useTheme } from 'next-themes';
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger,
    DropdownMenuSeparator
} from '@/components/ui/dropdown-menu';

export function Navbar() {
    const [isSearchFocused, setIsSearchFocused] = useState(false);
    const [searchValue, setSearchValue] = useState('');
    const { theme, setTheme } = useTheme();
    const [mounted, setMounted] = useState(false);

    useEffect(() => setMounted(true), []);

    return (
        <motion.header
            initial={{ y: -100, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
            className="fixed top-6 left-6 right-6 h-[72px] z-50"
        >
            <div className="relative h-full rounded-2xl backdrop-blur-xl bg-cosmic-navy/70 border border-white/10 shadow-glass flex items-center justify-between px-6 transition-all duration-300 hover:shadow-glass-lg">
                {/* Left: Brand */}
                <div className="flex items-center gap-3">
                    <motion.div
                        whileHover={{ rotate: 180 }}
                        transition={{ duration: 0.6 }}
                        className="w-10 h-10 rounded-xl bg-gradient-primary flex items-center justify-center shadow-lg"
                    >
                        <Sparkles className="w-5 h-5 text-white" />
                    </motion.div>
                    <span className="text-xl font-bold bg-gradient-to-r from-white via-white to-white/70 bg-clip-text text-transparent tracking-wide">
                        Antigravity
                    </span>
                </div>

                {/* Center: Omnibar Search */}
                <div className="absolute left-1/2 -translate-x-1/2">
                    <motion.div
                        animate={{
                            width: isSearchFocused ? 600 : 500,
                            backgroundColor: isSearchFocused ? 'rgba(255, 255, 255, 0.06)' : 'rgba(255, 255, 255, 0.03)'
                        }}
                        className="relative h-12 rounded-xl border border-white/10 flex items-center px-4 transition-colors"
                    >
                        <Search
                            className={`w-5 h-5 mr-3 transition-colors ${isSearchFocused ? 'text-cyan-400' : 'text-white/40'}`}
                        />
                        <input
                            type="text"
                            value={searchValue}
                            onChange={(e) => setSearchValue(e.target.value)}
                            onFocus={() => setIsSearchFocused(true)}
                            onBlur={() => setIsSearchFocused(false)}
                            placeholder="Search tasks, projects, or type '/' for magic..."
                            className="bg-transparent w-full h-full outline-none text-white placeholder-white/30 text-sm"
                        />
                        <div className="flex items-center gap-2 text-xs text-white/20 font-mono">
                            <span className="border border-white/10 rounded px-1.5 py-0.5">⌘</span>
                            <span className="border border-white/10 rounded px-1.5 py-0.5">K</span>
                        </div>

                        {/* Search Dropdown */}
                        <AnimatePresence>
                            {isSearchFocused && (
                                <motion.div
                                    initial={{ opacity: 0, y: 10 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    exit={{ opacity: 0, y: 10 }}
                                    className="absolute top-full left-0 right-0 mt-4 bg-cosmic-navy/95 backdrop-blur-2xl border border-white/10 rounded-xl shadow-2xl overflow-hidden p-2"
                                >
                                    <div className="text-xs font-medium text-white/40 px-3 py-2 uppercase tracking-wider">Recent</div>
                                    {['Project Alpha', 'Design System', 'Q4 Goals'].map((item, i) => (
                                        <motion.div
                                            key={item}
                                            initial={{ opacity: 0, x: -10 }}
                                            animate={{ opacity: 1, x: 0 }}
                                            transition={{ delay: i * 0.05 }}
                                            className="flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-white/5 cursor-pointer group"
                                        >
                                            <div className="w-8 h-8 rounded-lg bg-white/5 flex items-center justify-center group-hover:bg-gradient-to-br from-cyan-500/20 to-purple-500/20 transition-colors">
                                                <Command className="w-4 h-4 text-white/40 group-hover:text-white transition-colors" />
                                            </div>
                                            <span className="text-white/80 group-hover:text-white transition-colors">{item}</span>
                                        </motion.div>
                                    ))}
                                </motion.div>
                            )}
                        </AnimatePresence>
                    </motion.div>
                </div>

                {/* Right: Action Cluster */}
                <div className="flex items-center gap-4">
                    {/* Notifications */}
                    <motion.button
                        whileHover={{ rotate: [0, -10, 10, -10, 10, 0] }}
                        className="relative w-10 h-10 rounded-full flex items-center justify-center hover:bg-white/5 transition-colors"
                    >
                        <Bell className="w-5 h-5 text-white/70" />
                        <span className="absolute top-2 right-2 w-2 h-2 rounded-full bg-red-500 shadow-[0_0_8px_rgba(239,68,68,0.6)]" />
                    </motion.button>

                    {/* AI Assistant */}
                    <motion.button
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        className="w-10 h-10 rounded-full bg-gradient-to-br from-purple-500/20 to-cyan-500/20 border border-white/10 flex items-center justify-center group"
                    >
                        <Sparkles className="w-5 h-5 text-white/70 group-hover:text-white transition-colors" />
                    </motion.button>

                    {/* Theme Toggle */}
                    <motion.button
                        onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
                        whileHover={{ rotate: 180 }}
                        transition={{ duration: 0.5 }}
                        className="w-10 h-10 rounded-full flex items-center justify-center hover:bg-white/5 transition-colors"
                    >
                        {mounted && theme === 'dark' ? (
                            <Moon className="w-5 h-5 text-white/70" />
                        ) : (
                            <Sun className="w-5 h-5 text-white/70" />
                        )}
                    </motion.button>

                    {/* User Avatar */}
                    <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                            <motion.button
                                whileHover={{ scale: 1.05 }}
                                className="w-10 h-10 rounded-full bg-gradient-to-br from-cyan-400 to-purple-600 p-[2px] cursor-pointer"
                            >
                                <div className="w-full h-full rounded-full bg-cosmic-navy flex items-center justify-center overflow-hidden">
                                    <img
                                        src="https://api.dicebear.com/7.x/avataaars/svg?seed=Felix"
                                        alt="User"
                                        className="w-full h-full object-cover"
                                    />
                                </div>
                            </motion.button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent align="end" className="w-56 bg-cosmic-navy/95 backdrop-blur-xl border-white/10 text-white">
                            <div className="flex items-center gap-3 p-2">
                                <div className="w-10 h-10 rounded-full bg-gradient-to-br from-cyan-400 to-purple-600 p-[2px]">
                                    <div className="w-full h-full rounded-full bg-cosmic-navy flex items-center justify-center overflow-hidden">
                                        <img
                                            src="https://api.dicebear.com/7.x/avataaars/svg?seed=Felix"
                                            alt="User"
                                            className="w-full h-full object-cover"
                                        />
                                    </div>
                                </div>
                                <div>
                                    <div className="font-medium">Felix The Cat</div>
                                    <div className="text-xs text-white/50">felix@antigravity.app</div>
                                </div>
                            </div>
                            <DropdownMenuSeparator className="bg-white/10" />
                            <DropdownMenuItem className="focus:bg-white/10 focus:text-white cursor-pointer">
                                <User className="w-4 h-4 mr-2" /> Profile
                            </DropdownMenuItem>
                            <DropdownMenuItem className="focus:bg-white/10 focus:text-white cursor-pointer">
                                <Settings className="w-4 h-4 mr-2" /> Settings
                            </DropdownMenuItem>
                            <DropdownMenuSeparator className="bg-white/10" />
                            <DropdownMenuItem className="focus:bg-red-500/20 focus:text-red-400 text-red-400 cursor-pointer">
                                <LogOut className="w-4 h-4 mr-2" /> Log out
                            </DropdownMenuItem>
                        </DropdownMenuContent>
                    </DropdownMenu>
                </div>
            </div>
        </motion.header>
    );
}
