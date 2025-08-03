import { defineConfig } from 'vite'

import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'
import svgLoader from 'vite-svg-loader'

import path from 'path'


// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    tailwindcss(),
    svgLoader(),

  ],

  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
  },

  server: { // ★ proxy設定は server オプションの中に入れます
    proxy: {
      '/api': {
        // targetをDockerのサービス名に変更
        target: 'http://backend:5000',
        changeOrigin: true,
      }
    },
  },

  //// ビルドの設定
  // build: {
  //   // ビルド成果物の出力先ディレクトリ
  //   // Flaskのstaticフォルダを指定することが多い
  //   outDir: '../static/dist',

  //   // manifest.json を生成する
  //   manifest: true,

  //   // rollupの設定
  //   rollupOptions: {
  //     // manifest.jsonから読み込むため、ここではエントリーポイントを直接指定しない
  //     // 必要に応じて設定する
  //     input: {
  //       main: './src/main.js',
  //     }
  //   }
  // }




})
