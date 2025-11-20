'use client';

import { useState, useRef, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { motion, useMotionValue, useTransform } from 'framer-motion';
import { Mail, Lock, Sparkles } from 'lucide-react';
import { apiClient } from '@/lib/api-client';
import { ParticleBackground } from '@/components/ui/particle-background';
import { toast } from 'sonner';

export default function LoginPage() {
    const router = useRouter();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [emailFocused, setEmailFocused] = useState(false);
    const [passwordFocused, setPasswordFocused] = useState(false);

    const cardRef = useRef<HTMLDivElement>(null);
    const mouseX = useMotionValue(0);
    const mouseY = useMotionValue(0);

    // 3D parallax effect
    const rotateX = useTransform(mouseY, [-300, 300], [5, -5]);
    const rotateY = useTransform(mouseX, [-300, 300], [-5, 5]);

    useEffect(() => {
        const handleMouseMove = (e: MouseEvent) => {
            if (!cardRef.current) return;
            const rect = cardRef.current.getBoundingClientRect();
            const centerX = rect.left + rect.width / 2;
            const centerY = rect.top + rect.height / 2;
            mouseX.set(e.clientX - centerX);
            mouseY.set(e.clientY - centerY);
        };

        window.addEventListener('mousemove', handleMouseMove);
        return () => window.removeEventListener('mousemove', handleMouseMove);
    }, [mouseX, mouseY]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);

        try {
            await apiClient.login(email, password);
            toast.success('Welcome back!');
            router.push('/dashboard');
        } catch (error: any) {
            toast.error(error.response?.data?.error || 'Invalid credentials');
        } finally {
            setIsLoading(false);
        }
    };

    const useDemoCredentials = () => {
        setEmail('demo@antigravity.app');
        setPassword('DemoPass123!');
    };

    return (
        <div className="min-h-screen relative overflow-hidden bg-gradient-cosmic">
            {/* Particle Background */}
            <ParticleBackground />

            {/* Main Content */}
            <div className="relative z-10 min-h-screen flex items-center justify-center p-6">
                <motion.div
                    ref={cardRef}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8, ease: [0.6, -0.05, 0.01, 0.99] }}
                    style={{
                        rotateX,
                        rotateY,
                        transformStyle: 'preserve-3d',
                    }}
                    className="w-full max-w-md"
                >
                    {/* Glass Card */}
                    <div className="relative">
                        {/* Glowing border animation */}
                        <div className="absolute -inset-[1px] bg-gradient-to-r from-cyan-500 via-purple-500 to-cyan-500 rounded-3xl opacity-75 blur-sm animate-gradient-shift"
                            style={{ backgroundSize: '200% 200%' }}
                        />

                        {/* Main card */}
                        <div className="relative backdrop-blur-3xl bg-white/[0.02] border border-white/10 rounded-3xl p-8 shadow-glass-lg">
                            {/* Logo Section */}
                            <motion.div
                                initial={{ opacity: 0, scale: 0.5 }}
                                animate={{ opacity: 1, scale: 1 }}
                                transition={{ delay: 0.2, duration: 0.6 }}
                                className="text-center mb-8"
                            >
                                <motion.h1
                                    className="text-5xl font-bold bg-gradient-to-r from-[#667EEA] via-[#764BA2] to-[#F093FB] bg-clip-text text-transparent mb-2"
                                    animate={{
                                        backgroundPosition: ['0% 50%', '100% 50%', '0% 50%'],
                                    }}
                                    transition={{
                                        duration: 5,
                                        repeat: Infinity,
                                        ease: 'linear',
                                    }}
                                    style={{
                                        backgroundSize: '200% 200%',
                                        letterSpacing: '0.05em',
                                    }}
                                >
                                    Antigravity
                                </motion.h1>
                                <p className="text-white/60 text-sm">Weightless Productivity</p>
                            </motion.div>

                            {/* Form */}
                            <form onSubmit={handleSubmit} className="space-y-6">
                                {/* Email Field */}
                                <motion.div
                                    initial={{ opacity: 0, x: -20 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    transition={{ delay: 0.3 }}
                                    className="relative"
                                >
                                    <div className="relative">
                                        <Mail className="absolute left-0 top-1/2 -translate-y-1/2 w-5 h-5 text-cyan-400/60" />
                                        <input
                                            type="email"
                                            value={email}
                                            onChange={(e) => setEmail(e.target.value)}
                                            onFocus={() => setEmailFocused(true)}
                                            onBlur={() => setEmailFocused(false)}
                                            placeholder="Email"
                                            className={`
                        w-full bg-transparent border-b-2 border-white/10 py-4 pl-8 pr-4
                        text-white placeholder-white/40 outline-none transition-all duration-300
                        ${emailFocused ? 'border-b-cyan-400 shadow-[0_8px_24px_rgba(6,182,212,0.2)]' : ''}
                      `}
                                            required
                                        />
                                        {emailFocused && (
                                            <motion.div
                                                layoutId="focus-glow"
                                                className="absolute -inset-x-4 -inset-y-2 bg-cyan-500/5 rounded-lg -z-10"
                                                initial={{ opacity: 0 }}
                                                animate={{ opacity: 1 }}
                                            />
                                        )}
                                    </div>
                                </motion.div>

                                {/* Password Field */}
                                <motion.div
                                    initial={{ opacity: 0, x: -20 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    transition={{ delay: 0.4 }}
                                    className="relative"
                                >
                                    <div className="relative">
                                        <Lock className="absolute left-0 top-1/2 -translate-y-1/2 w-5 h-5 text-purple-400/60" />
                                        <input
                                            type="password"
                                            value={password}
                                            onChange={(e) => setPassword(e.target.value)}
                                            onFocus={() => setPasswordFocused(true)}
                                            onBlur={() => setPasswordFocused(false)}
                                            placeholder="Password"
                                            className={`
                        w-full bg-transparent border-b-2 border-white/10 py-4 pl-8 pr-4
                        text-white placeholder-white/40 outline-none transition-all duration-300
                        ${passwordFocused ? 'border-b-purple-400 shadow-[0_8px_24px_rgba(139,92,246,0.2)]' : ''}
                      `}
                                            required
                                        />
                                        {passwordFocused && (
                                            <motion.div
                                                className="absolute -inset-x-4 -inset-y-2 bg-purple-500/5 rounded-lg -z-10"
                                                initial={{ opacity: 0 }}
                                                animate={{ opacity: 1 }}
                                            />
                                        )}
                                    </div>
                                </motion.div>

                                {/* Submit Button */}
                                <motion.button
                                    type="submit"
                                    disabled={isLoading}
                                    initial={{ opacity: 0, y: 20 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    transition={{ delay: 0.5 }}
                                    whileHover={{ scale: 1.02, y: -4 }}
                                    whileTap={{ scale: 0.98 }}
                                    className="relative w-full h-14 rounded-xl overflow-hidden group disabled:opacity-50"
                                >
                                    {/* Animated gradient background */}
                                    <div
                                        className="absolute inset-0 bg-gradient-shimmer animate-gradient-shift"
                                        style={{ backgroundSize: '300% 300%' }}
                                    />

                                    {/* Button content */}
                                    <div className="relative z-10 h-full flex items-center justify-center font-semibold text-white">
                                        {isLoading ? (
                                            <motion.div
                                                animate={{ rotate: 360 }}
                                                transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
                                                className="w-6 h-6 border-2 border-white/30 border-t-white rounded-full"
                                            />
                                        ) : (
                                            <span className="flex items-center gap-2">
                                                Sign In
                                                <Sparkles className="w-4 h-4" />
                                            </span>
                                        )}
                                    </div>

                                    {/* Hover shimmer effect */}
                                    <motion.div
                                        className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent"
                                        initial={{ x: '-100%' }}
                                        whileHover={{ x: '100%' }}
                                        transition={{ duration: 0.6 }}
                                    />

                                    {/* Shadow */}
                                    <motion.div
                                        className="absolute -inset-1 bg-gradient-primary opacity-0 group-hover:opacity-60 blur-xl -z-10 transition-opacity duration-300"
                                    />
                                </motion.button>

                                {/* Demo Credentials */}
                                <motion.div
                                    initial={{ opacity: 0 }}
                                    animate={{ opacity: 1 }}
                                    transition={{ delay: 0.6 }}
                                    className="text-center"
                                >
                                    <button
                                        type="button"
                                        onClick={useDemoCredentials}
                                        className="text-sm text-cyan-400/80 hover:text-cyan-400 transition-colors"
                                    >
                                        Use demo credentials
                                    </button>
                                </motion.div>
                            </form>

                            {/* Sign Up Link */}
                            <motion.div
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                transition={{ delay: 0.7 }}
                                className="mt-6 text-center text-sm text-white/60"
                            >
                                Don't have an account?{' '}
                                <a href="/auth/signup" className="text-purple-400 hover:text-purple-300 transition-colors">
                                    Sign up
                                </a>
                            </motion.div>
                        </div>
                    </div>
                </motion.div>
            </div>
        </div>
    );
}
