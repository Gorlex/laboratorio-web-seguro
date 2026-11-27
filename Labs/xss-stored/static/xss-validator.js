(function () {
    "use strict";

    const alertOriginal = window.alert;

    window.alert = function (...args) {
        try {
            const script = document.currentScript;

            const nota = script
                ? script.closest(".nota-content[data-nota-id]")
                : null;

            if (nota) {
                const notaId = nota.dataset.notaId;

                console.info(
                    "[XSS Validator] Ejecución candidata detectada",
                    {
                        lab_id: "xss-stored",
                        nota_id: notaId,
                        metodo: "xss_stored_alert"
                    }
                );
                
                // Enviar el evento al endpoint Flask
                const notaIdInt = parseInt(notaId);
                if (!isNaN(notaIdInt) && notaIdInt > 0) {
                    fetch('/validar-reto', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            nota_id: notaIdInt
                        })
                    })
                    .then(response => {
                        if (response.ok) {
                            console.log("[XSS Validator] Evento candidato aceptado por Flask");
                        } else {
                            console.warn("[XSS Validator] Evento candidato rechazado por Flask");
                        }
                    })
                    .catch(error => {
                        console.warn("[XSS Validator] Error de conexión al enviar evento:", error);
                    });
                }
            }
        } catch (error) {
            console.warn("[XSS Validator] Error de detección");
        }

        return Reflect.apply(alertOriginal, window, args);
    };
})();