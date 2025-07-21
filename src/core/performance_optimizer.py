"""
Performance Optimization Module for TalentScout Hiring Assistant
Implements async processing, caching, and performance monitoring
"""

import asyncio
import time
import json
from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass, asdict
from functools import wraps
import hashlib
from datetime import datetime, timedelta

@dataclass
class PerformanceMetrics:
    """Performance metrics tracking"""
    response_time: float
    cache_hit: bool
    memory_usage: float
    timestamp: datetime
    operation_type: str

class ResponseCache:
    """Intelligent caching system for common responses and questions"""
    
    def __init__(self, max_size: int = 1000, ttl_hours: int = 24):
        self.cache = {}
        self.access_times = {}
        self.max_size = max_size
        self.ttl = timedelta(hours=ttl_hours)
        
    def _generate_key(self, data: Any) -> str:
        """Generate cache key from input data"""
        if isinstance(data, dict):
            data_str = json.dumps(data, sort_keys=True)
        else:
            data_str = str(data)
        return hashlib.md5(data_str.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """Get item from cache if not expired"""
        if key not in self.cache:
            return None
            
        access_time = self.access_times.get(key, datetime.min)
        if datetime.now() - access_time > self.ttl:
            # Expired, remove from cache
            del self.cache[key]
            del self.access_times[key]
            return None
            
        # Update access time
        self.access_times[key] = datetime.now()
        return self.cache[key]
    
    def set(self, key: str, value: Any) -> None:
        """Set item in cache with LRU eviction if needed"""
        # Remove oldest items if cache is full
        if len(self.cache) >= self.max_size:
            oldest_key = min(self.access_times, key=self.access_times.get)
            del self.cache[oldest_key]
            del self.access_times[oldest_key]
        
        self.cache[key] = value
        self.access_times[key] = datetime.now()
    
    def cache_response(self, input_data: Any) -> Callable:
        """Decorator for caching function responses"""
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Generate cache key from function name and arguments
                cache_data = {
                    'func': func.__name__,
                    'args': args,
                    'kwargs': kwargs,
                    'input_data': input_data
                }
                cache_key = self._generate_key(cache_data)
                
                # Try to get from cache
                cached_result = self.get(cache_key)
                if cached_result is not None:
                    return cached_result
                
                # Execute function and cache result
                result = func(*args, **kwargs)
                self.set(cache_key, result)
                return result
            return wrapper
        return decorator

class AsyncChatbot:
    """Asynchronous chatbot for improved performance"""
    
    def __init__(self, base_chatbot, cache: ResponseCache):
        self.base_chatbot = base_chatbot
        self.cache = cache
        self.performance_metrics = []
        
    async def generate_response_async(self, user_input: str, context: Dict[str, Any]) -> str:
        """Generate response asynchronously with caching"""
        start_time = time.time()
        
        # Check cache first
        cache_key = self.cache._generate_key({
            'input': user_input,
            'context': context,
            'type': 'response'
        })
        
        cached_response = self.cache.get(cache_key)
        if cached_response:
            response_time = time.time() - start_time
            self._record_metrics(response_time, True, 'response_generation')
            return cached_response
        
        # Generate new response asynchronously
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None, 
            self.base_chatbot.generate_response, 
            user_input, 
            context
        )
        
        # Cache the response
        self.cache.set(cache_key, response)
        
        response_time = time.time() - start_time
        self._record_metrics(response_time, False, 'response_generation')
        
        return response
    
    async def generate_tech_questions_async(self, tech_stack: List[str]) -> List[str]:
        """Generate technical questions asynchronously with caching"""
        start_time = time.time()
        
        # Check cache for similar tech stacks
        cache_key = self.cache._generate_key({
            'tech_stack': sorted(tech_stack),
            'type': 'tech_questions'
        })
        
        cached_questions = self.cache.get(cache_key)
        if cached_questions:
            response_time = time.time() - start_time
            self._record_metrics(response_time, True, 'question_generation')
            return cached_questions
        
        # Generate new questions asynchronously
        loop = asyncio.get_event_loop()
        questions = await loop.run_in_executor(
            None,
            self.base_chatbot.generate_technical_questions,
            tech_stack
        )
        
        # Cache the questions
        self.cache.set(cache_key, questions)
        
        response_time = time.time() - start_time
        self._record_metrics(response_time, False, 'question_generation')
        
        return questions
    
    async def save_data_background(self, data: Dict[str, Any], data_handler) -> None:
        """Save data in background without blocking UI"""
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            data_handler.save_candidate_info,
            data
        )
    
    def _record_metrics(self, response_time: float, cache_hit: bool, operation_type: str) -> None:
        """Record performance metrics"""
        metrics = PerformanceMetrics(
            response_time=response_time,
            cache_hit=cache_hit,
            memory_usage=0.0,  # Could implement actual memory monitoring
            timestamp=datetime.now(),
            operation_type=operation_type
        )
        self.performance_metrics.append(metrics)
        
        # Keep only recent metrics (last 100)
        if len(self.performance_metrics) > 100:
            self.performance_metrics = self.performance_metrics[-100:]
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics"""
        if not self.performance_metrics:
            return {}
        
        response_times = [m.response_time for m in self.performance_metrics]
        cache_hits = [m.cache_hit for m in self.performance_metrics]
        
        return {
            'avg_response_time': sum(response_times) / len(response_times),
            'max_response_time': max(response_times),
            'min_response_time': min(response_times),
            'cache_hit_rate': sum(cache_hits) / len(cache_hits),
            'total_requests': len(self.performance_metrics),
            'recent_requests': len([m for m in self.performance_metrics 
                                  if datetime.now() - m.timestamp < timedelta(minutes=10)])
        }

class PreloadedQuestionBank:
    """Pre-generated question bank for common technologies"""
    
    def __init__(self):
        self.question_bank = {
            'python': [
                "Explain the difference between lists and tuples in Python.",
                "How does Python's garbage collection work?",
                "What are decorators and how would you implement one?",
                "Explain the concept of list comprehensions with an example.",
                "What is the difference between `is` and `==` in Python?"
            ],
            'javascript': [
                "Explain the concept of closures in JavaScript.",
                "What is the difference between `var`, `let`, and `const`?",
                "How does the event loop work in JavaScript?",
                "Explain prototypal inheritance in JavaScript.",
                "What are Promises and how do they differ from callbacks?"
            ],
            'react': [
                "What is the difference between state and props in React?",
                "Explain the React component lifecycle methods.",
                "What are React Hooks and why were they introduced?",
                "How does Virtual DOM work in React?",
                "Explain the concept of React Context API."
            ],
            'sql': [
                "Explain the difference between INNER JOIN and LEFT JOIN.",
                "What is database normalization and why is it important?",
                "How would you optimize a slow SQL query?",
                "Explain the concept of database indexing.",
                "What are stored procedures and when would you use them?"
            ]
        }
    
    def get_questions(self, technology: str, count: int = 3) -> List[str]:
        """Get pre-loaded questions for a technology"""
        tech_lower = technology.lower()
        
        # Find matching technology
        for tech_key, questions in self.question_bank.items():
            if tech_key in tech_lower or tech_lower in tech_key:
                return questions[:count]
        
        return []  # No pre-loaded questions available
    
    def get_all_supported_technologies(self) -> List[str]:
        """Get list of all supported technologies"""
        return list(self.question_bank.keys())

def performance_monitor(func: Callable) -> Callable:
    """Decorator to monitor function performance"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            success = True
        except Exception as e:
            result = None
            success = False
            raise e
        finally:
            end_time = time.time()
            execution_time = end_time - start_time
            
            # Log performance metrics
            print(f"Function {func.__name__} executed in {execution_time:.3f}s - Success: {success}")
        
        return result
    return wrapper

# Example usage for Streamlit integration
def create_optimized_chatbot(base_chatbot):
    """Factory function to create optimized chatbot"""
    cache = ResponseCache(max_size=500, ttl_hours=12)
    async_chatbot = AsyncChatbot(base_chatbot, cache)
    question_bank = PreloadedQuestionBank()
    
    return {
        'async_chatbot': async_chatbot,
        'cache': cache,
        'question_bank': question_bank
    }

if __name__ == "__main__":
    # Performance testing
    cache = ResponseCache()
    
    # Test caching
    @cache.cache_response("test_input")
    def slow_function(x):
        time.sleep(0.1)  # Simulate slow operation
        return f"Result for {x}"
    
    # First call (uncached)
    start = time.time()
    result1 = slow_function("test")
    print(f"First call: {time.time() - start:.3f}s")
    
    # Second call (cached)
    start = time.time()
    result2 = slow_function("test")
    print(f"Second call: {time.time() - start:.3f}s")
    
    print(f"Results match: {result1 == result2}")
