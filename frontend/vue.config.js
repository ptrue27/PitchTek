const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {
      '/api': { 
        target: 'http://pitchtek.pro', 
        changeOrigin: true, 
        pathRewrite: { '^/api': '' }, 
        secure: false, 
      },
    }
  },
  pluginOptions: {
    vuetify: {
			// https://github.com/vuetifyjs/vuetify-loader/tree/next/packages/vuetify-loader
		}
  }
})
