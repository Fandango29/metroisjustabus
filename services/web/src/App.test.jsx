import { afterEach, describe, expect, it } from 'vitest'
import { cleanup, render, screen } from '@testing-library/react'
import App from './App.jsx'

afterEach(cleanup)

describe('ecrã inicial', () => {
  it('mostra o título MetroIsJustABus', () => {
    render(<App />)

    expect(
      screen.getByRole('heading', { level: 1, name: 'MetroIsJustABus' }),
    ).toBeInTheDocument()
  })
})
