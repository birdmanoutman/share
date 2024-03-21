// 函数用于转换特定的链接
function convertMyAppLinks() {
    document.querySelectorAll('a,span,div').forEach(link => {
        const url = link.getAttribute('href') || link.innerText;
        if (url && url.startsWith('myapp://')) {
            // 创建一个新的a标签包裹原文本或链接，使其可点击
            const newLink = document.createElement('a');
            newLink.href = url;
            newLink.innerText = link.innerText;
            if (link.parentNode) {
                link.parentNode.replaceChild(newLink, link);
            }
        }
    });
}

// 使用MutationObserver来应对动态内容
const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
        if (mutation.type === 'childList') {
            convertMyAppLinks();
        }
    });
});

// 配置观察器:
const config = {attributes: true, childList: true, subtree: true};

// 选择目标节点
const targetNode = document.body;

// 开始观察目标节点
observer.observe(targetNode, config);

// 初始转换
convertMyAppLinks();
