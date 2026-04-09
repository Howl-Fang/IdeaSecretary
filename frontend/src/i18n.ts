import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

const en = {
  "app": {
    "title": "IdeaSecretary",
    "tagline": "Organize Your Ideas, Effortlessly"
  },
  "nav": {
    "treasury": "Treasury",
    "ideaBase": "My Idea Base",
    "account": "Account",
    "settings": "Settings",
    "logout": "Logout"
  },
  "intro": {
    "mission": "Are you troubled with your fantastic ideas? Do you want to document your thoughts without wasting too much time? IDEA SECRETARY is a tool to help you organize your ideas. Message, speak, or chat, whatever you like. You may be inspired by chatting.",
    "loginBtn": "Login & Register"
  },
  "auth": {
    "login": "Login",
    "register": "Register",
    "email": "Email",
    "password": "Password",
    "confirmPassword": "Confirm Password",
    "forgotPassword": "Forgot Password?",
    "noAccount": "Don't have an account?",
    "haveAccount": "Already have an account?",
    "loginSuccess": "Login successful",
    "registerSuccess": "Registration successful"
  },
  "treasury": {
    "placeholder": "What comes up to your mind today?",
    "placeholderAlt": "Wanna have a brainstorm?",
    "submit": "Submit",
    "voice": "Voice",
    "image": "Image",
    "link": "Link",
    "features": {
      "keepInput": "Keep input",
      "inspiration": "Give me inspiration",
      "talkToYourself": "Talk to yourself"
    },
    "suggestions": "Suggestions",
    "stats": {
      "totalIdeas": "Total Ideas",
      "wordCount": "Word Count",
      "availableInspirations": "Available Inspirations"
    }
  },
  "ideaBase": {
    "title": "My Idea Base",
    "treeView": "Tree View",
    "mindmapView": "Mindmap View",
    "edit": "Edit",
    "rebalance": "Rebalance",
    "export": "Export"
  },
  "account": {
    "title": "Account",
    "profile": "Profile",
    "openaiApi": "OpenAI API",
    "apiKey": "API Key",
    "customUrl": "Custom URL (for self-hosted)",
    "save": "Save"
  },
  "settings": {
    "title": "Settings",
    "language": "Language",
    "theme": "Theme",
    "darkMode": "Dark Mode",
    "lightMode": "Light Mode",
    "auto": "Auto"
  },
  "common": {
    "loading": "Loading...",
    "error": "Error",
    "success": "Success",
    "cancel": "Cancel",
    "delete": "Delete",
    "edit": "Edit",
    "save": "Save",
    "close": "Close"
  }
};

const zh = {
  "app": {
    "title": "IdeaSecretary",
    "tagline": "轻松整理您的想法"
  },
  "nav": {
    "treasury": "想法库",
    "ideaBase": "我的知识库",
    "account": "账户",
    "settings": "设置",
    "logout": "退出登录"
  },
  "intro": {
    "mission": "为您的奇思妙想而烦恼?想要记录您的想法而不浪费太多时间?IDEA SECRETARY是一款帮助您组织想法的工具。消息、语音或聊天,随您喜欢。在聊天中您可能会获得灵感。",
    "loginBtn": "登录 & 注册"
  },
  "auth": {
    "login": "登录",
    "register": "注册",
    "email": "邮箱",
    "password": "密码",
    "confirmPassword": "确认密码",
    "forgotPassword": "忘记密码?",
    "noAccount": "还没有账户?",
    "haveAccount": "已有账户?",
    "loginSuccess": "登录成功",
    "registerSuccess": "注册成功"
  },
  "treasury": {
    "placeholder": "今天有什么新想法吗?",
    "placeholderAlt": "想来次头脑风暴?",
    "submit": "提交",
    "voice": "语音",
    "image": "图片",
    "link": "链接",
    "features": {
      "keepInput": "保留输入",
      "inspiration": "给我灵感",
      "talkToYourself": "和自己谈话"
    },
    "suggestions": "建议",
    "stats": {
      "totalIdeas": "想法总数",
      "wordCount": "字数统计",
      "availableInspirations": "可用灵感"
    }
  },
  "ideaBase": {
    "title": "我的知识库",
    "treeView": "树形视图",
    "mindmapView": "思维导图",
    "edit": "编辑",
    "rebalance": "重新排序",
    "export": "导出"
  },
  "account": {
    "title": "账户",
    "profile": "个人资料",
    "openaiApi": "OpenAI API",
    "apiKey": "API 密钥",
    "customUrl": "自定义URL (自建API)",
    "save": "保存"
  },
  "settings": {
    "title": "设置",
    "language": "语言",
    "theme": "主题",
    "darkMode": "深色模式",
    "lightMode": "浅色模式",
    "auto": "自动"
  },
  "common": {
    "loading": "加载中...",
    "error": "错误",
    "success": "成功",
    "cancel": "取消",
    "delete": "删除",
    "edit": "编辑",
    "save": "保存",
    "close": "关闭"
  }
};

const resources = {
  en: { translation: en },
  zh: { translation: zh },
};

i18n.use(initReactI18next).init({
  resources,
  lng: navigator.language.startsWith('zh') ? 'zh' : 'en',
  fallbackLng: 'en',
  interpolation: {
    escapeValue: false,
  },
});

export default i18n;
