import { defineConfig } from 'vite'

export default defineConfig({
    // minimalist config to ensure Vercel builds correctly
    build: {
        outDir: 'dist',
        assetsDir: 'assets',
    }
})
