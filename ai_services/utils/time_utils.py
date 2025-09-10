#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""时间工具"""

import time
import datetime
from typing import Optional, Union, Dict, Any, List
from dateutil import parser
from dateutil.relativedelta import relativedelta


class TimeUtils:
    """时间工具类"""
    
    # 默认日期时间格式
    DEFAULT_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
    DEFAULT_DATE_FORMAT = '%Y-%m-%d'
    DEFAULT_TIME_FORMAT = '%H:%M:%S'
    
    @staticmethod
    def now() -> datetime.datetime:
        """获取当前日期时间
        
        Returns:
            datetime.datetime: 当前日期时间
        """
        return datetime.datetime.now()
    
    @staticmethod
    def today() -> datetime.date:
        """获取今天的日期
        
        Returns:
            datetime.date: 今天的日期
        """
        return datetime.date.today()
    
    @staticmethod
    def yesterday() -> datetime.date:
        """获取昨天的日期
        
        Returns:
            datetime.date: 昨天的日期
        """
        return TimeUtils.today() - datetime.timedelta(days=1)
    
    @staticmethod
    def tomorrow() -> datetime.date:
        """获取明天的日期
        
        Returns:
            datetime.date: 明天的日期
        """
        return TimeUtils.today() + datetime.timedelta(days=1)
    
    @staticmethod
    def format_datetime(
        dt: Union[datetime.datetime, datetime.date, str, int, float],
        fmt: Optional[str] = None
    ) -> str:
        """格式化日期时间
        
        Args:
            dt: 日期时间对象或可解析的日期时间字符串、时间戳
            fmt: 格式化字符串，默认使用DEFAULT_DATETIME_FORMAT
            
        Returns:
            str: 格式化后的日期时间字符串
        """
        # 如果未指定格式，根据输入类型选择默认格式
        if fmt is None:
            if isinstance(dt, datetime.date) and not isinstance(dt, datetime.datetime):
                fmt = TimeUtils.DEFAULT_DATE_FORMAT
            else:
                fmt = TimeUtils.DEFAULT_DATETIME_FORMAT
        
        # 转换为datetime对象
        if isinstance(dt, (int, float)):
            dt = datetime.datetime.fromtimestamp(dt)
        elif isinstance(dt, str):
            dt = TimeUtils.parse_datetime(dt)
        
        # 格式化
        if isinstance(dt, datetime.datetime):
            return dt.strftime(fmt)
        elif isinstance(dt, datetime.date):
            return dt.strftime(fmt)
        else:
            raise TypeError(f"Cannot format {type(dt)} to string")
    
    @staticmethod
    def parse_datetime(
        dt_str: str,
        default: Optional[datetime.datetime] = None
    ) -> datetime.datetime:
        """解析日期时间字符串
        
        Args:
            dt_str: 日期时间字符串
            default: 解析失败时的默认值
            
        Returns:
            datetime.datetime: 解析后的日期时间对象
        """
        try:
            return parser.parse(dt_str)
        except ValueError:
            if default is not None:
                return default
            raise
    
    @staticmethod
    def to_timestamp(
        dt: Union[datetime.datetime, datetime.date, str]
    ) -> float:
        """转换为时间戳
        
        Args:
            dt: 日期时间对象或字符串
            
        Returns:
            float: 时间戳
        """
        if isinstance(dt, (int, float)):
            return dt
        elif isinstance(dt, str):
            dt = TimeUtils.parse_datetime(dt)
        
        if isinstance(dt, datetime.datetime):
            return dt.timestamp()
        elif isinstance(dt, datetime.date):
            # 转换日期为当天的0点
            return datetime.datetime.combine(dt, datetime.time.min).timestamp()
        else:
            raise TypeError(f"Cannot convert {type(dt)} to timestamp")
    
    @staticmethod
    def from_timestamp(ts: float) -> datetime.datetime:
        """从时间戳转换为日期时间对象
        
        Args:
            ts: 时间戳
            
        Returns:
            datetime.datetime: 日期时间对象
        """
        return datetime.datetime.fromtimestamp(ts)
    
    @staticmethod
    def add_days(
        dt: Union[datetime.datetime, datetime.date, str],
        days: int
    ) -> Union[datetime.datetime, datetime.date]:
        """添加天数
        
        Args:
            dt: 日期时间对象或字符串
            days: 要添加的天数
            
        Returns:
            Union[datetime.datetime, datetime.date]: 添加后的日期时间对象
        """
        if isinstance(dt, str):
            dt = TimeUtils.parse_datetime(dt)
        
        delta = datetime.timedelta(days=days)
        return dt + delta
    
    @staticmethod
    def add_hours(
        dt: Union[datetime.datetime, str],
        hours: int
    ) -> datetime.datetime:
        """添加小时数
        
        Args:
            dt: 日期时间对象或字符串
            hours: 要添加的小时数
            
        Returns:
            datetime.datetime: 添加后的日期时间对象
        """
        if isinstance(dt, str):
            dt = TimeUtils.parse_datetime(dt)
        
        delta = datetime.timedelta(hours=hours)
        return dt + delta
    
    @staticmethod
    def add_minutes(
        dt: Union[datetime.datetime, str],
        minutes: int
    ) -> datetime.datetime:
        """添加分钟数
        
        Args:
            dt: 日期时间对象或字符串
            minutes: 要添加的分钟数
            
        Returns:
            datetime.datetime: 添加后的日期时间对象
        """
        if isinstance(dt, str):
            dt = TimeUtils.parse_datetime(dt)
        
        delta = datetime.timedelta(minutes=minutes)
        return dt + delta
    
    @staticmethod
    def add_months(
        dt: Union[datetime.datetime, datetime.date, str],
        months: int
    ) -> Union[datetime.datetime, datetime.date]:
        """添加月数
        
        Args:
            dt: 日期时间对象或字符串
            months: 要添加的月数
            
        Returns:
            Union[datetime.datetime, datetime.date]: 添加后的日期时间对象
        """
        if isinstance(dt, str):
            dt = TimeUtils.parse_datetime(dt)
        
        return dt + relativedelta(months=months)
    
    @staticmethod
    def add_years(
        dt: Union[datetime.datetime, datetime.date, str],
        years: int
    ) -> Union[datetime.datetime, datetime.date]:
        """添加年数
        
        Args:
            dt: 日期时间对象或字符串
            years: 要添加的年数
            
        Returns:
            Union[datetime.datetime, datetime.date]: 添加后的日期时间对象
        """
        if isinstance(dt, str):
            dt = TimeUtils.parse_datetime(dt)
        
        return dt + relativedelta(years=years)
    
    @staticmethod
    def get_time_diff(
        start_time: Union[datetime.datetime, str],
        end_time: Union[datetime.datetime, str]
    ) -> Dict[str, float]:
        """计算两个时间之间的差异
        
        Args:
            start_time: 开始时间
            end_time: 结束时间
            
        Returns:
            Dict[str, float]: 包含各种时间单位差异的字典
        """
        if isinstance(start_time, str):
            start_time = TimeUtils.parse_datetime(start_time)
        if isinstance(end_time, str):
            end_time = TimeUtils.parse_datetime(end_time)
        
        diff = end_time - start_time
        total_seconds = diff.total_seconds()
        
        return {
            'days': total_seconds / (24 * 3600),
            'hours': total_seconds / 3600,
            'minutes': total_seconds / 60,
            'seconds': total_seconds,
            'milliseconds': total_seconds * 1000
        }
    
    @staticmethod
    def is_between(
        dt: Union[datetime.datetime, datetime.date, str],
        start_time: Union[datetime.datetime, datetime.date, str],
        end_time: Union[datetime.datetime, datetime.date, str]
    ) -> bool:
        """检查时间是否在指定范围内
        
        Args:
            dt: 要检查的时间
            start_time: 开始时间
            end_time: 结束时间
            
        Returns:
            bool: 是否在范围内
        """
        if isinstance(dt, str):
            dt = TimeUtils.parse_datetime(dt)
        if isinstance(start_time, str):
            start_time = TimeUtils.parse_datetime(start_time)
        if isinstance(end_time, str):
            end_time = TimeUtils.parse_datetime(end_time)
        
        # 确保类型一致
        if isinstance(dt, datetime.date) and not isinstance(dt, datetime.datetime):
            if isinstance(start_time, datetime.datetime):
                start_time = start_time.date()
            if isinstance(end_time, datetime.datetime):
                end_time = end_time.date()
        
        return start_time <= dt <= end_time
    
    @staticmethod
    def get_week_start(
        dt: Union[datetime.datetime, datetime.date, str]
    ) -> Union[datetime.datetime, datetime.date]:
        """获取当前时间所在周的开始（周一）
        
        Args:
            dt: 日期时间对象或字符串
            
        Returns:
            Union[datetime.datetime, datetime.date]: 周开始时间
        """
        if isinstance(dt, str):
            dt = TimeUtils.parse_datetime(dt)
        
        # 计算距离周一的天数差
        days_since_monday = dt.weekday()  # 0表示周一，6表示周日
        delta = datetime.timedelta(days=days_since_monday)
        
        if isinstance(dt, datetime.datetime):
            return (dt - delta).replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            return dt - delta
    
    @staticmethod
    def get_week_end(
        dt: Union[datetime.datetime, datetime.date, str]
    ) -> Union[datetime.datetime, datetime.date]:
        """获取当前时间所在周的结束（周日）
        
        Args:
            dt: 日期时间对象或字符串
            
        Returns:
            Union[datetime.datetime, datetime.date]: 周结束时间
        """
        if isinstance(dt, str):
            dt = TimeUtils.parse_datetime(dt)
        
        # 计算距离周日的天数差
        days_until_sunday = 6 - dt.weekday()  # 0表示周一，6表示周日
        delta = datetime.timedelta(days=days_until_sunday)
        
        if isinstance(dt, datetime.datetime):
            return (dt + delta).replace(hour=23, minute=59, second=59, microsecond=999999)
        else:
            return dt + delta
    
    @staticmethod
    def get_month_start(
        dt: Union[datetime.datetime, datetime.date, str]
    ) -> Union[datetime.datetime, datetime.date]:
        """获取当前时间所在月的开始
        
        Args:
            dt: 日期时间对象或字符串
            
        Returns:
            Union[datetime.datetime, datetime.date]: 月开始时间
        """
        if isinstance(dt, str):
            dt = TimeUtils.parse_datetime(dt)
        
        if isinstance(dt, datetime.datetime):
            return dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        else:
            return dt.replace(day=1)
    
    @staticmethod
    def get_month_end(
        dt: Union[datetime.datetime, datetime.date, str]
    ) -> Union[datetime.datetime, datetime.date]:
        """获取当前时间所在月的结束
        
        Args:
            dt: 日期时间对象或字符串
            
        Returns:
            Union[datetime.datetime, datetime.date]: 月结束时间
        """
        if isinstance(dt, str):
            dt = TimeUtils.parse_datetime(dt)
        
        # 获取下个月的第一天
        if isinstance(dt, datetime.datetime):
            next_month = dt.replace(day=28) + datetime.timedelta(days=4)  # 确保进入下个月
            last_day = next_month - datetime.timedelta(days=next_month.day)
            return last_day.replace(hour=23, minute=59, second=59, microsecond=999999)
        else:
            next_month = dt.replace(day=28) + datetime.timedelta(days=4)  # 确保进入下个月
            return next_month - datetime.timedelta(days=next_month.day)
    
    @staticmethod
    def get_year_start(
        dt: Union[datetime.datetime, datetime.date, str]
    ) -> Union[datetime.datetime, datetime.date]:
        """获取当前时间所在年的开始
        
        Args:
            dt: 日期时间对象或字符串
            
        Returns:
            Union[datetime.datetime, datetime.date]: 年开始时间
        """
        if isinstance(dt, str):
            dt = TimeUtils.parse_datetime(dt)
        
        if isinstance(dt, datetime.datetime):
            return dt.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        else:
            return dt.replace(month=1, day=1)
    
    @staticmethod
    def get_year_end(
        dt: Union[datetime.datetime, datetime.date, str]
    ) -> Union[datetime.datetime, datetime.date]:
        """获取当前时间所在年的结束
        
        Args:
            dt: 日期时间对象或字符串
            
        Returns:
            Union[datetime.datetime, datetime.date]: 年结束时间
        """
        if isinstance(dt, str):
            dt = TimeUtils.parse_datetime(dt)
        
        if isinstance(dt, datetime.datetime):
            return dt.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)
        else:
            return dt.replace(month=12, day=31)
    
    @staticmethod
    def generate_time_range(
        start_time: Union[datetime.datetime, str],
        end_time: Union[datetime.datetime, str],
        step: Union[int, float, datetime.timedelta] = 1,
        unit: str = 'days'
    ) -> List[datetime.datetime]:
        """生成时间范围内的时间点列表
        
        Args:
            start_time: 开始时间
            end_time: 结束时间
            step: 步长
            unit: 步长单位，支持 'days', 'hours', 'minutes', 'seconds'
            
        Returns:
            List[datetime.datetime]: 时间点列表
        """
        if isinstance(start_time, str):
            start_time = TimeUtils.parse_datetime(start_time)
        if isinstance(end_time, str):
            end_time = TimeUtils.parse_datetime(end_time)
        
        # 确定步长
        if isinstance(step, datetime.timedelta):
            delta = step
        else:
            if unit == 'days':
                delta = datetime.timedelta(days=step)
            elif unit == 'hours':
                delta = datetime.timedelta(hours=step)
            elif unit == 'minutes':
                delta = datetime.timedelta(minutes=step)
            elif unit == 'seconds':
                delta = datetime.timedelta(seconds=step)
            else:
                raise ValueError(f"Unsupported unit: {unit}")
        
        # 生成时间点列表
        time_points = []
        current_time = start_time
        while current_time <= end_time:
            time_points.append(current_time)
            current_time += delta
        
        return time_points
    
    @staticmethod
    def get_age(
        birth_date: Union[datetime.date, str],
        current_date: Optional[Union[datetime.date, str]] = None
    ) -> int:
        """计算年龄
        
        Args:
            birth_date: 出生日期
            current_date: 当前日期，默认为今天
            
        Returns:
            int: 年龄
        """
        if isinstance(birth_date, str):
            birth_date = TimeUtils.parse_datetime(birth_date).date()
        
        if current_date is None:
            current_date = TimeUtils.today()
        elif isinstance(current_date, str):
            current_date = TimeUtils.parse_datetime(current_date).date()
        
        # 计算年龄
        age = current_date.year - birth_date.year
        
        # 如果当前日期还没过生日，年龄减1
        if (current_date.month, current_date.day) < (birth_date.month, birth_date.day):
            age -= 1
        
        return age
    
    @staticmethod
    def format_duration(seconds: float) -> str:
        """格式化持续时间
        
        Args:
            seconds: 秒数
            
        Returns:
            str: 格式化的持续时间字符串
        """
        if seconds < 60:
            return f"{seconds:.2f}s"
        elif seconds < 3600:
            minutes, seconds = divmod(seconds, 60)
            return f"{int(minutes)}m {int(seconds)}s"
        elif seconds < 86400:
            hours, remainder = divmod(seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"
        else:
            days, remainder = divmod(seconds, 86400)
            hours, remainder = divmod(remainder, 3600)
            minutes, seconds = divmod(remainder, 60)
            return f"{int(days)}d {int(hours)}h {int(minutes)}m {int(seconds)}s"

# 创建全局时间工具实例
global_time_utils = TimeUtils()

# 便捷函数
def now() -> datetime.datetime:
    """获取当前日期时间（便捷函数）"""
    return global_time_utils.now()

def today() -> datetime.date:
    """获取今天的日期（便捷函数）"""
    return global_time_utils.today()

def yesterday() -> datetime.date:
    """获取昨天的日期（便捷函数）"""
    return global_time_utils.yesterday()

def tomorrow() -> datetime.date:
    """获取明天的日期（便捷函数）"""
    return global_time_utils.tomorrow()

def format_datetime(
    dt: Union[datetime.datetime, datetime.date, str, int, float],
    fmt: Optional[str] = None
) -> str:
    """格式化日期时间（便捷函数）"""
    return global_time_utils.format_datetime(dt, fmt)

def parse_datetime(
    dt_str: str,
    default: Optional[datetime.datetime] = None
) -> datetime.datetime:
    """解析日期时间字符串（便捷函数）"""
    return global_time_utils.parse_datetime(dt_str, default)

def to_timestamp(
    dt: Union[datetime.datetime, datetime.date, str]
) -> float:
    """转换为时间戳（便捷函数）"""
    return global_time_utils.to_timestamp(dt)

def from_timestamp(ts: float) -> datetime.datetime:
    """从时间戳转换为日期时间对象（便捷函数）"""
    return global_time_utils.from_timestamp(ts)

def add_days(
    dt: Union[datetime.datetime, datetime.date, str],
    days: int
) -> Union[datetime.datetime, datetime.date]:
    """添加天数（便捷函数）"""
    return global_time_utils.add_days(dt, days)

def add_hours(
    dt: Union[datetime.datetime, str],
    hours: int
) -> datetime.datetime:
    """添加小时数（便捷函数）"""
    return global_time_utils.add_hours(dt, hours)

def add_minutes(
    dt: Union[datetime.datetime, str],
    minutes: int
) -> datetime.datetime:
    """添加分钟数（便捷函数）"""
    return global_time_utils.add_minutes(dt, minutes)

def add_months(
    dt: Union[datetime.datetime, datetime.date, str],
    months: int
) -> Union[datetime.datetime, datetime.date]:
    """添加月数（便捷函数）"""
    return global_time_utils.add_months(dt, months)

def add_years(
    dt: Union[datetime.datetime, datetime.date, str],
    years: int
) -> Union[datetime.datetime, datetime.date]:
    """添加年数（便捷函数）"""
    return global_time_utils.add_years(dt, years)

def get_time_diff(
    start_time: Union[datetime.datetime, str],
    end_time: Union[datetime.datetime, str]
) -> Dict[str, float]:
    """计算两个时间之间的差异（便捷函数）"""
    return global_time_utils.get_time_diff(start_time, end_time)

def is_between(
    dt: Union[datetime.datetime, datetime.date, str],
    start_time: Union[datetime.datetime, datetime.date, str],
    end_time: Union[datetime.datetime, datetime.date, str]
) -> bool:
    """检查时间是否在指定范围内（便捷函数）"""
    return global_time_utils.is_between(dt, start_time, end_time)

def get_week_start(
    dt: Union[datetime.datetime, datetime.date, str]
) -> Union[datetime.datetime, datetime.date]:
    """获取当前时间所在周的开始（周一）（便捷函数）"""
    return global_time_utils.get_week_start(dt)

def get_week_end(
    dt: Union[datetime.datetime, datetime.date, str]
) -> Union[datetime.datetime, datetime.date]:
    """获取当前时间所在周的结束（周日）（便捷函数）"""
    return global_time_utils.get_week_end(dt)

def get_month_start(
    dt: Union[datetime.datetime, datetime.date, str]
) -> Union[datetime.datetime, datetime.date]:
    """获取当前时间所在月的开始（便捷函数）"""
    return global_time_utils.get_month_start(dt)

def get_month_end(
    dt: Union[datetime.datetime, datetime.date, str]
) -> Union[datetime.datetime, datetime.date]:
    """获取当前时间所在月的结束（便捷函数）"""
    return global_time_utils.get_month_end(dt)

def get_year_start(
    dt: Union[datetime.datetime, datetime.date, str]
) -> Union[datetime.datetime, datetime.date]:
    """获取当前时间所在年的开始（便捷函数）"""
    return global_time_utils.get_year_start(dt)

def get_year_end(
    dt: Union[datetime.datetime, datetime.date, str]
) -> Union[datetime.datetime, datetime.date]:
    """获取当前时间所在年的结束（便捷函数）"""
    return global_time_utils.get_year_end(dt)

def generate_time_range(
    start_time: Union[datetime.datetime, str],
    end_time: Union[datetime.datetime, str],
    step: Union[int, float, datetime.timedelta] = 1,
    unit: str = 'days'
) -> List[datetime.datetime]:
    """生成时间范围内的时间点列表（便捷函数）"""
    return global_time_utils.generate_time_range(start_time, end_time, step, unit)

def get_age(
    birth_date: Union[datetime.date, str],
    current_date: Optional[Union[datetime.date, str]] = None
) -> int:
    """计算年龄（便捷函数）"""
    return global_time_utils.get_age(birth_date, current_date)

def format_duration(seconds: float) -> str:
    """格式化持续时间（便捷函数）"""
    return global_time_utils.format_duration(seconds)