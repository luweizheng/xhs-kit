# Debug Workflow 使用示例

本示例展示如何在 agentic workflow 中使用 xhs-kit 的 **debug 模式**来测试内容生成流程。

## 核心特性

⚡️ **无需登录**：Debug 模式完全在本地运行，不会访问小红书服务器  
🚫 **不会发布**：只验证内容格式，不会实际发布  
♾️ **无限调用**：可以无限次调用，不消耗 API 配额  
🔍 **全面验证**：检查标题、图片、分辨率、文件大小等

## 使用场景

在 AI Agent 自动化工作流中：
1. Agent 根据主题生成文案和图片
2. 使用 `debug-publish` 验证内容是否符合小红书规范（**无需登录**）
3. 如果验证通过，再调用真实的 `publish` 发布到小红书
4. 避免频繁调用真实接口导致封号风险

## 工作流示例

### 1. 基本流程

```bash
# 步骤 1: Agent 生成内容
# (假设 Agent 已经生成了标题、文案和图片)

# 步骤 2: 使用 debug 模式验证
# 简洁模式（默认）：只显示验证结果
xhs-kit debug-publish \
  -t "AI 助手使用指南" \
  -c "分享我最近使用 AI 助手的心得..." \
  -i /path/to/generated_image1.jpg \
  -i /path/to/generated_image2.jpg \
  --tag "AI" \
  --tag "效率工具"

# 或使用 verbose 模式查看详细信息
xhs-kit debug-publish \
  -t "AI 助手使用指南" \
  -c "分享我最近使用 AI 助手的心得..." \
  -i /path/to/generated_image1.jpg \
  -i /path/to/generated_image2.jpg \
  --tag "AI" \
  --tag "效率工具" \
  --verbose

# 步骤 3: 如果验证通过，执行真实发布
# (只有在 debug 验证通过后才执行)
xhs-kit publish \
  -t "AI 助手使用指南" \
  -c "分享我最近使用 AI 助手的心得..." \
  -i /path/to/generated_image1.jpg \
  -i /path/to/generated_image2.jpg \
  --tag "AI" \
  --tag "效率工具"
```

### 2. Python 脚本示例

```python
#!/usr/bin/env python3
"""Debug Workflow 示例：自动生成并发布小红书内容"""

from xhs_kit.po.validator import ContentValidator
from xhs_kit.po.client import XhsClient
import asyncio

async def debug_workflow(topic: str):
    """
    完整的 debug workflow 示例
    
    Args:
        topic: 内容主题
    """
    # 步骤 1: Agent 生成内容（这里简化为示例）
    print(f"🤖 Agent 正在生成关于 '{topic}' 的内容...")
    
    # 模拟 Agent 生成的内容
    title = f"{topic}分享"
    content = f"今天来分享一下关于{topic}的心得体会..."
    images = [
        "/path/to/image1.jpg",
        "/path/to/image2.jpg"
    ]
    tags = [topic, "分享", "干货"]
    
    # 步骤 2: Debug 验证（无需登录，不会打开浏览器）
    print("\n📋 验证内容...")
    
    validation_result = ContentValidator.validate_publish_content(
        title=title,
        content=content,
        images=images,
        tags=tags
    )
    result = validation_result.to_dict()
    
    # 检查验证结果
    if not result["is_valid"]:
        print("❌ 验证失败:")
        for error in result["errors"]:
            print(f"  • {error}")
        
        # 根据错误自动修复
        if any("标题长度超过限制" in e for e in result["errors"]):
            print("\n🔧 自动修复：缩短标题...")
            title = title[:18] + "..."
            
            # 重新验证
            validation_result = ContentValidator.validate_publish_content(
                title=title,
                content=content,
                images=images,
                tags=tags
            )
            result = validation_result.to_dict()
    
    if result["warnings"]:
        print("\n⚠️  警告:")
        for warning in result["warnings"]:
            print(f"  • {warning}")
    
    # 步骤 3: 如果验证通过，发布到小红书（需要登录）
    if result["is_valid"]:
        print("\n✅ 验证通过！准备发布...")
        
        # 询问用户是否真的要发布
        confirm = input("是否发布到小红书？(y/n): ")
        
        if confirm.lower() == 'y':
            # 只有在真正发布时才需要 XhsClient（需要登录）
            async with XhsClient() as client:
                response = await client.publish(
                    title=title,
                    content=content,
                    images=images,
                    tags=tags
                )
                print(f"\n🎉 发布成功: {response.title}")
        else:
            print("\n⏸️  取消发布")
    else:
        print("\n❌ 验证未通过，请修复后重试")

# 运行示例
if __name__ == "__main__":
    asyncio.run(debug_workflow("AI 工具"))
```

### 3. MCP 工具调用示例

如果你在使用 MCP 协议（例如 Claude Desktop），可以这样调用：

```json
{
  "tool": "debug_publish_content",
  "arguments": {
    "title": "AI 助手使用指南",
    "content": "分享我最近使用 AI 助手的心得...",
    "images": [
      "/path/to/image1.jpg",
      "/path/to/image2.jpg"
    ],
    "tags": ["AI", "效率工具"]
  }
}
```

返回结果：
```json
{
  "is_valid": true,
  "errors": [],
  "warnings": [],
  "info": {
    "title_length": 8,
    "content_length": 20,
    "total_images": 2,
    "valid_images": 2,
    "image_details": [
      {
        "index": 1,
        "path": "/path/to/image1.jpg",
        "exists": true,
        "format_valid": true,
        "width": 1080,
        "height": 1920,
        "size_mb": 2.5
      }
    ]
  }
}
```

## 验证规则

Debug 模式会检查以下内容：

### 必须通过的验证（errors）
- ❌ 标题为空
- ❌ 标题长度超过 20 字符
- ❌ 图片文件不存在
- ❌ 图片格式不支持（仅支持 jpg/png/webp/heic）
- ❌ 图片数量超过 9 张

### 建议性警告（warnings）
- ⚠️ 标题接近长度限制（17-20 字符）
- ⚠️ 正文为空
- ⚠️ 正文过长（超过 1000 字符）
- ⚠️ 图片分辨率较低（小于 480x480）
- ⚠️ 图片文件较大（超过 20MB）
- ⚠️ 标签数量过多（超过 10 个）
- ⚠️ 单个标签过长（超过 20 字符）

## 最佳实践

1. **先 debug，后发布**
   - 在开发和测试阶段，始终使用 `debug-publish`
   - 确保内容符合规范后，再使用 `publish` 真实发布

2. **自动修复**
   - 根据 debug 返回的错误信息，自动调整内容
   - 例如：标题过长自动截断，图片不存在自动跳过

3. **批量测试**
   - 在批量生成内容时，先用 debug 模式验证所有内容
   - 筛选出通过验证的内容，再批量发布

4. **避免封号风险**
   - Debug 模式不会访问小红书，可以无限次调用
   - 只在确认内容无误后，才调用真实发布接口

## 常见问题

**Q: Debug 模式会消耗小红书的 API 配额吗？**
A: 不会。Debug 模式完全在本地运行，不会访问小红书服务器。

**Q: Debug 通过就一定能发布成功吗？**
A: Debug 只验证格式和文件，不保证内容审核通过。小红书可能因为内容违规拒绝发布。

**Q: 可以在 CI/CD 中使用 debug 模式吗？**
A: 可以。Debug 模式不需要登录，非常适合在自动化流程中使用。
