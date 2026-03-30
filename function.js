document.addEventListener('DOMContentLoaded', function() {
    const container = document.querySelector('.video-container');
    const video = document.getElementById('nexusVideo');

    if (!container || !video) return;

    // L'UNICO evento click che comanda tutto
    container.addEventListener('click', function(e) {
        // Se l'utente clicca sulla barra dei comandi nativa (se attiva), non interferiamo
        if (e.target.tagName === 'VIDEO' && video.controls) return;

        if (video.paused) {
            video.play();
        } else {
            video.pause();
        }
    });

    // Sincronizziamo la grafica con lo stato reale del video
    video.addEventListener('play', function() {
        container.classList.add('is-playing');
        video.controls = true; // Mostra i controlli quando parte
    });

    video.addEventListener('pause', function() {
        container.classList.remove('is-playing');
        video.controls = false; // Nascondi i controlli in pausa per far vedere il pulsante
    });

    video.addEventListener('ended', function() {
        container.classList.remove('is-playing');
        video.controls = false;
        video.currentTime = 0; // Torna al primo frame
    });
});