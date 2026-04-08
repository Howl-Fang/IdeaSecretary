# IdeaSecretary API 文档

## 基础信息

- **基础 URL**: `http://localhost:5000/api`
- **认证**: 使用用户 ID（待完善为 JWT）
- **响应格式**: JSON

## 认证相关 API

### 用户注册

**请求**
```http
POST /api/auth/register
Content-Type: application/json

{
  "username": "user123",
  "email": "user@example.com",
  "password": "secure_password",
  "language": "en",
  "theme": "light"
}
```

**响应**
```json
{
  "message": "User created successfully",
  "user": {
    "id": 1,
    "username": "user123",
    "email": "user@example.com"
  }
}
```

### 用户登录

**请求**
```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "user123",
  "password": "secure_password"
}
```

**响应**
```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "user123",
    "email": "user@example.com"
  }
}
```

## 想法库 API

### 获取所有库

**请求**
```http
GET /api/ideas/libraries?user_id=1
```

**响应**
```json
[
  {
    "id": "uuid-1",
    "name": "Technology Ideas",
    "description": "Ideas about tech",
    "total_ideas": 5,
    "total_words": 250,
    "created_at": "2026-04-08T10:00:00",
    "is_default": true
  }
]
```

### 创建新库

**请求**
```http
POST /api/ideas/libraries
Content-Type: application/json

{
  "user_id": 1,
  "name": "My New Library",
  "description": "A collection of new ideas",
  "is_default": false
}
```

**响应**
```json
{
  "message": "Library created",
  "id": "uuid-new"
}
```

### 获取库内的想法

**请求**
```http
GET /api/ideas/uuid-library-id
```

**响应**
```json
[
  {
    "id": "uuid-idea-1",
    "title": "Machine Learning Applications",
    "content": "# ML Ideas\nApplication 1...",
    "status": "draft",
    "created_at": "2026-04-08T10:00:00",
    "word_count": 150
  }
]
```

### 添加新想法

**请求**
```http
POST /api/ideas/uuid-library-id
Content-Type: application/json

{
  "parent_id": null,
  "title": "New Idea",
  "content": "The content of the idea",
  "status": "draft"
}
```

**响应**
```json
{
  "message": "Idea created",
  "id": "uuid-new-idea"
}
```

### 更新想法

**请求**
```http
PUT /api/ideas/uuid-idea-id
Content-Type: application/json

{
  "title": "Updated Title",
  "content": "Updated content",
  "status": "organized",
  "ai_thoughts": "AI insights here"
}
```

**响应**
```json
{
  "message": "Idea updated"
}
```

### 删除想法

**请求**
```http
DELETE /api/ideas/uuid-idea-id
```

**响应**
```json
{
  "message": "Idea deleted"
}
```

## AI 相关 API

### 组织想法

**请求**
```http
POST /api/ai/organize
Content-Type: application/json

{
  "user_id": 1,
  "idea_id": "uuid-idea-id",
  "content": "The idea content to organize"
}
```

**响应**
```json
{
  "message": "Idea organized successfully",
  "response": "Organized content with insights..."
}
```

### 获取灵感

**请求**
```http
POST /api/ai/inspire
Content-Type: application/json

{
  "library_id": "uuid-library-id"
}
```

**响应**
```json
{
  "inspiration": "Here are some inspiring suggestions based on your ideas..."
}
```

### 搜索想法

**请求**
```http
GET /api/ai/search?q=keyword&library_id=uuid-library-id
```

**响应**
```json
[
  {
    "id": "uuid-idea-1",
    "title": "Matching Idea",
    "content": "Matching content excerpt...",
    "created_at": "2026-04-08T10:00:00"
  }
]
```

## 账户相关 API

### 获取用户资料

**请求**
```http
GET /api/account/profile/1
```

**响应**
```json
{
  "id": 1,
  "username": "user123",
  "email": "user@example.com",
  "language": "en",
  "theme": "light",
  "created_at": "2026-04-08T10:00:00"
}
```

### 更新用户资料

**请求**
```http
PUT /api/account/profile/1
Content-Type: application/json

{
  "email": "newemail@example.com",
  "language": "zh",
  "theme": "dark"
}
```

**响应**
```json
{
  "message": "Profile updated"
}
```

### 获取 OpenAI 配置

**请求**
```http
GET /api/account/openai-config/1
```

**响应**
```json
{
  "has_api_key": true,
  "api_base": "https://api.openai.com/v1"
}
```

### 设置 OpenAI 配置

**请求**
```http
PUT /api/account/openai-config/1
Content-Type: application/json

{
  "api_key": "sk-...",
  "api_base": "https://api.openai.com/v1"
}
```

**响应**
```json
{
  "message": "OpenAI configuration updated"
}
```

## 错误响应

所有错误响应都遵循以下格式：

```json
{
  "error": "Error message description"
}
```

### 常见错误码

- 400: 请求参数错误
- 401: 未授权
- 404: 资源不存在
- 409: 资源冲突（如重复的用户名）
- 500: 服务器错误

## 开发建议

1. **认证改进**: 使用 JWT token 替代简单的 user_id
2. **错误处理**: 添加更详细的错误消息和错误码
3. **分页**: 为列表接口添加分页支持
4. **速率限制**: 添加 API 调用频率限制
5. **文档**: 使用 Swagger/OpenAPI 自动生成文档
