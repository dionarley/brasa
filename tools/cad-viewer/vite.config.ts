import { defineConfig } from 'vite'

// base './' para o app funcionar em qualquer caminho (raiz do nginx ou um
// subdiretório de um site estático).
export default defineConfig({
  base: './',
  build: {
    outDir: 'dist',
    modulePreload: false,
    chunkSizeWarningLimit: 4096
  },
  server: {
    port: 3000
  }
})
