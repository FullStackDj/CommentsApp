const { createApp, ref, reactive, computed, onMounted, nextTick } = Vue;

createApp({
    template: '#comment-template',

    setup() {
        const form = reactive({
            name: '',
            email: '',
            homepage: '',
            text: '',
            files: [],
            captcha: ''
        });

        const previewHtml = ref('');
        const comments = ref([]);
        const sortKey = ref('created_at');
        const sortOrder = ref('desc');
        const captchaUrl = ref('/api/captcha/?' + Date.now());
        const errors = ref([]);

        const handleFileChange = (event) => {
            form.files = Array.from(event.target.files);
        };

        const refreshCaptcha = () => {
            captchaUrl.value = '/api/captcha/?' + Date.now();
        };

        const handleSubmit = async () => {
            const formData = new FormData();
            formData.append('name', form.name);
            formData.append('email', form.email);
            formData.append('homepage', form.homepage);
            formData.append('text', form.text);
            formData.append('captcha', form.captcha);
            form.files.forEach(file => formData.append('files', file));

            errors.value = [];

            try {
                const response = await fetch('/api/create/', {
                    method: 'POST',
                    body: formData
                });

                if (response.ok) {
                    const data = await response.json();
                    comments.value.push(data);
                    form.text = '';
                    form.files = [];
                    form.captcha = '';
                    errors.value = [];
                    refreshCaptcha();
                } else {
                    const errData = await response.json();
                    if (errData.captcha) errors.value.push('Captcha error: ' + errData.captcha);
                    if (errData.detail) errors.value.push('Error: ' + errData.detail);
                    if (errors.value.length === 0) errors.value.push('Comment submission error');
                    refreshCaptcha();
                }
            } catch (error) {
                console.error('Error:', error);
                errors.value = ['Network error. Please try again.'];
                refreshCaptcha();
            }
        };

        const handlePreview = async () => {
            try {
                const response = await fetch('/api/comments/preview/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text: form.text })
                });
                if (response.ok) {
                    const data = await response.json();
                    previewHtml.value = data.preview;
                }
            } catch (error) {
                previewHtml.value = '<em>Error loading preview</em>';
            }
        };

        const sortedComments = computed(() => {
            return comments.value.slice().sort((a, b) => {
                const valA = a[sortKey.value];
                const valB = b[sortKey.value];
                if (valA < valB) return sortOrder.value === 'asc' ? -1 : 1;
                if (valA > valB) return sortOrder.value === 'asc' ? 1 : -1;
                return 0;
            });
        });

        const toggleSortOrder = (key) => {
            if (sortKey.value === key) {
                sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc';
            } else {
                sortKey.value = key;
                sortOrder.value = 'asc';
            }
        };

        const insertTag = (startTag, endTag) => {
            const textarea = document.querySelector('textarea');
            if (!textarea) return;

            const start = textarea.selectionStart;
            const end = textarea.selectionEnd;
            const text = form.text;

            form.text = text.substring(0, start) + startTag + text.substring(start, end) + endTag + text.substring(end);

            nextTick(() => {
                textarea.selectionStart = textarea.selectionEnd = end + startTag.length + endTag.length;
                textarea.focus();
            });

            handlePreview();
        };

        const getFileName = (path) => {
            if (!path) return '';
            const parts = path.split('/');
            return parts[parts.length - 1];
        };

        onMounted(() => {
            fetch('/api/comments/')
                .then(response => response.json())
                .then(data => {
                    comments.value = data;
                })
                .catch(error => console.error('Error:', error));
        });

        return {
            form,
            previewHtml,
            comments: sortedComments,
            captchaUrl,
            handleFileChange,
            handleSubmit,
            handlePreview,
            toggleSortOrder,
            refreshCaptcha,
            insertTag,
            getFileName,
            errors
        };
    }
}).mount('#app');