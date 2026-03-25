// JS Challengeat 2.0 Landing Page - Edizione 7

document.addEventListener('DOMContentLoaded', () => {

    // 1. ANIMATE ON SCROLL
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.15
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                // Opt-out from observing after it becomes visible
                // observer.unobserve(entry.target); 
            }
        });
    }, observerOptions);

    document.querySelectorAll('.animate-on-scroll').forEach(el => {
        observer.observe(el);
    });

    // 2. COUNTER ANIMATION FOR SOCIAL PROOF
    const counterElements = document.querySelectorAll('.kpi-number .counter');
    let countersStarted = false;

    const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !countersStarted) {
                countersStarted = true;
                counterElements.forEach(counter => {
                    const target = parseInt(counter.getAttribute('data-target'));
                    const duration = 2000; // ms
                    const stepTime = Math.abs(Math.floor(duration / target));
                    let current = 0;
                    const isPlus = counter.innerHTML.includes('+');

                    const timer = setInterval(() => {
                        const increment = Math.ceil(target / (duration / 50));
                        current += increment;
                        if (current >= target) {
                            counter.innerHTML = target.toLocaleString('it-IT');
                            clearInterval(timer);
                        } else {
                            counter.innerHTML = current.toLocaleString('it-IT');
                        }
                    }, 50);
                });
            }
        });
    }, { threshold: 0.5 });

    const socialProofBar = document.querySelector('.social-proof-bar');
    if (socialProofBar) counterObserver.observe(socialProofBar);

    // 3. FAQ ACCORDION
    const faqItems = document.querySelectorAll('.faq-question');
    faqItems.forEach(item => {
        item.addEventListener('click', () => {
            const isActive = item.classList.contains('active');

            // Chiudi tutti
            faqItems.forEach(faq => {
                faq.classList.remove('active');
                faq.nextElementSibling.style.maxHeight = null;
            });

            // Apri se non era attivo
            if (!isActive) {
                item.classList.add('active');
                const answer = item.nextElementSibling;
                answer.style.maxHeight = answer.scrollHeight + "px";
            }
        });
    });

    // 4. EXIT INTENT POPUP
    const exitModal = document.getElementById('modal-exit');
    let exitIntentShown = false;

    if (exitModal) {
        document.addEventListener('mouseleave', (e) => {
            if (e.clientY < 0 && !exitIntentShown) {
                exitIntentShown = true;
                exitModal.classList.add('open');
                sessionStorage.setItem('exitIntentShown', 'true');
            }
        });

        // Controlla se è già stato mostrato in questa sessione
        if (sessionStorage.getItem('exitIntentShown') === 'true') {
            exitIntentShown = true;
        }

        // Close logic
        const closeBtns = exitModal.querySelectorAll('.modal-close, .btn-outline');
        closeBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                exitModal.classList.remove('open');
            });
        });

        // Clicca fuori dalla modale per chiudere
        exitModal.addEventListener('click', (e) => {
            if (e.target === exitModal) {
                exitModal.classList.remove('open');
            }
        });
    }

    // 5. SMOOTH SCROLL ANCHORS
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href !== '#') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth'
                    });
                }

                // Chiudi menu modali o exit intent se presente
                if (this.closest('.modal-overlay')) {
                    this.closest('.modal-overlay').classList.remove('open');
                }
            }
        });
    });

    // 6. TRACKING PLACEHOLDER (come da TechSpec)
    let scrollTracked = false;
    window.addEventListener('scroll', function () {
        if (!scrollTracked && (window.scrollY / document.body.scrollHeight) > 0.5) {
            scrollTracked = true;
            if (typeof fbq !== 'undefined') fbq('track', 'ViewContent');
        }
    });

    document.querySelectorAll('a[href="#form"], .btn-primary').forEach(btn => {
        btn.addEventListener('click', function () {
            if (typeof fbq !== 'undefined') fbq('track', 'InitiateCheckout');
        });
    });

});
