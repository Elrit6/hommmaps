// Load and apply saved font preference
const savedFont = localStorage.getItem("font");
if (savedFont) {
    document.documentElement.style.setProperty("--font", savedFont);
    document.getElementById("font").value = savedFont; // Update input field
}

// Load and apply saved theme preference
const savedTheme = localStorage.getItem("theme");
if (savedTheme === "dark") {
    document.documentElement.style.setProperty("color-scheme", "dark");
    document.documentElement.style.setProperty("--bg-color-1", "#121212");
    document.documentElement.style.setProperty("--bg-color-2", "black");
    document.documentElement.style.setProperty("--text-color", "white");
} else {
    document.documentElement.style.setProperty("color-scheme", "light");
    document.documentElement.style.setProperty("--bg-color-1", "lightgray");
    document.documentElement.style.setProperty("--bg-color-2", "white");
    document.documentElement.style.setProperty("--text-color", "black");
}

document.getElementById("font").addEventListener("change", function() {
    const fontInput = document.getElementById("font").value;
    document.documentElement.style.setProperty("--font", fontInput);
    localStorage.setItem("font", fontInput);
});

document.getElementById("theme").addEventListener("click", function() {
    const currentScheme = getComputedStyle(document.documentElement).getPropertyValue("color-scheme").trim();

    if (currentScheme === "light") {
        document.documentElement.style.setProperty("color-scheme", "dark");
        document.documentElement.style.setProperty("--bg-color-1", "#121212");
        document.documentElement.style.setProperty("--bg-color-2", "black");
        document.documentElement.style.setProperty("--text-color", "white");
        localStorage.setItem("theme", "dark"); 
    } else {
        document.documentElement.style.setProperty("color-scheme", "light");
        document.documentElement.style.setProperty("--bg-color-1", "lightgray");
        document.documentElement.style.setProperty("--bg-color-2", "white");
        document.documentElement.style.setProperty("--text-color", "black");
        localStorage.setItem("theme", "light"); 
    } 
});
