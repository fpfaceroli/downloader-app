document.addEventListener('DOMContentLoaded', () => {

    const downloadForm = document.getElementById('download-form');
    const videoUrlInput = document.getElementById('video-url');
    const resultsContainer = document.querySelector('.results-container');

    downloadForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const videoUrl = videoUrlInput.value;
        resultsContainer.innerHTML = '<p class="loading-message">Buscando informações do vídeo, aguarde...</p>';

        try {
            const response = await fetch('http://127.0.0.1:5000/download', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url: videoUrl }),
            });

            const data = await response.json();

            // ---- LÓGICA PARA EXIBIR OS RESULTADOS ----

            if (data.success) {
                // Se o backend retornou sucesso, construímos o HTML dos resultados
                let html = `
                    <div class="video-info">
                        <img src="${data.thumbnail}" alt="Miniatura do vídeo" class="thumbnail">
                        <h3 class="video-title">${data.title}</h3>
                    </div>
                    <div class="download-links">
                        <h4>Selecione um formato para baixar:</h4>
                `;

                // Criamos um botão de download para cada formato encontrado
                data.formats.forEach(format => {
                    html += `<a href="${format.url}" class="download-button" target="_blank" download>
                                Baixar (${format.quality} - ${format.ext})
                             </a>`;
                });

                html += `</div>`;
                resultsContainer.innerHTML = html;

            } else {
                // Se deu erro, mostramos a mensagem de erro do backend
                resultsContainer.innerHTML = `<p class="error-message">${data.message}</p>`;
            }

        } catch (error) {
            console.error('Ocorreu um erro:', error);
            resultsContainer.innerHTML = `<p class="error-message">Erro de comunicação com o servidor. Verifique se ele está rodando.</p>`;
        }
    });
});