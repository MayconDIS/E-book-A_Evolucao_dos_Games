/**
 * script.js
 * Comportamento do e-book, escrito em funções pequenas e nomeadas:
 * cada uma resolve uma responsabilidade só.
 */

document.addEventListener("DOMContentLoaded", initializeEbook);

function initializeEbook() {
    setupPdfExport();
    setupMissionTracking();
    scheduleSheetOverflowAudit();
}

/**
 * Liga o botão que dispara a caixa de impressão do navegador.
 */
function setupPdfExport() {
    const exportButton = document.getElementById("btn-pdf");

    if (exportButton) {
        exportButton.addEventListener("click", () => window.print());
    }
}

/**
 * Destaca no menu de pausa a missão que está na área de leitura.
 */
function setupMissionTracking() {
    const menuLinks = document.querySelectorAll("#pause-menu a");
    const missionTitles = document.querySelectorAll(".sheet h2[id]");

    if (!menuLinks.length || !missionTitles.length) {
        return;
    }

    const observer = new IntersectionObserver(
        (entries) => highlightVisibleMission(entries, menuLinks),
        { rootMargin: "-30% 0px -70% 0px" }
    );

    missionTitles.forEach((title) => observer.observe(title));
}

/**
 * @param {IntersectionObserverEntry[]} entries
 * @param {NodeListOf<Element>} menuLinks
 */
function highlightVisibleMission(entries, menuLinks) {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
            activateMenuLink(entry.target.id, menuLinks);
        }
    });
}

/**
 * @param {string} visibleMissionId
 * @param {NodeListOf<Element>} menuLinks
 */
function activateMenuLink(visibleMissionId, menuLinks) {
    menuLinks.forEach((link) => {
        const pointsToVisibleMission = link.getAttribute("href") === `#${visibleMissionId}`;
        link.classList.toggle("active", pointsToVisibleMission);
    });
}

/**
 * A altura do texto só é confiável depois que Anton e Inter carregam,
 * por isso a medição espera as fontes ficarem prontas.
 */
function scheduleSheetOverflowAudit() {
    if (document.fonts && document.fonts.ready) {
        document.fonts.ready.then(auditSheetOverflow);
        return;
    }

    window.addEventListener("load", auditSheetOverflow);
}

/**
 * Avisa quando o conteúdo de uma folha passa do limite da A4 e seria
 * cortado sem aviso no PDF. Abra a página com ?debug para ver marcado.
 */
function auditSheetOverflow() {
    const isDebugMode = new URLSearchParams(window.location.search).has("debug");
    const sheets = document.querySelectorAll(".sheet");

    sheets.forEach((sheet, sheetIndex) => {
        const overflowInPixels = Math.round(sheet.scrollHeight - sheet.clientHeight);

        if (overflowInPixels <= 1) {
            return;
        }

        console.warn(
            `[e-book] Folha ${sheetIndex + 1} passa da A4 em ~${overflowInPixels}px ` +
            `e será cortada no PDF. Reduza o texto ou o espaçamento desta folha.`
        );

        if (isDebugMode) {
            sheet.classList.add("is-overflowing");
        }
    });
}
