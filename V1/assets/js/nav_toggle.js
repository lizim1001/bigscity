// BIGSCity Website Navigation & Archive Switcher
function toggleArchiveNav(show) {
    var archivedItems = document.querySelectorAll('.nav-archived-section');
    for (var i = 0; i < archivedItems.length; i++) {
        archivedItems[i].style.display = show ? 'block' : 'none';
    }
    try {
        localStorage.setItem('bigscity_show_archived', show ? 'true' : 'false');
    } catch(e) {}
    var cb = document.getElementById('toggle-archive-nav');
    if (cb) {
        cb.checked = show;
    }
}

document.addEventListener('DOMContentLoaded', function() {
    var defaultShow = (typeof window.BIGSCITY_DEFAULT_SHOW_ARCHIVED !== 'undefined') ? window.BIGSCITY_DEFAULT_SHOW_ARCHIVED : false;
    var saved = null;
    try {
        saved = localStorage.getItem('bigscity_show_archived');
    } catch(e) {}
    var show = (saved !== null) ? (saved === 'true') : defaultShow;
    toggleArchiveNav(show);
});
