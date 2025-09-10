#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""NLP文本处理工具"""

import re
import jieba
import jieba.analyse
import jieba.posseg as pseg
from typing import List, Dict, Optional, Set, Tuple

# 设置jieba分词
# 确保中文分词准确
jieba.setLogLevel(jieba.logging.INFO)

# 尝试导入nltk库
try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
    from nltk.tokenize import word_tokenize, sent_tokenize
    
    # 下载必要的nltk资源
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')
    
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords')
    
    try:
        nltk.data.find('corpora/wordnet')
    except LookupError:
        nltk.download('wordnet')
except ImportError:
    print("Warning: nltk library not found. Please install it with 'pip install nltk'")
    
    # 创建简单的模拟nltk模块
    class MockNLTK:
        def word_tokenize(self, text):
            return text.split()
        
        def sent_tokenize(self, text):
            return text.split('.')
        
        class WordNetLemmatizer:
            def lemmatize(self, word, pos='n'):
                return word
        
    nltk = MockNLTK()
    word_tokenize = nltk.word_tokenize
    sent_tokenize = nltk.sent_tokenize
    WordNetLemmatizer = nltk.WordNetLemmatizer


class TextProcessor:
    """文本处理工具类"""
    
    def __init__(self):
        """初始化文本处理器"""
        # 中文停用词表
        self.chinese_stopwords = self._load_chinese_stopwords()
        
        # 英文停用词表
        try:
            self.english_stopwords = set(stopwords.words('english'))
        except:
            self.english_stopwords = set()
        
        # 英文词形还原器
        self.lemmatizer = WordNetLemmatizer()
        
        # 添加金融领域的自定义词典（可选）
        # self.add_custom_dict('path/to/financial_dict.txt')
    
    def _load_chinese_stopwords(self) -> Set[str]:
        """加载中文停用词表
        
        Returns:
            Set[str]: 中文停用词集合
        """
        # 常用中文停用词
        stopwords = {
            '的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', 
            '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这', '把', 
            '那', '得', '以', '于', '对于', '关于', '与之', '等等', '然而', '但是', '却', '此外', 
            '例如', '还是', '或者', '不过', '如果', '因为', '所以', '虽然', '尽管', '并且', '而且',
            '因此', '由此', '一方面', '另一方面', '总之', '综上所述', '据悉', '据了解'
        }
        return stopwords
    
    def add_custom_dict(self, dict_path: str) -> None:
        """添加自定义词典
        
        Args:
            dict_path: 词典文件路径
        """
        try:
            jieba.load_userdict(dict_path)
        except Exception as e:
            print(f"Failed to load custom dictionary: {e}")
    
    def tokenize_chinese(self, text: str) -> List[str]:
        """中文分词
        
        Args:
            text: 中文文本
            
        Returns:
            List[str]: 分词结果
        """
        return list(jieba.cut(text))
    
    def tokenize_english(self, text: str) -> List[str]:
        """英文分词
        
        Args:
            text: 英文文本
            
        Returns:
            List[str]: 分词结果
        """
        return word_tokenize(text)
    
    def tokenize(self, text: str) -> List[str]:
        """智能分词（中英文混合）
        
        Args:
            text: 输入文本
            
        Returns:
            List[str]: 分词结果
        """
        # 简单的中英文混合分词策略
        # 1. 先使用jieba进行分词
        tokens = self.tokenize_chinese(text)
        
        # 2. 对英文单词进行二次分词
        final_tokens = []
        for token in tokens:
            # 如果包含英文，尝试进一步分词
            if re.search(r'[a-zA-Z]', token):
                # 对英文部分进行分词
                en_tokens = self.tokenize_english(token)
                final_tokens.extend(en_tokens)
            else:
                final_tokens.append(token)
        
        return final_tokens
    
    def remove_stopwords(self, tokens: List[str], language: str = 'chinese') -> List[str]:
        """移除停用词
        
        Args:
            tokens: 分词结果
            language: 语言类型，支持'chinese'和'english'
            
        Returns:
            List[str]: 移除停用词后的分词结果
        """
        if language == 'chinese':
            stopwords = self.chinese_stopwords
        elif language == 'english':
            stopwords = self.english_stopwords
        else:
            stopwords = set()
        
        return [token for token in tokens if token not in stopwords and token.strip()]
    
    def extract_keywords(self, text: str, top_k: int = 10, method: str = 'tfidf') -> List[Tuple[str, float]]:
        """提取关键词
        
        Args:
            text: 输入文本
            top_k: 返回的关键词数量
            method: 提取方法，支持'tfidf'和'textrank'
            
        Returns:
            List[Tuple[str, float]]: 关键词和权重的列表
        """
        if method == 'tfidf':
            # 使用TF-IDF提取关键词
            keywords = jieba.analyse.extract_tags(
                text, 
                topK=top_k, 
                withWeight=True, 
                allowPOS=('n', 'nr', 'ns', 'nt', 'nz', 'v', 'vn', 'a')
            )
        elif method == 'textrank':
            # 使用TextRank提取关键词
            keywords = jieba.analyse.textrank(
                text, 
                topK=top_k, 
                withWeight=True, 
                allowPOS=('n', 'nr', 'ns', 'nt', 'nz', 'v', 'vn', 'a')
            )
        else:
            raise ValueError(f"Unsupported keyword extraction method: {method}")
        
        return keywords
    
    def extract_entities(self, text: str, entity_types: Optional[List[str]] = None) -> List[Tuple[str, str]]:
        """提取实体
        
        Args:
            text: 输入文本
            entity_types: 要提取的实体类型列表（可选）
            
        Returns:
            List[Tuple[str, str]]: 实体和类型的列表
        """
        # 使用jieba的词性标注进行简单实体识别
        # 注意：这是一个简化实现，实际应用中可能需要使用更复杂的NER模型
        words = pseg.cut(text)
        
        # 定义常见的实体词性
        entity_pos_map = {
            'nr': 'PERSON',    # 人名
            'ns': 'LOCATION',  # 地名
            'nt': 'ORGANIZATION',  # 机构名
            'nz': 'TERM'       # 其他专有名词
        }
        
        entities = []
        for word, pos in words:
            # 检查词性是否对应实体
            if pos in entity_pos_map:
                entity_type = entity_pos_map[pos]
                # 如果指定了实体类型，则只保留指定类型的实体
                if entity_types is None or entity_type in entity_types:
                    entities.append((word, entity_type))
        
        return entities
    
    def clean_text(self, text: str) -> str:
        """清理文本
        
        Args:
            text: 输入文本
            
        Returns:
            str: 清理后的文本
        """
        # 移除多余的空格和换行符
        text = re.sub(r'\s+', ' ', text)
        
        # 移除特殊字符（保留中文、英文、数字和常见标点）
        text = re.sub(r'[^一-龥a-zA-Z0-9,.!?，。！？:：;；]', ' ', text)
        
        # 移除首尾空格
        text = text.strip()
        
        return text
    
    def split_sentences(self, text: str, language: str = 'chinese') -> List[str]:
        """分句
        
        Args:
            text: 输入文本
            language: 语言类型，支持'chinese'和'english'
            
        Returns:
            List[str]: 句子列表
        """
        if language == 'chinese':
            # 中文分句（简单实现）
            # 使用中文句号、问号、感叹号等作为分句标志
            sentences = re.split(r'[。！？；；\n\r]', text)
            # 过滤空句子
            sentences = [s.strip() for s in sentences if s.strip()]
        elif language == 'english':
            # 英文分句
            sentences = sent_tokenize(text)
        else:
            raise ValueError(f"Unsupported language: {language}")
        
        return sentences
    
    def normalize_text(self, text: str, language: str = 'chinese') -> str:
        """文本标准化
        
        Args:
            text: 输入文本
            language: 语言类型，支持'chinese'和'english'
            
        Returns:
            str: 标准化后的文本
        """
        # 清理文本
        text = self.clean_text(text)
        
        # 转换为小写（仅对英文有效）
        if language == 'english':
            text = text.lower()
        
        return text
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """计算文本相似度（简单实现）
        
        Args:
            text1: 第一个文本
            text2: 第二个文本
            
        Returns:
            float: 相似度分数（0-1之间）
        """
        # 分词并移除停用词
        tokens1 = set(self.remove_stopwords(self.tokenize(text1)))
        tokens2 = set(self.remove_stopwords(self.tokenize(text2)))
        
        # 如果两个文本都为空，返回1.0
        if not tokens1 and not tokens2:
            return 1.0
        
        # 如果其中一个文本为空，返回0.0
        if not tokens1 or not tokens2:
            return 0.0
        
        # 计算Jaccard相似度
        intersection = len(tokens1 & tokens2)
        union = len(tokens1 | tokens2)
        similarity = intersection / union
        
        return similarity
    
    def extract_summary(self, text: str, num_sentences: int = 3) -> str:
        """提取文本摘要（简单实现）
        
        Args:
            text: 输入文本
            num_sentences: 摘要的句子数量
            
        Returns:
            str: 文本摘要
        """
        # 分句
        sentences = self.split_sentences(text)
        
        # 如果句子数量少于要求的摘要句子数量，直接返回原文
        if len(sentences) <= num_sentences:
            return text
        
        # 提取关键词
        keywords = self.extract_keywords(text, top_k=20)
        keyword_set = {word for word, _ in keywords}
        
        # 计算每个句子的得分（基于关键词出现频率）
        sentence_scores = []
        for i, sentence in enumerate(sentences):
            # 分词
            tokens = self.tokenize(sentence)
            # 计算句子得分
            score = sum(1 for token in tokens if token in keyword_set)
            sentence_scores.append((i, score))
        
        # 按照得分排序，选择前几个句子作为摘要
        sentence_scores.sort(key=lambda x: x[1], reverse=True)
        selected_indices = sorted([i for i, _ in sentence_scores[:num_sentences]])
        
        # 按照原顺序组织摘要
        summary = ' '.join([sentences[i] for i in selected_indices])
        
        return summary