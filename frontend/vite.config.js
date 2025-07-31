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

  proxy: {
      // '/api' で始まるパスへのリクエストをFlaskサーバーに転送する
    '/api': {
      target: 'http://127.0.0.1:5000', // Flaskサーバーのアドレス
      changeOrigin: true, // オリジンを変更してCORSエラーを回避
    }
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
