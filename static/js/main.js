window.addEventListener("DOMContentLoaded", function() {

    const font = localStorage.getItem("font");
    const theme = localStorage.getItem("theme");
    console.log("Font:", font);
    console.log("Theme:", theme);

    if (font) {
        document.documentElement.style.setProperty("--font", font);
    }

    if (true) {
        document.documentElement.style.setProperty("color-scheme", theme);
        if (theme === "dark") {
            document.documentElement.style.setProperty("--bg-color-1", "#121212");
            document.documentElement.style.setProperty("--bg-color-2", "black");
            document.documentElement.style.setProperty("--text-color", "white");
        } else {
            document.documentElement.style.setProperty("--bg-color-1", "lightgray");
            document.documentElement.style.setProperty("--bg-color-2", "white");
            document.documentElement.style.setProperty("--text-color", "black");
        }
    }
});