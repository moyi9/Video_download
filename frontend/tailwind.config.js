/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#1777FF',
          600: '#1565e0',
          700: '#1254c1',
          800: '#0f43a2',
          900: '#0c3283',
        }
      }
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}
