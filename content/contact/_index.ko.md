---
title: "문의하기"
description: "JE Tech Holdings에 문의하세요"
date: 2024-01-01
layout: "simple"
---

<div class="contact-form-container">
  <p class="text-lg mb-6">질문이 있거나 프로젝트에 대해 논의하고 싶으신가요? 아래 양식을 작성해 주시면 24시간 이내에 연락드리겠습니다.</p>
  
  <form id="contact-form" action="https://formspree.io/f/xqedkeja" method="POST" class="space-y-4">
    
    <div>
      <label for="email" class="block text-sm font-medium mb-1">이메일 주소 <span class="text-red-500">*</span></label>
      <input 
        type="email" 
        id="email" 
        name="email" 
        required 
        placeholder="your@email.com"
        class="w-full px-4 py-2 border border-neutral-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-neutral-700 dark:border-neutral-600"
      />
      <p id="email-error" class="text-red-500 text-sm mt-1 hidden">올바른 이메일 주소를 입력해 주세요.</p>
    </div>
    
    <div>
      <label for="subject" class="block text-sm font-medium mb-1">제목 <span class="text-red-500">*</span></label>
      <input 
        type="text" 
        id="subject" 
        name="subject" 
        required 
        placeholder="무엇을 도와드릴까요?"
        class="w-full px-4 py-2 border border-neutral-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-neutral-700 dark:border-neutral-600"
      />
    </div>
    
    <div>
      <label for="message" class="block text-sm font-medium mb-1">메시지 <span class="text-red-500">*</span></label>
      <textarea 
        id="message" 
        name="message" 
        rows="5" 
        required 
        placeholder="프로젝트나 문의 사항에 대해 알려주세요..."
        class="w-full px-4 py-2 border border-neutral-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-neutral-700 dark:border-neutral-600"
      ></textarea>
    </div>
    
    <button 
      type="submit" 
      class="w-full bg-primary-600 text-white py-3 px-6 rounded-md hover:bg-primary-500 transition-colors font-medium"
    >
      메시지 보내기
    </button>
  </form>
</div>

<script>
document.getElementById('contact-form').addEventListener('submit', function(e) {
  const email = document.getElementById('email').value;
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  const errorEl = document.getElementById('email-error');
  
  if (!emailRegex.test(email)) {
    e.preventDefault();
    errorEl.classList.remove('hidden');
    document.getElementById('email').focus();
    return false;
  }
  errorEl.classList.add('hidden');
});

document.getElementById('email').addEventListener('input', function() {
  document.getElementById('email-error').classList.add('hidden');
});
</script>
