// Reading enhancements; content and navigation also work without JavaScript.
document.querySelectorAll('.prose pre').forEach((pre) => {
  const wrapper = document.createElement('div');
  wrapper.className = 'code-wrap';
  pre.before(wrapper);
  wrapper.append(pre);
  const button = document.createElement('button');
  button.type = 'button';
  button.className = 'copy-button';
  button.textContent = '複製';
  button.setAttribute('aria-label', '複製程式碼');
  wrapper.append(button);
  button.addEventListener('click', async () => {
    const feedback = document.getElementById('copy-feedback');
    try {
      await navigator.clipboard.writeText(pre.querySelector('code')?.textContent ?? pre.textContent);
      button.textContent = '已複製';
      feedback.textContent = '已複製程式碼';
    } catch {
      button.textContent = '請手動選取';
      feedback.textContent = '無法使用剪貼簿，請選取程式碼後手動複製。';
    }
    window.setTimeout(() => { button.textContent = '複製'; }, 2000);
  });
});

const headings = [...document.querySelectorAll('.prose h2[id], .prose h3[id]')];
const tocLinks = [...document.querySelectorAll('.toc a')];
if (headings.length && 'IntersectionObserver' in window) {
  const markCurrent = (id) => {
    tocLinks.forEach((link) => {
      if (decodeURIComponent(link.hash.slice(1)) === id) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
  };
  markCurrent(headings[0].id);
  const observer = new IntersectionObserver(() => {
    const passed = headings.filter((heading) => heading.getBoundingClientRect().top <= 160);
    markCurrent((passed.at(-1) ?? headings[0]).id);
  }, { rootMargin: '-96px 0px -65% 0px', threshold: 0 });
  headings.forEach((heading) => observer.observe(heading));
}
