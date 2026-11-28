import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  test: {
    // Os testes de componentes correm num DOM simulado (jsdom), sem browser
    environment: 'jsdom',
    setupFiles: ['./src/setupTests.js'],
    // Cobertura (RNF-18): conta todo o src/, mesmo os ficheiros que nenhum teste importa
    coverage: {
      provider: 'v8',
      include: ['src/**/*.{js,jsx}'],
      reporter: ['text'],
      thresholds: { statements: 70, branches: 70, functions: 70, lines: 70 },
    },
  },
})
