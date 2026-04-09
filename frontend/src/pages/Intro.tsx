import React from 'react'
import { useTranslation } from 'react-i18next'
import { useTheme } from '@/hooks/useTheme'

const Intro: React.FC = () => {
  const { t } = useTranslation()
  const { theme, toggleTheme } = useTheme()

  return (
    <div className={`min-h-screen ${theme === 'dark' ? 'dark' : ''}`}>
      <div className="bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 transition-colors">
        {/* Navigation */}
        <nav className="flex justify-between items-center px-6 py-4 border-b border-gray-200 dark:border-gray-800">
          <h1 className="text-2xl font-bold text-primary-500">{t('app.title')}</h1>
          <div className="flex gap-4 items-center">
            <button
              onClick={toggleTheme}
              className="px-3 py-2 rounded-lg bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
            >
              {theme === 'dark' ? '☀️' : '🌙'}
            </button>
            <a href="/login" className="px-4 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition-colors">
              {t('intro.loginBtn')}
            </a>
          </div>
        </nav>

        {/* Main Content */}
        <main className="flex flex-col items-center justify-center min-h-[calc(100vh-80px)] px-4">
          {/* Animated Title */}
          <div className="text-5xl md:text-7xl font-bold text-center mb-8">
            <div className="text-primary-500 mb-4">
              {t('app.title')}
            </div>
            <div className="text-3xl md:text-4xl text-gray-500 dark:text-gray-400 font-normal">
              {t('app.tagline')}
            </div>
          </div>

          {/* Mission Statement */}
          <div className="max-w-2xl text-center my-12">
            <p className="text-lg text-gray-600 dark:text-gray-300 leading-relaxed">
              {t('intro.mission')}
            </p>
          </div>

          {/* Footer Links */}
          <div className="mt-16 flex gap-8 text-sm text-gray-500 dark:text-gray-400">
            <a href="https://github.com/Howl-Fang/IdeaSecretary" target="_blank" rel="noopener noreferrer" className="hover:text-primary-500 transition-colors">
              GitHub
            </a>
            <a href="https://howl-fang.github.io" target="_blank" rel="noopener noreferrer" className="hover:text-primary-500 transition-colors">
              Author
            </a>
          </div>
        </main>
      </div>
    </div>
  )
}

export default Intro
