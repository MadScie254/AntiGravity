/**
 * Toast notification system using Sonner.
 */

'use client'

import { Toaster as Sonner } from 'sonner'

type ToasterProps = React.ComponentProps<typeof Sonner>

const Toaster = ({ ...props }: ToasterProps) => {
    return (
        <Sonner
            className="toaster group"
            toastOptions={{
                classNames: {
                    toast:
                        'group toast group-[.toaster]:bg-white group-[.toaster]:text-muted-900 group-[.toaster]:border-muted-200 group-[.toaster]:shadow-lg dark:group-[.toaster]:bg-muted-900 dark:group-[.toaster]:text-muted-50 dark:group-[.toaster]:border-muted-800',
                    description: 'group-[.toast]:text-muted-500 dark:group-[.toast]:text-muted-400',
                    actionButton:
                        'group-[.toast]:bg-primary group-[.toast]:text-white',
                    cancelButton:
                        'group-[.toast]:bg-muted-100 group-[.toast]:text-muted-500 dark:group-[.toast]:bg-muted-800 dark:group-[.toast]:text-muted-400',
                },
            }}
            {...props}
        />
    )
}

export { Toaster }
