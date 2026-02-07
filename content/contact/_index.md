---
title: "Contact Us"
description: "Get in touch with JE Tech Holdings"
date: 2024-01-01
layout: "simple"
---

<div class="contact-form-container">
  <p class="text-lg mb-6">Have a question or want to discuss a project? Fill out the form below and we'll get back to you within 24 hours.</p>
  
  <form id="contact-form" action="https://formspree.io/f/xqedkeja" method="POST" class="space-y-4">
    
    <div>
      <label for="email" class="block text-sm font-medium mb-1">Email Address <span class="text-red-500">*</span></label>
      <input 
        type="email" 
        id="email" 
        name="email" 
        required 
        placeholder="your@email.com"
        class="w-full px-4 py-2 border border-neutral-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-neutral-700 dark:border-neutral-600"
      />
      <p id="email-error" class="text-red-500 text-sm mt-1 hidden">Please enter a valid email address.</p>
    </div>
    
    <div>
      <label for="subject" class="block text-sm font-medium mb-1">Subject <span class="text-red-500">*</span></label>
      <input 
        type="text" 
        id="subject" 
        name="subject" 
        required 
        placeholder="How can we help?"
        class="w-full px-4 py-2 border border-neutral-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-neutral-700 dark:border-neutral-600"
      />
    </div>
    
    <div>
      <label for="message" class="block text-sm font-medium mb-1">Message <span class="text-red-500">*</span></label>
      <textarea 
        id="message" 
        name="message" 
        rows="5" 
        required 
        placeholder="Tell us about your project or inquiry..."
        class="w-full px-4 py-2 border border-neutral-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-neutral-700 dark:border-neutral-600"
      ></textarea>
    </div>
    
    <button 
      type="submit" 
      class="w-full bg-primary-600 text-white py-3 px-6 rounded-md hover:bg-primary-500 transition-colors font-medium"
    >
      Send Message
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
