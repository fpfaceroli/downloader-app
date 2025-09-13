document.addEventListener('DOMContentLoaded', () => {

    const downloadForm = document.getElementById('download-form');
    const videoUrlInput = document.getElementById('video-url');
    const resultsContainer = document.querySelector('.results-container');

    downloadForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const videoUrl = videoUrlInput.value;
        resultsContainer.innerHTML = '<p class="loading-message">Buscando informações do vídeo, aguarde...</p>';

        try {
            // ---- A MUDANÇA ESTÁ AQUI ----
            // Removemos o "http://127.0.0.1:5000" para que o navegador
            // procure o endpoint /download no próprio domínio do site.
            const response = await fetch('/download', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url: videoUrl }),
            });

            const data = await response.json();

            if (data.success) {
                let html = `
                    <div class="video-info">
                        <img src="${data.thumbnail}" alt="Miniatura do vídeo" class="thumbnail">
                        <h3 class="video-title">${data.title}</h3>
                    </div>
                    <div class="download-links">
                        <h4>Selecione um formato para baixar:</h4>
                `;

                data.formats.forEach(format => {
                    html += `<a href="${format.url}" class="download-button" target="_blank" download>
                                Baixar (${format.quality} - ${format.ext})
                             </a>`;
                });

                html += `</div>`;
                resultsContainer.innerHTML = html;

            } else {
                resultsContainer.innerHTML = `<p class="error-message">${data.message}</p>`;
            }

        } catch (error) {
            console.error('Ocorreu um erro:', error);
            resultsContainer.innerHTML = `<p class="error-message">Erro de comunicação com o servidor. Verifique se ele está rodando.</p>`;
        }
    });
});