/*
 * main.js — Frontend enhancements para Trino
 *
 * 1. Paginación: clase Paginator / PostPaginator con botón "Cargar más"
 * 2. Skeletons: showSkeletons / hideSkeletons con shimmer animation
 * 3. Chat polling: ChatPoller con intervalo, cleanup en navigation, retry
 * 4. Image compression: compressImage via canvas, preserva PNG con transparencia
 * 5. Like button: micro-interacción pop + optimistic update
 * 6. Toast feedback: showToast para errores y éxito
 */

/* ─── Constants ─── */
const CHAT_POLL_INTERVAL = 5000;
const IMAGE_MAX_WIDTH = 1200;
const IMAGE_QUALITY = 0.7;

/* ─── 1. Pagination: "Cargar más" ─── */
class Paginator {
  constructor(containerSelector, buttonSelector) {
    this.container = document.querySelector(containerSelector);
    this.button = document.querySelector(buttonSelector);
    this.nextPageUrl = null;
    this.loading = false;
    if (this.button) {
      this.button.addEventListener('click', () => this.loadNextPage());
    }
  }

  setNextPage(url) {
    this.nextPageUrl = url;
    if (this.button) {
      this.button.classList.toggle('hidden', !url);
    }
  }

  async loadNextPage() {
    if (!this.nextPageUrl || this.loading) return;
    this.loading = true;
    if (this.button) {
      this.button.disabled = true;
      this.button.textContent = 'Cargando...';
    }
    try {
      const response = await fetch(this.nextPageUrl, { headers: { 'Accept': 'application/json' } });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();
      this.renderItems(data.results);
      this.setNextPage(data.next);
    } catch (err) {
      showToast('Error al cargar más publicaciones', 'error');
    } finally {
      this.loading = false;
      if (this.button) {
        this.button.disabled = false;
        this.button.textContent = 'Cargar más';
      }
    }
  }

  renderItems(items) {
    items.forEach(item => {
      const el = this.createItemElement(item);
      if (el) {
        this.container.appendChild(el);
        requestAnimationFrame(() => el.classList.add('fade-in'));
      }
    });
  }

  createItemElement(item) {
    return null;
  }
}

/* ─── Post Paginator (feed, profile, search) ─── */
class PostPaginator extends Paginator {
  createItemElement(post) {
    const template = document.getElementById('post-template');
    if (!template) return null;
    const clone = template.content.cloneNode(true);
    const article = clone.querySelector('.card');

    const avatar = clone.querySelector('.post-avatar');
    if (avatar) avatar.src = post.author?.avatar || '/static/img/default-avatar.svg';
    const author = clone.querySelector('.post-author');
    if (author) author.textContent = post.author?.username || 'Anónimo';
    const date = clone.querySelector('.post-date');
    if (date) date.textContent = post.created_at ? new Date(post.created_at).toLocaleDateString() : '';
    const content = clone.querySelector('.post-content');
    if (content) content.textContent = post.content;
    const img = clone.querySelector('.post-image');
    if (img && post.image) {
      img.src = post.image;
      img.classList.remove('hidden');
    }
    const likeBtn = clone.querySelector('.btn-like');
    if (likeBtn) {
      likeBtn.dataset.postId = post.id;
      likeBtn.dataset.liked = post.is_liked || false;
      if (post.is_liked) likeBtn.classList.add('liked');
      const count = clone.querySelector('.like-count');
      if (count) count.textContent = post.likes_count || 0;
      likeBtn.addEventListener('click', () => handleLike(likeBtn));
    }
    return article;
  }
}

/* ─── Search Paginator (reusa PostPaginator.createItemElement sin crear instancias) ─── */
class SearchPaginator extends Paginator {
  createItemElement(post) {
    return PostPaginator.prototype.createItemElement.call(this, post);
  }
}

/* ─── 2. Skeletons ─── */
function showSkeletons(container, count = 3) {
  const skeletonHTML = Array(count).fill(`
    <div class="post-skeleton">
      <div class="skeleton-avatar"></div>
      <div class="skeleton-line"></div>
      <div class="skeleton-line"></div>
      <div class="skeleton-line"></div>
      <div class="skeleton-image"></div>
    </div>
  `).join('');
  container.innerHTML = skeletonHTML;
}

function hideSkeletons(container) {
  container.querySelectorAll('.post-skeleton').forEach(el => el.remove());
}

/* ─── 3. Real-Time Chat Polling con cleanup y retry ─── */
class ChatPoller {
  constructor(chatAreaSelector, options = {}) {
    this.chatArea = document.querySelector(chatAreaSelector);
    this.messagesContainer = this.chatArea?.querySelector('.chat-messages');
    this.activeChatId = null;
    this.lastMessageId = null;
    this.intervalId = null;
    this.pollInterval = options.pollInterval || CHAT_POLL_INTERVAL;
    this.apiBase = options.apiBase || '/api/messages/';
    this.onNewMessages = options.onNewMessages || (() => {});
    this.retryDelay = 1000;
    this.maxRetryDelay = 30000;

    // Cleanup al salir de la página o cambiar visibilidad
    this._handleBeforeUnload = () => this.stop();
    this._handleVisibilityChange = () => {
      if (document.hidden) {
        this.stop();
      } else if (this.activeChatId) {
        this.start(this.activeChatId);
      }
    };
    window.addEventListener('beforeunload', this._handleBeforeUnload);
    document.addEventListener('visibilitychange', this._handleVisibilityChange);
  }

  start(chatId) {
    this.activeChatId = chatId;
    this.lastMessageId = this.getLastMessageId();
    this.retryDelay = 1000;
    if (this.intervalId) clearInterval(this.intervalId);
    this.intervalId = setInterval(() => this.poll(), this.pollInterval);
  }

  stop() {
    if (this.intervalId) {
      clearInterval(this.intervalId);
      this.intervalId = null;
    }
    this.activeChatId = null;
    this.retryDelay = 1000;
  }

  destroy() {
    this.stop();
    window.removeEventListener('beforeunload', this._handleBeforeUnload);
    document.removeEventListener('visibilitychange', this._handleVisibilityChange);
  }

  getLastMessageId() {
    if (!this.messagesContainer) return null;
    const msgs = this.messagesContainer.querySelectorAll('.message');
    const last = msgs[msgs.length - 1];
    return last ? last.dataset.messageId : null;
  }

  async poll() {
    if (!this.activeChatId) return;
    try {
      const since = this.lastMessageId ? `&since_id=${this.lastMessageId}` : '';
      const response = await fetch(`${this.apiBase}${this.activeChatId}/?format=json${since}`, {
        headers: { 'Accept': 'application/json' }
      });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      this.retryDelay = 1000;
      const data = await response.json();
      const messages = data.results || data;
      if (messages.length > 0) {
        this.appendMessages(messages);
        this.lastMessageId = messages[messages.length - 1].id;
        this.onNewMessages(messages);
      }
    } catch (err) {
      // Backoff exponencial para no saturar en caso de error
      this.retryDelay = Math.min(this.retryDelay * 2, this.maxRetryDelay);
      if (this.intervalId) {
        clearInterval(this.intervalId);
        this.intervalId = setInterval(() => this.poll(), this.retryDelay);
      }
    }
  }

  appendMessages(messages) {
    if (!this.messagesContainer) return;
    messages.forEach(msg => {
      if (this.messagesContainer.querySelector(`[data-message-id="${msg.id}"]`)) return;
      const el = document.createElement('div');
      el.className = `message ${msg.is_sender ? 'sent' : 'received'}`;
      el.dataset.messageId = msg.id;
      el.textContent = msg.content;
      this.messagesContainer.appendChild(el);
      requestAnimationFrame(() => el.classList.add('fade-in'));
    });
    this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
  }
}

/* ─── 4. Client-side Image Compression (preserva PNG con transparencia) ─── */
function compressImage(file, maxWidth = IMAGE_MAX_WIDTH, quality = IMAGE_QUALITY) {
  return new Promise((resolve, reject) => {
    if (!file.type.startsWith('image/')) {
      resolve(file);
      return;
    }
    const reader = new FileReader();
    reader.onload = (e) => {
      const img = new Image();
      img.onload = () => {
        const canvas = document.createElement('canvas');
        let { width, height } = img;
        if (width > maxWidth) {
          height = Math.round((height * maxWidth) / width);
          width = maxWidth;
        }
        canvas.width = width;
        canvas.height = height;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(img, 0, 0, width, height);
        // Preserva PNG si el original tiene transparencia, sino JPEG
        const outputType = (file.type === 'image/png') ? 'image/png' : 'image/jpeg';
        canvas.toBlob((blob) => {
          if (!blob) { resolve(file); return; }
          const ext = outputType === 'image/png' ? '.png' : '.jpg';
          const compressedFile = new File([blob], file.name.replace(/\.[^.]+$/, ext), {
            type: outputType,
            lastModified: Date.now(),
          });
          resolve(compressedFile);
        }, outputType, quality);
      };
      img.onerror = () => reject(new Error('Error al cargar la imagen'));
      img.src = e.target.result;
    };
    reader.onerror = () => reject(new Error('Error al leer el archivo'));
    reader.readAsDataURL(file);
  });
}

/* ─── 5. Like Button Micro-interaction con optimistic update ─── */
async function handleLike(btn) {
  btn.classList.add('pop');
  setTimeout(() => btn.classList.remove('pop'), 350);

  const postId = btn.dataset.postId;
  const isLiked = btn.dataset.liked === 'true';
  const countEl = btn.querySelector('.like-count');
  const currentCount = parseInt(countEl?.textContent || '0');

  // Optimistic update
  btn.dataset.liked = (!isLiked).toString();
  btn.classList.toggle('liked', !isLiked);
  if (countEl) countEl.textContent = isLiked ? currentCount - 1 : currentCount + 1;

  try {
    const response = await fetch('/api/interactions/like/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken(),
      },
      body: JSON.stringify({ post_id: postId, action: isLiked ? 'unlike' : 'like' }),
    });
    if (!response.ok) throw new Error('Error en like');
  } catch {
    // Revertir optimistic update si falla
    btn.dataset.liked = isLiked.toString();
    btn.classList.toggle('liked', isLiked);
    if (countEl) countEl.textContent = currentCount;
    showToast('Error al actualizar like', 'error');
  }
}

/* ─── 6. Toast feedback system ─── */
function showToast(message, type = 'info') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    container.style.cssText =
      'position:fixed;top:1rem;right:1rem;z-index:9999;display:flex;flex-direction:column;gap:0.5rem;';
    document.body.appendChild(container);
  }
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.textContent = message;
  toast.style.cssText =
    'padding:0.75rem 1.25rem;border-radius:8px;color:#fff;font-weight:600;' +
    'box-shadow:0 4px 12px rgba(0,0,0,0.15);animation:slideInToast 0.3s ease forwards;' +
    'max-width:360px;word-wrap:break-word;';
  if (type === 'error') toast.style.background = '#ff4757';
  else if (type === 'success') toast.style.background = '#2ed573';
  else toast.style.background = '#6c63ff';
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.animation = 'slideOutToast 0.3s ease forwards';
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

/* ─── Helpers ─── */
function getCSRFToken() {
  const meta = document.querySelector('meta[name="csrf-token"]');
  return meta ? meta.getAttribute('content') : '';
}

/* ─── Init on DOM ready ─── */
document.addEventListener('DOMContentLoaded', () => {
  const loadMoreBtn = document.querySelector('.btn-load-more');
  const postsContainer = document.querySelector('.posts-container');

  if (postsContainer && loadMoreBtn) {
    const paginator = new PostPaginator('.posts-container', '.btn-load-more');
    const nextUrl = loadMoreBtn.dataset.nextUrl || null;
    paginator.setNextPage(nextUrl);
    window.paginator = paginator;
  }
});
