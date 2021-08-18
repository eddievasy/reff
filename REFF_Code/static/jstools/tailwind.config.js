module.exports = {
  future: {
      removeDeprecatedGapUtilities: true,
      purgeLayersByDefault: true,
  },
  purge: {
      enabled: false, //true for production build
      content: [
          '../**/templates/*.html',
          '../**/templates/**/*.html'
      ]
  },
  theme: {
      extend: {
        fontFamily: {
            shadows: ["Shadows Into Light"],
            // To be used for logo
            cookie: ['Cookie'],
            // To be used for titles
            epilogue : ['Epilogue'],
            // To be used for body
            source_sans_pro : ['"Source Sans Pro"'],
            // To be used for quotes
            jet_brains_mono : ['"JetBrains Mono"'],
            // To use for logo
            lobster: ['Lobster'],
        }
      },
  },
  variants: {},
  plugins: [],
}