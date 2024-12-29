document.addEventListener('DOMContentLoaded', function() {
    // 处理点赞按钮点击
    document.querySelectorAll('.like-btn').forEach(button => {
        button.addEventListener('click', function() {
            const postId = this.dataset.postId;
            const likeCount = this.querySelector('.like-count');

            // 发送点赞请求
            fetch(`/like/${postId}`, { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        likeCount.textContent = data.likes;
                    }
                });
        });
    });
});