print("Starting test...")

try:
    import asyncio
    print("Asyncio imported")
    
    import sys
    sys.path.append('.')
    print("Path added")
    
    from modules.knowledge_base import KnowledgeBase
    print("KnowledgeBase imported")
    
    async def test():
        print("Test function started")
        kb = KnowledgeBase()
        print("KnowledgeBase created")
        
        await kb.initialize()
        print("KnowledgeBase initialized")
        
        test_item = {
            'title': '测试知识条目',
            'content': '这是一个测试内容',
            'category': '测试分类',
            'effective_date': '2025-06-05'
        }
        
        print('Testing add_item...')
        result = await kb.add_item(test_item)
        print('Result:', result)
        
        print('Getting all items...')
        items = await kb.get_all_items()
        print('Total items:', len(items))
    
    print("Running async test...")
    asyncio.run(test())
    print("Test completed")
    
except Exception as e:
    print('Error:', str(e))
    import traceback
    traceback.print_exc() 