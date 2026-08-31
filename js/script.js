function initApp() {
    var hamburger = document.querySelector('.hamburger');
    var navLinks = document.querySelector('.nav-links');

    var backdrop = document.createElement('div');
    backdrop.className = 'nav-backdrop';
    document.body.appendChild(backdrop);

    // The drawer open/close is fully handled by CSS transitions: they interpolate from the
     // current pixel position, so no "animation in progress" mutex flag is needed — that flag
     // swallows clicks during the animation, causing a stale-then-jump effect that looks like jitter.
    function openMenu() {
        hamburger.classList.add('active');
        navLinks.classList.add('open');
        backdrop.classList.add('active');
        document.body.classList.add('menu-open');
    }

    function closeMenu() {
        hamburger.classList.remove('active');
        navLinks.classList.remove('open');
        backdrop.classList.remove('active');
        document.body.classList.remove('menu-open');
    }

    if (hamburger && navLinks) {
        hamburger.addEventListener('click', function () {
            if (navLinks.classList.contains('open')) {
                closeMenu();
            } else {
                openMenu();
            }
        });

        backdrop.addEventListener('click', function (e) {
            e.stopPropagation();
            closeMenu();
        });

        var links = document.querySelectorAll('.nav-link');
        for (var linkIndex = 0; linkIndex < links.length; linkIndex = linkIndex + 1) {
            links[linkIndex].addEventListener('click', closeMenu);
        }

        var mobileBreakpoint = 960;
        var wasMobile = window.innerWidth <= mobileBreakpoint;
        var resizeScheduled = false;

        function resolveResponsiveNavigation() {
            resizeScheduled = false;
            var isMobile = window.innerWidth <= mobileBreakpoint;
            if (isMobile === wasMobile) {
                return;
            }
            wasMobile = isMobile;
            // If the drawer is open when crossing a breakpoint it would cover the body,
             // so force it closed; disable transitions to avoid a half-open intermediate frame.
            navLinks.style.transition = 'none';
            closeMenu();
            requestAnimationFrame(function () {
                requestAnimationFrame(function () {
                    navLinks.style.transition = '';
                });
            });
        }

        window.addEventListener('resize', function () {
            if (resizeScheduled) {
                return;
            }
            resizeScheduled = true;
            requestAnimationFrame(resolveResponsiveNavigation);
        }, { passive: true });
    }

    var navbar = document.querySelector('.navbar');
    var shrinkTopLimit = 50;
    var directionFlipThreshold = 12;
    var directionBaselineTop = window.pageYOffset || document.documentElement.scrollTop;
    var scrollScheduled = false;
    var rebaselineAfterFlip = false;

    function readScrollTop() {
        return window.pageYOffset || document.documentElement.scrollTop;
    }

    function applyShrinkState(nextShrunk) {
        if (navbar.classList.contains('shrink') !== nextShrunk) {
            rebaselineAfterFlip = true;
            navbar.classList.toggle('shrink', nextShrunk);
        }
        directionBaselineTop = readScrollTop();
    }

    function resolveNavbarShrink() {
        scrollScheduled = false;
        var currentTop = readScrollTop();

        // When the shrink state changes, the navbar shrinks by 1rem; at the bottom of the
         // page the browser clamps scrollTop back once and fires another scroll event.  That
         // event does not represent user intent — use it only to re-baseline, otherwise
         // shrink and expand would cross-trigger at the bottom, producing jitter.
        if (rebaselineAfterFlip) {
            rebaselineAfterFlip = false;
            directionBaselineTop = currentTop;
            return;
        }

        var displacement = currentTop - directionBaselineTop;
        if (currentTop <= shrinkTopLimit) {
            applyShrinkState(false);
            return;
        }
        // Displacement accumulates from the last decision point; a single 1-2 px difference
         // is not enough to flip state, so inertial scroll micro-bounces no longer toggle it.
        if (displacement >= directionFlipThreshold) {
            applyShrinkState(true);
        } else if (displacement <= -directionFlipThreshold) {
            applyShrinkState(false);
        }
    }

    window.addEventListener('scroll', function () {
        if (scrollScheduled) {
            return;
        }
        scrollScheduled = true;
        window.requestAnimationFrame(resolveNavbarShrink);
    }, { passive: true });

    var themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', function () {
            var current = document.documentElement.getAttribute('data-theme');
            var next = current === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', next);
            setPref('theme', next);
        });
    }

    function updateThemeImages() {
        var theme = document.documentElement.getAttribute('data-theme');
        var imgs = document.querySelectorAll('[data-theme-img]');
        for (var i = 0; i < imgs.length; i++) {
            var lightSrc = imgs[i].getAttribute('data-light');
            var darkSrc = imgs[i].getAttribute('data-dark');
            if (lightSrc && darkSrc) {
                imgs[i].src = theme === 'dark' ? darkSrc : lightSrc;
            }
        }
    }

    updateThemeImages();

    var observer = new MutationObserver(function (mutations) {
        for (var i = 0; i < mutations.length; i++) {
            if (mutations[i].attributeName === 'data-theme') {
                updateThemeImages();
            }
        }
    });
    observer.observe(document.documentElement, { attributes: true });
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initApp);
} else {
    initApp();
}
