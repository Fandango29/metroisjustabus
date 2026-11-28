import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  test: {
    // Os testes de componentes correm num DOM simulado (jsdom), sem browser
    environment: 'jsdom',
    setupFiles: ['./src/setupTests.js'],
  },
})
