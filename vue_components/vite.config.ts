import { defineConfig, splitVendorChunkPlugin } from 'vite'
import { resolve } from 'path'
import vue from '@vitejs/plugin-vue'
import UnoCSS from 'unocss/vite'

const componentRoot = 'src/components'

const entrys = [
  'Counter',
  'ECharts',
  'UseDraggable',
  'UseMouse',
  'DropZone'
]

const libEntrys = entrys.map(p => resolve(__dirname, componentRoot, p, `${p}.ts`))
const targetName = 'ECharts'
const targetEntry = resolve(__dirname, componentRoot, targetName, `${targetName}.ts`)

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  define: {
    'process.env': {}
  },
  build: {
    cssCodeSplit: false,

    lib: {
      // Could also be a dictionary or array of multiple entry points
      entry: targetEntry,
      formats: ['es'],
      // name: 'UseDraggable',
      // the proper extensions will be added
      fileName: targetName,
      // fileName(format, entryName) {
      //   return  entryName
      // },
    },
    rollupOptions: {
      // 确保外部化处理那些你不想打包进库的依赖
      external: ['vue'],
      output: {
        // 在 UMD 构建模式下为这些外部化的依赖提供一个全局变量
        globals: {
          vue: 'Vue',
        },
        // inlineDynamicImports: true,
        // experimentalMinChunkSize: 0

        // manualChunks(id) {
        //   if (id.includes('@vueuse/core')) {
        //     return 'my-test'
        //   }
        // }
      },
    },
  },
})
