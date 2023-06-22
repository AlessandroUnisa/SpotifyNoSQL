$(document).ready(function() {
    // Funzione per generare il grafico a barre
    function generateBarChart(labels, values, title) {
        // Codice per generare il grafico a barre usando una libreria grafica (es. Chart.js)
        // ...

        // Esempio di generazione del grafico a barre con HTML puro
        var chartContainer = document.getElementById('chart-container');
        chartContainer.innerHTML = '';

        var chartTitle = document.createElement('h2');
        chartTitle.innerText = title;
        chartContainer.appendChild(chartTitle);

        var chartCanvas = document.createElement('canvas');
        chartContainer.appendChild(chartCanvas);

        var ctx = chartCanvas.getContext('2d');
        // Genera il grafico a barre utilizzando i dati passati
        // ...

        // Esempio di generazione di un grafico a barre semplice
        var chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Danceability',
                    data: values,
                    backgroundColor: 'rgba(0, 123, 255, 0.7)',
                    borderColor: 'rgba(0, 123, 255, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    // Gestisce il click del pulsante "Genera Grafico"
    $('#generate-chart-button').click(function() {
        var selectedCollection = $('#collection-select').val();
        var url = '/collection/' + selectedCollection + '/danceability/top/10';  // Modifica l'URL della richiesta in base alla tua struttura delle route

        // Effettua una richiesta AJAX per ottenere i dati dalla collezione selezionata
        $.ajax({
            url: url,
            method: 'GET',
            success: function(response) {
                var labels = [];
                var values = [];

                // Estrae i dati dalla risposta
                for (var i = 0; i < response.length; i++) {
                    labels.push(response[i]['name']);  // Sostituisci con il campo corretto per artisti, canzoni o generi
                    values.push(response[i]['danceability']);  // Sostituisci con il campo corretto per la danceability
                }

                // Chiama la funzione per generare il grafico a barre
                generateBarChart(labels, values, 'Top 10 con Danceability maggiore (' + selectedCollection + ')');
            },
            error: function(xhr, status, error) {
                console.error(error);
            }
        });
    });
});
