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
            }
        } catch (error) {
            console.warn("[XSS Validator] Error de detección");
        }

        return Reflect.apply(alertOriginal, window, args);
    };
})();