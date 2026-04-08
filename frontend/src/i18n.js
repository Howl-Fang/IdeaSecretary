import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

const resources = {
  en: {
    translation: {
      // Navigation
      login: 'Login',
      register: 'Register',
      logout: 'Logout',
      noAccount: "Don't have an account?",
      haveAccount: 'Already have an account?',
      
      // Landing Page
      'landing.title': 'Are you troubled with your fantastic ideas?',
      'landing.description': 'IDEA SECRETARY is a tool to help you organize your ideas. Message, speak, or chat, whatever you like. You may be inspired by chatting.',
      
      // Features
      'features.input': 'Easy Input',
      'features.inputDesc': 'Share your ideas in any format - text, voice, or images',
      'features.ai': 'AI Organization',
      'features.aiDesc': 'Let AI organize and enhance your thoughts automatically',
      'features.search': 'Quick Search',
      'features.searchDesc': 'Find your ideas instantly with powerful search',
      
      // Dashboard
      treasury: 'Treasury',
      myIdeaBase: 'My Idea Base',
      account: 'Account',
      settings: 'Settings',
      getStarted: 'Get Started',
      
      // Treasury Panel
      whatOnYourMind: "What's on your mind today? Wanna have a brainstorm?",
      voice: 'Voice',
      image: 'Image',
      submit: 'Submit',
      totalIdeas: 'Total Ideas',
      totalWords: 'Total Words',
      inspirations: 'Inspirations',
      recentIdeas: 'Recent Ideas',
      
      // Common
      username: 'Username',
      email: 'Email',
      password: 'Password',
      confirmPassword: 'Confirm Password',
      loading: 'Loading...',
      toggleTheme: 'Toggle Theme',
      switchLanguage: 'Switch Language',
      
      // Messages
      passwordMismatch: 'Passwords do not match',
      loginFailed: 'Login failed',
      registrationFailed: 'Registration failed',
      registrationSuccess: 'Registration successful! Redirecting to login...'
    }
  },
  zh: {
    translation: {
      // Navigation
      login: '登录',
      register: '注册',
      logout: '登出',
      noAccount: '没有账户？',
      haveAccount: '已有账户？',
      
      // Landing Page
      'landing.title': '想法繁杂？让 IdeaSecretary 帮您整理',
      'landing.description': 'IdeaSecretary 是一个帮助您组织想法的工具。通过文字、语音或聊天，以任何您喜欢的方式分享。与 AI 对话，可能会获得启发。',
      
      // Features
      'features.input': '简单输入',
      'features.inputDesc': '用任何格式分享您的想法 - 文字、语音或图像',
      'features.ai': 'AI 整理',
      'features.aiDesc': '让 AI 自动整理和增强您的想法',
      'features.search': '快速搜索',
      'features.searchDesc': '通过强大的搜索功能快速找到您的想法',
      
      // Dashboard
      treasury: '金库',
      myIdeaBase: '我的想法库',
      account: '账户',
      settings: '设置',
      getStarted: '开始使用',
      
      // Treasury Panel
      whatOnYourMind: '今天有什么想法？想要进行头脑风暴吗？',
      voice: '语音',
      image: '图像',
      submit: '提交',
      totalIdeas: '想法总数',
      totalWords: '单词总数',
      inspirations: '灵感数',
      recentIdeas: '最近的想法',
      
      // Common
      username: '用户名',
      email: '邮箱',
      password: '密码',
      confirmPassword: '确认密码',
      loading: '加载中...',
      toggleTheme: '切换主题',
      switchLanguage: '切换语言',
      
      // Messages
      passwordMismatch: '密码不匹配',
      loginFailed: '登录失败',
      registrationFailed: '注册失败',
      registrationSuccess: '注册成功！正在跳转到登录页面...'
    }
  }
};

i18n
  .use(initReactI18next)
  .init({
    resources,
    lng: 'en',
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false
    }
  });

export default i18n;
