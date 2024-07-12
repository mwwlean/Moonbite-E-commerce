
/* Modified tailwind.config.js content */
module.exports = {
  content: ["./**/**/*.html", './node_modules/flowbite/**/*.js'],
  theme: {
    extend: {
      fontFamily: {
        'montserrat': ['Montserrat', 'sans-serif'],
      },
      colors: {
        'color-1': '#FFC700',
        'color-2': '#FFEFB6',
        'color-3': '#FF0000',
        'color-4': '#101010',
        'color-5': '#1E1E1E',
      },
    },
  },
  plugins: [
    require('flowbite/plugin')
  ],
};
