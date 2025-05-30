// 通知面板控制
$(document).ready(function() {
    // 获取当前用户ID
    const userId = getCurrentUserId(); // 从session或cookie中获取

    // 加载通知和备忘录
    function loadNotifications() {
        // 加载提醒
        $.ajax({
            url: '/api/notifications',
            method: 'GET',
            success: function(response) {
                updateNotificationList(response.notifications);
            },
            error: function(xhr) {
                if (xhr.status === 401) {
                    window.location.href = '/auth/login';
                }
            }
        });

        // 加载用户备忘录
        $.ajax({
            url: '/api/memos',
            method: 'GET',
            data: { userId: userId },
            success: function(response) {
                updateMemoList(response.memos);
            },
            error: function(xhr) {
                if (xhr.status === 401) {
                    window.location.href = '/auth/login';
                }
            }
        });
    }

    // 更新通知列表
    function updateNotificationList(notifications) {
        const $list = $('.notification-list');
        $list.empty();
        
        notifications.forEach(notification => {
            $list.append(`
                <div class="notification-item">
                    <div class="notification-time">
                        <span class="date">${notification.date}</span>
                        <span class="time">${notification.time}</span>
                    </div>
                    <div class="notification-content">${notification.content}</div>
                </div>
            `);
        });
    }

    // 更新备忘录列表
    function updateMemoList(memos) {
        const $list = $('.memo-list');
        $list.empty();
        
        memos.forEach(memo => {
            $list.append(`
                <div class="memo-item">
                    <div class="memo-content">${memo.content}</div>
                    <div class="memo-time">${memo.time}</div>
                </div>
            `);
        });
    }

    // 保存备忘录
    $('.save-memo').click(function() {
        const title = $('.memo-title').val();
        const content = $('.memo-text').val();
        
        if (title && content) {
            $.ajax({
                url: '/api/memos',
                method: 'POST',
                data: {
                    userId: userId,
                    title: title,
                    content: content
                },
                success: function(response) {
                    if (response.success) {
                        // 重新加载备忘录列表
                        loadNotifications();
                        // 清空输入框
                        $('.memo-title').val('');
                        $('.memo-text').val('');
                    }
                }
            });
        } else {
            alert('请填写标题和内容');
        }
    });

    // 通知按钮点击事件
    $('.notification-btn').click(function(e) {
        e.stopPropagation();
        $('.notification-panel').slideToggle(200);
        // 每次打开通知面板时重新加载数据
        loadNotifications();
    });

    // 通知面板关闭按钮点击事件
    $('.notification-panel .close-btn').click(function() {
        $('.notification-panel').slideUp(200);
    });

    // 点击页面其他区域关闭通知面板
    $(document).click(function(e) {
        if (!$(e.target).closest('.notification-panel, .notification-btn').length) {
            $('.notification-panel').slideUp(200);
        }
    });

    // 初始化加载
    loadNotifications();
});

// 获取当前用户ID的辅助函数
function getCurrentUserId() {
    // 从session或cookie中获取用户ID
    // 这里需要根据你的实际用户认证系统来实现
    return document.cookie.match(/userId=([^;]+)/)?.[1] || '';
}

// 通知面板控制
$(document).ready(function() {
    // 显示通知面板
    $('.notification-button').click(function(e) {
        e.stopPropagation(); // 阻止事件冒泡
        $('.notification-panel').toggle();
    });

    // 关闭通知面板
    $('.close-notification').click(function() {
        $('.notification-panel').hide();
    });

    // 点击页面其他地方关闭通知面板
    $(document).click(function(e) {
        if (!$(e.target).closest('.notification-panel, .notification-button').length) {
            $('.notification-panel').hide();
        }
    });

    // 打开备忘录编辑器
    $('.add-memo').click(function() {
        $('#memo-title').val('');
        $('#memo-content').val('');
        $('.memo-editor').addClass('active');
    });

    // 关闭备忘录编辑器
    $('.close-editor, .cancel-btn').click(function() {
        $('.memo-editor').removeClass('active');
    });

    // 保存备忘录
    $('.save-btn').click(function() {
        saveMemo();
    });

    // 加载备忘录
    loadMemos();
});

// 保存备忘录到本地
function saveMemo() {
    const title = $('#memo-title').val().trim();
    const content = $('#memo-content').val().trim();
    
    if (title && content) {
        const memo = {
            id: new Date().getTime(),
            title: title,
            content: content,
            date: new Date().toISOString()
        };

        // 获取现有备忘录
        let memos = JSON.parse(localStorage.getItem('memos') || '[]');
        memos.push(memo);
        localStorage.setItem('memos', JSON.stringify(memos));

        // 清空输入框并关闭编辑器
        $('#memo-title').val('');
        $('#memo-content').val('');
        $('.memo-editor').removeClass('active');
        
        // 重新加载备忘录列表
        loadMemos();
    } else {
        alert('请输入标题和内容');
    }
}

// 加载备忘录
function loadMemos() {
    const memos = JSON.parse(localStorage.getItem('memos') || '[]');
    const memoList = $('.memo-list');
    memoList.empty();

    memos.forEach(memo => {
        const memoItem = $(`
            <div class="memo-item">
                <div class="memo-title">${memo.title}</div>
                <div class="memo-content">${memo.content}</div>
                <div class="memo-date">${new Date(memo.date).toLocaleString()}</div>
            </div>
        `);
        memoList.append(memoItem);
    });
}

// 点击通知项时显示完整内容
document.querySelectorAll('.notification-item').forEach(item => {
    item.addEventListener('click', function() {
        const content = this.querySelector('.notification-content');
        const fullContent = content.getAttribute('data-full-content');
        const time = this.querySelector('.notification-time').textContent;
        
        // 创建新窗口显示完整内容
        const detailWindow = window.open('', '_blank', 'width=600,height=400');
        detailWindow.document.write(`
            <html>
            <head>
                <title>通知详情</title>
                <style>
                    body { 
                        font-family: Arial, sans-serif;
                        padding: 20px;
                        line-height: 1.6;
                    }
                    .time { 
                        color: #666;
                        margin-bottom: 10px;
                    }
                    .content {
                        white-space: pre-wrap;
                        word-break: break-all;
                    }
                </style>
            </head>
            <body>
                <div class="time">${time}</div>
                <div class="content">${fullContent}</div>
            </body>
            </html>
        `);
    });
}); 