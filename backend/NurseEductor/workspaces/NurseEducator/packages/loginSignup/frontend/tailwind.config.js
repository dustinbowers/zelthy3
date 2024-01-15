/** @type {import('tailwindcss').Config} */
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    colors: {
      // primary: '#5048ED',
      primary: 'var(--primary)',
      secondary: 'var(--secondary)',
      bgColor: 'var(--bgColor)',
      boxBg: 'var(--boxBg)',
      white: "#ffffff",
      black: "#000000",
      gray: "#c7c7c7",
      GrayText: "#6C747D",
      warningText: "#694200",
      warninBg: "#ffefd4",
      error: "#F3A29A",
      errorText: "#ed4337"
  },
  fontFamily: {
    'display': ['Oswald'],
    'body': ['"Open Sans"'],
    'open-sans': ['"Open Sans"', 'sans-serif'],
    'invention-app': ['"Invention App"', 'sans-serif'],
    'source-sans-pro': ['"Source Sans Pro"', 'sans-serif'],
    lato: ['"Lato"', 'sans-serif'],
  },
    extend: {},
  },
  plugins: [],
}
