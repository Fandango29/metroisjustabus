import { afterEach, describe, expect, it } from 'vitest'
import { screen } from '@testing-library/react'

afterEach(() => {
  document.body.innerHTML = ''
})

describe('arranque da aplicação', () => {
  it('monta a App dentro do elemento #root', async () => {
    const raiz = document.createElement('div')
    raiz.id = 'root'
    document.body.appendChild(raiz)

    await import('./main.jsx')

    const titulo = await screen.findByRole('heading', { level: 1, name: 'MetroIsJustABus' })
    expect(raiz).toContainElement(titulo)
  })
})
