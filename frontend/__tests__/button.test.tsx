/**
 * @jest-environment jsdom
 */

import { render, screen } from '@testing-library/react'
import { Button } from '@/components/ui/button'

describe('Button Component', () => {
    it('renders button with text', () => {
        render(<Button>Click me</Button>)
        expect(screen.getByText('Click me')).toBeInTheDocument()
    })

    it('applies variant classes correctly', () => {
        const { container } = render(<Button variant="destructive">Delete</Button>)
        const button = container.querySelector('button')
        expect(button).toHaveClass('bg-red-500')
    })

    it('handles click events', () => {
        const handleClick = jest.fn()
        render(<Button onClick={handleClick}>Click</Button>)
        screen.getByText('Click').click()
        expect(handleClick).toHaveBeenCalledTimes(1)
    })

    it('can be disabled', () => {
        render(<Button disabled>Disabled</Button>)
        expect(screen.getByText('Disabled')).toBeDisabled()
    })
})
