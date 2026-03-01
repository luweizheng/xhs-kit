"""内容验证模块 - 用于 debug 模式验证发布内容"""

import os
from typing import Optional
from pathlib import Path
from PIL import Image
import logging

logger = logging.getLogger(__name__)


class ValidationResult:
    """验证结果"""
    
    def __init__(self):
        self.is_valid = True
        self.errors = []
        self.warnings = []
        self.info = {}
    
    def add_error(self, message: str):
        """添加错误"""
        self.is_valid = False
        self.errors.append(message)
    
    def add_warning(self, message: str):
        """添加警告"""
        self.warnings.append(message)
    
    def add_info(self, key: str, value):
        """添加信息"""
        self.info[key] = value
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "is_valid": self.is_valid,
            "errors": self.errors,
            "warnings": self.warnings,
            "info": self.info
        }


class ContentValidator:
    """内容验证器"""
    
    # 验证规则
    MIN_IMAGE_WIDTH = 480
    MIN_IMAGE_HEIGHT = 480
    MAX_IMAGE_SIZE_MB = 20
    MAX_TITLE_LENGTH = 20
    MAX_CONTENT_LENGTH = 1000
    CONTENT_WARN_LENGTH = 900
    MAX_IMAGES = 16
    SUPPORTED_IMAGE_FORMATS = {'.jpg', '.jpeg', '.png', '.webp', '.heic'}
    
    @classmethod
    def validate_publish_content(
        cls,
        title: str,
        content: str,
        images: list[str],
        tags: Optional[list[str]] = None
    ) -> ValidationResult:
        """验证发布内容
        
        Args:
            title: 标题
            content: 正文
            images: 图片路径列表
            tags: 标签列表
            
        Returns:
            ValidationResult: 验证结果
        """
        result = ValidationResult()
        
        # 验证标题
        cls._validate_title(title, result)
        
        # 验证正文
        cls._validate_content(content, result)
        
        # 验证图片
        cls._validate_images(images, result)
        
        # 验证标签
        if tags:
            cls._validate_tags(tags, result)
        
        return result
    
    @classmethod
    def _validate_title(cls, title: str, result: ValidationResult):
        """验证标题"""
        if not title or not title.strip():
            result.add_error("标题不能为空")
            return
        
        title_len = cls._calc_length(title)
        result.add_info("title_length", title_len)
        
        if title_len > cls.MAX_TITLE_LENGTH:
            result.add_error(
                f"标题长度超过限制：{title_len} > {cls.MAX_TITLE_LENGTH} 字符"
            )
        elif title_len > cls.MAX_TITLE_LENGTH - 3:
            result.add_warning(
                f"标题接近长度限制：{title_len}/{cls.MAX_TITLE_LENGTH} 字符"
            )
    
    @classmethod
    def _validate_content(cls, content: str, result: ValidationResult):
        """验证正文"""
        if not content or not content.strip():
            result.add_warning("正文为空")
            return
        
        content_len = len(content)
        result.add_info("content_length", content_len)
        
        if content_len > cls.MAX_CONTENT_LENGTH:
            result.add_warning(
                f"正文较长：{content_len} 字符（建议 {cls.MAX_CONTENT_LENGTH} 字符以内）"
            )
        elif content_len > cls.CONTENT_WARN_LENGTH:
            result.add_warning(
                f"正文接近上限：{content_len}/{cls.MAX_CONTENT_LENGTH} 字符"
            )
    
    @classmethod
    def _validate_images(cls, images: list[str], result: ValidationResult):
        """验证图片"""
        if not images:
            result.add_error("至少需要一张图片")
            return
        
        if len(images) > cls.MAX_IMAGES:
            result.add_error(
                f"图片数量超过限制：{len(images)} > {cls.MAX_IMAGES}"
            )
        
        valid_images = []
        image_details = []
        
        for i, img_path in enumerate(images):
            img_info = cls._validate_single_image(img_path, i + 1)
            image_details.append(img_info)
            
            if img_info["exists"]:
                valid_images.append(img_path)
            else:
                result.add_error(f"图片 {i+1} 不存在: {img_path}")
            
            # 检查格式
            if img_info["exists"] and not img_info["format_valid"]:
                result.add_error(
                    f"图片 {i+1} 格式不支持: {img_info['format']} "
                    f"(支持: {', '.join(cls.SUPPORTED_IMAGE_FORMATS)})"
                )
            
            # 检查分辨率
            if img_info["exists"] and img_info["format_valid"]:
                width = img_info.get("width", 0)
                height = img_info.get("height", 0)
                
                if width < cls.MIN_IMAGE_WIDTH or height < cls.MIN_IMAGE_HEIGHT:
                    result.add_warning(
                        f"图片 {i+1} 分辨率较低: {width}x{height} "
                        f"(建议至少 {cls.MIN_IMAGE_WIDTH}x{cls.MIN_IMAGE_HEIGHT})"
                    )
                
                # 检查文件大小
                size_mb = img_info.get("size_mb", 0)
                if size_mb > cls.MAX_IMAGE_SIZE_MB:
                    result.add_warning(
                        f"图片 {i+1} 文件较大: {size_mb:.2f}MB "
                        f"(建议 {cls.MAX_IMAGE_SIZE_MB}MB 以内)"
                    )
        
        result.add_info("total_images", len(images))
        result.add_info("valid_images", len(valid_images))
        result.add_info("image_details", image_details)
    
    @classmethod
    def _validate_single_image(cls, img_path: str, index: int) -> dict:
        """验证单张图片"""
        info = {
            "index": index,
            "path": img_path,
            "exists": False,
            "format_valid": False
        }
        
        if not os.path.exists(img_path):
            return info
        
        info["exists"] = True
        
        # 检查文件扩展名
        ext = Path(img_path).suffix.lower()
        info["format"] = ext
        info["format_valid"] = ext in cls.SUPPORTED_IMAGE_FORMATS
        
        if not info["format_valid"]:
            return info
        
        # 获取文件大小
        size_bytes = os.path.getsize(img_path)
        info["size_mb"] = size_bytes / (1024 * 1024)
        
        # 获取图片尺寸
        try:
            with Image.open(img_path) as img:
                info["width"] = img.width
                info["height"] = img.height
                info["mode"] = img.mode
        except Exception as e:
            logger.warning(f"无法读取图片 {img_path}: {e}")
            info["format_valid"] = False
        
        return info
    
    @classmethod
    def _validate_tags(cls, tags: list[str], result: ValidationResult):
        """验证标签"""
        if not tags:
            return
        
        result.add_info("total_tags", len(tags))
        
        if len(tags) > 10:
            result.add_warning(f"标签数量较多：{len(tags)} 个（建议 10 个以内）")
        
        for i, tag in enumerate(tags):
            if not tag or not tag.strip():
                result.add_warning(f"标签 {i+1} 为空")
            elif len(tag) > 20:
                result.add_warning(f"标签 {i+1} 较长：{len(tag)} 字符")
    
    @classmethod
    def _calc_length(cls, text: str) -> int:
        """计算文本长度（中文、emoji 等都算 1 个字符）"""
        return len(text)
