/* ============================================================
   PORTE ACOUSTIQUE — JavaScript principal
   ============================================================ */

document.addEventListener('DOMContentLoaded', function () {

    // ---- Menu mobile ----
    var toggle = document.getElementById('mobileToggle');
    var navLinks = document.getElementById('navLinks');

    if (toggle) {
        toggle.addEventListener('click', function () {
            navLinks.classList.toggle('active');
        });
    }

    // Fermer au clic sur un lien
    if (navLinks) {
        navLinks.querySelectorAll('a').forEach(function (link) {
            link.addEventListener('click', function () {
                navLinks.classList.remove('active');
            });
        });
    }

    // Fermer au clic en dehors
    document.addEventListener('click', function (e) {
        if (navLinks && toggle && !navLinks.contains(e.target) && !toggle.contains(e.target)) {
            navLinks.classList.remove('active');
        }
    });

    // ---- Lien actif dans la nav ----
    var currentPage = window.location.pathname.split('/').pop() || 'index.html';
    if (navLinks) {
        navLinks.querySelectorAll('a').forEach(function (link) {
            var href = link.getAttribute('href').split('?')[0].split('#')[0];
            if (href === currentPage || (currentPage === '' && href === 'index.html')) {
                link.classList.add('active');
            }
        });
    }

    // ---- Formulaire contact ----
    var contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function (e) {
            e.preventDefault();
            alert('Merci pour votre message ! Notre équipe vous répondra dans les meilleurs délais.');
            contactForm.reset();
        });
    }

    // ---- Formulaire devis ----
    var devisForm = document.getElementById('devisForm');
    if (devisForm) {
        devisForm.addEventListener('submit', function (e) {
            e.preventDefault();
            alert('Votre demande de devis a bien été envoyée ! Vous recevrez notre réponse sous 24 heures.');
            devisForm.reset();
        });
    }

    // ---- Pré-remplissage depuis URL params ----
    if (window.location.pathname.includes('devis')) {
        var params = new URLSearchParams(window.location.search);
        var modeleField = document.getElementById('modele');
        var dimensionField = document.getElementById('dimension');

        if (modeleField && params.get('modele')) modeleField.value = params.get('modele');
        if (dimensionField && params.get('dimension')) dimensionField.value = params.get('dimension');

        var preselect = document.getElementById('preselection');
        if (preselect && (params.get('modele') || params.get('dimension'))) {
            preselect.style.display = 'block';
            var el = document.getElementById('preModel');
            var el2 = document.getElementById('preDimension');
            var el3 = document.getElementById('prePrice');
            if (el) el.textContent = params.get('modele') || '-';
            if (el2) el2.textContent = params.get('dimension') || '-';
            if (el3) el3.textContent = params.get('prix') ? params.get('prix') + ' € HT' : '-';
        }
    }

    // ---- Boutons devis dans tableau tarifs ----
    document.querySelectorAll('[data-model]').forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            var p = new URLSearchParams();
            if (this.dataset.model) p.set('modele', this.dataset.model);
            if (this.dataset.size) p.set('dimension', this.dataset.size);
            if (this.dataset.price) p.set('prix', this.dataset.price);
            window.location.href = 'devis.html?' + p.toString();
        });
    });

    // ---- Onglets pages produit ----
    document.querySelectorAll('.tab-btn').forEach(function (btn) {
        btn.addEventListener('click', function () {
            var target = this.dataset.tab;
            document.querySelectorAll('.tab-btn').forEach(function (b) { b.classList.remove('active'); });
            document.querySelectorAll('.tab-panel').forEach(function (p) { p.classList.remove('active'); });
            this.classList.add('active');
            var panel = document.getElementById(target);
            if (panel) panel.classList.add('active');
        });
    });

    // ---- Tooltip swatches finition ----
    document.querySelectorAll('.swatch').forEach(function (sw) {
        sw.setAttribute('title', sw.dataset.name || '');
    });

});
